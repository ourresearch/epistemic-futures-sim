"""Run the simulated summit through its published schedule.

  python run.py --out run1                 # full day + manifesto (resumable: rerun the same command)
  python run.py --out smoke-s3 --only s3   # one session, for the smoke test

Every turn is persisted as it happens (out/sessions/<id>.json); rerunning resumes. All generated Markdown starts
with the SIMULATED header. The sim reads only the public corpus (cards, dossiers, summit/website)."""
import argparse, hashlib, json, random, sys, threading, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import set_log, SIM_HEADER, MODEL, words, name_of, write_md, LOG as _LOG
import common
from schedule import SESSIONS, OPENING, UNCONFERENCE_TOPICS, SESSION_FORMAT, CONCEPT_NOTE_FOR
from agents import (Attendee, Convener, ROSTER, load_concept_note_sections, SHARED_INSTRUCTIONS, CONVENER_SYSTEM,
                    LENGTH_MIN, LENGTH_MAX, LENGTH_TARGET, LENGTH_RULE)
import recall as R

SLUGS = [r["slug"] for r in ROSTER]
WORKERS = 8


def jdump(p, o): Path(p).parent.mkdir(parents=True, exist_ok=True); Path(p).write_text(json.dumps(o, ensure_ascii=False, indent=1))
def jload(p, default=None): p = Path(p); return json.loads(p.read_text()) if p.exists() else default


class Run:
    def __init__(self, out, seed):
        self.out = Path(out); self.out.mkdir(parents=True, exist_ok=True)
        self.seed = seed
        self.log = set_log(self.out / "calls.jsonl")
        self.state = jload(self.out / "state.json", {"phases": {}, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        self.attendees = {s: Attendee(s) for s in SLUGS}
        self.convener = Convener()
        self.harvests = jload(self.out / "harvests.json", {})
        self.callons = jload(self.out / "convener-log.json", [])
        for s in SLUGS:
            self.attendees[s].diary = jload(self.out / "diaries" / f"{s}.json", [])
        self.opening_text = ""
        self.io_lock = threading.Lock()  # the three unconference rooms run in parallel and share these files

    # ---------- persistence ----------
    def save_state(self):
        with self.io_lock: jdump(self.out / "state.json", self.state)
    def done(self, phase): return self.state["phases"].get(phase, False)
    def mark(self, phase): self.state["phases"][phase] = True; self.save_state()
    def spath(self, sid): return self.out / "sessions" / f"{sid}.json"
    def save_harvests(self):
        with self.io_lock: jdump(self.out / "harvests.json", self.harvests)
    def save_diary(self, slug): jdump(self.out / "diaries" / f"{slug}.json", self.attendees[slug].diary)
    def log_callon(self, rec):
        with self.io_lock: self.callons.append(rec); jdump(self.out / "convener-log.json", self.callons)

    def offset(self, sid, n):
        return random.Random(f"{self.seed}:{sid}").randrange(n) if n else 0

    # ---------- one turn ----------
    def turn(self, sess, slug, role, prompt, max_words, turns, context_intro, tag, reason=None):
        a = self.attendees[slug]
        t = a.speak(context_title=sess["title"], context_intro=context_intro, turns=turns, prompt=prompt,
                    max_words=max_words, phase=sess["id"], tag=tag)
        t.update({"role": role, "i": len(turns), "ts": time.strftime("%H:%M:%S")})
        if reason: t["called_on_reason"] = reason
        turns.append(t)
        print(f"  [{sess['id']}] {len(turns):3d} {role:<12} {a.name:<24} {t['words']:3d}w recalls={t['n_recall']} ${self.log.totals['usd']:.2f}", flush=True)
        return t

    # ---------- generic session runner (queue-based, resumable) ----------
    def run_queue(self, sess, context_intro, plan, callon_every=8, callon_pool=None):
        """plan: list of dicts {slug, role, prompt, max_words, tag}. Persists after every turn."""
        data = jload(self.spath(sess["id"]), {"turns": [], "queue": plan, "floor_since_check": 0, "done": False})
        if data["done"]: return data["turns"]
        turns = data["turns"]
        while data["queue"]:
            item = data["queue"][0]
            self.turn(sess, item["slug"], item["role"], item["prompt"], item["max_words"], turns, context_intro,
                      item.get("tag", item["role"]), reason=item.get("reason"))
            data["queue"].pop(0)
            if item["role"] in ("floor", "called"):
                data["floor_since_check"] += 1
            jdump(self.spath(sess["id"]), data)
            # convener check-in: may call on up to two people
            if callon_pool and data["floor_since_check"] >= callon_every and data["queue"]:
                data["floor_since_check"] = 0
                spoken = list(dict.fromkeys(t["slug"] for t in turns))
                not_yet = [q["slug"] for q in data["queue"] if q["role"] == "floor"]
                for c in self.convener.call_on(sess, turns, spoken, not_yet, phase=sess["id"]):
                    self.log_callon({"session": sess["id"], "after_turn": len(turns), "slug": c["slug"], "reason": c["reason"]})
                    data["queue"].insert(0, {"slug": c["slug"], "role": "called", "max_words": 150, "tag": "called",
                                             "reason": c["reason"],
                                             "prompt": f"The convener has called on you: {c['reason']}\nRespond to that, at most 150 words."})
                jdump(self.spath(sess["id"]), data)
        data["done"] = True; jdump(self.spath(sess["id"]), data)
        return turns

    # ---------- phases ----------
    def plenary_intro(self, sess, with_harvests=False):
        intro = sess["description"] + "\n\n" + SESSION_FORMAT
        if self.opening_text: intro += "\n\n## Opening remarks this morning\n\n" + self.opening_text
        if with_harvests: intro += "\n\n## Harvests so far today\n\n" + self.harvests_text()
        return intro

    def harvests_text(self, ids=None):
        parts = []
        for sid, h in self.harvests.items():
            if ids and sid not in ids: continue
            parts.append(f"### {h['title']}\n\n{h['claims']}\n\n**Minority positions**\n\n{h['minority']}")
        return "\n\n".join(parts)

    def do_harvest(self, sess, turns, kind="normal"):
        if sess["id"] in self.harvests: return
        h = self.convener.harvest_interventions(sess, turns, phase=sess["id"]) if kind == "interventions" \
            else self.convener.harvest(sess, turns, phase=sess["id"])
        h["title"] = sess["title"]; self.harvests[sess["id"]] = h; self.save_harvests()

    def do_diaries(self, sess, turns, slugs):
        key = f"diary:{sess['id']}"
        if self.done(key): return
        h = self.harvests.get(sess["id"], {})
        htext = (h.get("claims", "") + "\n\n" + h.get("minority", "")).strip()
        def one(slug):
            a = self.attendees[slug]
            if any(d["session"] == sess["id"] for d in a.diary): return
            a.write_diary(sess["id"], sess["title"], turns, htext, phase=sess["id"]); self.save_diary(slug)
        with ThreadPoolExecutor(WORKERS) as ex: list(ex.map(one, slugs))
        self.mark(key)

    def phase_unconference(self):
        if self.done("unconference"): return
        # 1. each attendee ranks the topics, grounded in recall
        cpath = self.out / "unconference" / "choices.json"
        choices = jload(cpath, {})
        topics = "\n".join(f"{i+1}. {t}" for i, t in enumerate(UNCONFERENCE_TOPICS))
        sess = {"id": "unconf-choice", "title": "Wednesday unconference: choosing a breakout room"}
        def choose(slug):
            if slug in choices: return
            a = self.attendees[slug]
            t = a.speak(context_title=sess["title"],
                        context_intro="Three breakout rooms; topics proposed by attendees in advance after reading the concept note.",
                        turns=[], max_words=60, phase="unconference", tag="choice",
                        prompt=("Five topics were proposed:\n" + topics + "\n\nRank all five by how much you personally have to "
                                "contribute, from your own record (call recall first). Answer with JSON only: "
                                '{"ranking": [topic numbers, best first], "why": "one sentence"}'))
            j = common.parse_json(t["text"]) or {}
            rk = [int(x) for x in (j.get("ranking") or []) if str(x).isdigit() and 1 <= int(x) <= len(UNCONFERENCE_TOPICS)]
            for i in range(1, len(UNCONFERENCE_TOPICS) + 1):
                if i not in rk: rk.append(i)
            choices[slug] = {"ranking": rk, "why": j.get("why", ""), "raw": t["text"], "recall": t["recall"]}
        with ThreadPoolExecutor(WORKERS) as ex: list(ex.map(choose, SLUGS))
        jdump(cpath, choices)
        # 2. allocate: top-3 first choices become rooms; everyone joins their best-ranked open room
        first = Counter(c["ranking"][0] for c in choices.values())
        rooms = [t for t, _ in sorted(first.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
        members = {t: [] for t in rooms}
        for slug in SLUGS:
            for t in choices[slug]["ranking"]:
                if t in members: members[t].append(slug); break
        alloc = {"rooms": [{"topic_no": t, "topic": UNCONFERENCE_TOPICS[t-1], "members": members[t]} for t in rooms],
                 "first_choice_counts": {UNCONFERENCE_TOPICS[t-1]: n for t, n in first.items()}}
        jdump(self.out / "unconference" / "allocation.json", alloc)
        self.log_callon({"session": "unconference", "allocation": alloc})
        # 3. run the three rooms in parallel, two rounds each
        def run_room(i, room):
            sess = {"id": f"unconf-{i+1}", "title": f"Unconference room {i+1}: {room['topic']}",
                    "description": "Wednesday evening breakout (8:00–9:00 PM). Topic proposed by attendees after reading the concept note. Small room, informal."}
            m = room["members"]; off = self.offset(sess["id"], len(m)); order = m[off:] + m[:off]
            plan = []
            for r in (1, 2):
                for slug in order:
                    p = ("Round 1 of 2 in this breakout. Say what you bring to this topic from your own work, and what you think the "
                         "summit should take from it. At most 200 words.") if r == 1 else \
                        ("Round 2 of 2. Respond to what the others in the room said: where you agree, where you differ, and what one "
                         "point from this room should reach the manifesto. At most 200 words.")
                    plan.append({"slug": slug, "role": f"round{r}", "prompt": p, "max_words": 200, "tag": f"unconf-r{r}"})
            turns = self.run_queue(sess, sess["description"], plan, callon_pool=None)
            self.do_harvest(sess, turns)
            self.do_diaries(sess, turns, m)
        with ThreadPoolExecutor(3) as ex: list(ex.map(lambda ir: run_room(*ir), enumerate(alloc["rooms"])))
        self.mark("unconference")

    def phase_opening(self):
        sess = dict(OPENING)
        if not self.done("opening"):
            cn = load_concept_note_sections(CONCEPT_NOTE_FOR["opening"])
            plan = []
            for slug in OPENING["people"]:
                plan.append({"slug": slug, "role": "convener", "max_words": 250, "tag": "opening",
                             "prompt": ("You are one of the conveners opening the day. Set the arc of the day in at most 250 words: why "
                                        "you convened this, what you want the room to produce, and the one thing you most want argued "
                                        "about. The concept note you co-wrote is the reference:\n\n" + cn)})
            self.run_queue(sess, OPENING["description"], plan)
            self.mark("opening")
        turns = jload(self.spath("opening"))["turns"]
        self.opening_text = "\n\n".join(f"**{t['name']}**: {t['text']}" for t in turns)

    def phase_session(self, sess):
        sid = sess["id"]; fmt = sess.get("format", "roundtable")
        people = sess["people"]; lead = people[0]; panel = people[1:]
        with_h = sid in ("s5", "s6")
        intro = self.plenary_intro(sess, with_harvests=with_h)
        cn = load_concept_note_sections(CONCEPT_NOTE_FOR.get(sid, []))
        plan = []
        others = [s for s in SLUGS if s not in people]
        off = self.offset(sid, len(others)); floor = others[off:] + others[:off]
        if fmt in ("roundtable", "interventions"):
            plan.append({"slug": lead, "role": "lead", "max_words": 350, "tag": "provocation",
                         "prompt": ("You are leading this session. Give the opening provocation (5–10 minutes spoken; at most 350 "
                                    "words). State the diagnosis or claim you want the room to argue with, in your own terms and from "
                                    "your own record. The organizers pre-published the arguments the session draws on in the concept "
                                    "note; the relevant sections:\n\n" + cn)})
            for slug in panel:
                plan.append({"slug": slug, "role": "panel", "max_words": 200, "tag": "panel",
                             "prompt": "You are a named panelist in this session. Respond to the provocation and to what has been said so far. At most 200 words."})
            fp = ("You are in the room, not on the panel. The convener has opened the floor and it is your turn. Address the "
                  "session question and what has been said; disagree with the panel where your record does. At most 200 words.")
            if fmt == "interventions":
                fp = ("The floor is open and it is your turn. Answer the session's three questions from your own record: the "
                      "intervention you would put in the roadmap (problem / action / who acts), the open question you cannot yet "
                      "answer, and who is not in the room who should be. At most 220 words.")
            for slug in floor:
                plan.append({"slug": slug, "role": "floor", "max_words": 220 if fmt == "interventions" else 200, "tag": "floor", "prompt": fp})
            turns = self.run_queue(sess, intro, plan, callon_pool=True)
            self.do_harvest(sess, turns, kind="interventions" if fmt == "interventions" else "normal")
            self.do_diaries(sess, turns, SLUGS)
        elif fmt == "talks":
            for slug in people:
                plan.append({"slug": slug, "role": "talk", "max_words": 400, "tag": "talk",
                             "prompt": ("Give your 7-minute talk on what a well-designed AI-mediated knowledge marketplace would look "
                                        "like, from your own work. At most 400 words.")})
            for slug in floor[:sess["floor_turns"]]:
                plan.append({"slug": slug, "role": "floor", "max_words": 150, "tag": "floor",
                             "prompt": "Discussion after the three talks. It is your turn: respond to one or more of the talks from your own record. At most 150 words."})
            turns = self.run_queue(sess, intro, plan, callon_pool=True)
            self.do_harvest(sess, turns)
            self.do_diaries(sess, turns, SLUGS)
        elif fmt == "synthesis":
            for slug in people:
                plan.append({"slug": slug, "role": "synthesis", "max_words": 600, "tag": "synthesis",
                             "prompt": ("You are one of the two closing sensemakers. From the day's harvests (in the session context) and "
                                        "your own notes, give your synthesis: what emerged, what remains contested, what demands action. "
                                        "At most 600 words.")})
            for slug in floor[:sess["floor_turns"]]:
                plan.append({"slug": slug, "role": "floor", "max_words": 150, "tag": "floor",
                             "prompt": "Open floor after the synthesis. It is your turn: what did the synthesis get right or miss, from your own record? At most 150 words."})
            turns = self.run_queue(sess, intro, plan, callon_pool=True)
            self.do_harvest(sess, turns)
            self.do_diaries(sess, turns, SLUGS)

    def fit(self, doc, ver):
        """Length enforcement: keep the uncut text on disk, re-ask until in range, record every attempt in state.json."""
        n = words(doc)
        rec = {"raw_words": n, "attempts": [], "final_words": n}
        if not (LENGTH_MIN <= n <= LENGTH_MAX):
            (self.out / f"manifesto-{ver}.uncut.md").write_text(SIM_HEADER + "\n\n" + doc + "\n")
            doc, rec["attempts"] = self.convener.fit_length(doc, tag=f"fit_{ver}", phase="manifesto")
            rec["final_words"] = words(doc)
        rec["in_spec"] = LENGTH_MIN <= rec["final_words"] <= LENGTH_MAX
        self.state.setdefault("length", {})[ver] = rec; self.save_state()
        return doc

    def phase_manifesto(self):
        mdir = self.out
        v1p = mdir / "manifesto-v1.md"
        if not v1p.exists():
            syn = jload(self.spath("s6"), {"turns": []})["turns"]
            syntheses = "\n\n".join(f"### Closing synthesis — {t['name']}\n\n{t['text']}" for t in syn if t["role"] == "synthesis")
            v1 = self.convener.draft_manifesto(self.harvests_text(), "# Closing syntheses\n\n" + syntheses, phase="manifesto")
            v1 = self.fit(v1, "v1")
            v1p.write_text(SIM_HEADER + "\n\n" + v1 + "\n")
        draft = v1p.read_text().split("\n", 2)[2].strip()
        for rnd in (1, 2):
            rp = mdir / "reviews" / f"round{rnd}.json"
            reviews = jload(rp, {})
            def one(slug):
                if slug in reviews: return
                reviews[slug] = self.attendees[slug].review(draft, rnd, phase="manifesto")
            with ThreadPoolExecutor(WORKERS) as ex: list(ex.map(one, SLUGS))
            jdump(rp, reviews)
            vp = mdir / f"manifesto-v{rnd+1}.md"
            if not vp.exists():
                revised = self.convener.revise_manifesto(draft, [reviews[s] for s in SLUGS], rnd, phase="manifesto")
                revised = self.fit(revised, f"v{rnd+1}")
                vp.write_text(SIM_HEADER + "\n\n" + revised + "\n")
            draft = vp.read_text().split("\n", 2)[2].strip()
        # final = v3 + signature summary from round 2
        r2 = jload(mdir / "reviews" / "round2.json")
        c = Counter(r["action"] for r in r2.values())
        final = (SIM_HEADER + "\n\n" + draft.rstrip() + "\n\n---\n\n## Signatures\n\n"
                 f"Of 33 simulated participants in the second review round: {c['sign']} signed as written, {c['edit']} signed "
                 f"conditional on one proposed edit, {c['dissent']} filed a dissent (printed above under Noted dissents).\n")
        (mdir / "manifesto.md").write_text(final)
        self.mark("manifesto")

    # ---------- human-readable outputs ----------
    def write_outputs(self):
        out = self.out
        for p in sorted((out / "sessions").glob("*.json")):
            d = jload(p); sid = p.stem
            title = {**{s["id"]: s["title"] for s in SESSIONS}, "opening": OPENING["title"]}.get(sid, sid)
            lines = []
            for t in d["turns"]:
                extra = f" — called on: {t['called_on_reason']}" if t.get("called_on_reason") else ""
                lines.append(f"### {t['i']+1}. {t['name']} ({t['role']}{extra})\n\n{t['text']}\n\n"
                             f"<sub>recall: {t['n_recall']} queries; chunks: {', '.join(i for r in t['recall'] for i in r['ids'])}</sub>")
            write_md(out / "transcripts" / f"{sid}.md", f"Transcript — {title}", "\n\n".join(lines))
        for sid, h in self.harvests.items():
            write_md(out / "harvests" / f"{sid}.md", f"Harvest — {h['title']}", h["claims"] + "\n\n## Minority positions\n\n" + h["minority"])
        for slug in SLUGS:
            a = self.attendees[slug]
            if a.diary:
                write_md(out / "diaries" / f"{slug}.md", f"Diary — {a.name}", "\n\n".join(f"## {d['session']}\n\n{d['text']}" for d in a.diary))
        # convener log
        lines = []
        for c in self.callons:
            if "allocation" in c:
                lines.append("## Unconference allocation\n\n" + "\n".join(f"- **{r['topic']}**: {', '.join(name_of(s, ROSTER) for s in r['members'])}" for r in c["allocation"]["rooms"]))
            else:
                lines.append(f"- {c['session']} after turn {c['after_turn']}: called on **{name_of(c['slug'], ROSTER)}** — {c['reason']}")
        write_md(out / "convener-log.md", "Convener log (call-ons and allocations)", "\n".join(lines) or "(no call-ons)")
        for rnd in (1, 2):
            r = jload(out / "reviews" / f"round{rnd}.json")
            if r:
                write_md(out / "reviews" / f"round{rnd}.md", f"Review round {rnd}",
                         "\n\n".join(f"### {v['name']} — {v['action']}\n\n{('Target: ' + v.get('target','') + chr(10)) if v.get('target') else ''}{v.get('text','')}\n\n<sub>{v.get('reason','')}</sub>" for v in r.values()))
        self.write_run_md()

    def write_run_md(self):
        out = self.out; tot = self.log.totals
        calls = [json.loads(l) for l in open(out / "calls.jsonl")]
        turns = [t for p in (out / "sessions").glob("*.json") for t in jload(p)["turns"]]
        att_turn_cost = sum(c["usd"] for c in calls if c["agent"] not in ("convener",) and c["tag"] not in ("diary", "review1", "review2", "choice"))
        n_turns = len(turns)
        recalls = [i for t in turns for r in t["recall"] for i in r["ids"]]
        distinct = len(set(recalls))
        with_recall = sum(1 for t in turns if t["n_recall"] > 0)
        h = lambda s: hashlib.sha256(s.encode()).hexdigest()[:16]
        r2 = jload(out / "reviews" / "round2.json", {}); c2 = Counter(r["action"] for r in r2.values())
        started = self.state.get("started", "?"); ended = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        length_row = "; ".join(f"{v}: {r['raw_words']:,} → {r['final_words']:,} words after {len(r['attempts'])} cut(s)"
                               + ("" if r["in_spec"] else " (STILL OUT OF SPEC)")
                               for v, r in sorted(self.state.get("length", {}).items())) or "(no manifesto phase in this run)"
        body = f"""| | |
|---|---|
| Started (UTC) | {started} |
| Finished (UTC) | {ended} |
| Model | `{MODEL}` (every agent and the convener); adaptive thinking; effort: attendee turns medium, diaries low, convener call-ons low, harvests/drafts high |
| Seed | {self.seed} (per-session round-robin offsets only) |
| Prompt hashes | shared attendee instructions `{h(SHARED_INSTRUCTIONS)}`; convener system `{h(CONVENER_SYSTEM)}`; recall tool `{h(json.dumps(R.TOOL, sort_keys=True))}` |
| Cards | `cards/` (33; sim 1's cards reused unchanged) |
| Retrieval | hybrid BM25 + multilingual-e5-base (RRF), MMR λ=0.6 (normalised RRF relevance − max cosine to chosen; exact-duplicate texts skipped), k≤10, scoped to the caller's own dossier; chunk IDs logged per turn |
| API calls | {tot['calls']} |
| Tokens | input {tot['input']:,}; cache write {tot['cache_write']:,}; cache read {tot['cache_read']:,}; output {tot['output']:,} |
| Cost (list price, see common.PRICE) | ${tot['usd']:.2f} |
| Attendee turns | {n_turns} (spoken turns in sessions; cost ${att_turn_cost:.2f}, ${att_turn_cost/max(n_turns,1):.3f} per turn) |
| Recall | {with_recall}/{n_turns} turns called recall; {len(recalls)} passages retrieved, {distinct} distinct ({distinct/max(len(recalls),1):.0%}) |
| Review round 2 | sign {c2['sign']}, edit {c2['edit']}, dissent {c2['dissent']} |
| Length enforcement | {LENGTH_MIN:,}–{LENGTH_MAX:,} words (target {LENGTH_TARGET:,}) on the manifesto text, header and signature footer excluded; out-of-range drafts re-asked at effort low with per-section budgets, up to 3 times. {length_row} |

Assumptions recorded: the first name listed for each session on the published schedule is treated as its lead; the
unconference topic pool is the organizers' sign-up sheet as of 2026-08-23 (titles only); the marketplace and closing
open-floor rounds are capped at 12 speakers instead of a full-room floor; call-ons are limited to two per convener
check-in, one check-in per eight floor turns. Known limitations are stated in `DESIGN.md`.
"""
        write_md(out / "RUN.md", f"Run record — {out.name}", body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--only", help="run a single session id (smoke test), e.g. s3")
    a = ap.parse_args()
    run = Run(Path(__file__).resolve().parent / a.out, a.seed)
    t0 = time.time()
    if a.only:
        sess = next(s for s in SESSIONS if s["id"] == a.only)
        run.phase_session(sess)
    else:
        run.phase_unconference()
        run.phase_opening()
        for sess in SESSIONS:
            run.phase_session(sess)
        run.phase_manifesto()
    run.write_outputs()
    print(f"done in {(time.time()-t0)/60:.1f} min; total ${run.log.totals['usd']:.2f}")


if __name__ == "__main__":
    main()
