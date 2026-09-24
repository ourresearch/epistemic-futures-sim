# sim2-agents — one Opus 5.5 agent per attendee, run through the summit's schedule

Design and rationale: `../DESIGN.md`. Job: oxjobs #1339.

## What is here

| File | What |
|---|---|
| `common.py` | paths, model (`claude-opus-5-5`), pricing, API call with retries + JSONL usage log, roster parser, SIMULATED header |
| `build_index.py` | chunk every dossier (`by/`, `av/`, `social/`) → `../index/<slug>/{chunks.jsonl,emb.npy}`; resumable per person |
| `recall.py` | the one tool agents get: hybrid BM25 + e5 search over the caller's own dossier, MMR-diversified, chunk IDs logged |
| `schedule.py` | the published schedule as data (sessions, people in page order, unconference topic titles) |
| `agents.py` | `Attendee` (shared instructions → transcript → card → `recall` tool loop; diary; manifesto review) and `Convener` (call-ons with logged reasons, harvests + minority pass, manifesto draft/revise) |
| `run.py` | the day: unconference → opening → Sessions 1–6 (marketplace between 2 and 3) → manifesto v1 → two review rounds → final. Resumable. |
| `<out>/` | one run: `sessions/*.json` (turns + recall log), `transcripts/`, `harvests/`, `diaries/`, `convener-log.md`, `reviews/`, `manifesto*.md`, `calls.jsonl`, `RUN.md` |

## Run recipe (desk)

```bash
source ~/.zshenv                                   # CLAUDE_API_KEY
cd ~/ox/epistemic-futures-sim/sim2-agents
PY=~/.venvs/topics1268/bin/python                  # anthropic, sentence-transformers, rank_bm25, torch (MPS)

# 1. index (once; ~40 min on MPS; one GPU job at a time; watchdog because macOS has no `timeout`)
perl -e 'alarm 7200; exec @ARGV' $PY build_index.py > ../index/build.log 2>&1

# 2. smoke test: one session
$PY run.py --out smoke-s3 --only s3

# 3. full run (hours; detach it, then rerun the same command to resume after any interruption)
nohup $PY run.py --out run1 --seed 1 > run1.log 2>&1 &
# runs 2 and 3 (2026-09-23, after the length-enforcement change): same command, --seed 2 --out run2 / --seed 3 --out run3;
# they were launched in parallel (CPU-only retrieval; ~16 concurrent API calls in total)
```

Manifesto length: every draft or revision outside 1,500–2,400 words is sent back to the convener with per-section budgets
(`Convener.fit_length`, up to 5 passes at effort low); the uncut text stays beside it as `manifesto-v*.uncut.md`, and
`RUN.md` reports raw → final words per version. Added after run 1 (which is frozen with its 4,216-word final).

Inputs: `../cards/` and the public corpus at `~/ox/epistemic-futures-corpus` (`EFS_CORPUS` to override). The sim never
reads the private repo. Every generated Markdown file starts with the SIMULATED header at generation time.

## Reading a run

- `transcripts/<session>.md`: every turn with role, word count, recall queries and the chunk IDs retrieved.
- `convener-log.md`: every call-on with its reason, and the unconference allocation. Read this before trusting the manifesto.
- `harvests/<session>.md`: 3–5 claims, then minority positions (Session 5: interventions / open questions / who isn't here).
- `diaries/<slug>.md`: each agent's notes after each session (its medium-term memory).
- `reviews/round{1,2}.md`: every agent's sign / edit / dissent on the draft.
- `RUN.md`: model IDs, effort, prompt hashes, seed, tokens, cost, turn and recall statistics, stated assumptions.
