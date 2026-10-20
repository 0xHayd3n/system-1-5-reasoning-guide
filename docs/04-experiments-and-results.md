# 4. Experiments: what the numbers establish

The strongest empirical claim in v3 is a favorable accuracy–speed tradeoff on three reported reasoning datasets. Table 1 reports System-1.5 close to the CoT baseline on two mathematical datasets, slightly higher on StrategyQA, and faster in all three comparisons. These are paper-reported measurements. This guide has checked the transcription and arithmetic; it has not trained the models or reproduced the timings.

**Source map:** [§3 and Table 1, PDF p. 7](https://arxiv.org/pdf/2505.18962v3#page=7), [§3.1–3.2 and Figures 3–4, p. 8](https://arxiv.org/pdf/2505.18962v3#page=8), [§3.2 discussion, p. 9](https://arxiv.org/pdf/2505.18962v3#page=9). This 15-page v3 has one table and four figures; it has no appendix or additional results table.

## Read the evaluation design first

The authors train mathematical reasoning on an augmented GSM8K dataset. GSM8K supplies the in-domain evaluation, and GSM-HARD supplies an out-of-domain mathematical test. For commonsense reasoning, the authors use StrategyQA and merge annotated facts and decomposed subquestions into a training CoT. They describe training on the official training splits and evaluating on the respective test sets. Both training datasets receive criticality annotations through atomic thought decomposition. [§3, p. 7](https://arxiv.org/pdf/2505.18962v3#page=7)

The comparison includes CoT fine-tuning and six efficient alternatives:

| Approach in the paper | Listed baselines | What the comparison probes |
| --- | --- | --- |
| Conditional computation in language space | LITE, LayerSkip | Whether reducing model depth alone gives the same tradeoff |
| Compressed latent reasoning | iCoT, Coconut, CODI | Whether a short latent trajectory preserves accuracy without dynamic shortcuts |
| Extended latent reasoning | pause token | Whether spending additional latent computation improves accuracy at a latency cost |

The authors say they implement System-1.5 with GPT-2 124M and LLaMA 3.2 1B because the baseline implementations use different model families. **Table 1 does not label which backbone produced each row or supply separate tables for the two backbones.** The stated fairness motivation is therefore clearer than the row-level experimental specification. Do not assume every number came from a single backbone or that the table fully demonstrates a matched-backbone comparison. [§3, p. 7](https://arxiv.org/pdf/2505.18962v3#page=7)

## Keep the four metrics separate

1. **Accuracy** is a percentage of answers judged correct under the authors’ evaluation.
2. **Pre-answer decoding steps** count the steps before the final answer is generated. For language CoT this covers explicit intermediate generation; for latent methods it covers latent computation steps. This is not a count of all final-output tokens.
3. **FLOPs reduction per step** is displayed as a multiplicative factor relative to CoT. The caption calls it a reduction rate, but a cell such as 1.95× is a factor, not 1.95% savings or a total-run measurement.
4. **Speedup** is the reported wall-clock inference speedup relative to CoT. A value below 1 means slower inference in that comparison.

Reducing the number of steps and reducing work per step address different costs. Their arithmetic product need not equal the measured latency ratio, because latency also depends on execution overhead and the measurement protocol. For example, the GSM8K counts and per-step factor give `(26 / 2) × 1.95 = 25.35`, while Table 1 reports a wall-clock speedup of 20.27×. Treat 25.35 as a simple calculation, not an alternative measured speedup. The PDF does not supply a timing breakdown that explains the gap. [Table 1, p. 7](https://arxiv.org/pdf/2505.18962v3#page=7)

## Main results, using Table 1 consistently

| Dataset | CoT accuracy | System-1.5 accuracy | Difference, percentage points | System-1.5 steps | Reported speedup |
| --- | ---: | ---: | ---: | ---: | ---: |
| GSM8K | 46.94% | 46.66% | −0.28 | 2 versus 26 | 20.27× |
| GSM-HARD | 38.32% | 38.28% | −0.04 | 4 versus 26 | 12.45× |
| StrategyQA | 47.62% | 48.61% | +0.99 | 2 versus 52 | 55.65× |

The accuracies, steps, and speedups are reported values; the differences are guide calculations. The full 24 method–dataset rows are preserved in [reported-results.csv](../data/reported-results.csv). Its blank CoT factors represent the source table’s dashes, not zero.

System-1.5 has higher reported accuracy and speedup than each of the six efficient baselines on all three datasets. Relative to ordinary CoT, the mathematical accuracies decrease slightly and the StrategyQA accuracy increases. There are no confidence intervals or repeated-run statistics in v3, so these point differences do not establish statistical equivalence or significant superiority. “Comparable” is a qualitative description of the paper’s reported point estimates. [Table 1, p. 7](https://arxiv.org/pdf/2505.18962v3#page=7)

The frequently repeated “over 20×” claim needs a dataset attached: GSM8K reports 20.27× and StrategyQA reports 55.65×, but GSM-HARD reports 12.45×. The table supports a benchmark-dependent speedup, not a universal minimum.

### What does the token-reduction headline mean?

From the table’s pre-answer step counts:

- GSM8K: `1 − 2/26 = 92.31%` fewer pre-answer steps.
- GSM-HARD: `1 − 4/26 = 84.62%` fewer pre-answer steps.
- StrategyQA: `1 − 2/52 = 96.15%` fewer pre-answer steps.

These are derived reductions in the reported step count. The paper describes the GSM8K and StrategyQA values as intermediate-token reductions. The table does not report full generated-sequence token counts, final-answer length, or the number of words represented by a latent state. A latent step still performs computation even when no intermediate text is decoded. [§3.1, pp. 7–8](https://arxiv.org/pdf/2505.18962v3#page=7)

## The ablations: useful direction, limited precision

Figure 3 compares shortcut learning starting from Coconut, CODI, and the authors’ language-to-latent student. It also tests joint training of alignment and shortcuts, and updating the full backbone during shortcut learning. The figure uses lighter bars for the latent students and solid bars for the resulting System-1.5 models. It does **not** print numerical bar labels, so this guide does not estimate exact ablation values. [Figure 3 and §3.2, p. 8](https://arxiv.org/pdf/2505.18962v3#page=8)

The Coconut-based shortcut model loses substantial accuracy compared with its student. The CODI-based and authors’ alignment-based shortcut models are stronger in this chart. Joint learning and full-parameter shortcut learning both trail the authors’ staged method, with joint learning showing the larger degradation. This supports the practical value of separating latent alignment from router training in these experiments.

The authors propose that optimization conflicts between reasoning parameters and routing parameters explain the joint-learning drop. That explanation is a hypothesis about the mechanism; Figure 3 directly measures the final performance difference, not the proposed conflict itself. The specified Coconut comparator schedule is six epochs initially and three at each later curriculum stage. A complete training schedule for the authors’ method is absent from v3. [§3.2, pp. 8–9](https://arxiv.org/pdf/2505.18962v3#page=8)

## Test-time scaling: two controls, no latency grid

Figure 4 varies the depth exit threshold `lambda_depth` across `{0.1, 0.2, 0.5, 0.6, 0.8, 1.0}` and the latent step constant `lambda_step` across `{2, 4, 8, 16, 32, 64}`. Raising the depth threshold makes early exit harder; a threshold of 1 forces full depth under the strict `router > threshold` decision. Raising the step constant allows more latent reasoning steps. [Eq. 3, p. 4](https://arxiv.org/pdf/2505.18962v3#page=4); [§3.2, p. 9](https://arxiv.org/pdf/2505.18962v3#page=9)

The 36 printed accuracy cells are in [test-time-scaling.csv](../data/test-time-scaling.csv). Its dataset is intentionally not a column: the caption does not explicitly name one. Its 46.94% CoT reference matches GSM8K in Table 1, so reading it as GSM8K is a contextual inference.

The best printed cell is 49.26% at depth 0.8 and 64 steps. Increasing depth to 1 at the same step budget gives 49.25%, so the grid is not strictly monotonic everywhere. The 46.66% cell at depth 0.6 and two steps matches the System-1.5 GSM8K value in Table 1, but the PDF does not explicitly state that Table 1 used that configuration.

The red boundary marks configurations exceeding the 46.94% baseline, and the caption calls it a Pareto boundary. The figure provides no latency or FLOPs measurement for each configuration. It supports the claim that these two inference controls change accuracy; it does not by itself establish a measured hardware latency–accuracy frontier. [Figure 4, p. 8](https://arxiv.org/pdf/2505.18962v3#page=8)

## Source inconsistencies to keep visible

This module and the CSV use Table 1 for reported numerical results. That is a transparent editorial choice, not a correction verified by rerunning the experiment.

| Location | Conflict in v3 | How to read this guide |
| --- | --- | --- |
| §3.1, p. 8 | Prose attributes 46.94%/38.32% to System-1.5 and 46.67%/38.28% to CoT; Table 1 assigns 46.66%/38.28% to System-1.5 and 46.94%/38.32% to CoT | Use the table and flag the reversed assignments and 46.67/46.66 mismatch |
| §3.1, p. 8 | CoT StrategyQA accuracy is 47.36% in prose and 47.62% in Table 1 | Use 47.62% for table-based comparisons |
| Abstract, p. 1; introduction, p. 3 | Intermediate-token reduction is 92.31% “on average” in the abstract and 91.0% “on average” in the introduction | Preserve both as source claims; the averaging behind 91.0% is unspecified; 92.31% matches the GSM8K step-count calculation |

For method-level interpretation, also inspect Equation 10: its surrounding prose describes a final-layer student target, while the displayed target carries the layer index `l`. This affects how confidently one can implement the distillation loss directly from the text. [§2.2, p. 6](https://arxiv.org/pdf/2505.18962v3#page=6)

## What a reproduction would still need

The PDF does not supply hardware, timing batch size, warm-up protocol, optimizer and learning rate, random seeds, run count, uncertainty estimates, a complete training schedule, a FLOPs accounting formula, or a per-row backbone mapping. It also supplies no code or weights URL. These are limitations of the permitted source, not proof that such materials cannot exist elsewhere.

A careful reproduction would first resolve the backbone mapping and source contradictions, then implement matched baselines, specify timing conditions, and measure accuracy and latency across the same inference budgets. Without that work, the practical inference is that adaptive latent computation looks promising on these reported tasks; the magnitude of a production speedup remains an open question.

## Questions to test your reading

1. If a method generates two latent steps instead of 26 text steps, why does that not automatically imply 13× lower latency?
2. Which Table 1 comparisons are against CoT, and which are against other compressed latent methods? Does System-1.5 lead in accuracy in both cases?
3. What would you need to know before treating a 0.28-point accuracy decrease as negligible?
4. Why is a high-accuracy Figure 4 cell insufficient to claim a favorable latency tradeoff?
5. If implementing Equation 10, what evidence would resolve the disagreement between the prose’s final-layer target and the equation’s layer index?

**Suggested answers:** The model still incurs per-step computation and execution overhead; mathematical CoT accuracy remains slightly higher while all listed efficient baselines are lower; repeated-run uncertainty and application tolerance are needed; the grid lacks per-cell cost measurements; authoritative clarification or an inspected implementation would be needed for the loss target.
