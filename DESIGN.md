# Simulation 2 — one agent per attendee, run through the summit's own schedule

*Design notes, 2026-09-23. Jason's decisions are marked **(J)**; the rest are recommendations for
his review. Prior art: `oxjobs/archived/agent-simulation-prior-art/EXPLORE.md` (#782).*

## Fixed by Jason (J)

- One agent per attendee (33 incl. Jason), all on **`claude-opus-5-5`**. No cheaper model anywhere
  in the attendee loop.
- Each agent's long-term intellectual memory is **its own corpus, reached by retrieval**. Before
  every contribution the agent searches its own writing for what it has actually said on the
  matter. The corpus, not the prompt, is what makes the character faithful.
- **No personality.** Every attendee has the same force of personality: nobody is louder, more
  charismatic, more stubborn or more retiring. Each represents its intellectual position as fairly
  and directly as it can. This is a stated limitation of the simulation, not something to paper over.
- **Bitter-lesson build.** Short instructions; no cognitive-architecture modules; the model does
  the interpreting. The one structural thing we add is retrieval.
- **One convener/referee agent**, not a cast of timekeepers and thread-finders. It sees everything,
  keeps people on task, keeps things converging on a manifesto.
- Procedural turn-taking (round robin and the like) instead of simulated initiative. Limited
  randomization; randomness must never be what decides the outcome.
- Budget: tens of dollars to a few hundred per run; under $1,000 total. Multiple runs are out of
  scope until a single run is costed.
- Product = the manifesto (1,500–2,500 words, principles, noted dissents).

## Recommendation: mirror the real schedule, not a caucus or a convention

The real event already solves the problem personality would otherwise solve: it says who speaks
first and when. Session leads give provocations; named panelists respond; the room follows; each
session ends in a harvest; Session 5 names interventions; a small writing committee drafts.
That is a procedural skeleton that needs no initiative from anyone, which is exactly the
constraint we are under. It is also what the charter (decision 10) says to anchor to, it keeps the
pre-registered-prediction property (we predict the output of *this* process), and it is cheap:
about 400 attendee turns per run instead of 528 pairwise conversations.

Against the two alternatives:

- **Pairwise speed-dating → clustering → caucus representatives.** Lovely artifacts (528
  transcripts, an affinity matrix), but it invents a social process that never happens, the
  "want to work with" score is precisely the personality-flavoured judgement we said we don't have
  data for, and it is the expensive part: ~$1.50 per conversation on Opus 5.5 → ~$800 before the
  workshop even starts. Keep it as a labelled variant. The cheap version of its one real payoff
  (birds of a feather) is below, under unconference rooms.
- **Constitutional convention: 33-person loop until convergence.** Simple, but a single
  undifferentiated room is where the literature says consensus collapses fastest (Okawa: conformity
  pressure scales with N), and "until convergence" rewards the collapse. The scheduled sessions
  partition the room by topic, which preserves variance for free. Keep as a labelled variant.

## The pipeline

### 0. Character cards (Phase 2, never built)

There are no cards. The only per-person summaries that exist are Jason's private briefing, which is
opinionated and barred from the simulation by the charter. Build cards now, cheaply:

- One Opus 5.5 call per attendee: `INDEX.md` + a recency-weighted sample of `by/` and `av/`
  (~150K tokens, 2024–2026 first) → a card of **positions with citations** (file path + quote), what
  they would push back on, and **where the corpus is silent** (topics they have never addressed,
  so the agent can abstain instead of confabulating). No adjectives about temperament.
- Cost ≈ $1/person, ~$35 total. Public-bound, opinion-free, lives here in `cards/`.
- Why a card at all if retrieval does the work: retrieval has a cold-start problem. The card tells
  the agent what it cares about so it knows what to look up; the corpus supplies the words.

### 1. Retrieval index

- Chunk `by/` + `av/` into ~400-token passages tagged (person, file, year, source_url); social posts
  as single chunks. ~120K passages for 23M words.
- Hybrid: BM25 + a local sentence embedding (multilingual-e5-base or bge on MPS; ~20–30 min for the
  whole corpus, one GPU job at a time, watchdog). `~/.venvs/topics1268` already has
  sentence-transformers and anthropic.
- One tool exposed to agents: `recall(query, k)`, scoped to the calling agent's own dossier,
  MMR-diversified (plain top-k makes retrieval a variance-reduction operator), returns passages
  with year and source, and **logs chunk IDs per turn** (the prior-art detector for "retrieval
  keeps returning the same quotable passages").

### 2. The attendee agent

System prompt, ~10 lines: you are simulating <name> at this workshop; your job is to say what
they would actually say, as accurately as you can; before each contribution call `recall` on the
matter at hand (2–4 searches) and speak from what you find; where your corpus has nothing, say
less rather than invent; speak plainly, ≤200 words a turn, first person, no stage directions; you
have the same force of personality as everyone else. Then the card, then the tool. Cache order:
shared instructions → **transcript so far** → card, so the growing transcript is a shared cached
prefix across all 33 agents in a round.

After each session, one short diary entry (what I heard, what I now think). It is the agent's
medium-term memory across the day and the human-readable trace (Park et al. 2023).

### 3. The convener

One Opus 5.5 agent (or Claude Code as orchestrator) that runs the schedule and writes the
harvests. Its powers, and the limits on them:

- Runs each session: the lead's provocation (grounded in the concept note's own arguments), then
  named panelists in schedule order, then room turns.
- **Room turns: may call on people, but every attendee gets a floor of one turn per session it
  attends, and every call-on is logged with a one-line reason.** Calling on people is lifelike and
  fixes the "who goes next" problem, but it is real steering power; floors and a log are how we
  keep it from silently choosing the outcome. Default order for uncalled turns is round robin from
  a per-session random offset (the only randomness in the run).
- Writes the harvest: 3–5 claims, then a separate pass that preserves minority positions
  (Habermas-Machine style). Dissent is a first-class output from Session 1 on.
- **Never edits an attendee's words and never speaks as one.**
- Any diagnostic scoring (drift, caricature) is a separate, non-steering pass whose output never
  enters an agent's context (#782 implication 17).

### 4. The day

1. **Wed unconference (3 rooms).** Topics = the real sheet (cognitive atrophy; who pays and who
   gets paid; when books can converse; the role of knowledge in the age of LLMs; citation justice,
   plus whatever else landed). Each agent picks its room by one `recall`-grounded choice: that is
   the cheap "birds of a feather" step. 2 rounds per room.
2. **Thu Sessions 1–4** as scheduled, leads and panelists as published.
3. **Marketplace talks** (O'Reilly, Springer, Vincent): three provocations, one discussion round.
4. **Session 5**: interventions, open questions, who isn't in the room.
5. **Session 6**: Cukier + Miller synthesis, as agents, from the harvests and diaries.

### 5. The manifesto

The real process is a 3–4 person writing committee drafting within two weeks. We don't know who.
So, per Jason's lean: **the drafters are persona-free.** The convener drafts v1 from the six
harvests, the interventions and the synthesis. Then two review rounds where every attendee agent,
grounded in its corpus, does one of: sign, propose a specific edit, or file a ≤150-word dissent.
The convener revises between rounds. Final = manifesto + noted dissents by name + signature count.
The signature count and dissent count are also the two metrics theory says will be most wrong
(too consensual), so we get the charter's §3 scoring axes for free.

## Cost (Opus 5.5 at $4 in / $20 out per MTok)

| Item | Turns | Per turn | Total |
|---|---:|---|---:|
| Attendee turns (unconference 66 + sessions ~240 + reviews 66 + diaries) | ~400 | ~3 calls × ~30K in, ~3K out | ~$150 before cache |
| Prompt cache on the shared transcript prefix | | ≥50% of input | −$50 |
| Cards (once) | 33 | ~150K in, 3K out | ~$35 |
| Convener, harvests, drafts | ~40 | long context | ~$20 |
| **One run** | | | **~$130–170** |

Two or three runs fit the budget; the Batch API would halve it but adds latency and the memory
rule says not mid-build.

## Known limitations to state up front

- No personality data; equal force of personality assumed. Real outcomes depend heavily on it.
- Jason is in the real room having read this; sessions without him score cleaner.
- Prediction is expected to be more consensual, more confident and less idiosyncratic than the
  real manifesto (#782). Publish that prediction with the freeze.
- Model may already know these people's public positions; the corpus citation rate per claim is
  the only handle we have on that.
- Freeze: the summit is today. The manifesto is due ~Oct 8. Outputs committed before it exists,
  with model IDs and prompts, still count as a pre-registered prediction of the manifesto.
