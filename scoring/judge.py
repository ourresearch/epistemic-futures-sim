"""The scoring judge: fixed prompts, one model, structured labels, three votes, every raw answer kept.

Frozen before the real manifesto existed (see PROTOCOL.md). Changing a prompt, a label definition or the model means a
new JUDGE_VERSION, and every cached answer under the old version stops being reused.

Three tasks:
  presence(doc, props)   for each proposition: endorsed / partial / dissent_only / absent   (3 votes, median)
  extract(doc)           title, principles, commitments, named dissents                      (1 call, kept verbatim)
  classify(text, opts)   one label out of a closed set                                        (3 votes, mode)
"""
import hashlib, json, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sim2-agents"))
import anthropic  # noqa: E402
import common  # noqa: E402
from common import client, usage_cost, CallLog, text_of  # noqa: E402

JUDGE_VERSION = "j1"          # bump on any change to a prompt, a label definition, the model or the effort
MODEL = common.MODEL          # claude-opus-5-5
EFFORT = "medium"
VOTES = 3
CACHE = HERE / "cache"
LOG = CallLog(HERE / "calls.jsonl")

LABELS = ["endorsed", "partial", "dissent_only", "absent"]
RANK = {"endorsed": 3, "partial": 2, "dissent_only": 1, "absent": 0}

SYSTEM = """You are a careful reader scoring documents for a research study that compares predicted and real manifestos. Judge substance, not wording: two statements match when they commit to the same thing, even if phrased differently or argued differently. Do not reward vague gestures. Quote evidence from the document exactly and briefly."""

PRESENCE = """Below is a document, then a list of propositions. For each proposition, decide how the document treats it:

- endorsed: the document, in its own voice (title, preamble, principles and their argument, or commitments), adopts substantially this claim. Different wording, emphasis or mechanism detail is fine. A dissent against it elsewhere in the document does not change this.
- partial: the document adopts a claim on the same point that is materially narrower, weaker or different (for example the same goal by a clearly different means), or adopts only a minor part of it.
- dissent_only: the claim appears only in a noted dissent, or the document records it as an unresolved split without adopting it.
- absent: the document does not take this position. A passing mention of the topic, or listing it as an open question, counts as absent.

"Typical details" are examples of how the claim is often made; they are not required for a match.

For each proposition give the label and an exact quote of at most 30 words from the document as evidence (empty string when absent).

# Document

{doc}

# Propositions

{props}"""

EXTRACT = """Extract the structure of the document below, faithfully and without interpretation.

- title: the document's title, verbatim.
- principles: its principles in order. If it numbers or heads them, one entry per numbered or headed principle, and `n` is its number or heading. If it has no explicit principles, list its distinct normative claims in order of appearance (at most 15), with `n` empty. Restate each as one plain sentence of at most 35 words that captures what it says should be done or believed.
- commitments: each thing the signatories commit to do, one sentence each; an empty list if there is no such section.
- dissents: every person the document names as dissenting, disagreeing or holding a minority position, with their name exactly as written and one sentence of their position. An empty list if none.

# Document

{doc}"""

CLASSIFY = """{question}

Options:
{options}

Text:

{text}"""

PRESENCE_SCHEMA = lambda ids: {  # noqa: E731
    "type": "object", "additionalProperties": False, "required": ["items"],
    "properties": {"items": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["id", "label", "evidence"],
        "properties": {"id": {"type": "string", "enum": ids}, "label": {"type": "string", "enum": LABELS},
                       "evidence": {"type": "string"}}}}}}

EXTRACT_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["title", "principles", "commitments", "dissents"],
    "properties": {
        "title": {"type": "string"},
        "principles": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["n", "statement"],
                                                  "properties": {"n": {"type": "string"}, "statement": {"type": "string"}}}},
        "commitments": {"type": "array", "items": {"type": "string"}},
        "dissents": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["name", "position"],
                                                "properties": {"name": {"type": "string"}, "position": {"type": "string"}}}}}}

CLASSIFY_SCHEMA = lambda opts: {  # noqa: E731
    "type": "object", "additionalProperties": False, "required": ["choice", "why"],
    "properties": {"choice": {"type": "string", "enum": opts}, "why": {"type": "string"}}}


def strip_header(doc):
    """Drop the SIMULATED line so the judge reads every document, real or simulated, the same way."""
    lines = doc.splitlines()
    while lines and (lines[0].startswith("> SIMULATED") or not lines[0].strip()): lines = lines[1:]
    return "\n".join(lines).strip()


def _ask(user, schema, tag, vote):
    """One structured call, cached on disk by (version, prompt, vote). Returns the parsed object."""
    key = hashlib.sha256(json.dumps([JUDGE_VERSION, MODEL, EFFORT, SYSTEM, user, schema, vote], sort_keys=True).encode()).hexdigest()[:20]
    cp = CACHE / f"{key}.json"
    if cp.exists(): return json.loads(cp.read_text())["parsed"]
    kw = dict(model=MODEL, max_tokens=32000, system=SYSTEM, messages=[{"role": "user", "content": user}],
              output_config={"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}})
    t0 = time.time(); last = None
    for attempt in range(8):
        try:
            with client().messages.stream(**kw) as st: resp = st.get_final_message()
            break
        except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError) as e:
            last = e; time.sleep(min(60, 5 * 2 ** attempt))
    else:
        raise RuntimeError(f"{tag}: API failed after retries: {last}")
    raw = text_of(resp)
    if resp.stop_reason != "end_turn": raise RuntimeError(f"{tag}: stop_reason {resp.stop_reason}")
    parsed = json.loads(raw)
    usage, usd = usage_cost(resp.usage)
    LOG.add({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tag": tag, "vote": vote, "key": key,
             "judge_version": JUDGE_VERSION, "model": MODEL, "effort": EFFORT, "stop_reason": resp.stop_reason,
             "usage": usage, "usd": round(usd, 5), "secs": round(time.time() - t0, 1)})
    CACHE.mkdir(exist_ok=True)
    cp.write_text(json.dumps({"tag": tag, "vote": vote, "judge_version": JUDGE_VERSION, "user": user, "raw": raw,
                              "parsed": parsed}, ensure_ascii=False, indent=1))
    return parsed


def props_text(props):
    out = []
    for p in props:
        s = f"- id `{p['id']}`: {p['statement']}"
        if p.get("details"): s += f"\n  Typical details: {p['details']}"
        out.append(s)
    return "\n".join(out)


def presence(doc, props, tag):
    """props: [{id, statement, details?}]. Returns {id: {"label", "votes", "evidence"}}; label = median of VOTES votes."""
    user = PRESENCE.format(doc=strip_header(doc), props=props_text(props))
    ids = [p["id"] for p in props]
    with ThreadPoolExecutor(VOTES) as ex:
        runs = list(ex.map(lambda v: _ask(user, PRESENCE_SCHEMA(ids), tag, v), range(VOTES)))
    out = {}
    for pid in ids:
        votes = []; ev = ""
        for r in runs:
            hit = [it for it in r["items"] if it["id"] == pid]
            lab = hit[0]["label"] if hit else "absent"   # a proposition the judge skipped counts as absent
            votes.append(lab)
            if hit and hit[0]["evidence"] and not ev: ev = hit[0]["evidence"]
        med = sorted(votes, key=lambda l: RANK[l])[len(votes) // 2]
        out[pid] = {"label": med, "votes": votes, "evidence": ev}
    return out


def extract(doc, tag):
    return _ask(EXTRACT.format(doc=strip_header(doc)), EXTRACT_SCHEMA, tag, 0)


def classify(text, question, options, tag):
    """options: {key: description}. Returns {"choice", "votes", "why"}; mode of VOTES votes, ties go to the first vote."""
    user = CLASSIFY.format(question=question, options="\n".join(f"- {k}: {v}" for k, v in options.items()), text=text)
    with ThreadPoolExecutor(VOTES) as ex:
        runs = list(ex.map(lambda v: _ask(user, CLASSIFY_SCHEMA(list(options)), tag, v), range(VOTES)))
    votes = [r["choice"] for r in runs]
    top, n = Counter(votes).most_common(1)[0]
    choice = top if n > 1 else votes[0]
    return {"choice": choice, "votes": votes, "why": next(r["why"] for r in runs if r["choice"] == choice)}
