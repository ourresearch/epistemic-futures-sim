# Scoring protocol: the predicted manifestos against the real one

Written 2026-09-27 CT, after the summit and before its manifesto was published (due about 2026-10-08). This file,
`predictions.json`, `judge.py`, `score.py`, the no-corpus baseline in `../baseline-nocorpus/` and the judge's readings
of every predicted document in `pre/` are pushed and tagged together before the real manifesto exists, so the scoring
rule is registered the same way the predictions were: by a GitHub timestamp. Nothing here reads, or was written with
knowledge of, the real event's outputs.

## The question, and the null it needs

The charter's question is whether persona agents grounded in each attendee's own words can predict what a real
deliberative process produces. A match between a sim manifesto and the real one proves little by itself: any capable
model told the summit's theme, organizers and roster will guess that a manifesto about AI and knowledge says "cite
sources" and "fund the commons". So every score below is reported for three predictors side by side:

| Predictor | What it had | Samples | Registered |
|---|---|---:|---|
| **Sim 2**: one Opus 5.5 agent per attendee with retrieval over its own dossier, run through the real schedule | corpus + simulated day | 6 runs | `sim2-run{1..6}-freeze`, 2026-09-23/24 |
| **Sim 1**: one Claude Code session, 33 corpus-built position cards, then the manifesto | corpus, no simulated day | 1 | `sim1-freeze`, 2026-09-23 |
| **No-corpus baseline**: the same model, given only the summit's public pages and the roster (names, affiliations, roles) | public pages only | 6 samples | this tag |

The baseline is the null. It shares the model, the manifesto requirements and the length rule with sim 2's drafter,
and its prompt is sim 1's prompt with the corpus taken out (`../baseline-nocorpus/baseline.py`). What sim 2 gets right
that the baseline also gets right, the model already knew or the concept note already said.

## The instrument

One judge, fixed now: `judge.py`, version `j1`, `claude-opus-5-5` at effort medium, schema-constrained answers, three
votes per judgment. Every raw answer is cached in `cache/` with its full prompt, so any number below can be re-derived.

- **Presence**: given a document and a list of propositions, label each *endorsed* (the document adopts substantially
  this claim in its own voice), *partial* (a materially narrower, weaker or different claim on the same point),
  *dissent_only* (only in a noted dissent or a recorded split) or *absent*. The label is the median of three votes.
- **Extraction**: title, principles (one sentence each), commitments, named dissenters. One call, kept verbatim, never
  hand-edited.
- **Classification**: one choice from a closed list (which proposition a first principle expresses; which fault line
  a dissent sits on). The mode of three votes.

**Strict** means *endorsed*; **lenient** adds *partial*. Strict is primary everywhere.

Two checks before registration. Against the hand-read theme table in `../sim2-agents/COMPARE.md`, the judge agrees on
167 of 174 cells (96%; 29 themes × 6 runs), and where it differs it is the stricter reader. And a full scoring run with a
stand-in for the real manifesto (sim 2 run 4's pre-review draft; `dry/`, a plumbing test) shows the instrument tells
predictors apart: against that stand-in, sim 2 holds 13 of the 19 sim-distinctive propositions and a mean recall of 0.67,
the baseline 0.19.

Cost: the baseline $1.83; the judge's readings of the 13 predicted documents $9.76; the plumbing test about $5; scoring
day about $8.

## Measures

`pre/PRE.md` is the reference for everything below: how the judge read each predicted document, fixed before the real
one exists. The main thing it shows is that **sim 2 mostly contains the baseline.** Sim 2 endorses 6 of the baseline's 9
recurring principles in 5 or 6 of its 6 runs, and both endorse three of sim 2's themes (stop counting papers, cite by
default, honour open licences). On top of that sim 2 adds 19 propositions that the baseline makes in at most one
sample (the mechanisms: competence before reliance, telemetry with audit rights, an antitrust safe harbour, a levy,
consent to train, and so on). Any measure that rewards breadth will favour sim 2 for that reason alone. So the headline
is the 19.

### Primary (decided now)

1. **What the corpus and the simulated day added.** The *sim-distinctive* propositions are the ones sim 2 endorses in at
   least 4 of 6 runs and the baseline in at most 1 of 6 (19 of them, listed in `pre/PRE.md`). Count how many the real
   manifesto endorses (strict). **3 or more: the corpus and simulation added real predictive content beyond the model's
   priors. 1 or 0: no evidence that they did. 2: inconclusive.** The shared propositions (9) and the one
   baseline-distinctive proposition are reported beside it for scale.
2. **Real principles, per document.** The judge extracts the real manifesto's principles. For each predicted document:
   recall (the share of real principles it endorses), precision (the share of its own principles the real manifesto
   endorses) and their F1. Mean per predictor. Expected: sim 2 higher on recall, the baseline higher on precision.
3. **Dissenters.** Each predictor's ranking of names by how many of its documents record that person as dissenting
   (in `pre/PRE.md`), scored as precision at k, where k is the number of real named dissenters (a tie across the cut
   gets fractional credit). The two rankings share most of their top names (Becker, Bratton, Chan, Salib, Turkle), so
   the sharp test is the names only one side makes: Tim O'Reilly and Katherine Maher appear in 4 to 6 sim 2 runs and at
   most one baseline sample. Also reported: sim 2's registered seven filed dissenters (Salib, Becker, Bratton, Turkle,
   Johns, Agüera y Arcas, O'Reilly).

### Secondary

- Lenient versions of the above (*partial* counts); **coverage** (the share of real principles endorsed by at least one
  of a predictor's documents; sim 2 and the baseline both have six).
- **The 38 propositions** (sim 2's 29 registered themes plus the baseline's 9 recurring principles): the real label for
  each; Brier score of each predictor's endorsement rate, on all 38, on each set, and without the Jason-exposed ones.
- **Lead.** The share of each predictor's documents whose first principle makes the claim of the real first principle.
  Registered contrast: every baseline sample (and sim 1) opens with "AI accelerates old failures; diagnose before you
  prescribe", straight from the concept note; sim 2 opens with "stop counting papers" (3 runs), "fund the people who
  check" (2) or "keep disagreement visible" (1). Sim 2's call from COMPARE.md: "stop counting papers" first or second.
- **Consent rule**: the real label for "open to read is not open to train" (sim 2: majority text in 4 of 6, a split in 2).
- **Who isn't in the room**: the real label (sim 2: 3 of 6 endorsed by the judge, 4 counting partial; the baseline 6 of 6).
- **Manufactured consensus**: propositions sim 2 endorsed in at least 5 of 6 runs that the real manifesto records only
  as a dissent or split.
- **Missed entirely**: real principles no sim 2 run holds even partially. Charter §3 calls this the most informative bucket.
- **Fault lines**: each real dissent classified as consent/payment, model-in-the-loop, or other.
- **Open questions**, only if the summit publishes a list: each real question against every run's Session 5 harvest
  (`score.py questions`). Descriptive only, with no baseline. Batch 1's Session 5 harvests are broken (run 1 truncated,
  runs 2 and 3 empty; COMPARE.md), so effectively this is 4 runs, not 6.

### Expectations, stated now

The real manifesto is drafted by a writing committee of three or four people in two weeks. My guess is that it reads
more like the baseline than like sim 2: fewer principles, less mechanism. If so, sim 2 wins recall on breadth and loses
precision, and the verdict rests on test 1. On dissenters I expect no real difference between sim 2 and the baseline,
because the pre-pass shows the dissenter prediction is mostly the model's prior about these people.

## Contamination

Jason read sim outputs and then attended (charter §3, an accepted limitation). Two filters, both reported:

- **Automatic proxy**, fixed now: a proposition is *Jason-exposed* if the judge finds it endorsed in his own agent's
  turns (all sessions) in at least 2 of the 6 sim 2 runs: the ideas the simulation put in his mouth, which he could have
  echoed. Nine qualify, most of them open-infrastructure claims (`pre/PRE.md`). Brier is also reported without them.
  (A first proxy, anything raised in a sim Session 3 harvest, flagged 26 of 29 themes and was dropped as useless.)
- **Jason's own list**, if he gives one before the real manifesto is out: `jason-exposed.md`, the ideas he argued for
  or seconded in the real room and which sim outputs he had read by then. Real principles matching that list are
  reported separately.

## Rules for scoring day

1. Save the real manifesto as `real/manifesto.md`: a faithful text conversion of the published document (no edits,
   no reordering), with its source URL and retrieval date in `real/SOURCE.md`.
2. Run `score.py real real/manifesto.md`. Push `results/` as it comes out.
3. The judge is not re-prompted after the real manifesto is seen. If it fails on the real document (a format it
   cannot parse, a refusal), a new judge version is allowed only if it is re-run on every predicted document too,
   and both versions are reported.
4. No predicted document is dropped, and no extraction is hand-corrected. Disagreements with the judge go in the
   write-up as disagreements.

## Limitations

- The judge is the same model as the predictors, which may favour text in its own style. That bias applies to sim 2,
  sim 1 and the baseline alike, since all three were written by it.
- The baseline was generated on 2026-09-27, after the event, but from pre-event public pages only. Nothing about the
  event went into it. Its prompt carries no date cue beyond the summit's own dates.
- The propositions come from the predictors' own outputs (29 from sim 2, 9 from the baseline). Real-principle recall
  and precision are the measures that do not depend on that list.
- Small numbers: about ten real principles and a handful of dissenters. Differences of one principle are noise.

## Recipe

```bash
source ~/.zshenv; PY=~/.venvs/topics1268/bin/python
cd ~/ox/epistemic-futures-sim/scoring
$PY score.py pre                              # done 2026-09-27; cached, reruns free
$PY score.py real stand-in.md --out dry       # plumbing test (dry/ is never interpreted)
$PY score.py real real/manifesto.md           # scoring day → results/RESULTS.md
$PY score.py questions real/questions.md      # only if the open questions are published
```
