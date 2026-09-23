# sim1 run record

| | |
|---|---|
| Started (UTC) | 2026-09-23T15:44:54Z |
| Wall clock | 7.5 min (API time 94 min across parallel subagents) |
| Model | `claude-opus-5-5`, effort high, Claude Code 2.1.280, `-p` mode |
| Turns | 59 top-level; 11 research subagents (3 attendees each) + 1 concept-note-authorship agent |
| Tokens | 4.26M cache writes, 178.7M cache reads, 581K output |
| API-equivalent cost | $69.71 (billed to the claude.ai subscription, not the API) |
| Corpus modified | no (`git status` clean in epistemic-futures-corpus) |
| Inputs | public corpus only (`summit/website/`, `dossiers/`); no private repo material |

Outputs: `manifesto.md` (2,372 words, 12 named dissents from 11 attendees), `process-notes.md`,
`sources.md` (436 corpus files, all verified to exist), `work/cards/` (33 position cards with cited
quotes, ~60K words), `work/verify_quotes.py` (~70 anchoring quotes checked against the corpus).
