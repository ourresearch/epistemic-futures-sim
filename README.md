# Epistemic Futures — simulated summit

Simulations of the MIT Epistemic Futures Summit (Sept 23–24, 2026), run against the public corpus
at `ourresearch/epistemic-futures-corpus`. Charter: `oxjobs/plans/epistemic.md` (label `EPISTEMIC`).

**Reads only the public corpus.** Never `about/`, `prep/`, or `notes/` from the private repo.
**Every generated document carries a SIMULATED header.** These are predictions by AI agents; no
attendee wrote or endorsed any of it.

| Dir | What |
|---|---|
| `sim1-simple/` | One Claude Code session (Opus 5.5) told to predict the manifesto from the corpus. Prompt, outputs, run log. |
| `sim2-agents/` | One RAG-grounded Opus 5.5 agent per attendee, run through the summit's real schedule. See `DESIGN.md`. |

The real manifesto is due within two weeks of the summit (~Oct 8, 2026). Anything committed here
before it exists is a pre-registered prediction; later runs must be labelled post-summit.
