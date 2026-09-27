"""Score the predictions against the real manifesto. The procedure is PROTOCOL.md; this file is it, executable.

    source ~/.zshenv; PY=~/.venvs/topics1268/bin/python
    $PY score.py pre                          # before the real manifesto: judge every predicted document (done 2026-09-27)
    $PY score.py real path/to/real.md         # the day it lands → results/
    $PY score.py real stand-in.md --out dry   # plumbing test with a stand-in document → dry/ (never interpreted)
    $PY score.py questions real-questions.md  # only if the summit publishes its open questions: one per bullet line

Every judge answer is cached under cache/ (keyed by judge version + prompt), so reruns are free and reproduce exactly.
"""
import argparse, json, re, sys, unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "sim2-agents"))
import judge  # noqa: E402
from common import load_roster  # noqa: E402

PRED = json.loads((HERE / "predictions.json").read_text())
THEMES = PRED["themes"]                 # 29: sim 2's registered themes
BTHEMES = PRED["baseline_themes"]       # 9: the baseline's recurring principles
PROPS = THEMES + BTHEMES
PIDS = [t["id"] for t in PROPS]
CANDS = {"sim2": [ROOT / f"sim2-agents/run{i}/manifesto.md" for i in range(1, 7)],
         "sim1": [ROOT / "sim1-simple/manifesto.md"],
         "baseline": [ROOT / f"baseline-nocorpus/b{i}/manifesto.md" for i in range(1, 7)]}
SAMPLES = [(s, i, p) for s, ps in CANDS.items() for i, p in enumerate(ps, 1)]
def sid(s, i): return f"{s}-{i}" if len(CANDS[s]) > 1 else s
def keys(s): return [sid(s, i) for i in range(1, len(CANDS[s]) + 1)]

LEAD_Q = ("Which one of these propositions does this manifesto's first principle mainly express? "
          "Choose none if it expresses none of them.")
LEAD_OPTS = {t["id"]: t["statement"] for t in PROPS} | {"none": "none of the above"}
FAULT_Q = "This is one dissent recorded in a manifesto about sustaining human knowledge in the age of AI. Which fault line does it fall on?"
FAULT_OPTS = {"consent_or_payment": PRED["fault_lines"]["consent_or_payment"],
              "model_in_loop": PRED["fault_lines"]["model_in_loop"],
              "other": "anything else"}
STRICT = {"endorsed"}; LENIENT = {"endorsed", "partial"}
JASON_MIN_RUNS = 2   # a proposition is Jason-exposed if his own agent's turns endorse it in at least this many sim 2 runs
VERDICT_YES, VERDICT_NO = 3, 1   # sim-distinctive propositions endorsed by the real text: >=3 = the corpus + sim added content; <=1 = not


def verdict(k): return "added content" if k >= VERDICT_YES else ("no evidence it added content" if k <= VERDICT_NO else "inconclusive")


def pmap(fn, xs, n=6):
    with ThreadPoolExecutor(n) as ex: return list(ex.map(fn, xs))


def first_principle(ex):
    return ex["principles"][0]["statement"] if ex["principles"] else "(no principles)"


def lead_text(ex): return f"Title: {ex['title']}\nFirst principle: {first_principle(ex)}"


def all_presence(doc, tag):
    """The 29 sim 2 themes and the 9 baseline themes, as two separate judge calls (so each set's cache stands alone)."""
    return judge.presence(doc, THEMES, tag) | judge.presence(doc, BTHEMES, f"{tag}:b")


# ---------- names ----------
def fold(s): return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()
ROSTER = load_roster()
def canon(name):
    """Map a dissenter's name as written to a roster name, or None. Full name first, then surname."""
    f = fold(name)
    for r in ROSTER:
        if fold(r["name"]) in f: return r["name"]
    for r in ROSTER:
        sur = "aguera y arcas" if "aguera" in fold(r["name"]) else fold(r["name"]).split()[-1]
        if sur == "caulfield" and "caufield" in f: return r["name"]
        if re.search(rf"\b{re.escape(sur)}\b", f): return r["name"]
    return None
def names(ex): return sorted({c for d in ex["dissents"] if (c := canon(d["name"]))})


def ranking(res, s):
    """Each predictor's dissenter ranking: how many of its documents name the person as a dissenter."""
    return Counter(n for k in keys(s) for n in res[k]["dissenters"])


def precision_at_k(rank, truth, k):
    """Precision of the top k names; a tie straddling the cut gets fractional credit (expected value of a random tie-break)."""
    if not k: return None
    got = 0.0; left = k
    for score in sorted(set(rank.values()), reverse=True):
        group = [n for n, v in rank.items() if v == score]
        take = min(left, len(group))
        got += take * sum(n in truth for n in group) / len(group); left -= take
        if not left: break
    return got / k


# ---------- before the real manifesto ----------
def jason_turns(i):
    turns = []
    for f in sorted((ROOT / f"sim2-agents/run{i}/sessions").glob("*.json")):
        for t in json.loads(f.read_text())["turns"]:
            if t["slug"] == "jason-priem": turns.append(f"[{f.stem}] {t['text']}")
    return "\n\n".join(turns)


def cmd_pre():
    out = HERE / "pre"; out.mkdir(exist_ok=True)
    def one(smp):
        s, i, p = smp; doc = p.read_text(); k = sid(s, i)
        ex = judge.extract(doc, f"pre:extract:{k}")
        return k, {"path": str(p.relative_to(ROOT)), "themes": all_presence(doc, f"pre:themes:{k}"), "extract": ex,
                   "lead": judge.classify(lead_text(ex), LEAD_Q, LEAD_OPTS, f"pre:lead:{k}"), "dissenters": names(ex)}
    res = dict(pmap(one, SAMPLES))
    # Contamination proxy, first try (kept for the record): themes raised in any Session 3 harvest. It flags 26 of 29.
    s3 = dict(pmap(lambda i: (i, judge.presence((ROOT / f"sim2-agents/run{i}/harvests/s3.md").read_text(), THEMES, f"pre:s3:run{i}")), range(1, 7)))
    s3_flagged = sorted({t for r in s3.values() for t, v in r.items() if v["label"] != "absent"})
    # Contamination proxy used: what the sim put in Jason's own mouth, every session, every run.
    jt = dict(pmap(lambda i: (f"run{i}", all_presence(jason_turns(i), f"pre:jason:run{i}")), range(1, 7)))
    exposed = sorted(t for t in PIDS if sum(jt[r][t]["label"] in STRICT for r in jt) >= JASON_MIN_RUNS)
    rate = {s: {t: sum(res[k]["themes"][t]["label"] in STRICT for k in keys(s)) / len(keys(s)) for t in PIDS} for s in CANDS}
    groups = {"sim_distinctive": [t for t in PIDS if rate["sim2"][t] >= 4/6 and rate["baseline"][t] <= 1/6],
              "baseline_distinctive": [t for t in PIDS if rate["baseline"][t] >= 4/6 and rate["sim2"][t] <= 1/6],
              "shared": [t for t in PIDS if rate["sim2"][t] >= 4/6 and rate["baseline"][t] >= 4/6]}
    ranks = {s: dict(ranking(res, s).most_common()) for s in CANDS}
    json.dump({"judge_version": judge.JUDGE_VERSION, "samples": res, "rates_strict": rate, "groups": groups,
               "dissenter_rankings": ranks, "jason_turns": jt, "jason_exposed": exposed, "jason_min_runs": JASON_MIN_RUNS,
               "s3_harvests": s3, "s3_flagged": s3_flagged}, open(out / "pre.json", "w"), ensure_ascii=False, indent=1)
    write_pre_md(res, rate, groups, ranks, exposed, jt, s3_flagged, out / "PRE.md")
    print(f"pre done: {len(res)} documents; judge spend so far ${judge.LOG.totals['usd']:.2f}")


def cnt(res, s, t, ok): return sum(res[k]["themes"][t]["label"] in ok for k in keys(s))


def write_pre_md(res, rate, groups, ranks, exposed, jt, s3_flagged, path):
    grp = {t: g for g, ts in groups.items() for t in ts}
    L = ["# Pre-registered judge readings of every predicted document", "",
         f"Judge `{judge.JUDGE_VERSION}` ({judge.MODEL}, effort {judge.EFFORT}, {judge.VOTES} votes, median label), 2026-09-27 CT, "
         "before the real manifesto was published. Each cell counts documents where the judge labels the proposition "
         "*endorsed*; the number after the slash adds *partial*. `hand` is COMPARE.md's reading of the six sim 2 runs. "
         "Group: *sim* = sim 2 endorses it in at least 4 of 6 and the baseline in at most 1 of 6; *base* = the reverse; "
         "*shared* = both at least 4 of 6. *Jason*: his own agent's turns endorse it in at least "
         f"{JASON_MIN_RUNS} of 6 runs (the contamination proxy).", "",
         "| Proposition | hand, sim 2 | sim 2 | sim 1 | baseline | Jason's agent | Group | Jason |", "|---|---:|---:|---:|---:|---:|---|:-:|"]
    for t in PROPS:
        tid = t["id"]; lab = t.get("compare_row", t["statement"])[:72]
        c = [f"{cnt(res, s, tid, STRICT)}/{cnt(res, s, tid, LENIENT)}" for s in ("sim2", "sim1", "baseline")]
        j = sum(jt[r][tid]["label"] in STRICT for r in jt)
        L.append(f"| {lab} | {t.get('hand_runs_of_6', '')} | {c[0]} | {c[1]} | {c[2]} | {j} | {grp.get(tid, '').replace('_distinctive', '')} | {'yes' if tid in exposed else ''} |")
    agree = n = 0
    for t in THEMES:
        for i in range(1, 7):
            agree += (t["hand"][f"run{i}"] not in ("–", "dissent")) == (res[f"sim2-{i}"]["themes"][t["id"]]["label"] in LENIENT); n += 1
    L += ["", f"**Judge vs the hand table** (endorsed or partial vs a principle cell), 29 themes × 6 runs: agree on {agree} of {n} cells ({agree/n:.0%}).", "",
          f"**Groups registered for scoring day.** Sim-distinctive ({len(groups['sim_distinctive'])}): " + ", ".join(f"`{x}`" for x in groups["sim_distinctive"]) +
          f". Baseline-distinctive ({len(groups['baseline_distinctive'])}): " + ", ".join(f"`{x}`" for x in groups["baseline_distinctive"]) +
          f". Shared ({len(groups['shared'])}): " + ", ".join(f"`{x}`" for x in groups["shared"]) + ".", "",
          f"**Jason-exposed** ({len(exposed)}): " + ", ".join(f"`{x}`" for x in exposed) +
          f". The first proxy tried, anything raised in a sim Session 3 harvest, flagged {len(s3_flagged)} of 29 themes and so separated nothing; it is kept in pre.json only.", "",
          "## Dissenter rankings (documents naming each person as a dissenter)", ""]
    for s in CANDS:
        L.append(f"- **{s}** ({len(keys(s))} docs): " + ", ".join(f"{n} {v}" for n, v in ranks[s].items()))
    L += ["", "## Titles and first principles", "", "| Document | Title | First principle | → proposition |", "|---|---|---|---|"]
    for k, r in res.items():
        L.append(f"| {k} | {r['extract']['title'][:60]} | {first_principle(r['extract'])[:110]} | `{r['lead']['choice']}` |")
    path.write_text("\n".join(L) + "\n")


# ---------- the day the real manifesto lands ----------
def brier(ps, ys): return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ps) if ps else None


def cmd_real(real_path, outdir):
    out = HERE / outdir; out.mkdir(exist_ok=True); tag = outdir
    pre = json.loads((HERE / "pre" / "pre.json").read_text())
    res = pre["samples"]
    real = Path(real_path).read_text()
    ex = judge.extract(real, f"{tag}:extract:real")
    R = {"themes": all_presence(real, f"{tag}:themes:real"), "extract": ex, "dissenters": names(ex),
         "lead": judge.classify(lead_text(ex), LEAD_Q, LEAD_OPTS, f"{tag}:lead:real")}
    RP = [{"id": f"R{j+1}", "statement": p["statement"]} for j, p in enumerate(ex["principles"])]
    R["dissent_fault_lines"] = [{"name": d["name"], **judge.classify(d["position"], FAULT_Q, FAULT_OPTS, f"{tag}:fault:{d['name']}")}
                                for d in ex["dissents"]]
    R["top2"] = [judge.classify(f"Title: {ex['title']}\nPrinciple: {p['statement']}", LEAD_Q, LEAD_OPTS, f"{tag}:top2:{j}")["choice"]
                 for j, p in enumerate(ex["principles"][:2])]
    # recall: does each predicted document hold each real principle?  precision: does the real one hold each predicted principle?
    # lead: does each predicted document's first principle make the real first principle's claim?
    def rec(smp): k = sid(smp[0], smp[1]); return k, (judge.presence(smp[2].read_text(), RP, f"{tag}:recall:{k}") if RP else {})
    def prec(smp):
        k = sid(smp[0], smp[1]); pp = [{"id": f"P{j+1}", "statement": x["statement"]} for j, x in enumerate(res[k]["extract"]["principles"])]
        return k, (judge.presence(real, pp, f"{tag}:precision:{k}") if pp else {})
    def lead(smp):
        k = sid(smp[0], smp[1])
        return k, (judge.presence(f"First principle: {first_principle(res[k]['extract'])}", RP[:1], f"{tag}:lead-match:{k}")["R1"] if RP else None)
    R["recall"] = dict(pmap(rec, SAMPLES)); R["precision"] = dict(pmap(prec, SAMPLES)); R["lead_match"] = dict(pmap(lead, SAMPLES))
    M = metrics(pre, R, RP)
    json.dump({"judge_version": judge.JUDGE_VERSION, "real_path": str(real_path), "real": R, "metrics": M},
              open(out / "results.json", "w"), ensure_ascii=False, indent=1)
    write_results_md(pre, M, R, RP, out / "RESULTS.md", real_path)
    print(f"{outdir} done; judge spend so far ${judge.LOG.totals['usd']:.2f}")


def metrics(pre, R, RP):
    res, groups, exposed = pre["samples"], pre["groups"], set(pre["jason_exposed"])
    real_d = set(R["dissenters"]); M = {}
    for s in CANDS:
        ks = keys(s); m = {}
        for on, ok in (("strict", STRICT), ("lenient", LENIENT)):
            y = {t: int(R["themes"][t]["label"] in ok) for t in PIDS}
            p = {t: cnt(res, s, t, ok) / len(ks) for t in PIDS}
            for name, ids in (("all", PIDS), ("sim_themes", [t["id"] for t in THEMES]), ("baseline_themes", [t["id"] for t in BTHEMES]),
                              ("jason_absent", [t for t in PIDS if t not in exposed])):
                m[f"brier_{on}_{name}"] = brier([p[t] for t in ids], [y[t] for t in ids])
            per = [sum(v["label"] in ok for v in R["recall"][k].values()) / max(1, len(RP)) for k in ks]
            m[f"recall_{on}"] = sum(per) / len(ks); m[f"recall_{on}_per_doc"] = per
            per = [sum(v["label"] in ok for v in R["precision"][k].values()) / max(1, len(R["precision"][k])) for k in ks]
            m[f"precision_{on}"] = sum(per) / len(ks); m[f"precision_{on}_per_doc"] = per
            m[f"coverage_{on}"] = sum(any(R["recall"][k][rp["id"]]["label"] in ok for k in ks) for rp in RP) / len(RP) if RP else None
            f1 = [2 * p_ * r_ / (p_ + r_) if p_ + r_ else 0.0 for p_, r_ in zip(m[f"precision_{on}_per_doc"], m[f"recall_{on}_per_doc"])]
            m[f"f1_{on}"] = sum(f1) / len(ks)
        m["dissenter_precision_at_k"] = precision_at_k(pre["dissenter_rankings"][s], real_d, len(real_d))
        m["lead_match"] = sum((R["lead_match"][k] or {}).get("label") in STRICT for k in ks) / len(ks)
        M[s] = m
    fs = set(PRED["filed_dissents"])
    M["sim2_filed_seven"] = {"hits": sorted(fs & real_d), "precision": len(fs & real_d) / len(fs),
                             "recall": len(fs & real_d) / len(real_d) if real_d else None}
    M["group_hits"] = {g: {"n": len(ids), "strict": [t for t in ids if R["themes"][t]["label"] in STRICT],
                           "lenient": [t for t in ids if R["themes"][t]["label"] in LENIENT]} for g, ids in groups.items()}
    M["sim_distinctive_verdict"] = verdict(len(M["group_hits"]["sim_distinctive"]["strict"]))
    rs, rb = pre["dissenter_rankings"]["sim2"], pre["dissenter_rankings"]["baseline"]
    dd = {"sim2_only": sorted(n for n, v in rs.items() if v >= 4 and rb.get(n, 0) <= 1),
          "baseline_only": sorted(n for n, v in rb.items() if v >= 4 and rs.get(n, 0) <= 1)}
    M["dissent_distinctive"] = {g: {"names": ns, "really_dissented": sorted(set(ns) & real_d)} for g, ns in dd.items()}
    M["missed_by_all_sim2"] = [rp["id"] for rp in RP if not any(R["recall"][k][rp["id"]]["label"] in LENIENT for k in keys("sim2"))]
    M["missed_by_all_baseline"] = [rp["id"] for rp in RP if not any(R["recall"][k][rp["id"]]["label"] in LENIENT for k in keys("baseline"))]
    M["manufactured_consensus"] = [t for t in PIDS if cnt(res, "sim2", t, STRICT) >= 5 and R["themes"][t]["label"] == "dissent_only"]
    M["consent_real_label"] = R["themes"]["consent_to_train"]["label"]
    M["absent_voices_real_label"] = R["themes"]["absent_voices"]["label"]
    M["stop_counting_in_real_top2"] = "stop_counting_papers" in R["top2"]
    return M


def f2(x): return "–" if x is None else f"{x:.2f}"


def write_results_md(pre, M, R, RP, path, real_path):
    res = pre["samples"]
    stand_in = path.parent.name != "results"
    L = [f"# Scores against {'a STAND-IN for ' if stand_in else ''}the real manifesto (`{real_path}`)", ""]
    if stand_in:
        L += ["> **Plumbing test.** The document scored here is not the real manifesto; it stands in for it to check that "
              "every step runs. These numbers say nothing about the prediction.", ""]
    L += [
         f"Judge `{judge.JUDGE_VERSION}`; procedure in PROTOCOL.md. Strict = *endorsed*; lenient adds *partial*.", "",
         "## Primary", ""]
    gh = M["group_hits"]; dd = M["dissent_distinctive"]
    L += [f"**1. What the corpus and the simulated day added.** Of the {gh['sim_distinctive']['n']} propositions sim 2 makes and the "
          f"no-corpus baseline does not, the real manifesto endorses **{len(gh['sim_distinctive']['strict'])}** "
          f"({', '.join(gh['sim_distinctive']['strict']) or 'none'}); {len(gh['sim_distinctive']['lenient'])} counting partial. "
          f"Registered reading: **{M['sim_distinctive_verdict']}** (≥{VERDICT_YES} added content, ≤{VERDICT_NO} no evidence). "
          f"For scale: shared propositions endorsed {len(gh['shared']['strict'])} of {gh['shared']['n']}; baseline-only "
          f"{len(gh['baseline_distinctive']['strict'])} of {gh['baseline_distinctive']['n']}.", "",
          "**2. Real principles, per document.**", "", "| | sim 2 (6 runs) | sim 1 | no-corpus baseline (6) |", "|---|---:|---:|---:|"]
    for key, lab in (("recall_strict", "Recall: share of real principles the document holds"), ("precision_strict", "Precision: share of its own principles the real one holds"),
                     ("f1_strict", "F1")):
        L.append(f"| {lab} | {f2(M['sim2'][key])} | {f2(M['sim1'][key])} | {f2(M['baseline'][key])} |")
    L += ["", f"**3. Dissenters.** Real: {', '.join(R['dissenters']) or 'none'}. Ranking precision at k = {len(R['dissenters'])}: "
          f"sim 2 {f2(M['sim2']['dissenter_precision_at_k'])}, sim 1 {f2(M['sim1']['dissenter_precision_at_k'])}, baseline {f2(M['baseline']['dissenter_precision_at_k'])}. "
          f"Named by sim 2 only ({', '.join(dd['sim2_only']['names']) or 'none'}): really dissented {', '.join(dd['sim2_only']['really_dissented']) or 'none'}. "
          f"Named by the baseline only ({', '.join(dd['baseline_only']['names']) or 'none'}): really dissented {', '.join(dd['baseline_only']['really_dissented']) or 'none'}.",
          "", "## Secondary", "", "| | sim 2 | sim 1 | baseline |", "|---|---:|---:|---:|"]
    for key in ("recall_lenient", "precision_lenient", "f1_lenient", "coverage_strict", "coverage_lenient", "brier_strict_all",
                "brier_lenient_all", "brier_strict_sim_themes", "brier_strict_baseline_themes", "brier_strict_jason_absent", "lead_match"):
        L.append(f"| {key} | {f2(M['sim2'][key])} | {f2(M['sim1'][key])} | {f2(M['baseline'][key])} |")
    L += ["", f"- Sim 2's seven filed dissenters: hits {', '.join(M['sim2_filed_seven']['hits']) or 'none'}; "
          f"precision {f2(M['sim2_filed_seven']['precision'])}, recall {f2(M['sim2_filed_seven']['recall'])}.",
          f"- Real title: *{R['extract']['title']}*. First principle → `{R['lead']['choice']}`; 'stop counting papers' in the real top two: {M['stop_counting_in_real_top2']}.",
          f"- Consent rule in the real text: `{M['consent_real_label']}` (sim 2 registered: majority text 4 of 6).",
          f"- Who isn't in the room: `{M['absent_voices_real_label']}`.",
          f"- Manufactured consensus (sim 2 endorsed in ≥5 of 6; the real text records only a dissent or split): {', '.join(M['manufactured_consensus']) or 'none'}.",
          "", "## Real principles, and how many predicted documents hold them (strict)", "",
          "| # | Real principle | sim 2 (of 6) | sim 1 | baseline (of 6) |", "|---|---|---:|---:|---:|"]
    for rp in RP:
        c = {s: sum(R["recall"][k][rp["id"]]["label"] in STRICT for k in keys(s)) for s in CANDS}
        L.append(f"| {rp['id']} | {rp['statement']} | {c['sim2']} | {c['sim1']} | {c['baseline']} |")
    L += ["", f"Missed by every sim 2 run, even as partial (charter §3's most informative bucket): {', '.join(M['missed_by_all_sim2']) or 'none'}. "
          f"Missed by every baseline sample: {', '.join(M['missed_by_all_baseline']) or 'none'}.", "",
          "## Real dissents", "", "| Name as written | Fault line | Votes |", "|---|---|---|"]
    for d in R["dissent_fault_lines"]:
        L.append(f"| {d['name']} | `{d['choice']}` | {'/'.join(d['votes'])} |")
    L += ["", "## Every proposition in the real text", "", "| Proposition | Real | sim 2 (of 6) | baseline (of 6) |", "|---|---|---:|---:|"]
    for t in PROPS:
        L.append(f"| {t.get('compare_row', t['statement'])[:80]} | `{R['themes'][t['id']]['label']}` | {cnt(res, 'sim2', t['id'], STRICT)} | {cnt(res, 'baseline', t['id'], STRICT)} |")
    path.write_text("\n".join(L) + "\n")


def cmd_questions(path, outdir):
    """Open questions: the sim never put them in a manifesto; its prediction is each run's Session 5 harvest, part 2.
    No baseline produced questions, so this one is descriptive only. Runs 1-3's S5 harvests are broken (COMPARE.md)."""
    qs = [re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", l).strip() for l in Path(path).read_text().splitlines()]
    qs = [{"id": f"Q{j+1}", "statement": q} for j, q in enumerate(q for q in qs if q)]
    res = dict(pmap(lambda i: (f"run{i}", judge.presence((ROOT / f"sim2-agents/run{i}/harvests/s5.md").read_text(), qs,
                                                        f"{outdir}:questions:run{i}")), range(1, 7)))
    L = ["# Real open questions vs the sim 2 Session 5 harvests", "",
         "| # | Real open question | runs raising it (endorsed or partial; runs 1-3 had broken S5 harvests) |", "|---|---|---:|"]
    for q in qs:
        L.append(f"| {q['id']} | {q['statement']} | {sum(res[r][q['id']]['label'] in LENIENT for r in res)} |")
    out = HERE / outdir; out.mkdir(exist_ok=True)
    (out / "QUESTIONS.md").write_text("\n".join(L) + "\n")
    json.dump(res, open(out / "questions.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["pre", "real", "questions"]); ap.add_argument("path", nargs="?")
    ap.add_argument("--out", default="results"); a = ap.parse_args()
    if a.cmd == "pre": cmd_pre()
    elif a.cmd == "real": cmd_real(a.path, a.out)
    else: cmd_questions(a.path, a.out)
