"""
Build the public Hugging Face Space code (../hf-spaces/app) from ARGUS-KGQA.

PRIVATE tool. The runtime modules, ontology and mapping are copied unchanged in
logic; their text goes through one mechanical rewrite so that the public code
names nothing the anonymised data does not:
  - site names and sub-site place names -> the aliases in site_aliases.json
    (the same mapping anonymize_db.py applies to the data, so the rule table
    RULE_SPECS keeps its structure and is simply keyed by site_a … site_e);
  - the project name and domain -> "herikg" / heritage-kg.example.org
    (identifiers, env variables, ontology namespaces, mapping prefixes);
  - the LLM provider's URL -> nothing (it is set as a Space secret).
The whole Space directory is then scanned for forbidden words.

    python build_space.py [--src ~/workspace/ARGUS-KGQA]
"""

import argparse
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPACE = HERE.parent / "hf-spaces"

MODULES = ["pipeline.py", "1_semantic_parser.py", "2_sparql_retriever.py", "3_answer_generator.py",
           "analysis_ek.py", "analysis_geo.py", "analysis_temp.py", "backend.py", "ontology_schema.py", "domain.py"]
ONTOLOGY = ["panoptes3.owl", "panoptes3_extension.owl"]

IDENTITY = [
    (r"https?://chat\.kiconnect\.nrw/api/v1", ""),
    (r"argus-project\.eu", "heritage-kg.example.org"),
    (r"ARGUS", "HERIKG"),
    (r"Argus", "HeriKG"),
    (r"argus", "herikg"),
]
# words that must not appear anywhere in the Space (besides the data checks of anonymize_db.py)
EXTRA_FORBIDDEN = [r"argus", r"kiconnect", r"\bnrw\b", r"fraunhofer", r"athenarc", r"/home/kong", r"ollama\.fit"]


def rules(cfg):
    out = [(re.compile(p, re.I), r) for p, r in cfg["text"]]
    out += [(re.compile(re.escape(real), re.I), s["id"]) for real, s in cfg["sites"].items()]
    out += [(re.compile(p), r) for p, r in IDENTITY]
    return out


def rewrite(text, rs):
    for pat, rep in rs:
        text = pat.sub(rep, text)
    return strip_disabled(text)


def strip_disabled(text):
    """Drop what ARGUS-KGQA keeps only commented out for reference: lines between
    "[disabled-config] begin" and "[disabled-config] end" (inclusive), and any other
    line carrying the marker. The Space has the THOROUGH configuration only."""
    out, skipping = [], False
    for line in text.splitlines(keepends=True):
        if "[disabled-config] begin" in line:
            skipping = True
            continue
        if "[disabled-config] end" in line:
            skipping = False
            continue
        if not skipping and "[disabled-config]" not in line:
            out.append(line)
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(Path.home() / "workspace/ARGUS-KGQA"))
    args = ap.parse_args()
    src = Path(args.src)
    cfg = json.loads((HERE / "site_aliases.json").read_text())
    rs = rules(cfg)

    app = SPACE / "app"
    for sub in ("scripts", "material"):
        shutil.rmtree(app / sub, ignore_errors=True)
        (app / sub).mkdir(parents=True)
    for m in MODULES:
        (app / "scripts" / m).write_text(rewrite((src / "scripts" / m).read_text(), rs))
    for o in ONTOLOGY:
        (app / "material" / o).write_text(rewrite((src / "material" / o).read_text(), rs))
    (SPACE / "ontop").mkdir(exist_ok=True)
    (SPACE / "ontop" / "mapping.obda").write_text(rewrite((src / "obda" / "argus.obda").read_text(), rs))
    (SPACE / "ontop" / "jdbc").mkdir(exist_ok=True)
    shutil.copy(src / "obda" / "jdbc" / "postgresql.jar", SPACE / "ontop" / "jdbc" / "postgresql.jar")
    print(f"copied {len(MODULES)} modules, {len(ONTOLOGY)} ontology files and the mapping")

    forbidden = re.compile("|".join([re.escape(w) for w in cfg["forbidden"]] + EXTRA_FORBIDDEN), re.I)
    leaks = []
    for f in sorted(SPACE.rglob("*")):
        if not f.is_file() or f.suffix in (".dump", ".pyc") or ".git" in f.parts:
            continue
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if forbidden.search(line):
                leaks.append(f"{f.relative_to(SPACE)}:{i}: {line.strip()[:120]}")
    if leaks:
        print("\n".join(leaks))
        raise SystemExit(f"{len(leaks)} forbidden occurrence(s) in the Space")
    print("forbidden-word scan: clean")

    # only THOROUGH and its two ablations exist in the Space
    stale = re.compile(r"\bFAST\b|\bBALANCED\b|[\"']fast[\"']|[\"']balanced[\"']")
    hits = [f"{f.relative_to(SPACE)}:{i}: {line.strip()[:100]}"
            for f in sorted((SPACE / "app").rglob("*.py")) for i, line in enumerate(f.read_text().splitlines(), 1)
            if stale.search(line)]
    if hits:
        print("\n".join(hits))
        raise SystemExit(f"{len(hits)} reference(s) to removed configurations in the Space")
    print("configuration scan: THOROUGH only")


if __name__ == "__main__":
    main()
