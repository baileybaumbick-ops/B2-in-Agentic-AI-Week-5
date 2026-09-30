# Ask: What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?

**Status:** answered

HSC created $400-600M of value for Coke and Pepsi but captured little of it [S3]. HSC needed a credible commitment to enter successfully [S3]. If Coke and Pepsi could not commit, they would only buy from NutraSweet once HSC entered, meaning HSC should not have entered; conversely, with a binding commitment, HSC should have entered, which would have benefited Coke and Pepsi [S1].

## Cited sources
- [S1] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › HSC's major mistake
- [S3] vault/Company Cases/Intel Case.md › Key Points

## Retrieved passages
### [S1] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › HSC's major mistake
kind=source cosine=0.581 bm25=12.9

HSC created $400-600M of value for Coke and Pepsi but captured little of it. It believed Coke and Pepsi wanted it around, which was true, but once HSC had built its plant, they used it as leverage and then stayed with NutraSweet. HSC needed a credible commitment, a written purchase agreement signed before it built the plant. In game form: if Coke and Pepsi cannot commit, they will buy only from NutraSweet once HSC has entered, so HSC should not enter; with a binding commitment, HSC should enter, and Coke and Pepsi would benefit from signing it.

Market structure drove the case: high MES (with tiny MES, anyone could pick off small customers), Coke and Pepsi's large share, their reluctance to switch because of branding and safety, and delays to other sweeteners.

### [S2] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › Case - Bitter Competition, the setup
kind=source cosine=0.436 bm25=12.98

The case is about aspartame. NutraSweet (owned by Monsanto) held the patent, which expired in Europe and Canada in 1987 and in the US in 1992, giving a two-stage game. Minimum efficient scale was large (about 2,000 tons) compared with total demand (about 6,000 tons in 1986), and European demand was below one efficient plant. Buyers were concentrated: Coke and Pepsi bought about half. Safety regulation slowed rival sweeteners, and NutraSweet co-branded with its customers.

NutraSweet tried to stretch its patent with long-term exclusive contracts and ingredient branding (the swirl logo on cans). It charged about $70/lb, or $50/lb to Coke and Pepsi, against an estimated marginal cost of about $18/lb.

The entrant, Holland Sweetener Company (HSC), targeted buyers who wanted cheaper, possibly unbranded, aspartame. It was unlikely to be more efficient: it entered Europe at only 500 tons, below MES and low on the learning curve, with an estimated marginal cost of about $30/lb. The gap between $30 and $70 looked attractive, but NutraSweet had lower cost, a stronger brand and deep pockets.

### [S3] vault/Company Cases/Intel Case.md › Key Points
kind=note cosine=0.413 bm25=17.2

### From Class 8 - Strategic and Repeated Interactions
- HSC created $400-600M of value for Coke and Pepsi but captured little of it. ([[Class 8 - Strategic and Repeated Interactions#HSC's major mistake|Class 8 › HSC's major mistake]])
- HSC needed a credible commitment to enter successfully. ([[Class 8 - Strategic and Repeated Interactions#HSC's major mistake|Class 8 › HSC's major mistake]])
- Market structure drove the case, including high MES and large shares. ([[Class 8 - Strategic and Repeated Interactions#HSC's major mistake|Class 8 › HSC's major mistake]])

### [S4] vault/Sources/Class 4 - Industry Analysis.md › Case - Cola Wars
kind=source cosine=0.416 bm25=5.22

Carbonated soft drinks are about 27% of US beverage consumption and $48 billion in US sales. Coke and Pepsi hold about 70% of the market, and concentrate producers earn gross profit around 83% of net sales, versus 25-35% for an average US firm.

### [S5] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › What happened
kind=source cosine=0.478 bm25=4.79

NutraSweet retaliated in Europe: prices fell to about $22/lb, below HSC's marginal cost, and several other firms exited. HSC filed EU complaints about abuse of dominant position (NutraSweet's exclusive contracts with Coke and Pepsi ran to 1990) and dumping; the European Commission sided with HSC and imposed a $15/lb duty on NutraSweet. NutraSweet then committed to fight by planning a 2,000-ton plant in France and doubling its Augusta plant, and alternative sweeteners stalled in regulation, which raised the value of retaliating.

The US market was far larger (about 8,000 tons versus 1,400 in Europe). HSC expanded to 2,000 tons and entered the US about a year after the patent expired, which gave NutraSweet hundreds of millions in extra profit. Then Coke and Pepsi signed near-exclusive long-term deals with NutraSweet. They were the real winners: HSC's presence as an outside option let them push NutraSweet's price down from $50/lb, worth roughly $200M a year, about all of their US demand.

### [S6] vault/Company Cases/Cola Wars Case.md › (intro)
kind=note cosine=0.382 bm25=6.44

The Cola Wars illustrates how Coke and Pepsi shaped competition by focusing on advertising and differentiation rather than price wars.

## Checks and timing
```json
{
  "checks": {
    "best_cosine": 0.581,
    "keyword_overlap": true,
    "question_terms_absent_from_passages": [
      "make",
      "done"
    ],
    "answerability": {
      "answerable": true,
      "passages": [
        "S1",
        "S3"
      ],
      "reason": "The passages state that HSC needed a credible commitment to enter successfully and that HSC created value but captured little of it."
    },
    "attempt": 1,
    "invalid_citations": [],
    "uncited_sentences": []
  },
  "timing": {
    "retrieval_s": 0.08,
    "generation_s": 23.22,
    "model_load_s": 0.02,
    "prompt_tokens": 2839,
    "output_tokens": 142,
    "tokens_per_second": 17.5,
    "model_calls": 2,
    "total_s": 23.3
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