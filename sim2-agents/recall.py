"""recall(query, k): hybrid BM25 + embedding search over ONE person's dossier, MMR-diversified, chunk IDs logged."""
import json, re, threading
from pathlib import Path
import numpy as np
from rank_bm25 import BM25Okapi
from common import INDEX_DIR

EMB_MODEL = "intfloat/multilingual-e5-base"
_tok = re.compile(r"\w+")
def tokenize(s): return _tok.findall(s.lower())

_encoder = None; _enc_lock = threading.RLock()  # reentrant: embed_query holds it while calling encoder()
def encoder():
    global _encoder
    with _enc_lock:
        if _encoder is None:
            from sentence_transformers import SentenceTransformer
            _encoder = SentenceTransformer(EMB_MODEL, device="cpu")  # queries on CPU: never fight the GPU
            _encoder.max_seq_length = 256
    return _encoder

def embed_query(q):
    with _enc_lock:
        return encoder().encode(["query: " + q], normalize_embeddings=True, convert_to_numpy=True)[0].astype(np.float32)


class PersonIndex:
    def __init__(self, slug):
        d = INDEX_DIR / slug
        self.slug = slug
        self.chunks = [json.loads(l) for l in open(d / "chunks.jsonl")]
        self.emb = np.load(d / "emb.npy").astype(np.float32)
        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in self.chunks]) if self.chunks else None
        self.recall_log = []  # (query, [chunk ids]) per call

    def search(self, query, k=6, cand=40, lam=0.7):
        if not self.chunks: return []
        n = len(self.chunks)
        qv = embed_query(query)
        sims = self.emb @ qv
        bm = np.asarray(self.bm25.get_scores(tokenize(query)))
        # reciprocal-rank fusion of the two rankings
        def ranks(scores):
            order = np.argsort(-scores); r = np.empty(n); r[order] = np.arange(n); return r
        rrf = 1.0 / (60 + ranks(sims)) + 1.0 / (60 + ranks(bm))
        pool = list(np.argsort(-rrf)[:cand])
        # MMR over the candidate pool using embedding similarity
        chosen = []
        while pool and len(chosen) < k:
            best, best_s = None, -1e9
            for i in pool:
                div = max((float(self.emb[i] @ self.emb[j]) for j in chosen), default=0.0)
                s = lam * float(rrf[i]) * 60 - (1 - lam) * div  # rrf scaled to ~[0,2]
                if s > best_s: best, best_s = i, s
            chosen.append(best); pool.remove(best)
        out = [self.chunks[i] for i in chosen]
        self.recall_log.append({"query": query, "ids": [c["id"] for c in out]})
        return out


_cache = {}; _cache_lock = threading.Lock()
def get_index(slug):
    with _cache_lock:
        if slug not in _cache: _cache[slug] = PersonIndex(slug)
        return _cache[slug]


def format_passages(passages):
    if not passages: return "(nothing found in your own corpus for that query)"
    parts = []
    for p in passages:
        src = f" — {p['source_url']}" if p.get("source_url") else ""
        parts.append(f"[{p['id']}] ({p.get('year','?')}, {p['kind']}: {p['title']}{src})\n{p['text']}")
    return "\n\n".join(parts)


TOOL = {
    "name": "recall",
    "description": ("Search your own published writing, talks and posts for what you have actually said on a matter. "
                    "Returns passages with year and source. Call it two to four times, with different phrasings, "
                    "before each contribution, and speak from what it returns."),
    "input_schema": {"type": "object", "properties": {
        "query": {"type": "string", "description": "What you want to remember your own position on, in plain words."},
        "k": {"type": "integer", "description": "How many passages (default 6, max 10)."}},
        "required": ["query"], "additionalProperties": False},
    "strict": True,
}
