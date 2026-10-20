# 5. Limitations and open questions

This module separates contradictions inside the source from limitations inferred by the guide. All observations are scoped to [arXiv:2505.18962v3](https://arxiv.org/pdf/2505.18962v3), not a later revision or a separately released implementation.

## Conflicts that should travel with a citation

| Issue | What v3 says | How this guide handles it |
| --- | --- | --- |
| Main accuracy values | Table 1, p. 7: CoT/System-1.5 are 46.94/46.66 on GSM8K and 38.32/38.28 on GSM-HARD. §3.1, p. 8 assigns 46.94 and 38.32 to System-1.5 and 46.67 and 38.28 to CoT. | Numerical datasets follow the displayed table. Prose values remain recorded here; no hidden correction to the source. |
| StrategyQA baseline | Table 1 gives CoT 47.62%; §3.1 prose gives 47.36%. Both give System-1.5 48.61%. | Use 47.62% for table-based deltas and flag the alternative. |
| Token/step reduction | Abstract, p. 1 and §3.1, p. 7 give 92.31% on GSM8K; introduction, p. 3 says 91.0% on average. | `1 − 2/26` yields 92.31% for the displayed GSM8K step counts. The 91.0% statement is unresolved. |
| Shortcut target layer | Text introducing Eq. 10, p. 6 describes final-layer student states; the equation displays a student state indexed by `l,t`, not `L,t`. | Describe both. Do not claim that a faithful implementation can be chosen from this text without interpretation. |

Sources: [pp. 1–3](https://arxiv.org/pdf/2505.18962v3#page=1), [Eq. 10, p. 6](https://arxiv.org/pdf/2505.18962v3#page=6), [Table 1, p. 7](https://arxiv.org/pdf/2505.18962v3#page=7), [§3.1, p. 8](https://arxiv.org/pdf/2505.18962v3#page=8).

Table 1's point estimates put System-1.5 above all six efficient baselines on every dataset. Its accuracy advantages over pause token are 0.34, 0.11, and 0.47 percentage points on GSM8K, GSM-HARD, and StrategyQA respectively. Without dispersion or repeated-seed information, these numerical gaps do not establish a statistically significant advantage.

## What the experimental setup leaves unspecified

**Guide audit of the full PDF.** §3 names GPT-2 124M and LLaMA 3.2 1B as backbones, but Table 1 provides no explicit per-row backbone assignment. The paper reports wall-clock ratios without identifying hardware, batch size, timing boundaries, software/kernel versions, or measurement variability. There is no absolute latency table. Eqs. 9 and 13 introduce weights `alpha` and `beta`, but the PDF does not provide a complete training recipe with their selected values, optimizer and learning-rate schedule, seeds, all epoch counts, and architecture sizes for the adapters. The Coconut variant's six initial epochs and three per later stage are a particular ablation detail, not a complete recipe for the proposed method. [§3–3.2, pp. 7–9](https://arxiv.org/pdf/2505.18962v3#page=7).

These are reading findings, not claims that such information could not exist elsewhere. This guide intentionally did not use later versions, outside code, or the separate blog article to fill v3's gaps.

## Limits on causal conclusions

**Paper report.** Figure 3 compares students and training alternatives. The authors attribute the lower performance of joint/full-parameter training to conflicts between learning latent reasoning and learning routing. They suggest the hard curriculum used by Coconut limits the flexibility required by shortcuts. [§3.2, pp. 8–9](https://arxiv.org/pdf/2505.18962v3#page=8).

**Guide interpretation.** Those are plausible authors' explanations, not directly measured mechanisms. Figure 3 has no printed exact bar values, error bars, or detailed diagnostic measurements. It does not present a clean DS-only versus SS-only factorial ablation. Therefore it cannot by itself identify the marginal causal contribution of each shortcut, establish an optimization-conflict mechanism, or show that all curriculum schemes fail.

The criticality labels are another proxy. Independent DAG nodes are labeled non-critical; derived nodes requiring integration are labeled critical. This graph distinction need not measure task difficulty, error sensitivity, or causal necessity. The paper does not report labeler agreement, decomposition error rates, or a calibration study of router scores. Treat “critical” as an operational training category, not a theorem about the reasoning process. [§2.2, pp. 5–6](https://arxiv.org/pdf/2505.18962v3#page=5).

## Limits on the compute story

- **Intermediate steps are not all generated tokens.** The Table 1 count excludes the final-answer generation phase by its caption. Latent and text steps also differ in representation and execution.
- **Per-step FLOPs factors are not end-to-end speedups.** Adapters, routing, caching, batching, and answer generation can change total costs. Do not multiply column entries and relabel the result a measured latency.
- **Figure 4 shows accuracy, not cost measurements.** Its two axes are threshold and step budget. A caption-described frontier over configurations does not give elapsed time or FLOPs per cell. Dataset identification as GSM8K is inferred from the matching 46.94% baseline, rather than stated in the caption.
- **More compute is not strictly monotonic in every cell.** At step budget 64, depth threshold 0.8 gives 49.26% and 1.0 gives 49.25%. A general trend is different from a guarantee.

See [Table 1 and Figure 4](https://arxiv.org/pdf/2505.18962v3#page=7), [result definitions](04-experiments-and-results.md), and the [scaling data](../data/test-time-scaling.csv).

## Generalization boundaries

The evaluated tasks are grade-school mathematics and yes/no commonsense reasoning. GSM-HARD provides a mathematics transfer test; it does not stand in for long-horizon agents, code generation, safety-critical decisions, long context, or broad out-of-distribution robustness. References to capable foundation agents or future deployment in the introduction/conclusion are context and aspiration, not experiments on those capabilities. [§3, p. 7; §5, p. 10](https://arxiv.org/pdf/2505.18962v3#page=10).

**Guide question.** How would an operator diagnose an incorrect latent answer without a faithful text trace? The source does not solve interpretability, auditing, or fallback policy for deployment. A generated explanation after the answer would need its own faithfulness evaluation.

## Questions and short answers

- **Which number should I cite when source table and prose conflict?** State the location and use the table-specific value for table-based comparisons; disclose the conflict.
- **Do missing uncertainty estimates invalidate all observations?** No. They limit the strength of claims about small differences and stability.
- **Does the guide establish the speedup is reproducible on my GPU?** No. It validates documentation and transcriptions, not empirical performance.
- **Can later code settle an ambiguity for this guide?** It could be added as a separately versioned source with explicit provenance. It must not silently redefine what v3 says.

[Previous: results](04-experiments-and-results.md) · [Next: discussion and reproduction](06-discussion-and-reproduction.md)
