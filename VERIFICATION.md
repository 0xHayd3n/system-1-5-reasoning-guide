# Verification record

## What was checked

- Full 15-page v3 text read, including references; selected visual inspection verified title/authors/version, key equations, Table 1, and Figures 3–4. No appendices exist in this version.
- All 24 Table 1 method/dataset records and all 36 printed Figure 4 cells transcribed and cross-checked. Figure 3 bars were not assigned invented exact values.
- Source discrepancies retained: Table 1 versus §3.1, abstract versus introduction reduction, and Eq. 10 target-layer wording.
- Original companion modules distinguish reports, authors' explanations, guide interpretations, and proposed experiments.
- `python scripts/validate_repository.py` passed **760 checks across 27 files**, including relative links/anchors, JSON, metadata/citations, CSV structure and expected values, claim/result agreement, and prohibited source artifacts. The test is dependency-free and offline. CITATION.cff was also parsed as YAML, confirming four research authors.

## Publication checks

On **20 October 2026**, anonymous HTTP checks confirmed the [published repository](https://github.com/0xHayd3n/system-1-5-reasoning-guide) is public, has the intended description, and serves its files without authentication. At initial publication commit `9820447f45cd3adba96519442e74b362b527fcd4`, all **27 remote file paths and file contents matched** the validated local Git tree byte for byte. The v3 abstract/PDF, maintainer profile, companion repository, and available structural reference all returned HTTP 200: **five distinct external URL targets**. PDF page anchors were checked locally against the 15-page scope.

This verification note is a subsequent documentation update. The final publication audit repeats file/commit checks after it is pushed; the task completion report identifies the final audited commit. No source PDF or full paper extraction is in the published tree.

The requested `harness2-guide` reference returned 404. A nearby available companion, `harness-learning-guide`, was inspected for documentation structure only. Repository inventory and name checks found no existing matching System-1.5 companion before creation.

## What these checks do not establish

No models were trained, benchmarks rerun, latency measured, or empirical findings independently replicated. Source gaps remain: backbone mapping per table row, hardware/timing protocol, uncertainty, complete training hyperparameters, and Eq. 10 ambiguity. See [limitations](docs/05-limitations-and-open-questions.md), [provenance](metadata/sources.json), and [attribution](ATTRIBUTION.md).
