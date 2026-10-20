# Verification record

## What was checked

- Full 15-page v3 text read, including references; selected visual inspection verified title/authors/version, key equations, Table 1, and Figures 3–4. No appendices exist in this version.
- All 24 Table 1 method/dataset records and all 36 printed Figure 4 cells transcribed and cross-checked. Figure 3 bars were not assigned invented exact values.
- Source discrepancies retained: Table 1 versus §3.1, abstract versus introduction reduction, and Eq. 10 target-layer wording.
- Original companion modules distinguish reports, authors' explanations, guide interpretations, and proposed experiments.
- `python scripts/validate_repository.py` checks relative links/anchors, JSON, metadata/citations, CSV structure and expected values, claim/result agreement, and prohibited source artifacts. The test is dependency-free and offline.

## Publication checks

Publication verification is performed against the public GitHub repository: visibility and description, anonymous repository and raw-file access, recursive file listing, remote commit identity, and byte-for-byte comparison of published files with the validated local tree. The exact published verification outcome is returned in the task completion report; this file intentionally makes no advance success claim.

The requested `harness2-guide` reference returned 404. A nearby available companion, `harness-learning-guide`, was inspected for documentation structure only. Repository inventory and name checks found no existing matching System-1.5 companion before creation.

## What these checks do not establish

No models were trained, benchmarks rerun, latency measured, or empirical findings independently replicated. Source gaps remain: backbone mapping per table row, hardware/timing protocol, uncertainty, complete training hyperparameters, and Eq. 10 ambiguity. See [limitations](docs/05-limitations-and-open-questions.md), [provenance](metadata/sources.json), and [attribution](ATTRIBUTION.md).
