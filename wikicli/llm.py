"""Thin wrapper around the local Ollama runtime.

Everything the harness sends to a model goes through LocalModel, which
refuses non-local hosts so there is no silent cloud fallback.
"""
import time
from dataclasses import dataclass, field
from urllib.parse import urlparse

import httpx
import numpy as np
import ollama

from . import config

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


class HarnessError(RuntimeError):
    """An error with a message that is safe to show the user as-is."""


@dataclass
class ModelCall:
    text: str
    seconds: float
    prompt_tokens: int = 0
    output_tokens: int = 0
    load_seconds: float = 0.0
    stats: dict = field(default_factory=dict)


class LocalModel:
    def __init__(self, chat_model=config.CHAT_MODEL, embed_model=config.EMBED_MODEL,
                 url=config.OLLAMA_URL):
        host = urlparse(url).hostname
        if host not in LOCAL_HOSTS:
            raise HarnessError(
                f"Refusing non-local model host '{url}'. Local mode only talks to "
                "Ollama on this computer (localhost)."
            )
        self.url = url
        self.chat_model = chat_model
        self.embed_model = embed_model
        self.client = ollama.Client(host=url, timeout=900)

    # ---- helpers -------------------------------------------------------
    def _wrap(self, fn, model):
        try:
            return fn()
        except (httpx.ConnectError, ConnectionError) as exc:
            raise HarnessError(
                f"Cannot reach Ollama at {self.url}. Start the Ollama app "
                "(or run `ollama serve`) and try again."
            ) from exc
        except ollama.ResponseError as exc:
            if exc.status_code == 404:
                raise HarnessError(
                    f"Model '{model}' is not installed locally. While online, run: "
                    f"ollama pull {model}"
                ) from exc
            raise HarnessError(f"Ollama error: {exc.error}") from exc

    def version(self) -> str:
        try:
            return httpx.get(f"{self.url}/api/version", timeout=5).json().get("version", "?")
        except httpx.HTTPError:
            return "unreachable"

    def memory(self) -> list[dict]:
        """Loaded models and their memory footprint, as reported by Ollama."""
        try:
            running = self.client.ps().models
        except Exception:  # memory reporting is best-effort
            return []
        return [
            {
                "model": m.model,
                "size_gb": round(m.size / 1e9, 2),
                "vram_gb": round((m.size_vram or 0) / 1e9, 2),
                "context": getattr(m, "context_length", None),
            }
            for m in running
        ]

    # ---- generation ----------------------------------------------------
    def chat(self, messages, *, temperature=0.3, json_schema=None, num_predict=None) -> ModelCall:
        options = {"temperature": temperature, "num_ctx": config.NUM_CTX}
        if num_predict:
            options["num_predict"] = num_predict
        start = time.perf_counter()
        resp = self._wrap(
            lambda: self.client.chat(
                model=self.chat_model,
                messages=messages,
                format=json_schema,
                think=False,
                options=options,
            ),
            self.chat_model,
        )
        seconds = time.perf_counter() - start
        eval_s = (resp.eval_duration or 0) / 1e9
        return ModelCall(
            text=resp.message.content or "",
            seconds=seconds,
            prompt_tokens=resp.prompt_eval_count or 0,
            output_tokens=resp.eval_count or 0,
            load_seconds=(resp.load_duration or 0) / 1e9,
            stats={
                "tokens_per_second": round((resp.eval_count or 0) / eval_s, 1) if eval_s else None,
            },
        )

    # ---- embeddings ----------------------------------------------------
    def embed(self, texts: list[str], kind: str) -> np.ndarray:
        """Embed texts with EmbeddingGemma's recommended task prefixes.

        kind="query" for questions, kind="document" for passages
        (documents are passed as (title, text) joined with a tab).
        """
        if kind == "query":
            inputs = [f"task: search result | query: {t}" for t in texts]
        else:
            inputs = []
            for t in texts:
                title, _, body = t.partition("\t")
                inputs.append(f"title: {title or 'none'} | text: {body}")
        vectors = []
        for i in range(0, len(inputs), 16):
            batch = inputs[i:i + 16]
            resp = self._wrap(
                lambda: self.client.embed(model=self.embed_model, input=batch),
                self.embed_model,
            )
            vectors.extend(resp.embeddings)
        arr = np.asarray(vectors, dtype=np.float32)
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        return arr / np.clip(norms, 1e-9, None)
