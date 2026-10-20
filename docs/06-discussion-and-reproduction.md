# 6. Discussion and reproduction

This repository has **not trained or run System-1.5**. The steps below are guide proposals for interrogating or reproducing the method, not additional procedures reported by the paper. Read [the training module](03-training-and-objectives.md) and [the unresolved details](05-limitations-and-open-questions.md) first.

## Work through one computational decision

Suppose a router produces 0.7 at an intermediate layer. With a depth threshold of 0.6, the strict `score > threshold` rule takes the shortcut; with threshold 0.8 it continues through the standard path. This example uses invented scores to illustrate [Eq. 3, p. 4](https://arxiv.org/pdf/2505.18962v3#page=4); it is not an observed routing trace.

Now draw the next latent step. DS asks whether to spend more depth at the present step. SS asks whether an already available intermediate state can carry computation into the next step at that layer. Do not draw SS as dropping an unread word from the question, or describe the threshold as a probability that the answer is correct.

## Read a result precisely

**Exercise.** Write one sentence about Table 1's GSM8K result that preserves its scope.

**Suggested answer.** “In v3 Table 1, System-1.5 is reported at 46.66% accuracy versus CoT's 46.94%, using 2 rather than 26 intermediate decoding steps and a 20.27× wall-clock speedup; the table's backbone assignment and timing protocol are not specified.” This sentence keeps the accuracy tradeoff and measurement limitations attached to the speed claim. [Table 1, p. 7](https://arxiv.org/pdf/2505.18962v3#page=7).

**Exercise.** Does a 1.95× per-step FLOPs factor and a 13× step-count factor prove a 25.35× end-to-end speedup?

**Suggested answer.** No. Their product is a simplified derived work estimate. Measured latency also depends on overhead, different step types, question processing, answer generation, execution scheduling, and hardware. The actual table reports 20.27×. A real reproduction should measure both estimates and latency.

## A proposed reproduction plan

| Phase | Concrete work | Evidence to retain |
| --- | --- | --- |
| Resolve the specification | Decide the Eq. 10 target layer with a documented rationale; specify Eq. 5 combination and inference/cache behavior | An implementation decision log distinguishing source text from assumptions |
| Freeze the environment | Pin backbone checkpoint and tokenizer, dataset revision/splits, precision, libraries, hardware, and seeds | Versions, licenses, configuration, and hashes |
| Build data | Reproduce augmented GSM8K and StrategyQA CoT preparation; record atomic decomposition and label generation | Counts, filtering, annotation prompts/models if used, and sampled label audits |
| Establish baselines | Train/evaluate CoT and each relevant latent/depth baseline on the same backbone and data | Comparable accuracy and execution protocol rather than cross-model leaderboard mixtures |
| Learn latent reasoning | Implement teacher/student NLL and answer-position state alignment; test teacher-forced training and free-running inference separately | Loss masks, state indices, and rollout-quality checks |
| Learn shortcuts | Freeze Transformer parameters; train router-adapter parameters with criticality weighting | Trainable-parameter audit, loss values, and routing distributions |
| Measure execution | Sweep threshold and latent budget; log actual layer/adaptor execution, latency, throughput, memory, and FLOPs definition | Per-example outputs and repeated timing samples, including warmup rules |
| Evaluate stability | Use multiple seeds and report dispersion; preserve accuracy/cost tradeoffs | Confidence intervals or suitable uncertainty summaries and error analysis |

The source names the two training stages, datasets, backbone families, and losses; this table adds the operational evidence that a reproducible study would need. It is not a claim that v3 supplies all of it. [§2–3, pp. 3–9](https://arxiv.org/pdf/2505.18962v3#page=3).

## Experiments that would answer open questions

1. **Separate DS from SS.** Compare full-path latent reasoning, DS-only, SS-only, and DS+SS at matched accuracy and matched budgets. This would help isolate each mechanism; Figure 3 does not provide that full decomposition.
2. **Test the criticality proxy.** Compare DAG labels with shuffled labels, uniform weights, and audited dependency labels. Report whether labels predict errors or extra-compute benefit, not merely whether they sound intuitive.
3. **Measure cost at each Figure 4 configuration.** Pair the printed accuracy grid with wall-clock time and executed operations. Plot an empirical accuracy/cost frontier rather than treating axes as already measured costs.
4. **Check teacher-forcing exposure.** Compare free-running hidden-state trajectories with training-conditioned ones, especially over longer reasoning budgets.
5. **Test transfer beyond arithmetic perturbations.** Evaluate new task types with appropriate baselines and an explicit protocol. Do not call the GSM-HARD result evidence for every domain.

These are **guide proposals**. The paper's own ablations examine student choice, joint training, full-parameter shortcut learning, and budget controls. [§3.2, pp. 8–9](https://arxiv.org/pdf/2505.18962v3#page=8).

## Discussion prompts

- When would preserving a human-auditable reasoning artifact be more valuable than lower latency? What evidence would show a generated explanation remains faithful?
- Could an independent graph node still be essential? How would the current labels treat that case?
- What is the distinction between a router taking a shortcut and a model correctly recognizing an easy problem?
- Why is 0.28 percentage points different from a 0.28% relative change? On GSM8K the former is the raw accuracy gap; a relative change requires division by the baseline.
- Why should a claimed near tie include uncertainty? A single aggregate result cannot reveal training variability or which examples changed.

## Reusing these notes responsibly

Use the source's own authors and v3 citation whenever discussing the research. Cite this companion only for its original explanations, transcription, or audit. Keep proposed experiments labeled, keep unreported setup values null, and rerun the [repository validator](../scripts/validate_repository.py) after edits. Publishing a guide does not establish an empirical replication.

[Previous: limitations](05-limitations-and-open-questions.md) · [Reading map](00-reading-map.md)
