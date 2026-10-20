# Read the full v3 paper alongside this guide

This map covers all 15 pages of [arXiv:2505.18962v3](https://arxiv.org/pdf/2505.18962v3), dated 31 May 2025. PDF and printed page numbers coincide. It contains five numbered sections, one table, four figures, and references; **no appendices or supplementary experimental section appear in this PDF**.

| Paper location | What to extract | Companion |
| --- | --- | --- |
| Title/abstract, [p. 1](https://arxiv.org/pdf/2505.18962v3#page=1) | Exact authors/version; headline efficiency claim | [README](../README.md), [provenance](../metadata/sources.json) |
| §1, [pp. 1–3](https://arxiv.org/pdf/2505.18962v3#page=1) | Motivation: text verbosity and uniform allocation of latent computation | [01](01-problem-and-context.md) |
| Figure 1, [p. 2](https://arxiv.org/pdf/2505.18962v3#page=2) | Authors' conceptual comparison of CoT, early exit, compressed/extended latent reasoning | [01](01-problem-and-context.md) |
| §2 overview, [p. 3](https://arxiv.org/pdf/2505.18962v3#page=3) | Two computational axes and two training stages | [02](02-dynamic-shortcuts.md), [03](03-training-and-objectives.md) |
| Figure 2, [p. 4](https://arxiv.org/pdf/2505.18962v3#page=4) | Training pipeline; diagram uses two layers for illustration | [03](03-training-and-objectives.md) |
| §2.1, Eqs. 1–5, [pp. 4–5](https://arxiv.org/pdf/2505.18962v3#page=4) | Soft training mixture versus thresholded inference; state reuse | [02](02-dynamic-shortcuts.md) |
| §2.2, Eqs. 6–13, [pp. 5–7](https://arxiv.org/pdf/2505.18962v3#page=5) | Teacher/student inputs and losses; criticality weighting and frozen backbone | [03](03-training-and-objectives.md) |
| Table 1 and §3 setup, [p. 7](https://arxiv.org/pdf/2505.18962v3#page=7) | Three datasets, eight methods, four metrics | [04](04-experiments-and-results.md), [CSV](../data/reported-results.csv) |
| §3.1, [pp. 7–8](https://arxiv.org/pdf/2505.18962v3#page=7) | Main results; compare prose against the table rather than silently merging | [04](04-experiments-and-results.md), [05](05-limitations-and-open-questions.md) |
| Figure 3 and §3.2, [pp. 8–9](https://arxiv.org/pdf/2505.18962v3#page=8) | Student initialization and optimization ablations | [04](04-experiments-and-results.md) |
| Figure 4 and §3.2, [pp. 8–9](https://arxiv.org/pdf/2505.18962v3#page=8) | Depth threshold × latent-step budget accuracy grid | [04](04-experiments-and-results.md), [CSV](../data/test-time-scaling.csv) |
| §4, [pp. 9–10](https://arxiv.org/pdf/2505.18962v3#page=9) | Related-work taxonomy, not an evaluation of every cited method | [01](01-problem-and-context.md) |
| §5, [p. 10](https://arxiv.org/pdf/2505.18962v3#page=10) | Conclusion and deployment aspirations | [05](05-limitations-and-open-questions.md) |
| References, [pp. 10–15](https://arxiv.org/pdf/2505.18962v3#page=10) | Attribution and routes for further reading | [bibliography](../references/paper.bib), [attribution](../ATTRIBUTION.md) |

## A three-pass reading plan

**First pass — mechanism.** Sketch a grid with layer depth on one axis and latent steps on the other. Point to the computation avoided by DS and SS. Then explain why a hidden-state model still needs training rather than simply removing text from a prompt.

**Second pass — training.** Trace the question, reasoning, and answer segments through Eqs. 6–9. Observe that Eq. 6 aligns answer-position states, even though the student is conditioned on teacher reasoning states. Then inspect the printed Eq. 10 rather than assuming its prose description is unambiguous.

**Third pass — evidence.** Read Table 1 before the prose summary; track accuracy, intermediate steps, per-step FLOPs factors, and wall-clock time separately. Read Figure 4 as a grid of accuracy observations, not a measured cost frontier. Finish with the [limitations](05-limitations-and-open-questions.md).

## Check your understanding

- **Where is the appendix that specifies the hardware?** There is none in v3. Missing details must remain missing.
- **Does Figure 2 depict the experimental architecture size?** No. Its caption says the two-layer drawing is illustrative.
- **Does the references section demonstrate every method mentioned?** No. Only the methods and results in the experimental section are evaluated here.

[Next: problem and context](01-problem-and-context.md)
