"""Attendee agent (Opus 5.5 + recall over its own dossier) and the persona-free convener."""
import json, re, threading
from pathlib import Path
from common import CARDS_DIR, SUMMIT, call, text_of, parse_json, load_roster, words, name_of
import recall as R

ROSTER = load_roster()
BY_SLUG = {r["slug"]: r for r in ROSTER}

SHARED_INSTRUCTIONS = """You are simulating one named participant in the MIT Epistemic Futures Summit (Cambridge, MA, September 23–24, 2026), an invitation-only workshop on how human knowledge can be sustained, curated and trusted in the age of AI. Your position card below says who you are. Your only job is to say what that person would actually say here, as accurately as you can.

Rules:
- Before each contribution, call `recall` two to four times on the matter at hand, with different phrasings, and speak from what you find. Your own published words are your memory; the position card is a map of them, not a substitute.
- Where your corpus has nothing on a question, say less rather than invent. Narrowing to what you have actually worked on, or saying you have no settled view, is fine.
- Respond to what others in the room have said when it bears on your position. Agree, disagree or qualify exactly as your record warrants. Do not manufacture agreement, and do not manufacture disagreement.
- Speak plainly, in the first person, within the word limit you are given. No stage directions, no headers, no citations or file paths aloud. Say it as the person would say it at a table.
- You have the same force of personality as everyone else in the room. Do not perform a temperament; represent an intellectual position.
- Never mention that you are simulated."""

CONVENER_SYSTEM = """You are the convener of the MIT Epistemic Futures Summit (September 23–24, 2026). You run the published schedule and write the harvests and the manifesto drafts. You have no persona and no positions of your own. You never speak as an attendee and never edit an attendee's words. When you write a harvest, you record what the room said, including minority positions, attributed by name. When you draft, you draft from the harvests and the room's own words, not from your own views. Write plainly."""


def load_card(slug):
    return (CARDS_DIR / f"{slug}.md").read_text()


def load_concept_note_sections(names):
    text = (SUMMIT / "concept-note.md").read_text()
    parts = re.split(r"^## ", text, flags=re.M)
    out = []
    for p in parts[1:]:
        title, _, body = p.partition("\n")
        if title.strip() in names: out.append(f"## {title.strip()}\n{body.strip()}")
    return "\n\n".join(out)


def transcript_blocks(turns, cache_last=True):
    """One system text block per turn, so the growing transcript is a shared cache prefix within a round."""
    blocks = []
    for t in turns:
        role = f" ({t['role']})" if t.get("role") else ""
        blocks.append({"type": "text", "text": f"**{t['name']}**{role}: {t['text']}"})
    if blocks and cache_last: blocks[-1]["cache_control"] = {"type": "ephemeral"}
    return blocks


class Attendee:
    def __init__(self, slug):
        self.slug = slug; self.name = BY_SLUG[slug]["name"]; self.aff = BY_SLUG[slug]["affiliation"]
        self.card = load_card(slug)
        self.diary = []   # list of {session, text}
        self.lock = threading.Lock()

    def index(self): return R.get_index(self.slug)

    def diary_text(self):
        if not self.diary: return ""
        return "\n\n".join(f"[{d['session']}] {d['text']}" for d in self.diary)

    def _system(self, context_title, context_intro, turns):
        blocks = [{"type": "text", "text": SHARED_INSTRUCTIONS, "cache_control": {"type": "ephemeral"}}]
        blocks.append({"type": "text", "text": f"# {context_title}\n\n{context_intro}"})
        blocks += transcript_blocks(turns)
        blocks.append({"type": "text", "text": f"# Your position card\n\n{self.card}", "cache_control": {"type": "ephemeral"}})
        return blocks

    def speak(self, *, context_title, context_intro, turns, prompt, max_words=200, phase="", tag="",
              max_tool_calls=4, effort="medium"):
        """Tool loop: recall up to max_tool_calls times, then a plain-text contribution."""
        idx = self.index(); n0 = len(idx.recall_log)
        diary = self.diary_text()
        user = prompt
        if diary: user = f"Your diary so far today (your own private notes):\n{diary}\n\n---\n\n{prompt}"
        user += f"\n\nOutput only the words you say, at most {max_words} words."
        messages = [{"role": "user", "content": user}]
        system = self._system(context_title, context_intro, turns)
        ncalls = 0; text = ""; usd = 0.0
        for it in range(max_tool_calls + 2):
            tc = {"type": "none"} if ncalls >= max_tool_calls else None
            resp = call(system=system, messages=messages, tools=[R.TOOL], tool_choice=tc, max_tokens=6000,
                        effort=effort, agent=self.slug, phase=phase, tag=tag)
            messages.append({"role": "assistant", "content": resp.content})
            if resp.stop_reason == "tool_use":
                results = []
                for b in resp.content:
                    if b.type == "tool_use":
                        q = b.input.get("query", ""); k = int(b.input.get("k") or 6)
                        with self.lock: passages = idx.search(q, k=min(k, 10))
                        results.append({"type": "tool_result", "tool_use_id": b.id, "content": R.format_passages(passages)})
                        ncalls += 1
                messages.append({"role": "user", "content": results})
                continue
            text = text_of(resp); break
        if not text:  # model returned nothing usable; one final forced-text attempt
            resp = call(system=system, messages=messages + [{"role": "user", "content": "Now give your contribution."}],
                        tools=[R.TOOL], tool_choice={"type": "none"}, max_tokens=4000, effort=effort,
                        agent=self.slug, phase=phase, tag=tag + ":retry")
            text = text_of(resp)
        recalls = idx.recall_log[n0:]
        return {"slug": self.slug, "name": self.name, "text": text.strip(), "recall": recalls,
                "n_recall": len(recalls), "words": words(text)}

    def write_diary(self, session_id, session_title, turns, harvest_text="", phase=""):
        blocks = [{"type": "text", "text": SHARED_INSTRUCTIONS, "cache_control": {"type": "ephemeral"}},
                  {"type": "text", "text": f"# {session_title}\n\nTranscript of the session you just sat in:"}]
        blocks += transcript_blocks(turns)
        if harvest_text: blocks.append({"type": "text", "text": f"# Convener's harvest\n\n{harvest_text}"})
        blocks.append({"type": "text", "text": f"# Your position card\n\n{self.card}", "cache_control": {"type": "ephemeral"}})
        prior = self.diary_text()
        user = ("Write a short private diary entry (at most 120 words) as this person: what you heard in that session that "
                "mattered to you, where you changed or sharpened your view, and what you want to say later today. First person, "
                "plain, no headers. Output only the entry.")
        if prior: user = f"Your earlier diary entries today:\n{prior}\n\n---\n\n{user}"
        resp = call(system=blocks, messages=[{"role": "user", "content": user}], max_tokens=3000, effort="low",
                    agent=self.slug, phase=phase, tag="diary")
        entry = text_of(resp)
        self.diary.append({"session": session_id, "text": entry})
        return entry

    def review(self, manifesto, round_no, phase=""):
        idx = self.index(); n0 = len(idx.recall_log)
        blocks = [{"type": "text", "text": SHARED_INSTRUCTIONS, "cache_control": {"type": "ephemeral"}},
                  {"type": "text", "text": f"# Draft manifesto (review round {round_no})\n\n{manifesto}",
                   "cache_control": {"type": "ephemeral"}},
                  {"type": "text", "text": f"# Your position card\n\n{self.card}", "cache_control": {"type": "ephemeral"}}]
        user = (f"Your diary from the summit:\n{self.diary_text()}\n\n---\n\n"
                "The drafting committee asks every participant to do exactly one of three things with this draft:\n"
                "1. sign it as written;\n"
                "2. propose ONE specific edit (quote the sentence or principle to change and give the replacement text, at most 120 words), "
                "on the understanding that you sign if it is accepted;\n"
                "3. file a dissent (at most 150 words) that will be printed under your name in the manifesto's noted dissents.\n"
                "Call recall first so the choice rests on your actual record. Then answer with JSON only, in this shape:\n"
                '{"action": "sign" | "edit" | "dissent", "target": "<quoted text to change, or empty>", '
                '"text": "<replacement text, or the dissent, or empty>", "reason": "<one sentence>"}')
        messages = [{"role": "user", "content": user}]
        ncalls = 0; out = None
        for it in range(5):
            tc = {"type": "none"} if ncalls >= 3 else None
            resp = call(system=blocks, messages=messages, tools=[R.TOOL], tool_choice=tc, max_tokens=6000, effort="medium",
                        agent=self.slug, phase=phase, tag=f"review{round_no}")
            messages.append({"role": "assistant", "content": resp.content})
            if resp.stop_reason == "tool_use":
                results = []
                for b in resp.content:
                    if b.type == "tool_use":
                        with self.lock: passages = idx.search(b.input.get("query", ""), k=min(int(b.input.get("k") or 6), 10))
                        results.append({"type": "tool_result", "tool_use_id": b.id, "content": R.format_passages(passages)})
                        ncalls += 1
                messages.append({"role": "user", "content": results}); continue
            out = parse_json(text_of(resp)); break
        if not out or out.get("action") not in ("sign", "edit", "dissent"):
            out = {"action": "unparsed", "target": "", "text": "", "reason": "unparseable review; not counted", "parse_error": True}
        out.update({"slug": self.slug, "name": self.name, "recall": idx.recall_log[n0:]})
        return out


# Length enforcement (added 2026-09-23 before run 2, after run 1's final came in at 4,216 words against a 1,500–2,500 spec).
# The whole manifesto text (title through Noted dissents; the SIMULATED header and the signature footer are not counted)
# must land in LENGTH_MIN..LENGTH_MAX. The ceiling is 2,400 rather than 2,500 so the written file, header and footer
# included, also stays under 2,500. Out-of-range drafts go back to the convener with per-section word budgets.
LENGTH_MIN, LENGTH_MAX, LENGTH_TARGET = 1500, 2400, 2100
LENGTH_RULE = ("Hard length limit: the whole document, 'Noted dissents' included, must be between 1,500 and 2,400 words; "
               "aim for about 2,100. A draft outside that range is sent back to you for cutting, so budget the words now: "
               "a preamble of at most 150 words, one paragraph of at most 130 words per principle, commitments of at most "
               "200 words in total, and each noted dissent in at most 60 words.")


def sections(doc):
    """Split a manifesto into (label, word_count) at Markdown headings and bold numbered principle lines."""
    out = []; label = "(title and preamble)"; buf = []
    for line in doc.splitlines():
        if re.match(r"^(#{1,3} |\*\*\d+\.)", line.strip()):
            if buf: out.append((label, words("\n".join(buf))))
            label = re.sub(r"[#*]", "", line).strip()[:80]; buf = [line]
        else:
            buf.append(line)
    if buf: out.append((label, words("\n".join(buf))))
    return out


class Convener:
    LADDER = ("high", "medium", "low")

    def _call(self, user, *, context=None, max_tokens=8000, effort="high", tag="", phase="", min_words=0):
        system = [{"type": "text", "text": CONVENER_SYSTEM, "cache_control": {"type": "ephemeral"}}]
        if context: system += context
        resp = call(system=system, messages=[{"role": "user", "content": user}], max_tokens=max_tokens, effort=effort,
                    agent="convener", phase=phase, tag=tag)
        out = text_of(resp)
        # Thinking can eat the whole output budget on long-document calls (run 1: 16K cap at high; runs 2–3: 48K cap at high
        # AND at medium on revise, 12K cap at high on the Session 5 harvest, all returning empty or truncated text). When the
        # caller sets min_words, retry down the effort ladder from wherever it started; low has always returned.
        for eff in self.LADDER[self.LADDER.index(effort) + 1:]:
            if not (min_words and (words(out) < min_words or resp.stop_reason == "max_tokens")): break
            resp = call(system=system, messages=[{"role": "user", "content": user}], max_tokens=max(max_tokens, 48000),
                        effort=eff, agent="convener", phase=phase, tag=f"{tag}:retry-{eff}")
            out = text_of(resp)
        if min_words and (words(out) < min_words or resp.stop_reason == "max_tokens"):
            raise RuntimeError(f"{tag}: {words(out)} words after the retry ladder (stop_reason {resp.stop_reason})")
        return out

    def call_on(self, session, turns, spoken, not_yet, phase=""):
        """May name up to 2 people to call on next, each with a one-line reason. Returns list of {slug, reason}."""
        ctx = [{"type": "text", "text": f"# {session['title']}\n\n{session['description']}"}] + transcript_blocks(turns)
        user = ("You are moderating the roundtable. Everyone still has a guaranteed turn coming in round-robin order. "
                "You may, in addition, call on up to two people now, because something just said needs their answer "
                "(a direct disagreement, a claim in their area, an unanswered question to them). Calling on nobody is the "
                "normal choice. Do not call on someone to steer the room toward a conclusion.\n\n"
                f"Already spoken this session: {', '.join(name_of(s, ROSTER) for s in spoken) or 'nobody'}.\n"
                f"Not yet spoken: {', '.join(name_of(s, ROSTER) for s in not_yet) or 'nobody'}.\n"
                f"Slugs: {json.dumps({name_of(s, ROSTER): s for s in spoken + not_yet})}\n\n"
                'Answer with JSON only: {"call_on": [{"slug": "...", "reason": "..."}]} (the list may be empty).')
        out = parse_json(self._call(user, context=ctx, max_tokens=2000, effort="low", tag="call_on", phase=phase)) or {}
        res = []
        for c in (out.get("call_on") or [])[:2]:
            if isinstance(c, dict) and c.get("slug") in BY_SLUG: res.append({"slug": c["slug"], "reason": str(c.get("reason", ""))})
        return res

    def harvest(self, session, turns, phase=""):
        ctx = [{"type": "text", "text": f"# {session['title']}\n\n{session['description']}"}] + transcript_blocks(turns)
        claims = self._call("Write the harvest for this session: 3–5 key claims, takeaways, or unresolved questions that the "
                            "room actually produced, each in one or two sentences, each attributed to the people who advanced it "
                            "by name. Number them. No preamble.", context=ctx, max_tokens=48000, min_words=120, tag="harvest", phase=phase)
        minority = self._call(f"Here is the harvest you just wrote:\n\n{claims}\n\nNow do a separate pass over the transcript "
                              "for minority positions: views stated by one or two people that the harvest does not capture, "
                              "or that cut against it, including outright disagreements. List each as one or two sentences under "
                              "the person's name. If there are none, say so. No preamble.", context=ctx, max_tokens=48000, min_words=10, tag="minority", phase=phase)
        return {"claims": claims, "minority": minority}

    def harvest_interventions(self, session, turns, phase=""):
        ctx = [{"type": "text", "text": f"# {session['title']}\n\n{session['description']}"}] + transcript_blocks(turns)
        out = self._call("Write the harvest for Session 5 in three parts, from what the room actually said, attributed by name: "
                         "(1) Interventions: the three the room weighted most, then the full list of others proposed, one line each "
                         "(problem / action / who acts). (2) Open questions the room said it cannot yet answer. (3) Who isn't in the "
                         "room who should be at the next convening. Then a fourth part, Minority positions: proposals or objections "
                         "held by one or two people that cut against the rest. No preamble.",
                         context=ctx, max_tokens=48000, min_words=300, tag="harvest_s5", phase=phase)
        return {"claims": out, "minority": ""}

    def draft_manifesto(self, harvests, syntheses, phase=""):
        ctx = [{"type": "text", "text": "# Harvests and syntheses from the summit\n\n" + harvests + "\n\n" + syntheses,
                "cache_control": {"type": "ephemeral"}}]
        spec = load_concept_note_sections(["Where this leads"])
        user = ("Draft the summit manifesto from these harvests. The organizers' brief (from the concept note):\n\n" + spec +
                "\n\nRequirements: a short, plain-spoken manifesto for sustaining human knowledge: a title, a "
                "short preamble, then numbered principles (each a bold one-line statement followed by one paragraph of argument in "
                "the room's own terms), then a short section on what the signatories commit to do. It is opinionated, not a "
                "consensus report; where the room split, take the majority position and record the split in a final section "
                "headed 'Noted dissents', attributing each dissent by name from the harvests' minority positions. Use no "
                "phrasing that the harvests do not support. " + LENGTH_RULE + " Output only the manifesto in Markdown, starting "
                "with a level-1 title.")
        return self._call(user, context=ctx, max_tokens=48000, effort="high", tag="draft_v1", phase=phase, min_words=1400)

    def revise_manifesto(self, draft, reviews, round_no, phase=""):
        edits = [r for r in reviews if r["action"] == "edit"]
        dissents = [r for r in reviews if r["action"] == "dissent"]
        signs = [r for r in reviews if r["action"] == "sign"]
        ctx = [{"type": "text", "text": f"# Current draft\n\n{draft}", "cache_control": {"type": "ephemeral"}}]
        rev = "\n\n".join(f"### {r['name']} — proposed edit\nTarget: {r.get('target','')}\nReplacement: {r.get('text','')}\nReason: {r.get('reason','')}" for r in edits)
        dis = "\n\n".join(f"### {r['name']} — dissent\n{r.get('text','')}" for r in dissents)
        user = (f"Review round {round_no}: {len(signs)} signed as written, {len(edits)} proposed an edit, {len(dissents)} dissented.\n\n"
                f"## Proposed edits\n\n{rev or '(none)'}\n\n## Dissents\n\n{dis or '(none)'}\n\n"
                "Revise the draft. Accept an edit when it is consistent with the harvests and with the rest of the room's "
                "positions; when two edits conflict, keep the one closer to the harvests and note the other as a dissent. "
                "Do not soften principles to win signatures. Replace the 'Noted dissents' section with "
                "the dissents filed this round, verbatim (trimmed only for length), under each dissenter's name; keep any "
                "earlier-round dissent whose author did not sign this round. " + LENGTH_RULE + " Output only the revised "
                "manifesto in Markdown, starting with the level-1 title.")
        return self._call(user, context=ctx, max_tokens=48000, effort="medium", tag=f"revise_v{round_no+1}", phase=phase, min_words=1400)

    def fit_length(self, doc, tag, phase="", tries=5):
        """Send an out-of-range manifesto back with per-section word budgets until it lands in LENGTH_MIN..LENGTH_MAX.
        Effort low on purpose: in run 1 a medium-effort compression call spent its whole 48K budget thinking. At effort low
        the model under-cuts (about 15% per pass in the pre-run test), so the budgets are hard ceilings aimed below the
        target and later passes are told the previous one fell short.
        Returns (doc, attempts): the candidate closest to LENGTH_TARGET, and one record per attempt."""
        attempts = []; cands = [doc]; prev = None
        if words(doc) < 100: raise RuntimeError(f"{tag}: nothing to fit ({words(doc)} words)")
        for i in range(tries):
            n = words(doc)
            if LENGTH_MIN <= n <= LENGTH_MAX: break
            over = n > LENGTH_MAX
            aim = (LENGTH_TARGET - 200) if over else LENGTH_TARGET
            scale = aim / n; verb = "Cut" if over else "Expand"
            budget = "\n".join(f"- {label}: {w} words now → {'at most' if over else 'about'} {max(15, round(w * scale))}"
                                for label, w in sections(doc))
            short = (f"Your previous attempt came back at {prev:,} words, still outside the limit, because it cut too little "
                     "in every section. This time the budgets below are hard ceilings; go under them.\n\n") if prev else ""
            user = (f"This draft is {n:,} words. The hard limit is 1,500–2,400 words and the target is about 2,100. {short}"
                    f"{verb} it section by section to these budgets (current → allowed), so the whole document totals about "
                    f"{aim:,} words:\n\n{budget}\n\n"
                    "Keep every principle, every commitment and every named dissent; cut argument, examples and repetition, "
                    "not positions, and do not add anything new. Commitments: one sentence each. Noted dissents: one entry "
                    "per person, at most 60 words each, no sub-bullets. Keep the title, the headings and the numbering. "
                    "Output only the manifesto in Markdown, starting with the level-1 title.")
            ctx = [{"type": "text", "text": f"# Current draft\n\n{doc}", "cache_control": {"type": "ephemeral"}}]
            system = [{"type": "text", "text": CONVENER_SYSTEM, "cache_control": {"type": "ephemeral"}}] + ctx
            resp = call(system=system, messages=[{"role": "user", "content": user}], max_tokens=48000, effort="low",
                        agent="convener", phase=phase, tag=f"{tag}:fit{i+1}")
            out = text_of(resp); m = words(out)
            ok = resp.stop_reason != "max_tokens" and m >= 1000 and out.lstrip().startswith("#")
            attempts.append({"attempt": i + 1, "words_in": n, "words_out": m, "stop_reason": resp.stop_reason, "usable": ok})
            if ok: doc = out; cands.append(out); prev = m
        best = min(cands, key=lambda d: abs(words(d) - LENGTH_TARGET))
        return best, attempts
