# Claim audit procedure

For any answer involving evidence:

1. Identify the exact claim and find its entry in [metadata/claims.json](../metadata/claims.json).
2. Check whether it is a paper report, authors' explanation, guide calculation, or guide interpretation.
3. Open the specified v3 PDF page. For numerical claims, compare the relevant row in [Table 1 data](../data/reported-results.csv) or [Figure 4 data](../data/test-time-scaling.csv).
4. Preserve units and denominator. Speedup is relative to CoT; FLOPs is per step; step counts precede answer generation.
5. Read the caveat and source-conflict fields. A source disagreement is part of the answer, not a defect to hide.
6. Say what was validated. A transcription or arithmetic check is different from retraining, rerunning evaluation, or measuring latency.

## Examples

- **Unsafe inference:** 92.31% fewer total operations. **Supported:** 92.31% fewer displayed intermediate steps on GSM8K, calculated from 26 and 2; the paper calls it intermediate-token reduction.
- **Unsafe inference:** the method is at least 20× faster on every benchmark. **Supported:** Table 1 reports 20.27×, 12.45×, and 55.65× for GSM8K, GSM-HARD, and StrategyQA respectively.
- **Unsafe inference:** DAG criticality proves which reasoning is dispensable. **Supported:** the labels are a training proxy distinguishing independent and derived subquestions.
- **Unsafe inference:** the source provides an appendix with all hyperparameters. **Supported:** v3 has no appendix; a full recipe is absent from the permitted source.

[Agent instructions](../AGENTS.md) · [Limitations](../docs/05-limitations-and-open-questions.md)
