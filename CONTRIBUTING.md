# Contributing

This companion stays pinned to arXiv:2505.18962v3. Improve explanations with original wording and exact source locations. Preserve full author credit.

For each change:

1. Classify added material as a paper report, authors' explanation, guide calculation, interpretation, or proposal.
2. Keep version, dataset, baseline, metric, and missing details visible. Add or update the [claim ledger](metadata/claims.json) when changing evidence claims.
3. If changing numerical data, inspect the printed table/grid and retain units and source page. Do not replace source dashes with zero or invent exact Figure 3 bar values.
4. Do not silently resolve the Table 1/prose or Eq. 10 conflicts. Document any independent clarification as a new source, with scope separated from v3.
5. Run `python scripts/validate_repository.py` and review the rendered Markdown. Changes to external URLs need live link checks.

Do not commit the PDF, extracted paper text, copied figures, private task information, tokens, or unrelated files. Do not describe documentation checks as empirical replication. See [AGENTS.md](AGENTS.md) for agent-specific instructions and [ATTRIBUTION.md](ATTRIBUTION.md) for rights boundaries.
