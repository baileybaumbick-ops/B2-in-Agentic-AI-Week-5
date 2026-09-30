# Ask: What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?

**Status:** insufficient_evidence

Insufficient evidence: The provided passages do not contain information about Holland Sweetener Company's actions or advice regarding Coke and Pepsi.

## Retrieved passages
### [S1] vault/Sources/Class 4 - Industry Analysis.md › Case - Cola Wars
kind=source cosine=0.416 bm25=6.29

Carbonated soft drinks are about 27% of US beverage consumption and $48 billion in US sales. Coke and Pepsi hold about 70% of the market, and concentrate producers earn gross profit around 83% of net sales, versus 25-35% for an average US firm.

### [S2] vault/Company Cases/Cola Wars Case.md › (intro)
kind=note cosine=0.382 bm25=7.78

The Cola Wars illustrates how Coke and Pepsi shaped competition by focusing on advertising and differentiation rather than price wars.

### [S3] vault/Industry Analysis/Rivalry.md › Key Points
kind=note cosine=0.307 bm25=7.83

- Price rivalry hurts profit most, while rivalry in quality or brand can be offset by higher prices. ([[Class 4 - Industry Analysis#Rivalry|Class 4 › Rivalry]])
- Price rivalry is fierce when products are homogeneous, search costs are low, and switching costs are low. ([[Class 4 - Industry Analysis#Rivalry|Class 4 › Rivalry]])
- In the Cola Wars, Coke and Pepsi competed on advertising and marketing instead of a price war. ([[Class 4 - Industry Analysis#Case - Cola Wars|Class 4 › Case - Cola Wars]])

### [S4] vault/Sources/Class 4 - Industry Analysis.md › Case - Cola Wars
kind=source cosine=0.382 bm25=6.0

Five Forces: substitutes are everywhere (water, coffee, juice, beer), but Coke kept its product "within arm's reach of desire." Buyer power ranges from low to high; profitability for concentrate producers ranks vending > convenience stores > grocery > fountain. Supplier power is low: concentrate costs about $0.11 per case and inputs are commodities. Rivalry: the two colas are nearly identical, so a price war would be ruinous; instead they compete on advertising and marketing (about 39% of net sales versus about 10% for an average firm) and on new flavors, moving competition from price to dimensions that grow the market. They fight harder abroad, where Pepsi is often a small entrant. Entry barriers: scale in distribution and marketing, established channels, limited shelf space, and brand; a concentrate plant costs only a few million dollars, so plant cost itself is not the barrier.

### [S5] vault/Company Cases/Cola Wars Case.md › Key Points
kind=note cosine=0.411 bm25=4.82

- Carbonated soft drinks represent 27% of US beverage consumption and $48 billion in US sales. ([[Class 4 - Industry Analysis#Case - Cola Wars|Class 4 › Case - Cola Wars]])
- Coke and Pepsi competed on advertising and marketing, moving competition from price to dimensions that grow the market. ([[Class 4 - Industry Analysis#Case - Cola Wars|Class 4 › Case - Cola Wars]])
- Entry barriers included scale in distribution, established channels, and brand recognition. ([[Class 4 - Industry Analysis#Case - Cola Wars|Class 4 › Case - Cola Wars]])

### [S6] vault/Sources/Class 4 - Industry Analysis.md › Takeaways
kind=source cosine=0.375 bm25=5.56

The cola industry is profitable because buyers and suppliers are weak and entry barriers are high, and Coke and Pepsi shaped competition by creating perceived differentiation. The Five Forces focus on splitting a fixed pie and leave out joint value creation, such as legally growing the market together. If the forces say an industry is attractive, ask why more firms have not entered: either entry is hard or the industry has changed.

## Checks and timing
```json
{
  "checks": {
    "best_cosine": 0.416,
    "keyword_overlap": true,
    "question_terms_absent_from_passages": [
      "major",
      "mistake",
      "holland",
      "sweetener",
      "company",
      "make",
      "done"
    ],
    "answerability": {
      "answerable": false,
      "passages": [],
      "reason": "The provided passages do not contain information about Holland Sweetener Company's actions or advice regarding Coke and Pepsi."
    },
    "gate": "answerability check said the passages do not answer the question"
  },
  "timing": {
    "retrieval_s": 0.15,
    "generation_s": 15.45,
    "model_load_s": 0.02,
    "prompt_tokens": 1134,
    "output_tokens": 44,
    "tokens_per_second": 19.2,
    "model_calls": 1,
    "total_s": 15.6
  },
  "memory": [
    {
      "model": "gemma4:e2b",
      "size_gb": 6.87,
      "vram_gb": 0.0,
      "context": 8192
    },
    {
      "model": "embeddinggemma:latest",
      "size_gb": 0.68,
      "vram_gb": 0.0,
      "context": 2048
    }
  ],
  "model": "gemma4:e2b"
}
```