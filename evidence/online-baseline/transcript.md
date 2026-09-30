# Test run: online-baseline

- Started 2026-09-29T21:55:21, finished 2026-09-29T21:57:05
- Network at start: **ONLINE**, at end: **ONLINE** (TCP check to 1.1.1.1:443)
- Device: Windows-11-10.0.26200-SP0, Intel64 Family 6 Model 189 Stepping 1, GenuineIntel, 31.6 GB RAM (8.1 GB available at start)
- Peak resident memory of Ollama processes during the run: **0.11 GB**

| Step | Wall time (s) | Exit |
|---|---|---|
| Status (model, runtime, device, network) | 2.6 | 0 |
| Help | 1.6 | 0 |
| Re-ingest the same source (duplicate check): vault/Sources/Class 3 - Added Value and Irreplaceability.md | 2.3 | 0 |
| Search: counter-positioning incumbent retaliate | 2.2 | 0 |
| Search: Enterprise referrals body shops insurance | 2.3 | 0 |
| Ask Q1 answerable | 14.9 | 0 |
| Ask Q2 answerable | 12.6 | 0 |
| Ask Q3 answerable | 17.3 | 0 |
| Ask Q4 unsupported | 4.2 | 0 |
| Chat session: casual, drafting, follow-up, ask/chat separation, notes | 41.1 | 0 |
| Status after tests (loaded model memory) | 3.3 | 0 |

## Status (model, runtime, device, network)

```text
> python wiki.py status
model:       gemma4:e2b (chat/ask/ingest), embeddinggemma (embeddings)
runtime:     Ollama 0.34.4 at http://127.0.0.1:11434
device:      Windows-11-10.0.26200-SP0 | Intel64 Family 6 Model 189 Stepping 1, GenuineIntel | RAM 31.6 GB, 8.0 GB available
index:       {'built_at': '2026-09-29T21:49:37', 'embed_model': 'embeddinggemma', 'chunks': 105, 'sources': 7, 'notes': 27, 'newly_embedded': 4}
loaded:      [{'model': 'gemma4:e2b', 'size_gb': 6.87, 'vram_gb': 0.0, 'context': 8192}, {'model': 'embeddinggemma:latest', 'size_gb': 0.68, 'vram_gb': 0.0, 'context': 2048}]
network:     online (internet reachable)
```

## Help

```text
> python wiki.py help
wiki - personal wiki assistant running on local Gemma (gemma4:e2b via Ollama)

MODES
  chat                 Talk with Atlas, your assistant. Keeps conversation context and
                       handles casual questions and drafting. It only looks at your notes
                       when you mention them ("in my notes...") or type /notes.
  ask "question"       Neutral factual answer built ONLY from retrieved wiki passages,
                       with [S#] citations, or an explicit insufficient-evidence reply.
                       Stateless: never sees chat history.
  search "query"       Returns the original passages and file paths. No model answer.
  ingest <path>...     Preserve a source (.md/.txt/.pdf) in vault/Sources, draft linked
                       concept notes with Gemma, and rebuild the index. Re-ingesting an
                       unchanged file is a no-op; --force redrafts the source's notes in place.
  rebuild              Re-apply naming rules and curation.json (renames, topic folders),
                       re-render notes, links and index pages, and reindex. No model calls.
  status               Show the model, runtime, index size and network state.
  help                 Show this message.

CHAT COMMANDS
  /ask <question>      Run ask mode from inside chat (chat history is NOT passed to it)
  /search <query>      Run search mode from inside chat
  /notes <message>     Chat, and include the top wiki passages as optional context
  /reset               Clear the conversation        /exit   Leave chat

Everything runs locally: models via Ollama at http://127.0.0.1:11434, index in .index/,
saved outputs in outputs/. There is no cloud fallback.
```

## Re-ingest the same source (duplicate check): vault/Sources/Class 3 - Added Value and Irreplaceability.md

```text
> python wiki.py ingest "vault/Sources/Class 3 - Added Value and Irreplaceability.md"
Ingesting Class 3 - Added Value and Irreplaceability.md
  preserved original: vault/Sources/Class 3 - Added Value and Irreplaceability.md
  unchanged since last ingest; no notes created or modified
  done in 0.0s

Class 3 - Added Value and Irreplaceability: unchanged
index: 105 chunks from 7 sources and 27 notes (0 newly embedded)
saved: outputs/ingest/20260929-215527-class-3-added-value-and-irreplaceabili.md
```

**duplicate_check:** `{"files_before": 36, "files_after": 36, "new_files": []}`

## Search: counter-positioning incumbent retaliate

```text
> python wiki.py search "counter-positioning incumbent retaliate"
Top 5 passages for: counter-positioning incumbent retaliate  (0.11s)

[R1] vault/Value and Advantage/Counter-Positioning.md
     section: Key Points | note | cosine 0.619 | bm25 8.78
     ### From Class 6 - Entry and Positioning
     - An entrant must choose a position regarding price and a bundle of features. ([[Class 6 -
     Entry and Positioning#Counter-positioning|Class 6 › Counter-positioning]])
     - Counter-positioning means choosing a position the incumbent does not want to fight.
     ([[Class 6 - Entry and Positioning#Counter-positioning|Class 6 › Counter-positioning]])
     - Fighting with incumbents would cost too much with their existing customers. ([[Class 6 -
     Entry and Positioning#Counter-positioning|Class 6 › Counter-positioning]])
     - Counter-positioning works better when the incumbent would find it hard to make your
     product well. ([[Class 6 - Entry and Positioning#Counter-positioning|Class 6 › Counter-
     positioning]])

[R2] vault/Sources/Class 7 - Entry Dynamics.md
     section: Dynamic entry games | source | cosine 0.499 | bm25 9.82
     An entry game is a structured way to think about how an incumbent will respond. The entrant
     chooses to enter or stay out; the incumbent chooses to retaliate or accommodate. You solve
     it by looking forward and reasoning backward (backward induction).

     In the basic Ryanair game the incumbent gets £69M if there is no entry, £60M if it
     accommodates and £34M if it retaliates, so it accommodates, and the entrant enters if its
     fixed cost F is below £4.4M.

     Add a second stage where, after accommodation, the entrant can enter another of the
     incumbent's markets (entrant £40M - F, incumbent £30M). Now the entrant would surely
     expand, so the incumbent compares £34M (retaliate) with £30M (accommodate then lose the
     second market) and retaliates. Knowing that, the entrant stays out. The counterintuitive
     lesson: having the extra option to expand makes the entrant worse off, because it triggers
     retaliation. The entrant would remove that option if it could.

     A threat to retaliate works only if it is credible: when the moment comes, the incumbent
     must actually want to carry it out.

[R3] vault/Value and Advantage/Counter-Positioning.md
     section: (intro) | note | cosine 0.599 | bm25 8.26
     Counter-positioning involves choosing a market position that the incumbent does not wish to
     fight over, thereby avoiding costly conflict with existing customers.

[R4] vault/Sources/Class 6 - Entry and Positioning.md
     section: Counter-positioning | source | cosine 0.604 | bm25 7.29
     An entrant has to choose a position: a price and a bundle of features. When you enter you
     take customers from incumbents, and incumbents may react. Counter-positioning means
     choosing a position the incumbent does not want to fight, because fighting would cost it
     too much with its existing customers.

[R5] vault/Entry and Competition/Water Bottle Exercise.md
     section: Key Points | note | cosine 0.436 | bm25 7.34
     - A monopolist selling the insulated bottle at $20 to all 10 customers earns a profit of
     $100. ([[Class 6 - Entry and Positioning#Water bottle exercise|Class 6 › Water bottle
     exercise]])
     - If the entrant copies the bottle at $19, the incumbent undercuts to $18.99, leading
     toward a price war. ([[Class 6 - Entry and Positioning#Water bottle exercise|Class 6 ›
     Water bottle exercise]])
     - To win back a few customers, the incumbent must lower its price to all of them. ([[Class
     6 - Entry and Positioning#Water bottle exercise|Class 6 › Water bottle exercise]])
     - Counter-positioning works better when the incumbent would find it hard to make your
     product well. ([[Class 6 - Entry and Positioning#Counter-positioning|Class 6 › Counter-
     positioning]])

saved: outputs/search/20260929-215530-counter-positioning-incumbent-retaliate.md
```

## Search: Enterprise referrals body shops insurance

```text
> python wiki.py search "Enterprise referrals body shops insurance"
Top 5 passages for: Enterprise referrals body shops insurance  (0.12s)

[R1] vault/Sources/Class 5 - Competitive Advantage.md
     section: Case - Enterprise Rent-A-Car | source | cosine 0.452 | bm25 18.26
     Enterprise was consistently the most profitable US rental car company. Its choices
     reinforce each other:
     - Locations: it served people who are not traveling and skipped the crowded airport market,
     opening many small, convenient, low-cost offices; about 90% of the US population lives
     within 15 minutes of one.
     - Referrals: close relationships with body shops and insurers, integrated through its
     ARMS/ECARS systems, with staff placed at insurers. Insurers pay for the rental, so
     Enterprise competes on service rather than price.
     - Organization: hires sociable college graduates, pays for performance tied to branch
     profit, promotes from within; runs its own reservation and inventory systems and sells used
     cars through about 30 lots.

     Locations justify referrals, referrals justify locations, and the organization sustains
     both, which creates a chicken-and-egg problem for Avis or Hertz trying to copy it. One risk
     is that promote-from-within needs constant growth.

[R2] vault/Entry and Competition/Dynamic Entry Games.md
     section: Key Points | note | cosine 0.241 | bm25 0.0
     - The incumbent gets £69M if there is no entry, £60M if it accommodates and £34M if it
     retaliates. ([[Class 7 - Entry Dynamics#Dynamic entry games|Class 7 › Dynamic entry
     games]])
     - The entrant enters if its fixed cost F is below £4.4M. ([[Class 7 - Entry
     Dynamics#Dynamic entry games|Class 7 › Dynamic entry games]])
     - Having the extra option to expand makes the entrant worse off because it triggers
     retaliation. ([[Class 7 - Entry Dynamics#Dynamic entry games|Class 7 › Dynamic entry
     games]])

[R3] vault/Entry and Competition/Dynamic Entry Games.md
     section: (intro) | note | cosine 0.218 | bm25 0.0
     This framework analyzes how incumbents will respond to an entrant's decision to enter,
     using backward induction to predict strategic responses.

[R4] vault/Value and Advantage/Joint Venture Exercise.md
     section: Key Points | note | cosine 0.217 | bm25 0.0
     - The three-firm venture creates the most value. ([[Class 3 - Added Value and
     Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
     - A firm should get at most its added value. ([[Class 3 - Added Value and
     Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
     - A firm should get at least its outside option (BATNA). ([[Class 3 - Added Value and
     Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])

[R5] vault/Sources/Class 5 - Competitive Advantage.md
     section: Value proposition | source | cosine 0.213 | bm25 0.0
     Firms in the same industry create value in different ways: Toyota (high-volume, reliable,
     practical cars) versus Porsche (low-volume, performance, distinctive styling); Uniqlo
     (quality basics with little style variety) versus Zara (fast-changing trend items); Apple
     (integrated hardware and software, ease of use, design) versus Microsoft (software with
     broad compatibility across third-party hardware). A value proposition is a short, precise
     statement of how the firm intends to create value, its plan for opening the gap between
     benefit B and cost C.

saved: outputs/search/20260929-215532-enterprise-referrals-body-shops-insurance.md
```

## Ask Q1 answerable

```text
> python wiki.py ask "In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?"
Q: In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?

Added values are calculated based on the total value created with a firm in the market minus the
total value created without it [S5]. In the three-firm venture, the added values are calculated
as follows: A = $100M - $40M = $60M, B = $100M - $70M = $30M, and C = $100M - $80M = $20M [S2].
A should get no less than $50M, and A's predicted share is between $50M and $60M [S2].

Sources:
  [S2] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Joint venture exercise
  [S5] vault/Value and Advantage/Added Value.md › Key Points

[answered | gemma4:e2b | total 12.37s, generation 12.17s, 18.3 tok/s]
saved: outputs/ask/20260929-215547-in-the-joint-venture-exercise-what-is-firm-a-s-a.md
```

## Ask Q2 answerable

```text
> python wiki.py ask "Why did the incumbents retaliate against Ryanair's first entry even though accommodating looked more profitable in the short run?"
Q: Why did the incumbents retaliate against Ryanair's first entry even though accommodating looked more profitable in the short run?

The incumbents retaliated against Ryanair's first entry because they expected Ryanair to expand
[S2]. The incumbents also retaliated harshly because Ryanair nearly went bankrupt [S2].

Sources:
  [S2] vault/Sources/Class 7 - Entry Dynamics.md › Case - Ryanair, first entry

[answered | gemma4:e2b | total 9.79s, generation 9.57s, 18.1 tok/s]
saved: outputs/ask/20260929-215559-why-did-the-incumbents-retaliate-against-ryanair.md
```

## Ask Q3 answerable

```text
> python wiki.py ask "What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?"
Q: What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?

Insufficient evidence: The provided passages do not contain information about Holland Sweetener
Company's actions or advice regarding Coke and Pepsi.

Retrieved (none cited):
  [S1] vault/Sources/Class 4 - Industry Analysis.md › Case - Cola Wars (cosine 0.416)
  [S2] vault/Company Cases/Cola Wars Case.md › (intro) (cosine 0.382)
  [S3] vault/Industry Analysis/Rivalry.md › Key Points (cosine 0.307)

[insufficient_evidence | gemma4:e2b | total 15.6s, generation 15.45s, 19.2 tok/s]
saved: outputs/ask/20260929-215617-what-major-mistake-did-holland-sweetener-company.md
```

## Ask Q4 unsupported

```text
> python wiki.py ask "What did the course conclude about Disney's boundaries of the firm?"
Q: What did the course conclude about Disney's boundaries of the firm?

Insufficient evidence: The provided passages do not contain information about Disney's
boundaries.

Retrieved (none cited):
  [S1] vault/Sources/Class 2 - Value Creation and Capture.md › Profit maximization as the goal (cosine 0.33)
  [S2] vault/Value and Advantage/Joint Venture Exercise.md › Key Points (cosine 0.327)
  [S3] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Joint venture exercise (cosine 0.318)

[insufficient_evidence | gemma4:e2b | total 2.0s, generation 1.91s, 21.2 tok/s]
saved: outputs/ask/20260929-215621-what-did-the-course-conclude-about-disney-s-boun.md
```

## Chat session: casual, drafting, follow-up, ask/chat separation, notes

```text
> python wiki.py chat
(stdin:)
  Hey Atlas! I have a strategy exam next week and I'm a bit nervous. Any quick tips for staying calm?
  Can you draft a short message to my study group proposing we meet Thursday at 6pm to review?
  Make it more casual and add that I'll bring snacks.
  By the way, my favorite company is Patagonia.
  /ask What is my favorite company?
  What's my favorite company again?
  /notes In my notes, what is counter-positioning? One or two sentences.
  /exit
Atlas (local gemma4:e2b). Type /help for commands, /exit to quit.

you> Hey Atlas! I have a strategy exam next week and I'm a bit nervous. Any quick tips for staying calm?

atlas> Hey there! Don't sweat it too much; we can definitely tackle this.

For staying calm before an exam, I usually suggest a few quick things:

1.  **Practice Mindfulness:** Take a few slow, deep breaths. Focusing on your breath can really reset your nervous system.
2.  **Review Your Plan:** Quickly look over the study plan you've already made. Knowing you've put in the work helps reduce anxiety.
3.  **Prioritize Rest:** Make sure you get decent sleep tonight. Being well-rested makes a huge difference in how you think.

You've got this! What topic are you focusing on right now?
       (12.05s, history msgs sent: 0)

you> Can you draft a short message to my study group proposing we meet Thursday at 6pm to review?

atlas> Sure, I can draft that for you. Here are a couple of options, depending on your group's vibe:

**Option 1 (Direct and Casual):**

> Hey everyone, want to meet up on Thursday at 6 PM to review for the exam? Let me know if that works for you!

**Option 2 (Slightly More Enthusiastic):**

> Team, I was thinking we could all meet on Thursday at 6 PM to go over some material. Sound good?

Which one feels better for your group?
       (7.99s, history msgs sent: 2)

you> Make it more casual and add that I'll bring snacks.

atlas> No problem! Let's inject some snack-related enthusiasm.

Here's a revised, more casual option:

> Hey team! How about we meet up on Thursday at 6 PM to review? I'll bring snacks to keep us energized! Let me know if you can make it.

How does that sound?
       (3.74s, history msgs sent: 4)

you> By the way, my favorite company is Patagonia.

atlas> Patagonia is a fantastic choice! They really nail the balance between business and purpose, which is something a lot of successful companies strive for. They've got a really strong reputation for sustainability and quality.

Is there anything specific about their business strategy you find interesting?
       (3.21s, history msgs sent: 6)

you> /ask What is my favorite company?
Q: What is my favorite company?

Insufficient evidence: The passages do not contain information about a favorite company.

Retrieved (none cited):
  [S1] vault/Sources/Class 5 - Competitive Advantage.md › Case - Enterprise Rent-A-Car (cosine 0.318)
  [S2] vault/Sources/Class 1 - Introduction to Strategy.md › Defining strategy (cosine 0.178)
  [S3] vault/Sources/Class 5 - Competitive Advantage.md › Three sources of competitive advantage (cosine 0.333)

[insufficient_evidence | gemma4:e2b | total 2.21s, generation 2.13s, 18.0 tok/s]
saved: outputs/ask/20260929-215652-what-is-my-favorite-company.md

you> What's my favorite company again?

atlas> Your favorite company is Patagonia. 😊
       (1.95s, history msgs sent: 8)

you> /notes In my notes, what is counter-positioning? One or two sentences.

atlas> Counter-positioning is choosing a market position that an incumbent competitor does not want to fight over, which helps an entrant avoid costly conflict with existing customers.
       (7.63s, history msgs sent: 10 | notes: N1 vault/Value and Advantage/Counter-Positioning.md › Key Points, N2 vault/Value and Advantage/Counter-Positioning.md › (intro), N3 vault/Sources/Class 6 - Entry and Positioning.md › Counter-positioning)

you> /exit
transcript saved: outputs/chat/20260929-215623.md
```

## Status after tests (loaded model memory)

```text
> python wiki.py status
model:       gemma4:e2b (chat/ask/ingest), embeddinggemma (embeddings)
runtime:     Ollama 0.34.4 at http://127.0.0.1:11434
device:      Windows-11-10.0.26200-SP0 | Intel64 Family 6 Model 189 Stepping 1, GenuineIntel | RAM 31.6 GB, 7.4 GB available
index:       {'built_at': '2026-09-29T21:55:27', 'embed_model': 'embeddinggemma', 'chunks': 105, 'sources': 7, 'notes': 27, 'newly_embedded': 0}
loaded:      [{'model': 'gemma4:e2b', 'size_gb': 6.87, 'vram_gb': 0.0, 'context': 8192}, {'model': 'embeddinggemma:latest', 'size_gb': 0.68, 'vram_gb': 0.0, 'context': 2048}]
network:     online (internet reachable)
```
