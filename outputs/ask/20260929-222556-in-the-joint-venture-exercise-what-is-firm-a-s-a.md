# Ask: In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?

**Status:** answered

Added values in the three-firm venture are calculated based on the total profits of $100M [S2]. The added value for Firm A is $60M, calculated as $100M minus the value created without A, which is $40M [S2]. Firm A should expect a share between $50M and $60M, as A should get no less than $100M minus ($30M + $20M) [S2].

## Cited sources
- [S2] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Joint venture exercise

## Retrieved passages
### [S1] vault/Value and Advantage/Joint Venture Exercise.md › Key Points
kind=note cosine=0.635 bm25=29.2

- The three-firm venture creates the most value. ([[Class 3 - Added Value and Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
- A firm should get at most its added value. ([[Class 3 - Added Value and Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
- A firm should get at least its outside option (BATNA). ([[Class 3 - Added Value and Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])

### [S2] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Joint venture exercise
kind=source cosine=0.687 bm25=20.36

Three firms can form partnerships with these profits: all three together $100M; A and B $80M; A and C $70M; B and C $40M; any firm alone $15M.

The three-firm venture creates the most value. Added values: A = 100 - 40 = $60M; B = 100 - 70 = $30M; C = 100 - 80 = $20M.

Upper bound: a firm should get at most its added value. If A took more than $60M, B and C would get less than the $40M they can earn alone and would leave.

Lower bound: a firm should get at least its outside option (BATNA), here $15M, and more when the others have low added value. A should get no less than 100 - (30 + 20) = $50M, so A's predicted share is between $50M and $60M.

Key principles: raise your own added value, raise your outside option, and lower other players' added value to improve your negotiating position.

### [S3] vault/Value and Advantage/Joint Venture Exercise.md › (intro)
kind=note cosine=0.528 bm25=16.91

Partnerships can be structured to maximize value, where the three-firm venture creates the most value.

### [S4] vault/Value and Advantage/Added Value.md › (intro)
kind=note cosine=0.477 bm25=11.24

Added value is the total value created by a firm minus the value created without it, representing what others would pay to keep the firm.

### [S5] vault/Value and Advantage/Added Value.md › Key Points
kind=note cosine=0.443 bm25=7.32

### From Class 3 - Added Value and Irreplaceability
- Added value equals total value created with you in the market minus total value created without you. ([[Class 3 - Added Value and Irreplaceability#Defining added value|Class 3 › Defining added value]])
- A player should not expect to get more than its added value. ([[Class 3 - Added Value and Irreplaceability#Defining added value|Class 3 › Defining added value]])

### From Class 8 - Strategic and Repeated Interactions
- NutraSweet charged about $70/lb, or $50/lb to Coke and Pepsi, against an estimated marginal cost of about $18/lb. ([[Class 8 - Strategic and Repeated Interactions#Case - Bitter Competition, the setup|Class 8 › Case - Bitter Competition, the setup]])
- HSC's presence allowed Coke and Pepsi to push NutraSweet's price down from $50/lb, worth roughly $200M a year, about all of their US demand. ([[Class 8 - Strategic and Repeated Interactions#What happened|Class 8 › What happened]])

### [S6] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Defining added value
kind=source cosine=0.402 bm25=6.7

Added value = total value created with you in the market minus total value created without you. Put differently: how much would everyone else together pay to keep you in? A player should not expect to get more than its added value, because the others would be better off letting it walk away and splitting what remains.

Capacity shows how added value moves. Before the AI boom, DRAM makers were easy to replace (a buyer who skipped Samsung bought Micron), so prices were low and SK Hynix lost money in 2023. With AI demand, capacity is tight: OpenAI's projected need of up to 900,000 DRAM wafers a month is more than double the industry's HBM capacity, so each supplier is hard to replace and profits jumped. Red Sea attacks in 2025 forced rerouting around the Cape of Good Hope, straining shipping capacity and raising profits for carriers like Maersk.

## Checks and timing
```json
{
  "checks": {
    "best_cosine": 0.687,
    "keyword_overlap": true,
    "question_terms_absent_from_passages": [
      "range",
      "payoffs"
    ],
    "answerability": {
      "answerable": true,
      "passages": [
        "S2"
      ],
      "reason": "Passage [S2] calculates Firm A's added value and its predicted share range."
    },
    "attempt": 1,
    "invalid_citations": [],
    "uncited_sentences": []
  },
  "timing": {
    "retrieval_s": 0.14,
    "generation_s": 33.55,
    "model_load_s": 0.02,
    "prompt_tokens": 2675,
    "output_tokens": 154,
    "tokens_per_second": 17.2,
    "model_calls": 2,
    "total_s": 33.69
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