"""Chunk every dossier's by/ + av/ + social/ into passages and embed them (resumable, per person).

Output: index/<slug>/chunks.jsonl (one passage per line) and index/<slug>/emb.npy (float16, L2-normalised,
multilingual-e5-base, 'passage: ' prefix). Rebuild: python build_index.py [slug ...]
One MPS job at a time on desk; run under a perl alarm watchdog (see README)."""
import json, re, sys, time
from pathlib import Path
import numpy as np
from common import DOSSIERS, INDEX_DIR, load_roster

TARGET_WORDS, MAX_WORDS = 180, 230
MIN_SOCIAL_CHARS = 60
EMB_MODEL = "intfloat/multilingual-e5-base"


def parse_front(text):
    if not text.startswith("---"): return {}, text
    end = text.find("\n---", 3)
    if end < 0: return {}, text
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m: fm[m.group(1)] = m.group(2).strip().strip('"')
    return fm, text[end + 4:]


def split_paragraphs(body):
    body = re.sub(r"^# .*\n", "", body.lstrip(), count=1)
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip() and not re.match(r"^#{1,3} ", p.strip())]


def chunk_words(paras):
    out, cur, n = [], [], 0
    for p in paras:
        w = len(p.split())
        if w > MAX_WORDS:  # split a long paragraph at sentence-ish boundaries
            if cur: out.append(" ".join(cur)); cur, n = [], 0
            sents = re.split(r"(?<=[.!?])\s+", p); buf, bn = [], 0
            for s in sents:
                sw = len(s.split())
                if bn + sw > MAX_WORDS and buf: out.append(" ".join(buf)); buf, bn = [], 0
                buf.append(s); bn += sw
            if buf: out.append(" ".join(buf))
            continue
        if n + w > TARGET_WORDS and cur:
            out.append("\n\n".join(cur)); cur, n = [], 0
        cur.append(p); n += w
    if cur: out.append("\n\n".join(cur))
    return [c for c in out if len(c.split()) >= 15]


def prose_chunks(slug):
    for section in ("by", "av"):
        d = DOSSIERS / slug / section
        if not d.exists(): continue
        for f in sorted(d.glob("*.md")):
            fm, body = parse_front(f.read_text(errors="ignore"))
            if fm.get("content") == "metadata-only": continue
            rel = f"{slug}/{section}/{f.name}"
            for i, c in enumerate(chunk_words(split_paragraphs(body))):
                yield {"id": f"{rel}#{i}", "person": slug, "kind": section, "file": rel, "title": fm.get("title", f.stem),
                       "year": fm.get("year", f.name[:4]), "source_url": fm.get("source_url", ""), "text": c}


def social_chunks(slug):
    d = DOSSIERS / slug / "social"
    if not d.exists(): return
    handle = None
    a = d / "bluesky-author.json"
    if a.exists():
        try: handle = json.loads(a.read_text()).get("handle")
        except Exception: pass
    for f in sorted(d.glob("*.jsonl")):
        rel = f"{slug}/social/{f.name}"
        for i, line in enumerate(f.read_text(errors="ignore").splitlines()):
            try: o = json.loads(line)
            except Exception: continue
            if "record" in o:  # bluesky
                if o.get("reason"): continue  # repost
                text = o["record"].get("text", ""); created = o["record"].get("createdAt", "")
                rkey = o.get("uri", "").rsplit("/", 1)[-1]
                url = f"https://bsky.app/profile/{handle}/post/{rkey}" if handle and rkey else ""
                platform = "bluesky"
            else:  # x
                text = o.get("text", ""); created = o.get("created_at", "")
                url = f"https://x.com/i/status/{o.get('id', o.get('conversation_id', ''))}"
                platform = "x"
            text = text.strip()
            if len(text) < MIN_SOCIAL_CHARS or text.startswith("RT @"): continue
            yield {"id": f"{rel}#{i}", "person": slug, "kind": "social", "file": rel, "title": f"{platform} post",
                   "year": created[:4], "source_url": url, "text": text}


def build_person(slug, model):
    out = INDEX_DIR / slug; out.mkdir(parents=True, exist_ok=True)
    cj, ej = out / "chunks.jsonl", out / "emb.npy"
    chunks = list(prose_chunks(slug)) + list(social_chunks(slug))
    if cj.exists() and ej.exists():
        n = sum(1 for _ in open(cj))
        if n == len(chunks) and np.load(ej, mmap_mode="r").shape[0] == n:
            print(f"{slug}: up to date ({n})", flush=True); return
    with open(cj, "w") as f:
        for c in chunks: f.write(json.dumps(c, ensure_ascii=False) + "\n")
    t0 = time.time()
    texts = ["passage: " + c["text"] for c in chunks]
    embs = model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False,
                        convert_to_numpy=True)
    np.save(ej, embs.astype(np.float16))
    print(f"{slug}: {len(chunks)} chunks, {time.time()-t0:.0f}s", flush=True)


def main(slugs):
    import torch
    from sentence_transformers import SentenceTransformer
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    model = SentenceTransformer(EMB_MODEL, device=dev)
    model.max_seq_length = 256
    for slug in slugs:
        build_person(slug, model)


if __name__ == "__main__":
    slugs = sys.argv[1:] or [r["slug"] for r in load_roster()]
    main(slugs)
