#!/usr/bin/env python3
"""Offline integrity checks for the original v3 reading companion, not model tests."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def load_json(path: str):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{path}: {exc}")
        return {}


def anchors(text: str) -> set[str]:
    result: set[str] = set()
    seen: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.replace("`", "").lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug + (f"-{count}" if count else ""))
    result.update(re.findall(r'<a\s+(?:id|name)=[\'"]([^\'"]+)', text))
    return result


required = [
    "README.md", "AGENTS.md", "LLMS.txt", "ATTRIBUTION.md", "CITATION.cff",
    "CONTRIBUTING.md", "LICENSE", "VERIFICATION.md", "agents/README.md", "agents/claim-audit.md",
    "docs/00-reading-map.md", "docs/01-problem-and-context.md", "docs/02-dynamic-shortcuts.md",
    "docs/03-training-and-objectives.md", "docs/04-experiments-and-results.md",
    "docs/05-limitations-and-open-questions.md", "docs/06-discussion-and-reproduction.md", "docs/glossary.md",
    "metadata/paper.json", "metadata/sources.json", "metadata/claims.json",
    "data/reported-results.csv", "data/test-time-scaling.csv", "references/paper.bib",
]
for name in required:
    check((ROOT / name).is_file(), f"Missing {name}")

files = [p for p in ROOT.rglob("*") if p.is_file() and not any(x in {".git", "__pycache__"} for x in p.relative_to(ROOT).parts)]
allowed_extensions = {".md", ".txt", ".json", ".csv", ".py", ".cff", ".bib"}
for path in files:
    rel = path.relative_to(ROOT).as_posix()
    check(path.suffix.lower() != ".pdf", f"Source PDF prohibited: {rel}")
    check(path.name.lower() not in {"paper.txt", "source.txt", "extracted.txt"}, f"Source extraction prohibited: {rel}")
    check("source" not in path.relative_to(ROOT).parts, f"Source directory prohibited: {rel}")
    check(path.suffix.lower() in allowed_extensions or path.name in {"LICENSE", ".gitignore", ".gitattributes"}, f"Unexpected artifact: {rel}")
    try:
        body = path.read_text(encoding="utf-8")
    except UnicodeError:
        errors.append(f"Invalid UTF-8: {rel}")
        continue
    check(not any(ord(c) < 32 and c not in "\n\r\t" for c in body), f"Unexpected control character: {rel}")
    if path.suffix == ".md":
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", body):
            target = target.strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//"):
                if "arxiv.org" in parsed.netloc:
                    check("2505.18962v3" in target, f"Unpinned arXiv link in {rel}: {target}")
                    if parsed.fragment.startswith("page="):
                        check(1 <= int(parsed.fragment[5:]) <= 15, f"Invalid source page in {rel}")
                continue
            local = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            check(local.is_relative_to(ROOT), f"Link escapes repository in {rel}: {target}")
            check(local.exists(), f"Broken local link in {rel}: {target}")
            if parsed.fragment and local.exists() and local.suffix == ".md":
                check(unquote(parsed.fragment) in anchors(local.read_text(encoding="utf-8")), f"Broken anchor in {rel}: {target}")

paper = load_json("metadata/paper.json")
sources = load_json("metadata/sources.json")
ledger = load_json("metadata/claims.json")
expected_authors = ["Xiaoqiang Wang", "Suyuchen Wang", "Yun Zhu", "Bang Liu"]
check(paper.get("authors") == expected_authors, "Author names/order differ from title page")
check(paper.get("arxiv_id") == "2505.18962" and paper.get("version") == "v3", "Wrong source/version")
check(paper.get("version_date") == "2025-05-31", "Wrong v3 date")
check(paper.get("pdf_pages") == 15 and paper.get("appendices") == [], "Incorrect page/appendix scope")
check(paper.get("tables") == 1 and paper.get("figures") == 4, "Incorrect table/figure counts")
check(paper.get("table_1_backbone_mapping") is None, "Do not invent table backbone mapping")
check(paper.get("guide", {}).get("empirical_reproduction") is False, "Guide must not claim replication")
source = next((s for s in sources.get("sources", []) if s.get("id") == "paper-v3"), {})
check(source.get("sha256_of_downloaded_official_pdf") == "df801de60be918210dec85f34866fe135da60ef1deacab2b08276dbbebe1da6a", "Official-PDF provenance digest changed")
check(source.get("acquisition", {}).get("byte_equality_to_attachment_verified") is False, "Attachment byte equality not established")

csv_path = ROOT / "data/reported-results.csv"
rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
methods = {"CoT", "LITE", "LayerSkip", "iCoT", "Coconut", "CODI", "pause token", "System-1.5"}
datasets = {"GSM8K", "GSM-HARD", "StrategyQA"}
check(len(rows) == 24, "Table 1 must contain 24 records")
keyed = {(r["dataset"], r["method"]): r for r in rows}
check(len(keyed) == 24, "Duplicate Table 1 key")
check(set(keyed) == {(d, m) for d in datasets for m in methods}, "Missing Table 1 combination")
for row in rows:
    label = row["dataset"] + "/" + row["method"]
    check(0 <= float(row["accuracy_pct"]) <= 100, f"Invalid accuracy: {label}")
    check(int(row["pre_answer_decoding_steps"]) > 0, f"Invalid step count: {label}")
    check(row["source_table"] == "1" and row["source_pdf_page"] == "7", f"Invalid source location: {label}")
    for field in ("flops_reduction_factor_per_step", "wall_clock_speedup_factor"):
        check(row[field] == "" if row["method"] == "CoT" else float(row[field]) > 0, f"Invalid/missing factor {label}/{field}")

expected_main = {
    "GSM8K": (46.66, 46.94, 2, 26, 1.95, 20.27),
    "GSM-HARD": (38.28, 38.32, 4, 26, 1.76, 12.45),
    "StrategyQA": (48.61, 47.62, 2, 52, 2.12, 55.65),
}
for dataset, values in expected_main.items():
    main, baseline = keyed[(dataset, "System-1.5")], keyed[(dataset, "CoT")]
    actual = (float(main["accuracy_pct"]), float(baseline["accuracy_pct"]), int(main["pre_answer_decoding_steps"]), int(baseline["pre_answer_decoding_steps"]), float(main["flops_reduction_factor_per_step"]), float(main["wall_clock_speedup_factor"]))
    check(actual == values, f"Table 1 headline mismatch: {dataset}")

grid = list(csv.DictReader((ROOT / "data/test-time-scaling.csv").open(encoding="utf-8", newline="")))
grid_keys = {(float(r["lambda_depth"]), int(r["lambda_step"])) for r in grid}
check(len(grid) == 36 and len(grid_keys) == 36, "Figure 4 must contain 36 unique cells")
check(grid_keys == {(d, s) for d in [0.1, 0.2, 0.5, 0.6, 0.8, 1.0] for s in [2, 4, 8, 16, 32, 64]}, "Figure 4 axes incomplete")
for row in grid:
    check(0 <= float(row["accuracy_pct"]) <= 100 and row["source_figure"] == "4" and row["source_pdf_page"] == "8", "Invalid Figure 4 record")
best = max(grid, key=lambda r: float(r["accuracy_pct"]))
check((float(best["lambda_depth"]), int(best["lambda_step"]), float(best["accuracy_pct"])) == (0.8, 64, 49.26), "Figure 4 maximum mismatch")
check(round(100 * (1 - 2 / 26), 2) == 92.31, "Step-reduction arithmetic mismatch")

claims = ledger.get("claims", [])
check(len(claims) == 12 and len({c["id"] for c in claims}) == 12, "Claim ledger count/IDs incorrect")
allowed_classes = set(ledger.get("classification_definitions", {}))
for claim in claims:
    check(claim.get("classification") in allowed_classes, f"Unknown class: {claim.get('id')}")
    check(bool(claim.get("caveats")) and bool(claim.get("source_location")), f"Missing caveat/location: {claim.get('id')}")
    check(all(1 <= p <= 15 for p in claim.get("pdf_pages", [])), f"Invalid claim page: {claim.get('id')}")
    if "data_path" in claim:
        check((ROOT / claim["data_path"]).is_file(), f"Missing claim data: {claim['id']}")
    if claim.get("dataset") in datasets:
        dataset = claim["dataset"]
        values = claim["values"]
        main, baseline = keyed[(dataset, "System-1.5")], keyed[(dataset, "CoT")]
        check(values["accuracy_pct"] == float(main["accuracy_pct"]) and values["baseline_accuracy_pct"] == float(baseline["accuracy_pct"]), f"Claim accuracy mismatch: {claim['id']}")
        check(values["speedup_factor"] == float(main["wall_clock_speedup_factor"]), f"Claim speedup mismatch: {claim['id']}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
bib = (ROOT / "references/paper.bib").read_text(encoding="utf-8")
for author in expected_authors:
    check(author in readme, f"Author missing from README: {author}")
for phrase in ["2505.18962v3", "2025-05-31"]:
    check(phrase in cff, f"Citation metadata missing {phrase}")
check("2505.18962v3" in bib and all(n in bib for n in ["Xiaoqiang", "Suyuchen", "Yun", "Bang"]), "Bibliography credit/version mismatch")
check("92.31" in readme and "46.66" in readme and "47.62" in readme, "README headline values missing")

summary = {"status": "PASS" if not errors else "FAIL", "checks": checks, "files_checked": len(files), "table_1_rows": len(rows), "figure_4_cells": len(grid), "claims": len(claims), "scope": "Documentation and data integrity only; no empirical reproduction", "errors": errors}
print(json.dumps(summary, indent=2))
sys.exit(bool(errors))
