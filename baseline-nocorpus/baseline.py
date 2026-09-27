"""No-corpus baseline: the same model predicts the manifesto from the summit's public pages and the roster alone.

This is the null for the question sim 2 asks ("does a swarm grounded in each attendee's own words predict the real
manifesto?"). It gets what any outsider had before the summit: the organizers' web pages (home, concept note,
schedule, attendee list) and the roster's names, affiliations and summit roles. No dossiers, no cards, no transcripts,
no harvests. Whatever it gets right, the model already knew or the concept note already said.

Same model and effort as the sim 2 drafter, the same manifesto requirements, the same length rule and the same
length-fit loop, so the only difference is the missing corpus and the missing simulated day. Six samples, to match
the six sim 2 runs; samples differ only by sampling.

    source ~/.zshenv; ~/.venvs/topics1268/bin/python baseline.py --n 6      # resumable: skips samples already written
"""
import argparse, json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sim2-agents"))
import common  # noqa: E402
from common import SUMMIT, SIM_HEADER, call, text_of, words, load_roster, prompt_hash  # noqa: E402
from agents import Convener, LENGTH_RULE, LENGTH_MIN, LENGTH_MAX, load_concept_note_sections  # noqa: E402

PAGES = ["home.md", "concept-note.md", "schedule.md", "attendees.md"]

SYSTEM = """You are predicting the outcome of a real workshop: the Epistemic Futures Summit (MIT, September 23–24, 2026). Your deliverable is the manifesto its participants will produce, written as you predict it will actually come out. Not the manifesto you would write, and not the best possible manifesto: the one this particular room, run through this particular process, will most likely produce.

You have the organizers' public web pages and the roster below, and nothing else: no transcripts, no position papers, no notes from the event. Use what you already know of these people's public work.

How to think about it:
- The manifesto is the product of a process. Six Thursday sessions, each ending in a five-minute harvest of three to five claims; Session 5 names interventions and open questions; Session 6 is Cukier and Miller's synthesis; then a small writing committee drafts.
- Assume every attendee has equal force of personality. Positions win or lose on their content and on how many people in the room hold them.
- The conveners' priors, as written in the concept note, shape the frame heavily. The organizers are Agüera y Arcas, Bilder, Brand, Krakauer and Shaub.
- Do not flatten people into stereotypes of their field or their best-known book."""

REQUIREMENTS = ("Write the manifesto. The organizers' brief (from the concept note):\n\n{spec}\n\n"
                "Requirements: a short, plain-spoken manifesto for sustaining human knowledge: a title, a "
                "short preamble, then numbered principles (each a bold one-line statement followed by one paragraph of argument in "
                "the room's own terms), then a short section on what the signatories commit to do. It is opinionated, not a "
                "consensus report; where the room split, take the majority position and record the split in a final section "
                "headed 'Noted dissents', attributing each dissent by name to the attendee most likely to hold it. "
                "{length} Output only the manifesto in Markdown, starting with a level-1 title.")


def context():
    pages = "\n\n".join(f"# Page: {p}\n\n{(SUMMIT / p).read_text().strip()}" for p in PAGES)
    roster = "\n".join(f"- {r['name']} ({r['affiliation']}): {r['role']}" for r in load_roster())
    return f"# The summit's public web pages\n\n{pages}\n\n# Roster (name, affiliation, summit role)\n\n{roster}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--out", default=str(HERE))
    a = ap.parse_args()
    out = Path(a.out)
    log = common.set_log(out / "calls.jsonl")
    system = [{"type": "text", "text": SYSTEM},
              {"type": "text", "text": context(), "cache_control": {"type": "ephemeral"}}]
    user = REQUIREMENTS.format(spec=load_concept_note_sections(["Where this leads"]), length=LENGTH_RULE)
    conv = Convener()
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def one(i):
        d = out / f"b{i}"; mp = d / "manifesto.md"
        if mp.exists(): return json.loads((d / "state.json").read_text())
        d.mkdir(parents=True, exist_ok=True)
        doc = ""
        for eff in ("high", "medium", "low"):  # the sim's ladder: thinking can eat the whole budget
            resp = call(system=system, messages=[{"role": "user", "content": user}], max_tokens=48000, effort=eff,
                        agent="baseline", phase="draft", tag=f"b{i}:draft:{eff}")
            doc = text_of(resp)
            if words(doc) >= 1400 and resp.stop_reason != "max_tokens": break
        else:
            raise RuntimeError(f"b{i}: {words(doc)} words after the ladder")
        rec = {"sample": i, "effort": eff, "raw_words": words(doc), "attempts": []}
        if not (LENGTH_MIN <= words(doc) <= LENGTH_MAX):
            (d / "manifesto.uncut.md").write_text(SIM_HEADER + "\n\n" + doc + "\n")
            doc, rec["attempts"] = conv.fit_length(doc, tag=f"b{i}:fit", phase="fit")
        rec["final_words"] = words(doc); rec["in_spec"] = LENGTH_MIN <= words(doc) <= LENGTH_MAX
        mp.write_text(SIM_HEADER + "\n\n" + doc + "\n")
        (d / "state.json").write_text(json.dumps(rec, indent=1))
        return rec

    with ThreadPoolExecutor(a.n) as ex: recs = list(ex.map(one, range(1, a.n + 1)))
    tot = log.totals
    rows = "\n".join(f"| b{r['sample']} | {r['effort']} | {r['raw_words']:,} | {len(r['attempts'])} | {r['final_words']:,} |" for r in recs)
    (out / "RUN.md").write_text(f"""{SIM_HEADER}

# Run record — no-corpus baseline

| | |
|---|---|
| Finished (UTC) | {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} (this invocation started {t0}) |
| Model | `{common.MODEL}`; adaptive thinking; draft effort high (ladder to medium, low if empty), length fit at low |
| Inputs | `summit/website/{{{",".join(PAGES)}}}` from the public corpus + roster names, affiliations, roles. Nothing else. |
| Prompt hash (system + first user message) | `{prompt_hash(system, [{"role": "user", "content": user}], None)}` |
| Samples | {a.n} (differ only by sampling) |
| API calls | {tot['calls']} |
| Tokens | input {tot['input']:,}; cache write {tot['cache_write']:,}; cache read {tot['cache_read']:,}; output {tot['output']:,} |
| Cost (list price, see common.PRICE) | ${tot['usd']:.2f} |

| Sample | Draft effort | Raw words | Fit passes | Final words |
|---|---|---:|---:|---:|
{rows}

Why this exists: `../scoring/PROTOCOL.md`. Generated 2026-09-27, after the real summit and before its manifesto was
published; the inputs are pre-summit public pages only, and nothing from or about the event itself went in.
""")
    print(f"done: {tot['calls']} calls, ${tot['usd']:.2f}")


if __name__ == "__main__":
    main()
