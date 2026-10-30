"""
Anonymised experiment results for the anonymous code repository (<repo>/results/).

PRIVATE tool. Reads the result sets the paper reports from ~/workspace/experiments and writes,
per system, one JSON line per question plus a summary:
  - results/benchmark/   six systems on the 500 benchmark questions: answers, accuracy (score.py
                         --verdicts, as in the paper), answer quality (FLASK judge), latency;
  - results/user/        six systems on the 80 user questions: answers, accuracy (rule-scored or
                         judged by an LLM against the reference);
  - results/multitq/     HeriKGQA and Interactive-KBQA on 500 MultiTQ questions (strict, lenient);
  - results/backbone/    HeriKGQA with qwen3-8-27b on the 500 benchmark questions (the gpt-oss-120b
                         run is results/benchmark/herikgqa.jsonl);
  - results/verdicts.json  the verdict each anomaly answer states, for score.py --verdicts;
  - results/human_eval/  the pairwise human evaluation (pairs, form, key, the three evaluators'
                         preferences) and analyze.py, which recomputes the paper's Table 6.
Anonymisation, on every text field: the rewrite of build_space.py (site, place and project names);
node coordinates moved exactly as anonymize_db.py moved the nodes (per site, fitted on the real and
the anonymised database); distances between sites scaled to the anonymised site locations. The
benchmark items' references are taken from the anonymised benchmark. Raw traces (Interactive-KBQA
dialogs, TextRAG retrieved rows, TableRAG prompts and pandas steps) are left out: they hold
retrieved readings and coordinates. Checks: no real coordinate, no real site distance left.

    python export_results.py [--out ~/workspace/HeriKGQA] [--dsn postgresql://argus@localhost:55432/argus_anon]
"""

import argparse
import csv
import hashlib
import importlib
import importlib.util
import json
import math
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

import psycopg

from build_space import IDENTITY, rewrite, rules

HERE = Path(__file__).resolve().parent
WS = Path.home() / "workspace"
EXP = WS / "experiments"
REAL_DSN = "postgresql://argus:argus@localhost:5432/argus_snapshot"

# published name of each system (no configuration names: the repository has one, unnamed)
SYSTEMS = {"herikgqa-thorough": "herikgqa", "herikgqa-thorough-nogrounding": "herikgqa-nogrounding",
           "herikgqa-thorough-noerrorcorrection": "herikgqa-noerrorcorrection",
           "interactive-kbqa": "interactive-kbqa", "textrag": "textrag", "tablerag": "tablerag"}
TYPES = ["basic", "spatial", "temporal", "anomaly", "followup"]
MTQ_TYPES = ["equal", "before_after", "first_last", "equal_multi", "before_last", "after_first"]
ITEM = ["id", "type", "template", "question", "history", "reference", "reference_value", "reference_value_alt",
        "unit", "answerable"]
RUN = {"herikgqa": ["prediction", "latency_s", "llm_calls", "intent", "sparql", "n_result_rows", "vote",
                    "check_failed", "template_fallback", "declined", "declined_oversized", "ad_rt_raw_rows"],
       "interactive-kbqa": ["prediction", "latency_s", "finish_reason", "prompt_tokens", "completion_tokens"],
       "textrag": ["prediction", "latency_s", "retrieval_s", "n_rows", "finish_reason", "prompt_tokens",
                   "completion_tokens"],
       "tablerag": ["prediction", "latency_s", "n_iter", "init_prompt_token_count", "total_token_count"]}


# Variants of site_aliases.json's place names as LLM answers write them (the aliases match the
# database's labels literally), applied after those rules.
LLM_VARIANTS = [(r"Dyonisios\s*&\s*pant?h?er\s+mosaic", "Mosaic B"), (r"\bDyonisios\b", "Mosaic A"),
                (r"\bDolphins\b(\s+mosaic)?", "Mosaic C"), (r"\bOrazio\b", "Location 1")]


def run_fields(system: str) -> list[str]:
    return RUN["herikgqa" if system.startswith("herikgqa") else system]


def haversine_km(a, b) -> float:
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


class Anonymiser:
    """Text rewrite, coordinate shift and site-distance scaling, fitted on the two databases."""

    def __init__(self, cfg, dsn: str):
        self.rs = rules(cfg) + [(re.compile(p, re.I), r) for p, r in LLM_VARIANTS]
        self.identity_rs = [(re.compile(p), r) for p, r in IDENTITY]
        q = """SELECT DISTINCT r.site_id, n.node_id, n.latitude, n.longitude FROM nodes n
               JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL"""
        with psycopg.connect(REAL_DSN) as c:
            real = {nid: (s, float(a), float(b)) for s, nid, a, b in c.execute(q)}
        with psycopg.connect(dsn) as c:
            anon = {nid: (float(a), float(b)) for _, nid, a, b in c.execute(q)}
        by = defaultdict(list)
        for nid, (s, la, lo) in real.items():
            if nid in anon:
                by[s].append((la, lo, *anon[nid]))
        self.sites = {}        # real site -> lat/lon ranges and the transform
        for s, v in by.items():
            v.sort(key=lambda x: x[1])
            (la1, lo1, a1, p1), (_, lo2, _, p2) = v[0], v[-1]
            k = (p2 - p1) / (lo2 - lo1)
            self.sites[s] = dict(dlat=a1 - la1, k=k, off=p1 - lo1 * k,
                                 lat=(min(x[0] for x in v), max(x[0] for x in v)),
                                 lon=(min(x[1] for x in v), max(x[1] for x in v)))
            for la, lo, a, p in v:   # the transform reproduces every node exactly
                assert abs(la + self.sites[s]["dlat"] - a) < 1e-9 and abs(lo * k + self.sites[s]["off"] - p) < 1e-9, s
        cent = {s: (mean(x[0] for x in v), mean(x[1] for x in v)) for s, v in by.items()}
        acent = {s: (mean(x[2] for x in v), mean(x[3] for x in v)) for s, v in by.items()}
        self.pairs = {}        # frozenset(real sites) -> (real km, anonymised km)
        for a in cent:
            for b in cent:
                if a < b:
                    self.pairs[frozenset((a, b))] = (haversine_km(cent[a], cent[b]), haversine_km(acent[a], acent[b]))
        self.real_names = {s: re.compile(rf"\b{re.escape(s)}\b", re.I) for s in self.sites}
        self.changes = []      # (kind, old, new, context) of every coordinate and distance replaced

    # numbers with decimals, the sign also written as a Unicode minus or hyphen; a coordinate is read
    # as one with four or more decimals, with two or three next to a coordinate word, or with one
    # followed by a degree sign and a direction
    MINUS = "-‐‑‒–−"
    NUM = re.compile(rf"(?<![\w.])([{MINUS}]?)(\d{{1,3}}\.(\d+))(?![\d])(\s*°\s*[NSEW]\b)?")
    COORD_WORD = re.compile(r"lat|lon|coordinat|centroid|°\s*[NSEW]\b|\b[NSEW]\b")
    # thousands separated by a comma or a (narrow, no-break, thin) space, as LLM answers write them
    KM = re.compile(r"(?<![\w.,])(\d{1,3}(?:[,    ]\d{3})+|\d+)(\.\d+)?(\s*(?:km|kilomet))", re.I)
    SPACES = re.compile(r"[    ]")

    def _coord(self, v: float, pad: float):
        """The anonymised value of a real latitude or longitude (a longitude also when its sign was
        dropped, as in "4.24° W", then flipped=True), or None."""
        for s in self.sites.values():
            if s["lat"][0] - pad <= v <= s["lat"][1] + pad:
                return v + s["dlat"], False
            for lon in (v, -v):
                if s["lon"][0] - pad <= lon <= s["lon"][1] + pad:
                    return lon * s["k"] + s["off"], lon != v
        return None

    def _is_coord(self, text: str, m):
        ndec = len(m.group(3))
        ctx = text[max(0, m.start() - 40):m.end() + 40]
        worded = bool(m.group(4) or self.COORD_WORD.search(ctx))
        if ndec >= 4 or (ndec >= 2 and worded) or m.group(4):
            v = float(m.group(2)) * (-1 if m.group(1) else 1)
            # an approximate coordinate (an LLM's estimate) may lie outside the nodes' range
            return self._coord(v, 0.1 if worded else 0.02)
        return None

    def coords(self, text: str) -> str:
        def sub(m):
            hit = self._is_coord(text, m)
            if hit is None:
                return m.group(0)
            new, flipped = hit
            ndec = len(m.group(3))
            direction = m.group(4) or ""
            if flipped and direction.rstrip().endswith("W") and new >= 0:
                direction = direction[:-1] + "E"
            out = f"{new:.{ndec}f}" + direction
            self.changes.append(("coordinate", m.group(0), out, text[max(0, m.start() - 40):m.end() + 40]))
            return out
        return self.NUM.sub(sub, text)

    def km(self, text: str, pair=None) -> str:
        """Distances between sites in km: scaled by the given pair, else by the pair whose real
        distance the number matches (1%)."""
        def sub(m):
            sep = next((c for c in m.group(1) if not c.isdigit()), None)
            v = float(re.sub(r"\D", "", m.group(1)) + (m.group(2) or ""))
            ratio = None
            if pair:
                real, anon = self.pairs[pair]
                ratio = anon / real
            elif v > 100:
                for real, anon in self.pairs.values():
                    if abs(v - real) <= 0.01 * real:
                        ratio = anon / real
            if ratio is None:
                return m.group(0)
            ndec = len(m.group(2) or "") - (1 if m.group(2) else 0)
            new = f"{v * ratio:,.{ndec}f}".replace(",", sep) if sep else f"{v * ratio:.{ndec}f}"
            self.changes.append(("site distance", m.group(0), new + m.group(3),
                                 text[max(0, m.start() - 40):m.end() + 40]))
            return new + m.group(3)
        return self.KM.sub(sub, text)

    def pair_of(self, question: str):
        named = [s for s, p in self.real_names.items() if p.search(question)]
        if len(named) == 2 and re.search(r"how far|distance", question, re.I):
            return frozenset(named)
        return None

    def text(self, s: str, pair=None) -> str:
        # names are matched with plain spaces: an LLM may write "H. Name"
        return rewrite(self.SPACES.sub(" ", self.coords(self.km(s, pair))), self.rs)

    def value(self, v, pair=None):
        """Any JSON value: strings anonymised, structure kept."""
        if v is None or isinstance(v, (bool, int, float)):
            return v
        if isinstance(v, str):
            return self.text(v, pair)
        return json.loads(self.text(json.dumps(v, ensure_ascii=False, default=str), pair))

    def identity(self, v, pair=None):
        """Only the project's name and domain replaced: for public data (MultiTQ), kept verbatim."""
        if v is None or isinstance(v, (bool, int, float)):
            return v
        s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)
        for pat, rep in self.identity_rs:
            s = pat.sub(rep, s)
        return s if isinstance(v, str) else json.loads(s)

    def leaks(self, v) -> list[str]:
        """Real coordinates or site distances in the strings of a JSON value (numbers such as
        latencies are not text)."""
        if isinstance(v, dict):
            return [p for x in v.values() for p in self.leaks(x)]
        if isinstance(v, list):
            return [p for x in v for p in self.leaks(x)]
        if not isinstance(v, str):
            return []
        text, out = v, []
        for m in self.NUM.finditer(text):
            if len(m.group(3)) < 2 and not m.group(4):
                continue
            v = float(m.group(2))
            ctx = text[max(0, m.start() - 40):m.end() + 40]
            pad = 0.1 if m.group(4) or self.COORD_WORD.search(ctx) else 0.02
            for s in self.sites.values():
                if (s["lat"][0] - pad <= v <= s["lat"][1] + pad
                        or any(s["lon"][0] - pad <= x <= s["lon"][1] + pad for x in (v, -v))):
                    out.append(f"coordinate-like {m.group(0)}: …{text[max(0, m.start() - 50):m.end() + 30]}…")
        for m in self.KM.finditer(text):
            v = float(re.sub(r"\D", "", m.group(1)) + (m.group(2) or ""))
            if any(abs(v - real) <= 0.02 * real for real, _ in self.pairs.values()):
                out.append(f"site distance {m.group(0)}: …{text[max(0, m.start() - 50):m.end() + 30]}…")
        return out


def load_dir(d: Path) -> dict:
    return {r["id"]: r for r in (json.load(open(f)) for f in sorted(d.glob("*.json")))}


def scores(path: Path, key="correct") -> dict:
    return {(r["system"], r["id"]): r[key] == "1" for r in csv.DictReader(open(path)) if r[key] != ""}


def p90(xs):
    xs = sorted(xs)
    return xs[int(0.9 * len(xs))]


def pct(xs):
    return round(100 * sum(xs) / len(xs), 1) if xs else None


def record(an: Anonymiser, system: str, rec: dict, item: dict | None, extra: dict, public=False) -> dict:
    """One published line: the item's fields (from the anonymised benchmark when given), the run's
    fields, anonymised (public data: only the project's name), and the scores."""
    pair = an.pair_of(rec["question"])
    anon = an.identity if public else an.value
    out = {}
    for k in ITEM:
        src = item if item is not None else rec
        if k in src and src[k] is not None or k in ("reference_value",):
            out[k] = src.get(k) if item is not None else anon(src.get(k), pair)
    for k in run_fields(system):
        if k in rec:
            v = rec[k]
            if k == "intent" and isinstance(v, str):
                try:
                    v = json.loads(v)
                except ValueError:
                    pass
            out[k] = anon(v, pair)
    out.update(extra)
    return out


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")


def flask_scores(results: Path, systems: list[str]) -> dict:
    """(system dir, id) -> the judge's three scores for the current answer."""
    sys.path.insert(0, str(EXP / "flask_judge"))
    fj = importlib.import_module("flask_judge")
    reviews = fj.load(fj.REVIEWS)
    out = {}
    for s, r in fj.items([str(results / s) for s in systems]):
        rv = reviews.get(fj.key(s, r, fj.build_prompt(r)))
        if rv and rv["scores"]:
            out[(s, r["id"])] = {sk: fj._score(rv["scores"].get(sk)) for sk in ("readability", "conciseness",
                                                                                 "comprehension")}
    return out


def verdict_key(question: str, prediction: str | None) -> str:
    """extract_verdicts.py's cache key."""
    return hashlib.sha1((question + "\x00" + (prediction or "")).encode()).hexdigest()


class Verdicts:
    """The verdict each anomaly answer states (experiments/verdicts.json, by extract_verdicts.py),
    re-keyed to the published, anonymised question and answer."""

    def __init__(self):
        self.real = json.load(open(EXP / "verdicts.json"))
        self.published = {}

    def add(self, rec: dict, row: dict) -> None:
        v = self.real.get(verdict_key(rec["question"], rec.get("prediction")))
        if v is not None:
            self.published[verdict_key(row["question"], row.get("prediction"))] = v


def export_benchmark(an, out: Path, bench: dict, verdicts: Verdicts) -> dict:
    res = EXP / "results_snapv2"
    verd = scores(res / "scores_verdicts.csv")   # score.py --verdicts, as in the paper
    quality = flask_scores(res, list(SYSTEMS))
    summary = {}
    for s, name in SYSTEMS.items():
        recs = load_dir(res / s)
        assert len(recs) == 500, (s, len(recs))
        rows = []
        for i, rec in recs.items():
            q = quality[(s, i)]
            rows.append(record(an, name, rec, bench[i], {
                "correct": verd[(s, i)], "quality": q, "quality_mean": round(mean(q.values()), 3)}))
            verdicts.add(rec, rows[-1])
        write_jsonl(out / f"benchmark/{name}.jsonl", rows)
        by = lambda key, t=None: [r[key] for r in rows if t is None or r["type"] == t]
        qs = [r["quality"] for r in rows]
        summary[name] = {
            "accuracy": {"overall": pct(by("correct")), **{t: pct(by("correct", t)) for t in TYPES}},
            "quality": {**{sk: round(mean(q[sk] for q in qs), 2) for sk in qs[0]},
                        "mean": round(mean(mean(q[sk] for q in qs) for sk in qs[0]), 2),
                        "below_4_pct": pct([min(q.values()) < 4 for q in qs]),
                        "by_type": {t: round(mean(r["quality_mean"] for r in rows if r["type"] == t), 2)
                                    for t in TYPES}},
            "latency_s": {"median": round(median(by("latency_s")), 1), "p90": round(p90(by("latency_s")), 1)},
        }
    (out / "benchmark/summary.json").write_text(json.dumps(summary, indent=1))
    return summary


def export_user(an, out: Path, verdicts: Verdicts) -> dict:
    res = EXP / "results_final/user"
    items = {q["id"]: q for q in json.load(open(WS / "ARGUS-KGQA/material/benchmark_user.json"))}
    auto = scores(res / "scores_user.csv")
    sys.path.insert(0, str(EXP))
    ju = importlib.import_module("judge_manual_user")
    cache = {}
    for line in open(ju.CACHE):
        r = json.loads(line)
        cache[r["key"]] = r
    summary = {}
    for s, name in SYSTEMS.items():
        rows = []
        for i, rec in load_dir(res / s).items():
            q = items[i]
            if q["score_mode"] == "manual":
                ok, by = bool(cache[ju.key(s, rec, q["reference"])]["correct"]), "llm_judge"
            else:
                ok, by = auto[(s, i)], "rule"
            item = {k: an.value(q.get(k), an.pair_of(q["question"])) for k in ITEM if k in q}
            row = record(an, name, rec, item, {"score_mode": q["score_mode"], "scored_by": by, "correct": ok})
            rows.append(row)
            if q["score_mode"] == "verdict":
                verdicts.add(rec, row)
        write_jsonl(out / f"user/{name}.jsonl", rows)
        summary[name] = {"accuracy": pct([r["correct"] for r in rows]),
                         "rule_scored": f"{sum(r['correct'] for r in rows if r['scored_by'] == 'rule')}"
                                        f"/{sum(r['scored_by'] == 'rule' for r in rows)}",
                         "llm_judged": f"{sum(r['correct'] for r in rows if r['scored_by'] == 'llm_judge')}"
                                       f"/{sum(r['scored_by'] == 'llm_judge' for r in rows)}",
                         "latency_s": {"median": round(median(r["latency_s"] for r in rows), 1),
                                       "p90": round(p90([r["latency_s"] for r in rows]), 1)}}
    (out / "user/summary.json").write_text(json.dumps(summary, indent=1))
    return summary


def export_multitq(an, out: Path) -> dict:
    res = EXP / "results_multitq500"
    sc = {(r["system"], r["id"]): r for r in csv.DictReader(open(EXP / "multitq/scores_multitq.csv"))}
    summary = {}
    for s in ("herikgqa-thorough", "interactive-kbqa"):
        name = SYSTEMS[s]
        rows = []
        for i, rec in load_dir(res / s).items():
            r = sc[(s, i)]
            row = record(an, name, rec, None, {"correct_strict": r["correct"] == "1",
                                               "correct_lenient": r["correct_lenient"] == "1",
                                               "lenient_rule": r["lenient_rule"] or None}, public=True)
            row["type"] = rec["type"]
            for k in ("answer_type", "time_level"):
                if k in rec:
                    row[k] = rec[k]
            rows.append(row)
        assert len(rows) == 500, (s, len(rows))
        write_jsonl(out / f"multitq/{name}.jsonl", rows)
        summary[name] = {m: {"mean_of_types": round(mean(pct([r[f"correct_{m}"] for r in rows if r["type"] == t])
                                                         for t in MTQ_TYPES), 1),
                             **{t: pct([r[f"correct_{m}"] for r in rows if r["type"] == t]) for t in MTQ_TYPES}}
                         for m in ("strict", "lenient")}
    (out / "multitq/summary.json").write_text(json.dumps(summary, indent=1))
    return summary


def export_backbone(an, out: Path, bench: dict, gpt: dict, verdicts: Verdicts) -> dict:
    """Scored as the benchmark (score.py --verdicts); the run only has a strict score file, so the
    experiments' scorer is run here with the verdict cache."""
    res = EXP / "results_snapv2_qwen3-8-27b"
    spec = importlib.util.spec_from_file_location("exp_score", EXP / "score.py")
    sc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sc)
    sc.VERDICT_CACHE = verdicts.real
    recs = load_dir(res / "herikgqa-thorough")
    assert len(recs) == 500
    rows = []
    for i, rec in recs.items():
        rows.append(record(an, "herikgqa", rec, bench[i], {"correct": bool(sc.score(rec))}))
        verdicts.add(rec, rows[-1])
    write_jsonl(out / "backbone/herikgqa-qwen3-8-27b.jsonl", rows)
    acc = lambda t=None: pct([r["correct"] for r in rows if t is None or r["type"] == t])
    summary = {"qwen3-8-27b": {"overall": acc(), **{t: acc(t) for t in TYPES}},
               "gpt-oss-120b": gpt["herikgqa"]["accuracy"]}
    (out / "backbone/summary.json").write_text(json.dumps(summary, indent=1))
    return summary


HUMAN_EVAL_FILES = {   # experiments/human_eval/ -> results/human_eval/ (the files behind the paper's Table 6)
    "pairs_thorough_vs_ikbqa.csv": "pairs_herikgqa_vs_ikbqa.csv",
    "annotation_shuffled.xlsx": "annotation_shuffled.xlsx",
    "annotation_key.xlsx": "annotation_key.xlsx",
    "annotation_shuffled_combi.xlsx": "annotation_shuffled_combi.xlsx",
}

HUMAN_EVAL_README = """# Human evaluation

The pairwise human evaluation of HeriKGQA against Interactive-KBQA (IKBQA) behind the paper's
Table 6. The answers are those of an earlier run of both systems on a previous version of the
snapshot (Appendix C); question ids are the benchmark's. Text is anonymised as the other results.

| File | Contents |
|---|---|
| `pairs_herikgqa_vs_ikbqa.csv` | the 100 questions: the judge's stratum and score gap, both answers with their blinded ids and the judge's three scores |
| `annotation_shuffled.xlsx` | the form the evaluators filled in: questions in random order, the two answers as A and B in random order |
| `annotation_key.xlsx` | which system answer A and answer B are |
| `annotation_shuffled_combi.xlsx` | the three evaluators' preferences (A, B or tie) and their majority (`combi`; a tie if all three disagree) |
| `analyze.py` | recomputes Table 6 from these files: `python analyze.py` |

Selection: the judge's verdict on a pair is the difference of the two answers' FLASK scores summed
over the three categories; the 34 pairs with the largest gaps in favour of HeriKGQA and the 33 in
favour of IKBQA, and 33 random ties (seed 20261013). Answers carry random five-character ids; the
answer order within a pair and the question order are shuffled (seed 42).
"""

HUMAN_EVAL_ANALYZE = '''"""
Table 6 of the paper from the files in this directory: human preference by the judge's verdict and
by evaluator, agreement with the judge, and Fleiss' kappa.

    python analyze.py          (needs pandas and openpyxl)
"""
from collections import Counter
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
EVALUATORS = ["volunteer 1", "volunteer 2", "volunteer 3"]
CATS = ["HeriKGQA", "IKBQA", "tie"]

ann = pd.read_excel(HERE / "annotation_shuffled_combi.xlsx")
key = pd.read_excel(HERE / "annotation_key.xlsx")
pairs = pd.read_csv(HERE / "pairs_herikgqa_vs_ikbqa.csv", encoding="utf-8-sig")
m = ann.merge(key, on="question_id").merge(pairs[["question_id", "stratum"]], on="question_id")


def system(row, label):
    label = str(label).strip().upper()
    return row["response_A_system"] if label == "A" else row["response_B_system"] if label == "B" else "tie"


for col in EVALUATORS + ["combi"]:
    m[col + "_system"] = [system(r, r[col]) for _, r in m.iterrows()]

print("By judge verdict (human label = majority):")
judge = {"HeriKGQA better": "HeriKGQA", "IKBQA better": "IKBQA", "tie": "tie"}
for stratum, verdict in judge.items():
    sub = m[m.stratum == stratum]
    c = Counter(sub["combi_system"])
    print(f"  {stratum:16s} n={len(sub):3d}  " + "  ".join(f"{k} {c[k]:2d}" for k in CATS)
          + f"  agree w/ judge {100 * c[verdict] / len(sub):.0f}%")
nontie = m[m.stratum != "tie"]
agree = sum(r["combi_system"] == judge[r["stratum"]] for _, r in nontie.iterrows())
print(f"  agreement on the judge's non-tie verdicts: {agree}/{len(nontie)} = {100 * agree / len(nontie):.0f}%")
print("By evaluator:")
for e in EVALUATORS:
    c = Counter(m[e + "_system"])
    print(f"  {e}: " + "  ".join(f"{k} {c[k]}" for k in CATS))
c = Counter(m["combi_system"])
print("Majority: " + "  ".join(f"{k} {c[k]}" for k in CATS))

n, N = len(EVALUATORS), len(m)
p_i, totals = [], Counter()
for _, r in m.iterrows():
    cnt = Counter(r[e + "_system"] for e in EVALUATORS)
    totals.update(cnt)
    p_i.append((sum(x * x for x in cnt.values()) - n) / (n * (n - 1)))
observed = sum(p_i) / N
chance = sum((totals[k] / (N * n)) ** 2 for k in CATS)
all3 = sum(len({r[e + "_system"] for e in EVALUATORS}) == 1 for _, r in m.iterrows())
two = sum(max(Counter(r[e + "_system"] for e in EVALUATORS).values()) >= 2 for _, r in m.iterrows())
print(f"Fleiss' kappa {(observed - chance) / (1 - chance):.3f} (observed {100 * observed:.1f}%, "
      f"chance {100 * chance:.1f}%); all three agree on {100 * all3 / N:.0f}%, at least two on {100 * two / N:.0f}%")
'''


def export_human_eval(an, out: Path) -> list[str]:
    """The human evaluation's files, every text cell anonymised; returns the strings written (for the
    leak checks, as the spreadsheets are not text files)."""
    import openpyxl
    src, dst = EXP / "human_eval", out / "human_eval"
    dst.mkdir(parents=True, exist_ok=True)
    texts = []
    for name, new in HUMAN_EVAL_FILES.items():
        if name.endswith(".csv"):
            with open(src / name, newline="", encoding="utf-8-sig") as f:
                rows = list(csv.reader(f))
            rows = [[an.value(c) if c else c for c in row] for row in rows]
            texts += [c for row in rows for c in row]
            with open(dst / new, "w", newline="", encoding="utf-8-sig") as f:
                csv.writer(f).writerows(rows)
        else:
            wb = openpyxl.load_workbook(src / name)
            for ws in wb.worksheets:
                for row in ws.iter_rows():
                    for cell in row:
                        if isinstance(cell.value, str):
                            cell.value = an.value(cell.value)
                            texts.append(cell.value)
                        cell.comment = None          # a comment carries its author's name
                texts.append(ws.title)
            # the document properties name who created and last saved the file
            wb.properties = openpyxl.packaging.core.DocumentProperties(creator="anonymous")
            texts += [str(v) for v in vars(wb.properties).values() if isinstance(v, str)]
            wb.save(dst / new)
    (dst / "README.md").write_text(HUMAN_EVAL_README)
    (dst / "analyze.py").write_text(HUMAN_EVAL_ANALYZE)
    return texts


def rescore(out: Path) -> dict:
    """The published benchmark answers re-scored by the repository's evaluation/score.py (with the
    published verdicts) against the anonymised references: the answers whose score differs, per
    system and template."""
    spec = importlib.util.spec_from_file_location("anon_score", out / "evaluation/score.py")
    sc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sc)
    sc.VERDICT_CACHE = json.load(open(out / "results/verdicts.json"))
    diff = defaultdict(lambda: defaultdict(list))
    for f in sorted((out / "results/benchmark").glob("*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if sc.score(r) != r["correct"]:
                diff[f.stem][r["template"]].append(r["id"])
    return {s: dict(t) for s, t in diff.items()}


def readme(b, u, m, k, d) -> str:
    def row(name, cells):
        return f"| {name} | " + " | ".join("–" if c is None else str(c) for c in cells) + " |"
    L = ["# Results", "",
         "The answers and scores behind the paper's tables, one JSON line per question and system, with a",
         "`summary.json` per experiment. All runs use snapshot v2 of the database; the LLM is gpt-oss-120b",
         "unless stated. Site, place and project names are replaced as in the dataset, node coordinates are",
         "moved as in the dataset, and distances between sites are scaled to the moved sites, so the",
         "answers read as if given on the anonymised snapshot. Raw traces (Interactive-KBQA dialogs,",
         "TextRAG's retrieved rows, TableRAG's prompts and pandas steps) are not included: they hold",
         "retrieved readings and coordinates of the original data.", "",
         "## Benchmark (500 questions): `benchmark/`", "",
         "`correct`: by `evaluation/score.py --verdicts`; an anomaly verdict counts wherever the answer",
         "states it, as classified by `evaluation/extract_verdicts.py` (the classifications of these answers",
         "are in `verdicts.json`). Quality: FLASK judge (DeepSeek-V4.1-Flash), Readability, Conciseness and",
         "Comprehension (1–5); `<4`: share of answers with a category below 4. Latency: seconds per question.", "",
         "| System | Mean | Basic | Spatial | Temporal | Anomaly | Follow-up | Quality | <4 (%) | Median s | p90 s |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for n, s in b.items():
        a = s["accuracy"]
        L.append(row(n, [a["overall"], *[a[t] for t in TYPES], s["quality"]["mean"], s["quality"]["below_4_pct"],
                         s["latency_s"]["median"], s["latency_s"]["p90"]]))
    n_diff = sum(len(ids) for t in d.values() for ids in t.values())
    templates = sorted({t for s in d.values() for t in s})
    L += ["", "The scores are those of the original data. Re-scoring the published answers with",
          "`evaluation/score.py --verdicts verdicts.json` against the anonymised references reproduces"]
    if n_diff:
        L += [f"`correct` for every answer except {n_diff}, all of templates {', '.join(templates)} (listed",
              "in `benchmark/summary.json`, `rescored_differences`): the anonymised site centroids are round",
              "numbers, which widens the scorer's precision tolerance, and distances between sites, scaled",
              "down, shrink an answer's error with them."]
    else:
        L += ["`correct` for every answer."]
    L += ["", "## User questions (80): `user/`", "",
          "`score_mode` manual: long lists or open questions, judged by an LLM against the reference",
          "(`scored_by: llm_judge`); the others are rule-scored (`scored_by: rule`), a verdict as for the",
          "benchmark (wherever the answer states it; `verdicts.json`).", "",
          "| System | Accuracy (%) | Rule-scored | LLM-judged | Median s | p90 s |", "|---|---|---|---|---|---|"]
    for n, s in u.items():
        L.append(row(n, [s["accuracy"], s["rule_scored"], s["llm_judged"], s["latency_s"]["median"],
                         s["latency_s"]["p90"]]))
    L += ["", "## MultiTQ (500 questions): `multitq/`", "",
          "`correct_strict`: exact match; `correct_lenient` also accepts an entity tied at the extreme time",
          "(`lenient_rule: tie`) and a month answered without its year (`month`). The paper reports lenient",
          "accuracy. Mean: over the six question types.", "",
          "| System | Scoring | Mean | " + " | ".join(MTQ_TYPES) + " |", "|---|---|---|" + "---|" * len(MTQ_TYPES)]
    for n, s in m.items():
        for mode in ("lenient", "strict"):
            L.append(row(n, [mode, s[mode]["mean_of_types"], *[s[mode][t] for t in MTQ_TYPES]]))
    L += ["", "## Backbone: `backbone/`", "",
          "HeriKGQA on the 500 benchmark questions with qwen3-8-27b; the gpt-oss-120b run is",
          "`benchmark/herikgqa.jsonl`. Accuracy (%), scored as the benchmark.", "",
          "| Backbone | Mean | " + " | ".join(t.capitalize() for t in TYPES) + " |", "|---|---|" + "---|" * len(TYPES)]
    for n in ("gpt-oss-120b", "qwen3-8-27b"):
        L.append(row(n, [k[n]["overall"], *[k[n][t] for t in TYPES]]))
    L += ["", "## Human evaluation: `human_eval/`", "",
          "Three evaluators' pairwise preferences between HeriKGQA and Interactive-KBQA on 100 questions;",
          "`human_eval/analyze.py` recomputes the paper's Table 6 (see `human_eval/README.md`)."]
    return "\n".join(L) + "\n"


def export_results(out: Path, cfg, dsn: str) -> list[str]:
    """Writes <out>/results; returns leak problems (coordinates or site distances left)."""
    an = Anonymiser(cfg, dsn)
    res = out / "results"
    if res.exists():
        for f in sorted(res.rglob("*"), reverse=True):
            f.unlink() if f.is_file() else f.rmdir()
    bench = {q["id"]: q for q in json.load(open(out / "material/benchmark_500.json"))}
    verdicts = Verdicts()
    b = export_benchmark(an, res, bench, verdicts)
    u = export_user(an, res, verdicts)
    m = export_multitq(an, res)
    k = export_backbone(an, res, bench, b, verdicts)
    (res / "verdicts.json").write_text(json.dumps(verdicts.published, indent=1, sort_keys=True))
    human_texts = export_human_eval(an, res)
    d = rescore(out)
    summary = json.loads((res / "benchmark/summary.json").read_text())
    summary["rescored_differences"] = d
    (res / "benchmark/summary.json").write_text(json.dumps(summary, indent=1))
    (res / "README.md").write_text(readme(b, u, m, k, d))
    problems = []
    for f in sorted(res.rglob("*.jsonl")):
        if f.parent.name == "multitq":
            continue   # MultiTQ is public data (ICEWS), no heritage-site coordinates
        for n, line in enumerate(open(f), 1):
            problems += [f"{f.relative_to(out)}:{n}: {p}" for p in an.leaks(json.loads(line))]
    # the spreadsheets are not text: their cells are checked here, also for forbidden words
    from export_repo import forbidden_pattern
    forbidden = re.compile(forbidden_pattern(cfg), re.I)
    for t in human_texts:
        problems += [f"results/human_eval: {p}" for p in an.leaks(t)]
        problems += [f"results/human_eval: forbidden {m.group(0)!r}: …{t[max(0, m.start() - 50):m.end() + 30]}…"
                     for m in forbidden.finditer(t)]
    kinds = defaultdict(int)
    for kind, *_ in an.changes:
        kinds[kind] += 1
    print(f"results: benchmark 6 x 500, user 6 x 80, MultiTQ 2 x 500, backbone 1 x 500 -> {res}; "
          f"replaced: {dict(kinds)}")
    audit = os.environ.get("EXPORT_RESULTS_AUDIT")   # a file to list every replacement in, for review
    if audit:
        with open(audit, "w") as f:
            for c in an.changes:
                f.write(" | ".join(x.replace("\n", " ") for x in c) + "\n")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(WS / "HeriKGQA"))
    ap.add_argument("--dsn", default="postgresql://argus@localhost:55432/argus_anon")
    args = ap.parse_args()
    cfg = json.loads((HERE / "site_aliases.json").read_text())
    problems = export_results(Path(args.out), cfg, args.dsn)
    from export_repo import scan   # forbidden words, secrets, configuration names (export_repo runs it on the repo)
    problems += scan(Path(args.out) / "results", cfg)
    if problems:
        print("\n".join(problems[:40]))
        raise SystemExit(f"{len(problems)} possible leak(s)")
    print("leak check: no real coordinate or site distance")


if __name__ == "__main__":
    main()
