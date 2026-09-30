# Test run: offline

- Started 2026-09-29T22:23:57, finished 2026-09-29T22:28:36
- Network at start: **ONLINE**, at end: **ONLINE** (TCP check to 1.1.1.1:443, repeated before and after every step)
- Offline for every step: **False**
- Device: Windows-11-10.0.26200-SP0, Intel64 Family 6 Model 189 Stepping 1, GenuineIntel, 31.6 GB RAM (11.0 GB available at start)
- Peak memory of the local runtime (ollama + llama-server) during the run: **4.32 GB working set, 5.02 GB private**; peak system RAM in use 23.87 GB of 31.6 GB
- Ollama-reported model allocations at end: `[{"model": "gemma4:e2b", "allocated_gb": 6.87, "gpu_gb": 0.0}, {"model": "embeddinggemma:latest", "allocated_gb": 0.68, "gpu_gb": 0.0}]`

| Step | Wall time (s) | Exit | Network before -> after |
|---|---|---|---|
| Status (model, runtime, device, network) | 1.4 | 0 | ONLINE -> ONLINE |
| Help | 0.7 | 0 | ONLINE -> ONLINE |
| Ingest new source: inbox/Class 8 - Strategic and Repeated Interactions.md | 77.8 | 0 | ONLINE -> ONLINE |
| Re-ingest the same source (duplicate check): inbox/Class 8 - Strategic and Repeated Interactions.md | 1.4 | 0 | ONLINE -> ONLINE |
| Search: counter-positioning incumbent retaliate | 1.5 | 0 | ONLINE -> ONLINE |
| Search: Enterprise referrals body shops insurance | 1.3 | 0 | ONLINE -> ONLINE |
| Ask Q1 answerable | 34.8 | 0 | ONLINE -> ONLINE |
| Ask Q2 answerable | 30.7 | 0 | ONLINE -> ONLINE |
| Ask Q3 answerable | 27.5 | 0 | ONLINE -> ONLINE |
| Ask Q4 unsupported | 27.6 | 0 | ONLINE -> ONLINE |
| Chat session: casual, drafting, follow-up, ask/chat separation, notes | 71.7 | 0 | ONLINE -> ONLINE |
| Status after tests (loaded model memory) | 1.9 | 0 | ONLINE -> ONLINE |

## Status (model, runtime, device, network)

```text
> python wiki.py status
model:       gemma4:e2b (chat/ask/ingest), embeddinggemma (embeddings)
runtime:     Ollama 0.34.4 at http://127.0.0.1:11434
device:      Windows-11-10.0.26200-SP0 | Intel64 Family 6 Model 189 Stepping 1, GenuineIntel | RAM 31.6 GB, 10.9 GB available
index:       {'built_at': '2026-09-29T22:23:23', 'embed_model': 'embeddinggemma', 'chunks': 105, 'sources': 7, 'notes': 27, 'newly_embedded': 2}
loaded:      [{'model': 'embeddinggemma:latest', 'size_gb': 0.68, 'vram_gb': 0.0, 'context': 2048}]
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

## Ingest new source: inbox/Class 8 - Strategic and Repeated Interactions.md

```text
> python wiki.py ingest "inbox/Class 8 - Strategic and Repeated Interactions.md"
Ingesting Class 8 - Strategic and Repeated Interactions.md
  preserved original: vault/Sources/Class 8 - Strategic and Repeated Interactions.md
  drafting concept notes with gemma4:e2b (local)...
  done in 72.6s

Class 8 - Strategic and Repeated Interactions: created
  created: Repeated Interactions, Pricing Game
  updated: Added Value, Entry Deterrence
index: 115 chunks from 8 sources and 29 notes (12 newly embedded)
saved: outputs/ingest/20260929-222517-class-8-strategic-and-repeated-interac.md
```

**files_added:** `["Industry Analysis/Pricing Game.md", "Sources/Class 8 - Strategic and Repeated Interactions.md", "Strategy Foundations/Repeated Interactions.md"]`

## Re-ingest the same source (duplicate check): inbox/Class 8 - Strategic and Repeated Interactions.md

```text
> python wiki.py ingest "inbox/Class 8 - Strategic and Repeated Interactions.md"
Ingesting Class 8 - Strategic and Repeated Interactions.md
  preserved original: vault/Sources/Class 8 - Strategic and Repeated Interactions.md
  unchanged since last ingest; no notes created or modified
  done in 0.0s

Class 8 - Strategic and Repeated Interactions: unchanged
index: 115 chunks from 8 sources and 29 notes (0 newly embedded)
saved: outputs/ingest/20260929-222518-class-8-strategic-and-repeated-interac.md
```

**duplicate_check:** `{"files_before": 39, "files_after": 39, "new_files": []}`

## Search: counter-positioning incumbent retaliate

```text
> python wiki.py search "counter-positioning incumbent retaliate"
Top 5 passages for: counter-positioning incumbent retaliate  (0.18s)

[R1] vault/Value and Advantage/Counter-Positioning.md
     section: Key Points | note | cosine 0.619 | bm25 9.16
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
     section: Dynamic entry games | source | cosine 0.499 | bm25 10.19
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
     section: (intro) | note | cosine 0.599 | bm25 8.61
     Counter-positioning involves choosing a market position that the incumbent does not wish to
     fight over, thereby avoiding costly conflict with existing customers.

[R4] vault/Sources/Class 6 - Entry and Positioning.md
     section: Counter-positioning | source | cosine 0.604 | bm25 7.62
     An entrant has to choose a position: a price and a bundle of features. When you enter you
     take customers from incumbents, and incumbents may react. Counter-positioning means
     choosing a position the incumbent does not want to fight, because fighting would cost it
     too much with its existing customers.

[R5] vault/Entry and Competition/Water Bottle Exercise.md
     section: Key Points | note | cosine 0.436 | bm25 7.68
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

saved: outputs/search/20260929-222520-counter-positioning-incumbent-retaliate.md
```

## Search: Enterprise referrals body shops insurance

```text
> python wiki.py search "Enterprise referrals body shops insurance"
Top 5 passages for: Enterprise referrals body shops insurance  (0.08s)

[R1] vault/Sources/Class 5 - Competitive Advantage.md
     section: Case - Enterprise Rent-A-Car | source | cosine 0.452 | bm25 18.84
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

[R5] vault/Entry and Competition/Entry Deterrence.md
     section: Key Points | note | cosine 0.216 | bm25 0.0
     ### From Class 7 - Entry Dynamics
     - Limit pricing to make entry unattractive (Alcoa). ([[Class 7 - Entry Dynamics#Entry
     deterrence|Class 7 › Entry deterrence]])
     - Capacity expansion to commit to fighting (DuPont in titanium dioxide, CF Industries).
     ([[Class 7 - Entry Dynamics#Entry deterrence|Class 7 › Entry deterrence]])
     - Product proliferation to fill every niche so there is no room (cereal, drug variants,
     railroad branch lines). ([[Class 7 - Entry Dynamics#Entry deterrence|Class 7 › Entry
     deterrence]])
     - Predatory pricing to build a reputation (OPEC, Uber, Walmart). ([[Class 7 - Entry
     Dynamics#Entry deterrence|Class 7 › Entry deterrence]])

     ### From Class 8 - Strategic and Repeated Interactions
     - Large incumbents expand capacity to deter entrants, slow entrants down while they are
     learning. ([[Class 8 - Strategic and Repeated Interactions#Takeaways|Class 8 › Takeaways]])
     - HSC needed a credible commitment, a written purchase agreement signed before it built the
     plant. ([[Class 8 - Strategic and Repeated Interactions#HSC's major mistake|Class 8 › HSC's
     major mistake]])

saved: outputs/search/20260929-222521-enterprise-referrals-body-shops-insurance.md
```

## Ask Q1 answerable

```text
> python wiki.py ask "In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?"
Q: In the joint venture exercise, what is Firm A's added value, and what range of payoffs should Firm A expect?

Added values in the three-firm venture are calculated based on the total profits of $100M [S2].
The added value for Firm A is $60M, calculated as $100M minus the value created without A, which
is $40M [S2]. Firm A should expect a share between $50M and $60M, as A should get no less than
$100M minus ($30M + $20M) [S2].

Sources:
  [S2] vault/Sources/Class 3 - Added Value and Irreplaceability.md › Joint venture exercise

[answered | gemma4:e2b | total 33.69s, generation 33.55s, 17.2 tok/s]
saved: outputs/ask/20260929-222556-in-the-joint-venture-exercise-what-is-firm-a-s-a.md
```

## Ask Q2 answerable

```text
> python wiki.py ask "Why did the incumbents retaliate against Ryanair's first entry even though accommodating looked more profitable in the short run?"
Q: Why did the incumbents retaliate against Ryanair's first entry even though accommodating looked more profitable in the short run?

The incumbents retaliated against Ryanair's first entry because they expected Ryanair to expand
[S2]. Ryanair's initial entry was an undifferentiated direct attack with a murky target
customer, which drew retaliation [S6].

Sources:
  [S2] vault/Sources/Class 7 - Entry Dynamics.md › Case - Ryanair, first entry
  [S6] vault/Value and Advantage/Counter-Positioning.md › Key Points

[answered | gemma4:e2b | total 29.31s, generation 29.16s, 17.8 tok/s]
saved: outputs/ask/20260929-222627-why-did-the-incumbents-retaliate-against-ryanair.md
```

## Ask Q3 answerable

```text
> python wiki.py ask "What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?"
Q: What major mistake did Holland Sweetener Company make with Coke and Pepsi, and what should it have done instead?

Insufficient evidence: The passages do not explicitly state the major mistake and what should
have been done by Holland Sweetener Company.

Retrieved (none cited):
  [S1] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › HSC's major mistake (cosine 0.581)
  [S2] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › Case - Bitter Competition, the setup (cosine 0.436)
  [S3] vault/Company Cases/Cola Wars Case.md › (intro) (cosine 0.382)

[insufficient_evidence | gemma4:e2b | total 26.0s, generation 25.9s, 16.9 tok/s]
saved: outputs/ask/20260929-222654-what-major-mistake-did-holland-sweetener-company.md
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

[insufficient_evidence | gemma4:e2b | total 26.17s, generation 25.86s, 17.1 tok/s]
saved: outputs/ask/20260929-222722-what-did-the-course-conclude-about-disney-s-boun.md
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

1.  **Practice Deep Breathing:** Take slow, deep breaths. It immediately signals your nervous system to calm down.
2.  **Quick Review, Not Cramming:** Instead of trying to absorb everything at once, focus on reviewing key concepts and areas you feel weakest on.
3.  **Prioritize Sleep:** Make sure you get some good rest the night before. Being well-rested makes a huge difference in focus.

You've got this! What subject is the exam in? Maybe we can brainstorm a study plan.
       (13.52s, history msgs sent: 0)

you> Can you draft a short message to my study group proposing we meet Thursday at 6pm to review?

atlas> Sure thing, I can draft that for you. How about this:

"Hey everyone, I was thinking it would be really helpful to review for the strategy exam. Would Thursday at 6 PM work for everyone to meet up and go over some material? Let me know what you think!"

Does that sound right, or would you like me to tweak the tone?
       (8.12s, history msgs sent: 2)

you> Make it more casual and add that I'll bring snacks.

atlas> No problem! Let's make it sound more relaxed.

How about this version:

"Hey team! Thinking we should link up to review for the strategy exam. How about we meet up on Thursday at 6 PM? I'll bring snacks to keep us fueled! Let me know if that time works for you all."

How does that feel?
       (5.18s, history msgs sent: 4)

you> By the way, my favorite company is Patagonia.

atlas> Patagonia is a fantastic choice! They really nail the mission-driven, sustainability-focused approach, which is pretty interesting from a business strategy perspective. They definitely stand out in the market.

Is there anything specific about their strategy or business model you're finding particularly interesting right now?
       (4.17s, history msgs sent: 6)

you> /ask What is my favorite company?
Q: What is my favorite company?

Insufficient evidence: The provided passages do not contain information about a favorite
company.

Retrieved (none cited):
  [S1] vault/Sources/Class 5 - Competitive Advantage.md › Case - Enterprise Rent-A-Car (cosine 0.318)
  [S2] vault/Sources/Class 8 - Strategic and Repeated Interactions.md › Case - Bitter Competition, the setup (cosine 0.267)
  [S3] vault/Sources/Class 1 - Introduction to Strategy.md › Defining strategy (cosine 0.178)

[insufficient_evidence | gemma4:e2b | total 27.81s, generation 27.7s, 17.1 tok/s]
saved: outputs/ask/20260929-222822-what-is-my-favorite-company.md

you> What's my favorite company again?

atlas> Your favorite company is Patagonia. 😊
       (2.24s, history msgs sent: 8)

you> /notes In my notes, what is counter-positioning? One or two sentences.

atlas> Based on your notes, counter-positioning is about choosing a market position that the incumbent does not wish to fight over, which avoids costly conflict with existing customers. It involves selecting a specific price and feature bundle for entry.
       (9.01s, history msgs sent: 10 | notes: N1 vault/Value and Advantage/Counter-Positioning.md › Key Points, N2 vault/Value and Advantage/Counter-Positioning.md › (intro), N3 vault/Sources/Class 6 - Entry and Positioning.md › Counter-positioning)

you> /exit
transcript saved: outputs/chat/20260929-222724.md
```

## Status after tests (loaded model memory)

```text
> python wiki.py status
model:       gemma4:e2b (chat/ask/ingest), embeddinggemma (embeddings)
runtime:     Ollama 0.34.4 at http://127.0.0.1:11434
device:      Windows-11-10.0.26200-SP0 | Intel64 Family 6 Model 189 Stepping 1, GenuineIntel | RAM 31.6 GB, 8.0 GB available
index:       {'built_at': '2026-09-29T22:25:18', 'embed_model': 'embeddinggemma', 'chunks': 115, 'sources': 8, 'notes': 29, 'newly_embedded': 0}
loaded:      [{'model': 'gemma4:e2b', 'size_gb': 6.87, 'vram_gb': 0.0, 'context': 8192}, {'model': 'embeddinggemma:latest', 'size_gb': 0.68, 'vram_gb': 0.0, 'context': 2048}]
network:     online (internet reachable)
```
