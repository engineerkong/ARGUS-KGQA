"""
Build the anonymous code repository (~/workspace/HeriKGQA) and the Hugging Face dataset
(~/workspace/HeriKGQA-dataset: benchmark and database snapshot) for the manuscript.

PRIVATE tool. It takes the method, the evaluation scripts and the ontology from
ARGUS-KGQA, the demo and the container from ../hf-spaces, and the anonymised
snapshot dump, and puts every text file through the rewrite of build_space.py
(site aliases, project name and domain, no LLM provider URL), plus patches for
paths and credentials. The repository has one configuration, without a name of its
own: the configurations kept commented out in ARGUS-KGQA, and the answer mode only
they used, are removed. Then:
  - the benchmark is generated again, by the rewritten build_benchmark.py, from the
    anonymised database (argus_anon), and aligned to the paper's 500 questions;
  - evaluation/node_labels.csv (used by the scorer) is written from argus_anon;
  - benchmark and dump go to the dataset directory; the repository has their
    checksums (data/SHA256SUMS) and downloads them when the container is built;
  - checks: forbidden words (also in the dump's content), secrets, configuration
    names, Python compiles, file sizes.

    python export_repo.py [--src ~/workspace/ARGUS-KGQA] [--out ~/workspace/HeriKGQA]
                          [--dataset-out ~/workspace/HeriKGQA-dataset]
                          [--dataset-repo anonymous-7989/herikgqa-benchmark] [--space-repo anonymous-7989/HeriKGQA]
                          [--dsn postgresql://argus@localhost:55432/argus_anon]
"""

import argparse
import csv
import hashlib
import json
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import psycopg

from build_space import EXTRA_FORBIDDEN, rewrite, rules

HERE = Path(__file__).resolve().parent
SPACE = HERE.parent / "hf-spaces"
WS = Path.home() / "workspace"
PG_BIN = Path.home() / "miniconda3/envs/pgtools/bin"

# method (the Space's runtime modules), entry points and benchmark builder
SCRIPTS = ["pipeline.py", "1_semantic_parser.py", "2_sparql_retriever.py", "3_answer_generator.py",
           "analysis_ek.py", "analysis_geo.py", "analysis_temp.py", "backend.py", "ontology_schema.py",
           "domain.py", "run_eval.py", "demo.py", "demo_ad.py", "build_benchmark.py"]
EVALUATION = ["score.py", "extract_verdicts.py"]           # from ~/workspace/experiments
ONTOLOGY = ["panoptes3.owl", "panoptes3_extension.owl"]
BENCHMARK = ["benchmark_500.json", "benchmark_500.csv", "benchmark_500.meta.json"]
REPO_FILES = ["Dockerfile", "start.sh", "requirements.txt", "README.md", ".gitignore"]

# Patches after the rewrite: (file, old, new); each old must occur exactly once.
PATCHES = [
    # sites are named by their label (site_a …), as in the data and in the scorer
    ("scripts/build_benchmark.py", "SITE = {s: s.capitalize() for s in SITES}", "SITE = {s: s for s in SITES}"),
    # the database of the container
    ("scripts/build_benchmark.py",
     'DSN = os.environ.get("HERIKG_SNAPSHOT_DSN", "postgresql://herikg:herikg@localhost:5432/herikg_snapshot")',
     'DSN = os.environ.get("HERIKG_SNAPSHOT_DSN", "postgresql://herikg@localhost:5432/herikg_snapshot")'),
    # credentials from the environment only
    ("evaluation/extract_verdicts.py",
     '''# Endpoint settings: the environment first (as the run scripts export them), the
# credentials file as fallback — the key may have been removed from the file.
CRED = Path("/home/kong/workspace/HERIKG-KGQA/scripts/test_llm2.py").read_text()


def cred(key: str, env: str) -> str:
    if os.environ.get(env):
        return os.environ[env]
    m = re.search(key + r'="([^"]+)"', CRED)
    if not m:
        sys.exit(f"no {key}: set {env} (the credentials file has none)")
    return m[1]''',
     '''# Endpoint settings come from the environment (see README.md).


def cred(key: str, env: str) -> str:
    if not os.environ.get(env):
        sys.exit(f"no {key}: set {env}")
    return os.environ[env]'''),
    # a site may be written "site A" as well as "site_a"
    ("evaluation/score.py",
     '''def site_of(rec: dict) -> str | None:''',
     '''_SITE_WORDS = re.compile(r"\\bsite[ _-]?([a-e])\\b", re.I)


def _sites_normalised(text: str) -> str:
    """ "site A", "Site-a" … as the label site_a."""
    return _SITE_WORDS.sub(lambda m: "site_" + m[1].lower(), text)


def site_of(rec: dict) -> str | None:'''),
    ("evaluation/score.py",
     '''            if s in text.lower():
                return s''',
     '''            if s in _sites_normalised(text).lower():
                return s'''),
    ("evaluation/score.py",
     '''        first = min(((text.lower().find(s), s) for s in SITES if s in text.lower()), default=None)''',
     '''        low = _sites_normalised(text).lower()
        first = min(((low.find(s), s) for s in SITES if s in low), default=None)'''),
    # the ontology's creator
    ("material/panoptes3.owl", "<dc:creator>HERIKG Project Consortium</dc:creator>", "<dc:creator>anonymous</dc:creator>"),
    ("material/panoptes3_extension.owl", "<dc:creator>HERIKG Project Consortium</dc:creator>",
     "<dc:creator>anonymous</dc:creator>"),
    # the demo: scripts/ and material/ are siblings of app/
    ("app/app.py", 'sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))',
     'sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))'),
]

# One configuration, named after the system; no --config option.
SINGLE_CONFIG = [
    ("scripts/pipeline.py", "one configuration, THOROUGH: n parse candidates voted, retry budget k = 2,",
     "one configuration: n = 3 parse candidates voted, retry budget k = 2,"),
    ("scripts/pipeline.py", '    answer: str             # "template" | "llm" | "llm+check"',
     '    answer: str             # "llm+check", or "llm" without the answer check'),
    ("scripts/pipeline.py",
     '''CONFIGS = {
    "thorough": Config("thorough", parse_candidates=3, max_retries=2, max_history=2, answer="llm+check"),
}


def get_config(name: str = "thorough", n: int | None = None, grounding: bool = True,
               error_correction: bool = True) -> Config:
    """THOROUGH; n overrides its number of parse candidates. grounding=False gives the
    w/o grounding ablation, error_correction=False the w/o error correction ablation: one
    parse candidate, no retries, and an LLM answer without the answer check (an
    anomaly answer still has to lead with the computed verdict)."""
    cfg = CONFIGS[name.lower()]
    if n is not None and cfg.parse_candidates > 1:
        cfg = replace(cfg, parse_candidates=n)
    if not error_correction:
        cfg = replace(cfg, name=cfg.name + "-noerrorcorrection", parse_candidates=1, max_retries=0,
                      answer="llm" if cfg.answer == "llm+check" else cfg.answer)''',
     '''DEFAULT_CONFIG = Config("herikgqa", parse_candidates=3, max_retries=2, max_history=2, answer="llm+check")


def get_config(n: int | None = None, grounding: bool = True, error_correction: bool = True) -> Config:
    """The system's configuration; n overrides its number of parse candidates. grounding=False
    gives the w/o grounding ablation, error_correction=False the w/o error correction ablation:
    one parse candidate, no retries, and an LLM answer without the answer check (an
    anomaly answer still has to lead with the computed verdict)."""
    cfg = DEFAULT_CONFIG
    if n is not None:
        cfg = replace(cfg, parse_candidates=n)
    if not error_correction:
        cfg = replace(cfg, name=cfg.name + "-noerrorcorrection", parse_candidates=1, max_retries=0,
                      answer="llm")'''),
    ("scripts/pipeline.py", '        config: str | Config = "thorough",', "        config: Config | None = None,"),
    ("scripts/pipeline.py", "        self.config = get_config(config) if isinstance(config, str) else config",
     "        self.config = config or get_config()"),
    ("scripts/pipeline.py",
     "            # THOROUGH: deterministic check against the evidence; one regeneration on failure.",
     "            # Deterministic check against the evidence; one regeneration on failure."),
    ("scripts/3_answer_generator.py", "    # THOROUGH: a previous answer failed check_answer(); say what was wrong.",
     "    # A previous answer failed check_answer(); say what was wrong."),
    ("scripts/run_eval.py",
     '''    python scripts/run_eval.py --questions trial20.json --out results/thorough
    python scripts/run_eval.py --questions q.json --out results/thorough --config thorough --n 3
    python scripts/run_eval.py --questions q.json --out results/thorough-nogrounding --no-grounding
    python scripts/run_eval.py --questions q.json --out results/thorough-noerrorcorrection --no-error-correction''',
     '''    python scripts/run_eval.py --questions material/benchmark_500.json --out evaluation/results/herikgqa
    python scripts/run_eval.py --questions material/benchmark_500.json --out evaluation/results/herikgqa-nogrounding --no-grounding
    python scripts/run_eval.py --questions material/benchmark_500.json --out evaluation/results/herikgqa-noerrorcorrection --no-error-correction'''),
    ("scripts/run_eval.py", "from pipeline import CONFIGS, Pipeline, get_config", "from pipeline import Pipeline, get_config"),
    ("scripts/run_eval.py", '    ap.add_argument("--config", choices=list(CONFIGS), default="thorough")\n', ""),
    ("scripts/run_eval.py", "    cfg = get_config(args.config, n=args.n,", "    cfg = get_config(n=args.n,"),
] + [
    entry for script in ("scripts/demo.py", "scripts/demo_ad.py") for entry in [
        (script, "from pipeline import CONFIGS, Pipeline, get_config", "from pipeline import Pipeline, get_config"),
        (script, '''    parser.add_argument("--config", choices=list(CONFIGS), default="thorough",
                        help="THOROUGH: n voted parses, retries, checked answer (the only configuration in use)")
''', ""),
        (script, "config=get_config(args.config, n=args.n,", "config=get_config(n=args.n,"),
    ]
] + [
    ("app/app.py", "set to THOROUGH's.", "set to the system's defaults."),
    ("app/app.py", "# Configuration options, defaulting to THOROUGH's (n=3, k=2, h=2, answer check on).",
     "# Configuration options, defaulting to the system's (n=3, k=2, h=2, answer check on)."),
    ("app/app.py", 'get_config("thorough", n=3)', "get_config(n=3)"),
    ("app/app.py", '"""The Config for these options: "thorough" for the defaults, else named by them."""',
     '"""The Config for these options: "herikgqa" for the defaults, else named by them."""'),
    ("app/app.py", 'name = ("thorough" if dict', 'name = ("herikgqa" if dict'),
]

# words that must not appear, besides site_aliases.json's and build_space.py's
REPO_FORBIDDEN = [r"\bkong\b", r"dayue", r"gmail", r"nfdi4ds", r"193\.175\.", r"test_llm",
                  r"argus_snapshot", r"argus_anon", r"consortium"]
SECRETS = re.compile(r"sk-[A-Za-z0-9]{16,}|(api_key|password|token)\s*[=:]\s*['\"][^'\"$<{]{6,}['\"]", re.I)
CONFIG_NAMES = re.compile(r"(?i:thorough|disabled-config)|\bFAST\b|\bBALANCED\b")   # "fast" as a word is fine
CONFIG_NAMES_PY = re.compile(r"[\"'](?i:fast|balanced)[\"']")                        # a config key in code


def put(out: Path, rel: str, text: str) -> None:
    p = out / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def patch(out: Path, patches) -> None:
    for rel, old, new in patches:
        p = out / rel
        s = p.read_text()
        if s.count(old) != 1:
            raise SystemExit(f"patch for {rel} does not apply ({s.count(old)} matches): {old[:60]!r}")
        p.write_text(s.replace(old, new))


def drop_template_mode(out: Path) -> None:
    """Remove the template-only answer mode (used only by the removed configurations):
    the branch goes, its else-block moves up one level. The template answer stays as the
    fallback of the answer check."""
    p = out / "scripts/pipeline.py"
    lines = p.read_text().split("\n")
    i = lines.index('        if self.config.answer == "template":')
    assert lines[i + 1].startswith("            answer = template_answer(") and lines[i + 3] == "        else:", lines[i:i + 4]
    del lines[i:i + 4]
    j = i
    while j < len(lines) and (not lines[j].strip() or lines[j].startswith(" " * 12)):
        lines[j] = lines[j][4:] if lines[j].strip() else lines[j]
        j += 1
    p.write_text("\n".join(lines))


def node_labels(dsn: str, out: Path) -> int:
    with psycopg.connect(dsn) as con:
        rows = con.execute("""SELECT DISTINCT r.site_id, n.label, coalesce(n.name, n.label) FROM nodes n
                              JOIN readings r USING (node_id)
                              WHERE r.site_id IN ('site_a', 'site_b', 'site_c', 'site_d', 'site_e')
                              ORDER BY 1, 2""").fetchall()
    with open(out / "evaluation/node_labels.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sl", "label", "name"])
        w.writerows(rows)
    return len(rows)


def align_benchmark(original: Path, out: Path, dsn: str, rs) -> list[str]:
    """The published benchmark has the paper's 500 questions.

    The regenerated benchmark asks the same questions, except where gen_spatial draws node
    pairs from a node list whose order (SELECT DISTINCT, no ORDER BY) followed the original
    names; there the draw differs. Such items keep the original question and get their
    reference from the anonymised coordinates, by the generator's own formulas. Returns
    the ids recomputed this way."""
    spec = importlib.util.spec_from_file_location("bench", out / "scripts/build_benchmark.py")
    bench = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bench)
    with psycopg.connect(dsn) as con:
        rows = con.execute("""SELECT DISTINCT r.site_id, n.label, n.latitude, n.longitude FROM nodes n
                              JOIN readings r USING (node_id) WHERE n.latitude IS NOT NULL""").fetchall()
    nodes = {}
    for s, label, lat, lon in rows:
        nodes.setdefault(s, []).append((label, float(lat), float(lon)))
    coord = {(s, n[0]): n[1:] for s, ns in nodes.items() for n in ns}

    def pair(q):
        site = re.search(r" at (site_[a-e])\?$", q)[1]
        mid = re.search(r"between sensor nodes (.+) at site_[a-e]\?$", q)[1]
        a, c = next((a, c) for a, _, _ in nodes[site] for c, _, _ in nodes[site] if f"{a} and {c}" == mid)
        d = bench.haversine(coord[site, a], coord[site, c])
        return f"{bench.fnum(d, 1)} m.", round(d, 1)

    def others(site, a):
        return sorted((bench.haversine(coord[site, a], n[1:]), n[0]) for n in nodes[site] if n[0] != a)

    def nearest(q):
        a, site = re.search(r"closest to (.+) at (site_[a-e])\?$", q).groups()
        d, lab = others(site, a)[0]
        return f"{lab}, {bench.fnum(d, 1)} m away.", lab

    def within(q):
        site, radius, a = re.search(r"nodes at (site_[a-e]) are within (\d+) m of (.+)\?$", q).groups()
        n = sum(1 for d, _ in others(site, a) if d <= int(radius))
        return f"{n}.", n

    recompute = {"pair_distance": pair, "nearest_node": nearest, "within_radius": within}
    regen = {d["id"]: d for d in json.loads((out / "material/benchmark_500.json").read_text())}
    final, changed = [], []
    for o in json.loads(original.read_text()):
        item = json.loads(rewrite(json.dumps(o, ensure_ascii=False), rs))
        n = regen[o["id"]]
        if n["template"] == item["template"] and n["question"] == item["question"]:
            final.append(n)
            continue
        if item["template"] not in recompute:
            raise SystemExit(f"{o['id']}: {item['template']} drawn differently and not recomputable")
        item["reference"], item["reference_value"] = recompute[item["template"]](item["question"])
        final.append(item)
        changed.append(o["id"])

    (out / "material/benchmark_500.json").write_text(json.dumps(final, indent=1, ensure_ascii=False, default=str))
    with open(out / "material/benchmark_500.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "type", "template", "answerable", "history", "question", "reference", "validated"])
        for it in final:
            hist = " || ".join(f"Q: {h['question']} A: {h['answer']}" for h in it.get("history") or [])
            w.writerow([it["id"], it["type"], it["template"], it["answerable"], hist, it["question"], it["reference"], ""])
    meta_path = out / "material/benchmark_500.meta.json"
    meta = json.loads(meta_path.read_text())
    meta["counts"] = {t: sum(1 for it in final if it["type"] == t) for t in meta["counts"]}
    meta["unanswerable"] = sum(1 for it in final if not it["answerable"])
    meta["note"] = ("The questions are those of the paper. Regenerating draws some spatial node pairs "
                    "differently: the draw follows the order of the original node names.")
    meta_path.write_text(json.dumps(meta, indent=1))
    return changed


def compare_benchmark(original: Path, regenerated: Path, rs) -> dict:
    """Regenerated vs. original (rewritten) benchmark, item by item."""
    old = {d["id"]: d for d in json.loads(original.read_text())}
    new = {d["id"]: d for d in json.loads(regenerated.read_text())}
    report = {"items": (len(old), len(new)), "missing": sorted(set(old) - set(new)),
              "extra": sorted(set(new) - set(old)), "template": [], "question": [], "value": []}
    for i in sorted(set(old) & set(new)):
        o, n = old[i], new[i]
        if o["template"] != n["template"]:
            report["template"].append(i)
            continue
        if rewrite(o["question"], rs) != n["question"]:
            report["question"].append(i)
        if json.loads(rewrite(json.dumps(o["reference_value"]), rs)) != n["reference_value"]:
            report["value"].append((i, n["template"]))
    return report


def forbidden_pattern(cfg) -> str:
    return "|".join([re.escape(w) for w in cfg["forbidden"]] + EXTRA_FORBIDDEN + REPO_FORBIDDEN)


def scan(root: Path, cfg) -> list[str]:
    forbidden = re.compile(forbidden_pattern(cfg), re.I)
    problems = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or ".git" in f.parts or "__pycache__" in f.parts or f.suffix in (".dump", ".jar"):
            continue
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            continue
        where = f"{root.name}/{f.relative_to(root)}"
        for i, line in enumerate(text.splitlines(), 1):
            for kind, pat in (("forbidden", forbidden), ("secret", SECRETS)):
                if pat.search(line):
                    problems.append(f"{kind}: {where}:{i}: {line.strip()[:110]}")
            if CONFIG_NAMES.search(line) or (f.suffix == ".py" and CONFIG_NAMES_PY.search(line)):
                problems.append(f"configuration: {where}:{i}: {line.strip()[:110]}")
    return problems


def neutral_dump(dsn: str, path: Path) -> None:
    """Dump the anonymised database under neutral names. A custom-format archive records
    the database name and every object's owner (pg_dump --no-owner does not change that),
    so argus_anon, owned by the instance's superuser, is copied into herikg_snapshot,
    owned by a role herikg, and dumped as herikg. argus_anon is only read."""
    m = re.match(r"postgresql://(\w+)@([\w.]+):(\d+)/(\w+)$", dsn)
    admin, host, port, source = m.groups()
    conn = ["-h", host, "-p", port]
    psql = [str(PG_BIN / "psql"), *conn, "-U", admin, "-d", "postgres", "-v", "ON_ERROR_STOP=1", "-q", "-c"]
    subprocess.run(psql + ["DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'herikg') "
                           "THEN CREATE ROLE herikg LOGIN; END IF; END $$;"], check=True)
    subprocess.run(psql + ["DROP DATABASE IF EXISTS herikg_snapshot"], check=True)
    subprocess.run(psql + ["CREATE DATABASE herikg_snapshot OWNER herikg"], check=True)
    dump = subprocess.Popen([str(PG_BIN / "pg_dump"), *conn, "-U", admin, "-d", source, "-Fc"], stdout=subprocess.PIPE)
    subprocess.run([str(PG_BIN / "pg_restore"), *conn, "-U", "herikg", "-d", "herikg_snapshot",
                    "--no-owner", "--no-privileges"], stdin=dump.stdout, check=True)
    dump.stdout.close()
    if dump.wait():
        raise SystemExit("pg_dump of the anonymised database failed")
    counts = {}
    for db, user in ((source, admin), ("herikg_snapshot", "herikg")):
        with psycopg.connect(f"postgresql://{user}@{host}:{port}/{db}") as con:
            counts[db] = [con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
                          for t in ("sites", "nodes", "sensors", "readings", "observations", "policies")]
    if counts[source] != counts["herikg_snapshot"]:
        raise SystemExit(f"row counts differ after the copy: {counts}")
    subprocess.run([str(PG_BIN / "pg_dump"), *conn, "-U", "herikg", "-d", "herikg_snapshot", "-Fc",
                    "-f", str(path)], check=True)
    subprocess.run(psql + ["DROP DATABASE herikg_snapshot"], check=True)   # 2 GB, only needed for the dump


def scan_dump(dump: Path, cfg) -> list[str]:
    """Forbidden words in the dump: its table of contents (database name, owners) and
    its content (every row), via pg_restore."""
    pattern = forbidden_pattern(cfg).replace(r"\ ", " ")
    problems = []
    for what, args in (("table of contents", ["-l"]), ("content", ["-f", "-"])):
        restore = subprocess.Popen([str(PG_BIN / "pg_restore"), *args, str(dump)], stdout=subprocess.PIPE)
        grep = subprocess.run(["grep", "-n", "-i", "-E", "-m", "5", pattern], stdin=restore.stdout,
                              capture_output=True, text=True, errors="replace")
        restore.stdout.close()
        restore.wait()
        problems += [f"forbidden in dump {what}: line {line[:120]}" for line in grep.stdout.splitlines()]
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(WS / "ARGUS-KGQA"))
    ap.add_argument("--experiments", default=str(WS / "experiments"))
    ap.add_argument("--out", default=str(WS / "HeriKGQA"))
    ap.add_argument("--dataset-out", default=str(WS / "HeriKGQA-dataset"))
    ap.add_argument("--dataset-repo", default="anonymous-7989/herikgqa-benchmark")
    ap.add_argument("--space-repo", default="anonymous-7989/HeriKGQA")
    ap.add_argument("--dsn", default="postgresql://argus@localhost:55432/argus_anon")
    args = ap.parse_args()
    src, exp, out, dout = Path(args.src), Path(args.experiments), Path(args.out), Path(args.dataset_out)
    cfg = json.loads((HERE / "site_aliases.json").read_text())
    rs = rules(cfg)

    for d in (out, dout):
        if d.exists():
            if not (d / ".herikgqa-export").exists():
                raise SystemExit(f"{d} exists and was not made by this script; not touching it")
            for child in d.iterdir():
                if child.name != ".git":
                    shutil.rmtree(child) if child.is_dir() else child.unlink()
        d.mkdir(parents=True, exist_ok=True)
        (d / ".herikgqa-export").write_text("made by export_repo.py; re-running it replaces everything but .git\n")

    # code and ontology, rewritten
    for m in SCRIPTS:
        put(out, f"scripts/{m}", rewrite((src / "scripts" / m).read_text(), rs))
    for m in EVALUATION:
        put(out, f"evaluation/{m}", rewrite((exp / m).read_text(), rs))
    for o in ONTOLOGY:
        put(out, f"material/{o}", rewrite((src / "material" / o).read_text(), rs))
    # demo, container, Ontop files: already anonymised in the Space
    put(out, "app/app.py", (SPACE / "app/app.py").read_text())
    put(out, "ontop/mapping.obda", rewrite((src / "obda/argus.obda").read_text(), rs))
    put(out, "ontop/ontop.properties.template", (SPACE / "ontop/ontop.properties.template").read_text())
    (out / "ontop/jdbc").mkdir(parents=True, exist_ok=True)
    shutil.copy(SPACE / "ontop/jdbc/postgresql.jar", out / "ontop/jdbc/postgresql.jar")
    for f in REPO_FILES:
        put(out, f, (HERE / "repo_files" / f).read_text().replace("{{DATASET_REPO}}", args.dataset_repo)
            .replace("{{SPACE_REPO}}", args.space_repo))
    put(dout, "README.md", (HERE / "repo_files/dataset_README.md").read_text().replace("{{DATASET_REPO}}",
                                                                                         args.dataset_repo))
    os.chmod(out / "start.sh", 0o755)
    patch(out, PATCHES)
    patch(out, SINGLE_CONFIG)
    drop_template_mode(out)
    print(f"copied {len(SCRIPTS)} scripts, {len(EVALUATION)} evaluation scripts, {len(ONTOLOGY)} ontology files; "
          f"one configuration")

    # benchmark and node labels from the anonymised database
    env = {**os.environ, "HERIKG_SNAPSHOT_DSN": args.dsn}
    subprocess.run([sys.executable, str(out / "scripts/build_benchmark.py")], check=True, env=env,
                   stdout=subprocess.DEVNULL)
    print(f"node labels: {node_labels(args.dsn, out)} nodes")
    rep = compare_benchmark(src / "material/benchmark_500.json", out / "material/benchmark_500.json", rs)
    print(f"regenerated benchmark: {len(rep['question'])} questions drawn differently")
    changed = align_benchmark(src / "material/benchmark_500.json", out, args.dsn, rs)
    print(f"aligned to the paper's questions: {len(changed)} references recomputed on the anonymised data "
          f"({', '.join(changed[:6])}{' …' if len(changed) > 6 else ''})")
    rep = compare_benchmark(src / "material/benchmark_500.json", out / "material/benchmark_500.json", rs)
    shutil.rmtree(out / "scripts/__pycache__", ignore_errors=True)   # left by align_benchmark's import
    by_template = {}
    for i, t in rep["value"]:
        by_template.setdefault(t, []).append(i)
    print(f"benchmark: {rep['items'][1]} items (original {rep['items'][0]}); missing {rep['missing'] or 0}, "
          f"extra {rep['extra'] or 0}, other template {rep['template'] or 0}, other question {len(rep['question'])}")
    print(f"  reference values that differ from the original (rewritten): {len(rep['value'])}")
    for t, ids in sorted(by_template.items()):
        print(f"    {t:28s} {len(ids):3d}  {', '.join(ids[:8])}{' …' if len(ids) > 8 else ''}")

    # benchmark and dump to the dataset; their checksums to the repository
    sums = []
    for f in BENCHMARK:
        shutil.move(out / "material" / f, dout / f)
        sums.append(f"{hashlib.sha256((dout / f).read_bytes()).hexdigest()}  material/{f}")
    neutral_dump(args.dsn, dout / "snapshot.dump")
    sums.append(f"{hashlib.sha256((dout / 'snapshot.dump').read_bytes()).hexdigest()}  data/snapshot.dump")
    put(out, "data/SHA256SUMS", "\n".join(sums) + "\n")
    print(f"dataset: {', '.join(BENCHMARK)}, snapshot.dump ({(dout / 'snapshot.dump').stat().st_size / 1e6:.0f} MB) "
          f"-> {dout} (for huggingface.co/datasets/{args.dataset_repo})")

    # checks
    problems = scan(out, cfg) + scan(dout, cfg) + scan_dump(dout / "snapshot.dump", cfg)
    for f in sorted(out.rglob("*.py")):
        try:
            compile(f.read_text(), str(f), "exec")
        except SyntaxError as e:
            problems.append(f"compile: {f.relative_to(out)}:{e.lineno}: {e.msg}")
    problems += [f"size: {f.relative_to(out)} {f.stat().st_size / 1e6:.0f} MB" for f in out.rglob("*")
                 if f.is_file() and ".git" not in f.parts and f.stat().st_size > 50e6]
    if problems:
        print("\n".join(problems))
        raise SystemExit(f"{len(problems)} problem(s)")
    print("checks: no forbidden word (code, benchmark, dump content), no secret, one unnamed configuration, "
          "all Python compiles, no data in the code repository")


if __name__ == "__main__":
    main()
