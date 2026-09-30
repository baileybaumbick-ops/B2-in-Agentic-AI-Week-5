# Test run: offline

- Started 2026-09-29T22:15:33, finished 2026-09-29T22:17:54
- Network at start: **OFFLINE**, at end: **OFFLINE** (TCP check to 1.1.1.1:443, repeated before and after every step)
- Offline for every step: **True**
- Device: Windows-11-10.0.26200-SP0, Intel64 Family 6 Model 189 Stepping 1, GenuineIntel, 31.6 GB RAM (7.6 GB available at start)
- Peak memory of the local runtime (ollama + llama-server) during the run: **4.34 GB working set, 5.05 GB private**; peak system RAM in use 24.09 GB of 31.6 GB
- Ollama-reported model allocations at end: `[{"model": "gemma4:e2b", "allocated_gb": 6.87, "gpu_gb": 0.0}, {"model": "embeddinggemma:latest", "allocated_gb": 0.68, "gpu_gb": 0.0}]`

| Step | Wall time (s) | Exit | Network before -> after |
|---|---|---|---|
| Status (model, runtime, device, network) | 1.1 | 0 | OFFLINE -> OFFLINE |
| Help | 0.7 | 0 | OFFLINE -> OFFLINE |
| Ingest new source: inbox/Class 8 - Strategic and Repeated Interactions.md | 0.9 | 0 | OFFLINE -> OFFLINE |
| Re-ingest the same source (duplicate check): inbox/Class 8 - Strategic and Repeated Interactions.md | 1.0 | 0 | OFFLINE -> OFFLINE |
| Search: counter-positioning incumbent retaliate | 1.1 | 0 | OFFLINE -> OFFLINE |
| Search: Enterprise referrals body shops insurance | 1.2 | 0 | OFFLINE -> OFFLINE |
| Ask Q1 answerable | 9.5 | 0 | OFFLINE -> OFFLINE |
| Ask Q2 answerable | 8.9 | 0 | OFFLINE -> OFFLINE |
| Ask Q3 answerable | 24.7 | 0 | OFFLINE -> OFFLINE |
| Ask Q4 unsupported | 23.5 | 0 | OFFLINE -> OFFLINE |
| Chat session: casual, drafting, follow-up, ask/chat separation, notes | 64.9 | 0 | OFFLINE -> OFFLINE |
| Status after tests (loaded model memory) | 1.6 | 0 | OFFLINE -> OFFLINE |

## Status (model, runtime, device, network)

```text
> python wiki.py status
model:       gemma4:e2b (chat/ask/ingest), embeddinggemma (embeddings)
runtime:     Ollama 0.34.4 at http://127.0.0.1:11434
device:      Windows-11-10.0.26200-SP0 | Intel64 Family 6 Model 189 Stepping 1, GenuineIntel | RAM 31.6 GB, 7.6 GB available
index:       {'built_at': '2026-09-29T22:13:52', 'embed_model': 'embeddinggemma', 'chunks': 117, 'sources': 8, 'notes': 29, 'newly_embedded': 0}
loaded:      [{'model': 'gemma4:e2b', 'size_gb': 6.87, 'vram_gb': 0.0, 'context': 8192}, {'model': 'embeddinggemma:latest', 'size_gb': 0.68, 'vram_gb': 0.0, 'context': 2048}]
network:     OFFLINE (no internet connection)
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

## Ingest new source: inbox/Class 8 - Strategic and Repeated Interactions.md

```text
> python wiki.py ingest "inbox/Class 8 - Strategic and Repeated Interactions.md"
Ingesting Class 8 - Strategic and Repeated Interactions.md
  preserved original: vault/Sources/Class 8 - Strategic and Repeated Interactions.md
  unchanged since last ingest; no notes created or modified
  done in 0.0s

Class 8 - Strategic and Repeated Interactions: unchanged
index: 117 chunks from 8 sources and 29 notes (0 newly embedded)
saved: outputs/ingest/20260929-221536-class-8-strategic-and-repeated-interac.md
```

**files_added:** `[]`

## Re-ingest the same source (duplicate check): inbox/Class 8 - Strategic and Repeated Interactions.md

```text
> python wiki.py ingest "inbox/Class 8 - Strategic and Repeated Interactions.md"
Ingesting Class 8 - Strategic and Repeated Interactions.md
  preserved original: vault/Sources/Class 8 - Strategic and Repeated Interactions.md
  unchanged since last ingest; no notes created or modified
  done in 0.0s

Class 8 - Strategic and Repeated Interactions: unchanged
index: 117 chunks from 8 sources and 29 notes (0 newly embedded)
saved: outputs/ingest/20260929-221537-class-8-strategic-and-repeated-interac.md
```

**duplicate_check:** `{"files_before": 39, "files_after": 39, "new_files": []}`

## Search: counter-positioning incumbent retaliate

```text
> python wiki.py search "counter-positioning incumbent retaliate"
Top 5 passages for: counter-positioning incumbent retaliate  (0.15s)

[R1] vault/Value and Advantage/Counter-Positioning.md
     section: Key Points | note | cosine 0.619 | bm25 9.21
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
     section: Dynamic entry games | source | cosine 0.499 | bm25 10.21
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
     section: (intro) | note | cosine 0.599 | bm25 8.66
     Counter-positioning involves choosing a market position that the incumbent does not wish to
     fight over, thereby avoiding costly conflict with existing customers.

[R4] vault/Sources/Class 6 - Entry and Positioning.md
     section: Counter-positioning | source | cosine 0.604 | bm25 7.66
     An entrant has to choose a position: a price and a bundle of features. When you enter you
     take customers from incumbents, and incumbents may react. Counter-positioning means
     choosing a position the incumbent does not want to fight, because fighting would cost it
     too much with its existing customers.

[R5] vault/Entry and Competition/Water Bottle Exercise.md
     section: Key Points | note | cosine 0.436 | bm25 7.71
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

saved: outputs/search/20260929-221538-counter-positioning-incumbent-retaliate.md
```

## Search: Enterprise referrals body shops insurance

```text
> python wiki.py search "Enterprise referrals body shops insurance"
Top 5 passages for: Enterprise referrals body shops insurance  (0.19s)

[R1] vault/Sources/Class 5 - Competitive Advantage.md
     section: Case - Enterprise Rent-A-Car | source | cosine 0.452 | bm25 18.83
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

[R3] vault/Entry and Competition/Entry Deterrence.md
     section: Key Points | note | cosine 0.234 | bm25 0.0
     ### From Class 8 - Strategic and Repeated Interactions
     - Incumbents expand capacity to deter entrants. ([[Class 8 - Strategic and Repeated
     Interactions#HSC's major mistake|Class 8 › HSC's major mistake]])
     - Lock large customers into long-term contracts. ([[Class 8 - Strategic and Repeated
     Interactions#HSC's major mistake|Class 8 › HSC's major mistake]])
     - Punish small entrants to send a message. ([[Class 8 - Strategic and Repeated
     Interactions#Takeaways|Class 8 › Takeaways]])
     - Slow entrants down while they are learning. ([[Class 8 - Strategic and Repeated
     Interactions#Takeaways|Class 8 › Takeaways]])

[R4] vault/Entry and Competition/Dynamic Entry Games.md
     section: (intro) | note | cosine 0.218 | bm25 0.0
     This framework analyzes how incumbents will respond to an entrant's decision to enter,
     using backward induction to predict strategic responses.

[R5] vault/Value and Advantage/Joint Venture Exercise.md
     section: Key Points | note | cosine 0.217 | bm25 0.0
     - The three-firm venture creates the most value. ([[Class 3 - Added Value and
     Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
     - A firm should get at most its added value. ([[Class 3 - Added Value and
     Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])
     - A firm should get at least its outside option (BATNA). ([[Class 3 - Added Value and
     Irreplaceability#Joint venture exercise|Class 3 › Joint venture exercise]])

saved: outputs/search/20260929-221540-enterprise-referrals-body-shops-insurance.md
```

## Ask Q1 answerable

```text
> python wiki.py ask "In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?"
Q: In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?

Added value for Firm A is calculated as $60M, derived from $100M total value minus $40M created
without Firm A [S2]. Firm A should expect a predicted share between $50M and $60M [S2].

Sources:
  [S2] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Joint venture exercise

[answered | gemma4:e2b | total 8.52s, generation 8.41s, 16.8 tok/s]
saved: outputs/ask/20260929-221549-in-the-joint-venture-exercise-what-is-firm-a-s-a.md
```

## Ask Q2 answerable

```text
> python wiki.py ask "Why did the incumbents retaliate against Ryanair's first entry even though accommodating looked more profitable in the short run?"
Q: Why did the incumbents retaliate against Ryanair's first entry even though accommodating looked more profitable in the short run?

The incumbents retaliated harshly against Ryanair's first entry because they expected Ryanair to
expand [S2]. This retaliation occurred despite the fact that accommodating would have yielded
more profit in the short run [S2].

Sources:
  [S2] vault/Sources/Class 7 - Entry Dynamics.md › Case - Ryanair, first entry

[answered | gemma4:e2b | total 7.37s, generation 7.27s, 17.8 tok/s]
saved: outputs/ask/20260929-221559-why-did-the-incumbents-retaliate-against-ryanair.md
```

## Ask Q3 answerable

```text
> python wiki.py ask "What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?"
Q: What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?

HSC created $400-600M of value for Coke and Pepsi but captured little of it [S3]. HSC needed a
credible commitment to enter successfully [S3]. If Coke and Pepsi could not commit, they would
only buy from NutraSweet once HSC entered, meaning HSC should not have entered; conversely, with
a binding commitment, HSC should have entered, which would have benefited Coke and Pepsi [S1].

Sources:
  [S1] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › HSC's major mistake
  [S3] vault/Company Cases/Intel Case.md › Key Points

[answered | gemma4:e2b | total 23.3s, generation 23.22s, 17.5 tok/s]
saved: outputs/ask/20260929-221623-what-major-mistake-did-holland-sweetener-company.md
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

[insufficient_evidence | gemma4:e2b | total 22.25s, generation 22.1s, 17.0 tok/s]
saved: outputs/ask/20260929-221647-what-did-the-course-conclude-about-disney-s-boun.md
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

atlas> Hey there! I totally get the pre-exam jitters; it happens to the best of us.

Here are a few quick tips for staying calm:

1.  **Practice Deep Breathing:** When you feel anxious, take slow, deep breaths. It immediately signals your body to relax.
2.  **Review, Don't Cram:** Spend time reviewing what you already know rather than trying to force in brand new material right before the test.
3.  **Get Some Rest:** Make sure you get a good night's sleep. A rested brain handles stress much better.

You've got this! Focus on what you've prepared.
       (12.79s, history msgs sent: 0)

you> Can you draft a short message to my study group proposing we meet Thursday at 6pm to review?

atlas> Sure, I can draft that for you. How does this sound?

"Hey everyone, I was thinking it would be really helpful to review for the strategy exam. Would Thursday at 6 PM work for everyone to meet up and go over some material? Let me know what you think!"
       (6.62s, history msgs sent: 2)

you> Make it more casual and add that I'll bring snacks.

atlas> No problem, let's make it more casual. How about this:

"Hey team! Thinking we should link up to review for the strategy exam. How about meeting up this Thursday at 6 PM? I'll bring snacks to keep us energized! Let me know if that works for you all."
       (4.4s, history msgs sent: 4)

you> By the way, my favorite company is Patagonia.

atlas> That's cool! Patagonia is a great company; they really focus on sustainability and quality. They definitely have a strong mission that resonates with a lot of people.
       (2.34s, history msgs sent: 6)

you> /ask What is my favorite company?
Q: What is my favorite company?

Insufficient evidence: The provided passages do not contain information about a favorite
company.

Retrieved (none cited):
  [S1] vault/Sources/Class 5 - Competitive Advantage.md › Case - Enterprise Rent-A-Car (cosine 0.318)
  [S2] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › Case - Bitter Competition, the setup (cosine 0.267)
  [S3] vault/Sources/Class 1 - Introduction to Strategy.md › Defining strategy (cosine 0.178)

[insufficient_evidence | gemma4:e2b | total 28.11s, generation 27.94s, 15.5 tok/s]
saved: outputs/ask/20260929-221743-what-is-my-favorite-company.md

you> What's my favorite company again?

atlas> Your favorite company is Patagonia.
       (1.69s, history msgs sent: 8)

you> /notes In my notes, what is counter-positioning? One or two sentences.

atlas> Counter-positioning is choosing a market position that the incumbent does not wish to fight over, which avoids costly conflict with existing customers.
       (7.61s, history msgs sent: 10 | notes: N1 vault/Value and Advantage/Counter-Positioning.md › Key Points, N2 vault/Value and Advantage/Counter-Positioning.md › (intro), N3 vault/Sources/Class 6 - Entry and Positioning.md › Counter-positioning)

you> /exit
transcript saved: outputs/chat/20260929-221649.md
```

## Status after tests (loaded model memory)

```text
> python wiki.py status
model:       gemma4:e2b (chat/ask/ingest), embeddinggemma (embeddings)
runtime:     Ollama 0.34.4 at http://127.0.0.1:11434
device:      Windows-11-10.0.26200-SP0 | Intel64 Family 6 Model 189 Stepping 1, GenuineIntel | RAM 31.6 GB, 7.7 GB available
index:       {'built_at': '2026-09-29T22:15:37', 'embed_model': 'embeddinggemma', 'chunks': 117, 'sources': 8, 'notes': 29, 'newly_embedded': 0}
loaded:      [{'model': 'gemma4:e2b', 'size_gb': 6.87, 'vram_gb': 0.0, 'context': 8192}, {'model': 'embeddinggemma:latest', 'size_gb': 0.68, 'vram_gb': 0.0, 'context': 2048}]
network:     OFFLINE (no internet connection)
```
