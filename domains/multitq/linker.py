"""
MultiTQ entity candidates for the parser (see pipeline.Pipeline._question_vocabulary).

The knowledge graph has ~10.5k entity labels, too many for the prompt, and questions name
them loosely ("the Australian police" for "Police (Australia)", "Defence" for "Defense").
The labels the question may mean are added to the parser's vocabulary, from two rankings:
  - lexical: IDF-weighted share of a label's words found in the question, on 5-letter word
    stems (Australian ~ Australia, Korean ~ Korea);
  - embedding: cosine similarity of question and label (ARGUS_EMBED_MODEL, the model the other
    experiments use), the label vectors computed once and cached next to the store.
Without an embedding endpoint the lexical ranking is used alone.
"""
from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ENTITIES = Path(os.environ.get("MULTITQ_KG_DIR", ROOT.parent / "MultiTQ/data/MultiTQ/kg")) / "entity2id.json"
CACHE = ROOT / "data_multitq" / "entity_embeddings.npy"
EMBED_MODEL = os.environ.get("ARGUS_EMBED_MODEL", "qwen3-embedding-8b")
N_LEXICAL, N_EMBED, N_MAX = 15, 15, 25
_STOP = set("""a an the of in on at to for from by with and or who whom whose what which when where why how did do does
was were is are be been first last after before same month year day between during into about than that this those these
his her its their other others""".split())
_WORD = re.compile(r"[a-z0-9]+")

_labels: list[str] | None = None
_stems: list[list[str]] = []
_idf: dict[str, float] = {}
_vectors: np.ndarray | None = None
_embed_failed = False


def _stem(w: str) -> str:
    return w[:5]


def _words(text: str) -> list[str]:
    return [_stem(w) for w in _WORD.findall(text.lower()) if w not in _STOP]


def _load() -> None:
    global _labels, _stems, _idf
    if _labels is not None:
        return
    _labels = [e.replace("_", " ") for e in json.load(open(ENTITIES))]
    _stems = [sorted(set(_words(lab))) for lab in _labels]
    df = Counter(s for st in _stems for s in st)
    _idf = {s: math.log(len(_labels) / c) + 1.0 for s, c in df.items()}


def _client():
    from openai import OpenAI
    return OpenAI(base_url=os.environ.get("OLLAMA_BASE_URL", "https://chat.kiconnect.nrw/api/v1"),
                  api_key=os.environ.get("OPENAI_API_KEY", "no-key"))


def _embed(texts: list[str]) -> np.ndarray:
    out = []
    client = _client()
    for i in range(0, len(texts), 64):
        r = client.embeddings.create(model=EMBED_MODEL, input=texts[i:i + 64])
        out += [d.embedding for d in r.data]
    v = np.asarray(out, dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def _label_vectors() -> np.ndarray | None:
    global _vectors, _embed_failed
    if _vectors is None and not _embed_failed:
        try:
            if CACHE.exists():
                _vectors = np.load(CACHE)
            else:
                _vectors = _embed(_labels)
                np.save(CACHE, _vectors)
        except Exception as e:  # no endpoint/key: lexical candidates only
            print(f"[linker] embeddings unavailable ({type(e).__name__}: {e}); lexical candidates only")
            _embed_failed = True
    return _vectors


def lexical(question: str, n: int = N_LEXICAL) -> list[str]:
    _load()
    q = set(_words(question))
    ql = question.lower()
    scored = []
    for lab, st in zip(_labels, _stems):
        if not st:
            continue
        hit = sum(_idf[s] for s in st if s in q)
        if hit:
            score = hit / sum(_idf[s] for s in st) + (1.0 if lab.lower() in ql else 0.0)
            scored.append((score, -len(lab), lab))
    return [lab for _, _, lab in sorted(scored, reverse=True)[:n]]


def embedding(question: str, n: int = N_EMBED) -> list[str]:
    _load()
    vecs = _label_vectors()
    if vecs is None:
        return []
    try:
        q = _embed([question])[0]
    except Exception:
        return []
    return [_labels[i] for i in np.argsort(-(vecs @ q))[:n]]


def candidates(question: str, earlier: list[str] | None = None) -> str | None:
    text = " ".join([*(earlier or []), question])
    labels = list(dict.fromkeys(lexical(text) + embedding(text)))[:N_MAX]
    if not labels:
        return None
    return ("Entity labels in this knowledge graph that the question may name (Actor.label / Recipient.label — "
            "filter with op equals on the exact label):\n" + "; ".join(labels))
