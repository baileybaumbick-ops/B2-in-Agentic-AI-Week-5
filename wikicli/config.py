"""Paths, model identifiers and tunable settings for the wiki harness."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
SOURCES_DIR = VAULT / "Sources"          # preserved originals (never edited)
INDEX_DIR = ROOT / ".index"              # machine data: manifest, chunks, embeddings
OUTPUTS_DIR = ROOT / "outputs"           # saved answers, searches and chat transcripts
PROMPTS_DIR = ROOT / "prompts"

# Local models served by Ollama. Override with environment variables if needed.
CHAT_MODEL = os.environ.get("WIKI_MODEL", "gemma4:e2b")
EMBED_MODEL = os.environ.get("WIKI_EMBED_MODEL", "embeddinggemma")
OLLAMA_URL = os.environ.get("WIKI_OLLAMA_URL", "http://127.0.0.1:11434")

# Topic folders for generated notes (a few, human-readable).
TOPICS = [
    "Strategy Foundations",
    "Value and Advantage",
    "Industry Analysis",
    "Entry and Competition",
    "Company Cases",
]

# Files in the vault that are generated navigation pages, not content.
NAV_PAGES = {"index.md", "Source Catalog.md"}

# Model call settings.
NUM_CTX = 8192
CHAT_TEMPERATURE = 0.7
ASK_TEMPERATURE = 0.1
INGEST_TEMPERATURE = 0.2
CHAT_HISTORY_MESSAGES = 12   # user+assistant messages kept in chat context

# Retrieval settings.
ASK_TOP_K = 6
SEARCH_TOP_K = 5
CHAT_NOTES_TOP_K = 3
CHUNK_MAX_CHARS = 1100
# If the best passage is this dissimilar AND shares no keywords with the
# question, ask mode refuses without calling the model.
ASK_MIN_COSINE = 0.30
# A "no" from the answerability check only refuses early if the best passage is
# below this similarity; above it, the answer step (which can still refuse) runs.
ASK_STRONG_MATCH = 0.50
