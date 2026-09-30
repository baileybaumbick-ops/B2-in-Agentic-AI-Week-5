# Ask: What did the course conclude about Disney's boundaries of the firm?

**Status:** insufficient_evidence

Insufficient evidence: The provided passages do not contain any information about Disney's boundaries.

## Retrieved passages
### [S1] vault/Sources/Class 2 - Value Creation and Capture.md › Profit maximization as the goal
kind=source cosine=0.33 bm25=3.98

Why assume firms maximize profit? A firm that ignores profit goes bankrupt, cannot fund the investments it needs, and gets its assets redeployed by the capital market (for example through a takeover). Long-run profit maximization is not quarterly earnings management, short-run exploitation of employees, suppliers or customers, or unethical shortcuts.

Social impact: for firms whose customers value it, social impact is part of the value proposition, so long-run profit and social impact line up. For firms whose customers do not value it, competition makes costly social goals hard to sustain, and regulation is needed to level the field. Large institutional shareholders can push managers either because they have pro-social preferences or because they believe it raises long-run profits. The course tools also apply to non-profits: how to best reach a social objective with limited resources.

"Maximize profit" is a goal, not a strategy, in the same way "win" is a coach's goal. Strategy is the set of decisions (inputs, processes, products, customers, prices) that lead to long-run profit.

### [S2] vault/Value and Advantage/Joint Venture Exercise.md › Key Points
kind=note cosine=0.327 bm25=2.62

- The three-firm venture creates the most value. ([[Class 3 - Added Value and Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
- A firm should get at most its added value. ([[Class 3 - Added Value and Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
- A firm should get at least its outside option (BATNA). ([[Class 3 - Added Value and Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])

### [S3] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Joint venture exercise
kind=source cosine=0.318 bm25=2.53

Three firms can form partnerships with these profits: all three together $100M; A and B $80M; A and C $70M; B and C $40M; any firm alone $15M.

The three-firm venture creates the most value. Added values: A = 100 - 40 = $60M; B = 100 - 70 = $30M; C = 100 - 80 = $20M.

Upper bound: a firm should get at most its added value. If A took more than $60M, B and C would get less than the $40M they can earn alone and would leave.

Lower bound: a firm should get at least its outside option (BATNA), here $15M, and more when the others have low added value. A should get no less than 100 - (30 + 20) = $50M, so A's predicted share is between $50M and $60M.

Key principles: raise your own added value, raise your outside option, and lower other players' added value to improve your negotiating position.

### [S4] vault/Value and Advantage/AAA Framework.md › Key Points
kind=note cosine=0.289 bm25=2.73

- Assets are what the firm has, including resources and capabilities. ([[Class 5 - Competitive Advantage#The AAA framework|Class 5 › The AAA framework]])
- Activities are what the firm chooses to do with its assets, and strategy lives in the activities. ([[Class 5 - Competitive Advantage#The AAA framework|Class 5 › The AAA framework]])
- Advantage results when the chosen activities suit the context. ([[Class 5 - Competitive Advantage#The AAA framework|Class 5 › The AAA framework]])

### [S5] vault/Sources/Class 1 - Introduction to Strategy.md › Why strategy is hard
kind=source cosine=0.27 bm25=3.31

Profit is revenue minus cost, so "raise revenue, cut cost" sounds easy. The lecture argued that good strategy is hard for three reasons: decisions can have counterintuitive effects that change outcomes a lot, you have to predict how other players will respond to your choices, and the world is noisy, so you must figure out which few factors actually matter. The two tools for making progress are understanding the context and dissecting the trade-offs.

A warm-up example: a heavy-machinery CEO is offered technology that makes plants easy to repurpose or sell. Flexibility sounds good, but if a potential entrant is watching, being able to walk away easily can weaken your threat to fight entry. This previews the entry-deterrence ideas later in the course.

### [S6] vault/Sources/Class 5 - Competitive Advantage.md › Value proposition
kind=source cosine=0.279 bm25=1.76

Firms in the same industry create value in different ways: Toyota (high-volume, reliable, practical cars) versus Porsche (low-volume, performance, distinctive styling); Uniqlo (quality basics with little style variety) versus Zara (fast-changing trend items); Apple (integrated hardware and software, ease of use, design) versus Microsoft (software with broad compatibility across third-party hardware). A value proposition is a short, precise statement of how the firm intends to create value, its plan for opening the gap between benefit B and cost C.

## Checks and timing
```json
{
  "checks": {
    "best_cosine": 0.33,
    "keyword_overlap": true,
    "question_terms_absent_from_passages": [
      "disney's",
      "boundaries"
    ],
    "answerability": {
      "answerable": "no",
      "passages": [],
      "reason": "The provided passages do not contain any information about Disney's boundaries."
    },
    "gate": "answerability 'no' with weak retrieval (best cosine below threshold)"
  },
  "timing": {
    "retrieval_s": 0.07,
    "generation_s": 17.9,
    "model_load_s": 0.14,
    "prompt_tokens": 1497,
    "output_tokens": 37,
    "tokens_per_second": 18.0,
    "model_calls": 1,
    "total_s": 17.97
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