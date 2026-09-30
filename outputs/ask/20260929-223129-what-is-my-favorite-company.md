# Ask: What is my favorite company?

**Status:** insufficient_evidence

Insufficient evidence: The provided passages do not contain information about a favorite company.

## Retrieved passages
### [S1] vault/Sources/Class 5 - Competitive Advantage.md › Case - Enterprise Rent-A-Car
kind=source cosine=0.318 bm25=2.63

Enterprise was consistently the most profitable US rental car company. Its choices reinforce each other:
- Locations: it served people who are not traveling and skipped the crowded airport market, opening many small, convenient, low-cost offices; about 90% of the US population lives within 15 minutes of one.
- Referrals: close relationships with body shops and insurers, integrated through its ARMS/ECARS systems, with staff placed at insurers. Insurers pay for the rental, so Enterprise competes on service rather than price.
- Organization: hires sociable college graduates, pays for performance tied to branch profit, promotes from within; runs its own reservation and inventory systems and sells used cars through about 30 lots.

Locations justify referrals, referrals justify locations, and the organization sustains both, which creates a chicken-and-egg problem for Avis or Hertz trying to copy it. One risk is that promote-from-within needs constant growth.

### [S2] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › Case - Bitter Competition, the setup
kind=source cosine=0.267 bm25=2.4

The case is about aspartame. NutraSweet (owned by Monsanto) held the patent, which expired in Europe and Canada in 1987 and in the US in 1992, giving a two-stage game. Minimum efficient scale was large (about 2,000 tons) compared with total demand (about 6,000 tons in 1986), and European demand was below one efficient plant. Buyers were concentrated: Coke and Pepsi bought about half. Safety regulation slowed rival sweeteners, and NutraSweet co-branded with its customers.

NutraSweet tried to stretch its patent with long-term exclusive contracts and ingredient branding (the swirl logo on cans). It charged about $70/lb, or $50/lb to Coke and Pepsi, against an estimated marginal cost of about $18/lb.

The entrant, Holland Sweetener Company (HSC), targeted buyers who wanted cheaper, possibly unbranded, aspartame. It was unlikely to be more efficient: it entered Europe at only 500 tons, below MES and low on the learning curve, with an estimated marginal cost of about $30/lb. The gap between $30 and $70 looked attractive, but NutraSweet had lower cost, a stronger brand and deep pockets.

### [S3] vault/Sources/Class 1 - Introduction to Strategy.md › Defining strategy
kind=source cosine=0.178 bm25=3.23

The lecture quoted Porter (1996): a company can outperform rivals only if it can establish a difference it can preserve. In innovative industries these differences close quickly, so innovation must be continual. Working definition: strategy is a plan of action to achieve the firm's goal (profit) that establishes a persistent difference over rivals, by dissecting context and trade-offs to understand how others will respond and which features of the environment matter.

Bad strategy is different from bad luck: Porsche decided in 2019 to make the next Macan electric-only, then in 2025 added combustion and hybrid versions back, saying it would have made the same call on the data available at the time.

### [S4] vault/Sources/Class 5 - Competitive Advantage.md › Three sources of competitive advantage
kind=source cosine=0.333 bm25=0.0

The sources mirror the ways to create value: benefit-based, cost-based, and niche (quantity)-based.

Cost-based: Chevron used sensors and machine learning for predictive maintenance on about 5,000 heat exchangers, saving millions. Porter argues operational excellence alone is not a competitive advantage, but it could be one if Chevron has more or better data or gets ahead and stays ahead. AMD under Lisa Su bet on PC and server CPUs and graphics when conventional wisdom favored mobile, paid $325 million to exit its contract with GlobalFoundries so TSMC could make its chips, and invested in graphics despite NVIDIA.

Benefit-based: Johnson & Johnson's brand certified quality for commodity products like children's Tylenol; the premium over the store brand was about 50% in 2019 ($7.49 versus $4.99). Supporting that brand required top-quality manufacturing and transparency. Around 2010, weak quality control, cost cutting and a "phantom recall" damaged the brand and pushed shoppers to generics.

### [S5] vault/Sources/Class 5 - Competitive Advantage.md › Value proposition
kind=source cosine=0.316 bm25=0.0

Firms in the same industry create value in different ways: Toyota (high-volume, reliable, practical cars) versus Porsche (low-volume, performance, distinctive styling); Uniqlo (quality basics with little style variety) versus Zara (fast-changing trend items); Apple (integrated hardware and software, ease of use, design) versus Microsoft (software with broad compatibility across third-party hardware). A value proposition is a short, precise statement of how the firm intends to create value, its plan for opening the gap between benefit B and cost C.

### [S6] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Case - Intel
kind=source cosine=0.3 bm25=0.0

In DRAM, Intel's 1972 strategy was innovation and product design, being first to market, pricing high and moving on. That fit a new market where innovation mattered more than scale. By 1979 the market grew fast, product cycles shrank, scale mattered more, and Japanese producers with better manufacturing entered. Intel's added value in DRAM collapsed, so it moved to a market that fit its strengths: microprocessors. Lessons from DRAM: protect IP, commodities are hard to profit from, and manufacturing yield matters.

In the early PC years IBM was the most irreplaceable player thanks to its mainframe reputation ("nobody ever got fired for buying IBM"), which let it set the architecture standard. IBM's open model brought many partners and growth but lower margins and less control; Apple's closed model kept margin and control but grew slower.

## Checks and timing
```json
{
  "checks": {
    "best_cosine": 0.333,
    "keyword_overlap": true,
    "question_terms_absent_from_passages": [
      "favorite"
    ],
    "answerability": {
      "answerable": "no",
      "passages": [],
      "reason": "The provided passages do not contain information about a favorite company."
    },
    "gate": "answerability 'no' with weak retrieval (best cosine below threshold)"
  },
  "timing": {
    "retrieval_s": 0.15,
    "generation_s": 18.08,
    "model_load_s": 0.08,
    "prompt_tokens": 1656,
    "output_tokens": 35,
    "tokens_per_second": 17.3,
    "model_calls": 1,
    "total_s": 18.22
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