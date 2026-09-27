# Scores against a STAND-IN for the real manifesto (`../sim2-agents/run4/manifesto-v1.md`)

> **Plumbing test.** The document scored here is not the real manifesto; it stands in for it to check that every step runs. These numbers say nothing about the prediction.

Judge `j1`; procedure in PROTOCOL.md. Strict = *endorsed*; lenient adds *partial*.

## Primary

**1. What the corpus and the simulated day added.** Of the 19 propositions sim 2 makes and the no-corpus baseline does not, the real manifesto endorses **13** (competence, situation, monoculture, independent_sources, telemetry, antitrust_safe_harbour, training_vs_grounding, refusal_fundable, identify_agents_not_readers, failure_data, charter_for_every_body, hitl_not_safeguard, apprenticeship); 18 counting partial. Registered reading: **added content** (≥3 added content, ≤1 no evidence). For scale: shared propositions endorsed 7 of 9; baseline-only 0 of 1.

**2. Real principles, per document.**

| | sim 2 (6 runs) | sim 1 | no-corpus baseline (6) |
|---|---:|---:|---:|
| Recall: share of real principles the document holds | 0.67 | 0.67 | 0.19 |
| Precision: share of its own principles the real one holds | 0.58 | 0.70 | 0.63 |
| F1 | 0.60 | 0.68 | 0.28 |

**3. Dissenters.** Real: Adam Becker, Adrian Johns, Amy Brand, Benjamin Bratton, Blaise Agüera y Arcas, David Weinberger, Geoffrey Bilder, Ivan Oransky, Jason Priem, Katherine Maher, Leslie Chan, Peter Pomerantsev, Peter Salib, Ramón Alvarado, Selena Deckelmann, Sherry Turkle, Tamar Gendler. Ranking precision at k = 17: sim 2 0.76, sim 1 0.59, baseline 0.65. Named by sim 2 only (Katherine Maher, Tim O'Reilly): really dissented Katherine Maher. Named by the baseline only (none): really dissented none.

## Secondary

| | sim 2 | sim 1 | baseline |
|---|---:|---:|---:|
| recall_lenient | 1.00 | 1.00 | 0.85 |
| precision_lenient | 0.98 | 0.90 | 0.90 |
| f1_lenient | 0.99 | 0.95 | 0.87 |
| coverage_strict | 1.00 | 0.67 | 0.33 |
| coverage_lenient | 1.00 | 1.00 | 1.00 |
| brier_strict_all | 0.18 | 0.34 | 0.43 |
| brier_lenient_all | 0.06 | 0.29 | 0.32 |
| brier_strict_sim_themes | 0.19 | 0.34 | 0.49 |
| brier_strict_baseline_themes | 0.16 | 0.33 | 0.25 |
| brier_strict_jason_absent | 0.20 | 0.41 | 0.47 |
| lead_match | 0.33 | 0.00 | 0.00 |

- Sim 2's seven filed dissenters: hits Adam Becker, Adrian Johns, Benjamin Bratton, Blaise Agüera y Arcas, Peter Salib, Sherry Turkle; precision 0.86, recall 0.35.
- Real title: *Pay for the People Who Check: A Manifesto for Sustaining Human Knowledge*. First principle → `b_evaluation_scarce`; 'stop counting papers' in the real top two: True.
- Consent rule in the real text: `dissent_only` (sim 2 registered: majority text 4 of 6).
- Who isn't in the room: `absent`.
- Manufactured consensus (sim 2 endorsed in ≥5 of 6; the real text records only a dissent or split): none.

## Real principles, and how many predicted documents hold them (strict)

| # | Real principle | sim 2 (of 6) | sim 1 | baseline (of 6) |
|---|---|---:|---:|---:|
| R1 | The scarce resource is the people who check, so fund checkers (fellowships, mentoring, tools, credit, legal defence for sleuths) rather than tokens, paying carefully so pay does not erode volunteer motivation. | 6 | 1 | 4 |
| R2 | Funders and provosts should stop counting outputs by a committed date, avoid substitute metrics, and credit curation, correction, maintenance, data sharing, mentoring and negative results. | 3 | 1 | 4 |
| R3 | AI answers used in scholarship must show representative sources, accurate citations, checkable open links and flags for thin evidence, with retraction checks at citation, stable shared pages and disclosed link-hallucination rates. | 4 | 1 | 0 |
| R4 | Checking must be checkable: no auditor paid by the count, no lab grading itself, auditor access to training checkpoints and retired models, findable funding, and a public no-fee audit layer. | 4 | 0 | 0 |
| R5 | Design the settings where claims are met, hiding cheap credibility cues and surfacing expensive ones, without penalizing language-barrier users, and measure human oversight rather than assuming it works. | 2 | 1 | 0 |
| R6 | Institutions must ensure competence precedes reliance on tools, practising and measuring oversight without tools, teaching programming before coding agents, with employers sharing this duty and a removal study funded. | 5 | 1 | 0 |
| R7 | Independence checks should examine who seeded corpora and who staffs checking roles, a commons of negative knowledge should be commissioned, and tail work funded independently of usage. | 2 | 0 | 0 |
| R8 | AI firms that use the commons must pay its infrastructure costs through deals with reporting and audit clauses, separate training and grounding controls, collective bargaining rights for producers, and multiple funders. | 6 | 1 | 2 |
| R9 | Every rule should name a policer, paymaster, review date and accountable outside overruler, with recipients committing to openness and forkability, dated self-assessments, Global South partners from the start, and funded refusal. | 4 | 0 | 0 |

Missed by every sim 2 run, even as partial (charter §3's most informative bucket): none. Missed by every baseline sample: none.

## Real dissents

| Name as written | Fault line | Votes |
|---|---|---|
| Sherry Turkle | `model_in_loop` | model_in_loop/model_in_loop/model_in_loop |
| Amy Brand | `consent_or_payment` | consent_or_payment/consent_or_payment/consent_or_payment |
| Selena Deckelmann | `consent_or_payment` | consent_or_payment/consent_or_payment/consent_or_payment |
| Katherine Maher | `consent_or_payment` | consent_or_payment/consent_or_payment/consent_or_payment |
| Jason Priem | `consent_or_payment` | consent_or_payment/consent_or_payment/consent_or_payment |
| Benjamin Bratton | `consent_or_payment` | consent_or_payment/consent_or_payment/consent_or_payment |
| Adam Becker | `other` | other/other/other |
| Peter Salib | `consent_or_payment` | consent_or_payment/consent_or_payment/consent_or_payment |
| Blaise Agüera y Arcas | `model_in_loop` | model_in_loop/model_in_loop/model_in_loop |
| David Weinberger | `other` | other/other/other |
| Geoffrey Bilder | `other` | other/other/other |
| Ivan Oransky | `other` | other/other/other |
| Leslie Chan | `other` | other/other/other |
| Peter Pomerantsev | `other` | other/other/other |
| Adrian Johns | `other` | other/other/other |
| Tamar Gendler | `other` | other/other/other |
| Ramón Alvarado | `model_in_loop` | model_in_loop/other/model_in_loop |

## Every proposition in the real text

| Proposition | Real | sim 2 (of 6) | baseline (of 6) |
|---|---|---:|---:|
| Competence before reliance; order of learning; take-the-tool-away test | `endorsed` | 6 | 1 |
| Change the situation, don't warn individuals; name who acts | `endorsed` | 6 | 1 |
| Monoculture / smoothness is the headline risk; show named disagreement | `endorsed` | 6 | 1 |
| Count independent sources, not repetitions | `endorsed` | 6 | 0 |
| Cite by default; link out; correction status travels in answers | `endorsed` | 6 | 4 |
| Behavioral audits outside the vendor; shared versioned battery; no generation mo | `endorsed` | 6 | 2 |
| Accountable owner + mandatory liability insurance, premiums disclosed | `partial` | 5 | 0 |
| Stop counting papers; publishers' correction duties; DORA with teeth | `endorsed` | 6 | 6 |
| Pay coarsely to communities, never per item; per-retrieval pay is gamed | `partial` | 5 | 0 |
| Event-level telemetry with audit rights; two witnesses; canaries | `endorsed` | 5 | 0 |
| Antitrust safe harbour for producers bargaining as a bloc | `endorsed` | 6 | 1 |
| Commons-rent tax / levy / owed dues as backstop | `partial` | 5 | 0 |
| Separate controls for training vs grounding | `endorsed` | 5 | 0 |
| "Open to read is not open to train" as majority text | `dissent_only` | 4 | 0 |
| Honour Wikipedia's chosen licence; crawlers self-identify; reusers fund infrastr | `partial` | 5 | 5 |
| Refusal is fundable | `endorsed` | 6 | 0 |
| Forkable infrastructure: CC0, open source, patent non-assertion, living will, no | `endorsed` | 6 | 2 |
| Whoever profits from a count doesn't set it | `partial` | 4 | 0 |
| Southern / diamond journals govern with binding say and funded seats | `partial` | 5 | 0 |
| Identify agents and campaigns, never readers; anonymity stays | `endorsed` | 5 | 0 |
| Failure and negative results as first-class data | `endorsed` | 6 | 1 |
| Checkers as a paid body with a charter / Ulysses pact for every body | `endorsed` | 5 | 0 |
| Human in the loop is not a safeguard; overreliance; explanations can worsen it | `endorsed` | 4 | 0 |
| Test every seat, human or machine, against a floor; novelty test | `absent` | 3 | 0 |
| No AI stand-ins for children, grief, therapy | `dissent_only` | 3 | 0 |
| Global majority is more hopeful than this room | `absent` | 1 | 0 |
| Environmental and moderator costs in the ledger | `absent` | 1 | 1 |
| Apprenticeship and first jobs as a funded line item | `endorsed` | 4 | 0 |
| Who isn't in the room (COMPARE.md § What the complete Session 5 harvest changed; | `absent` | 3 | 6 |
| Most of the crisis predates AI: AI accelerates old failures, so remedies must di | `endorsed` | 6 | 6 |
| AI systems should be described by what they actually do, neither as minds or ora | `dissent_only` | 1 | 6 |
| Evaluation and verification, not production, are now the scarce resource, so inv | `endorsed` | 3 | 6 |
| Credibility should rest on checkable process, track record and accountable peopl | `endorsed` | 5 | 6 |
| Provenance and attribution are infrastructure that must be built into knowledge  | `endorsed` | 6 | 6 |
| The human labor behind trustworthy knowledge (reviewing, editing, curating, chec | `endorsed` | 6 | 6 |
| AI tools should be designed to strengthen human judgment and capability rather t | `endorsed` | 5 | 6 |
| No single company, state or model should control the infrastructure of knowledge | `partial` | 6 | 6 |
| Knowledge institutions and the knowledge commons are public goods that deserve p | `partial` | 2 | 3 |
