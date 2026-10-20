# 3. Training: learn latent reasoning, then learn shortcuts

[Back to the guide](../README.md) · [Previous: dynamic shortcuts](02-dynamic-shortcuts.md)

**Reading target:** distinguish the two optimization stages, identify exactly where the displayed losses are applied, and separate the intended routing behavior from what the paper demonstrates. Primary evidence: [Section 2.2, pp. 5–7, Equations 6–13](https://arxiv.org/pdf/2505.18962v3#page=5). Figure 2 on [p. 4](https://arxiv.org/pdf/2505.18962v3#page=4) is a schematic, simplified to two layers.

## Three model roles, two stages

| Role | Purpose | Training relationship |
| --- | --- | --- |
| System-2 teacher | Produce ordinary language reasoning and an answer | Supplies detached hidden-state features for the latent student |
| System-2 student | Learn a full-depth latent reasoning process | Learns in stage 1 and initializes the stage-2 model |
| System-1.5 model | Learn shortcut routes through that latent process | Inherits the student's Transformer; stage 2 trains router-adapter parameters while freezing the underlying Transformer |

Stage 1 addresses how a model trained to predict words can use continuous states for intermediate reasoning. Stage 2 addresses how to shorten the computational route through that learned process. The paper's two-stage design keeps those tasks separate. It does not merely add an inference threshold to an otherwise unchanged pretrained model. [Section 2.2, p. 5](https://arxiv.org/pdf/2505.18962v3#page=5); [Equation 13 and surrounding text, p. 7](https://arxiv.org/pdf/2505.18962v3#page=7)

## Stage 1: language-to-latent alignment

The training sequence has a question `Q`, intermediate language reasoning `R`, and answer `A`, with lengths `T_Q`, `T_R`, and `T_A`. The teacher is supervised to predict reasoning tokens and answer tokens. The student receives the question together with extracted teacher hidden states representing the reasoning trajectory, and its language-model loss supervises final-answer tokens. The hidden-state inputs provide teacher forcing: training can use a supplied trajectory rather than generating each latent state through a free-running rollout. [Equations 7–8, p. 6](https://arxiv.org/pdf/2505.18962v3#page=6)

The distinction between **inputs** and **alignment targets** is easy to miss. The student consumes teacher reasoning states, but the displayed consistency loss in Equation 6 compares teacher and student **last-layer states at answer positions**. Its sum starts at `T_Q + T_R + 1` and ends at `T_Q + T_R + T_A`, and it is divided by `T_A`. It is therefore inaccurate to paraphrase this equation as an MSE loss over every intermediate reasoning position. [Equation 6, p. 6](https://arxiv.org/pdf/2505.18962v3#page=6)

Equation 9 combines three objectives: the teacher's language-model loss, the student's answer language-model loss, and the consistency term scaled by `alpha`. Stop-gradient detaches the teacher feature target in the consistency term. That detachment does not mean Equation 9 contains no teacher training objective: the teacher's own language-model loss remains explicitly present. [Equations 6–9, p. 6](https://arxiv.org/pdf/2505.18962v3#page=6)

**Guide interpretation:** hidden-state distillation is being used as a bridge between a language trajectory and a latent trajectory. Answer-position alignment supplies a representation-level constraint in addition to answer-token prediction. This does not establish that the latent states contain a faithful readable explanation, or that teacher-forced success automatically predicts free-running stability.

## Stage 2: criticality-guided shortcut learning

The System-1.5 model inherits the trained student's underlying Transformer parameters. Those parameters are frozen while the new router-adapter modules are optimized. The stage-2 objective combines an early-exit consistency loss with a final-answer language-model loss, with coefficient `beta` on the early-exit term. Equation 12 conditions answer prediction on student hidden states, again using teacher forcing. [Section 2.2, pp. 5–7, Equations 10–13](https://arxiv.org/pdf/2505.18962v3#page=6)

Criticality labels come from decomposing a language reasoning chain into a directed acyclic graph of subquestions. The paper labels independent nodes as non-critical and nodes that integrate other results as critical. These labels are training supervision; inference uses learned routers rather than consulting an oracle that knows which deductions are essential. [Section 2.2, p. 5](https://arxiv.org/pdf/2505.18962v3#page=5)

**Original illustrative example:** two independent subquestions might calculate the costs of two shopping items, and a later node might combine those costs with a discount. Under the paper's labeling rule, the combining node is critical. This example illustrates the rule; it does not show that calculating either item is intrinsically easy. Dependency structure and computational difficulty are different concepts.

The early-exit loss sums weighted state discrepancies across layers and intermediate reasoning positions. Equation 11 uses a layer-dependent cumulative fraction and its complement to produce different weights for the two label classes. The authors' stated goal is to favor earlier exits for non-critical steps and later exits for critical steps. That is an optimization intention, not a proof that every learned route has the intended criticality or that independent subquestions are safe to skip. [Equations 10–11, p. 6](https://arxiv.org/pdf/2505.18962v3#page=6)

## An unresolved target-layer discrepancy

The prose immediately before Equation 10 describes aligning shortcut states to the **final-layer** states of the System-2 student. The displayed equation instead writes the detached student target with layer index `l`: `h_student[l,t]`, not `h_student[L,t]`. Visual inspection of the v3 PDF confirms this difference; it is not introduced by text extraction. This guide preserves the discrepancy rather than selecting an intended correction. An implementation would need to resolve it using author clarification or independently inspected implementation evidence, which is outside this PDF-only guide. [Equation 10 and preceding paragraph, p. 6](https://arxiv.org/pdf/2505.18962v3#page=6)

## Why separate the stages?

The authors compare their approach with replacing the latent student by Coconut or CODI, jointly learning latent alignment and shortcuts, and updating all model parameters during shortcut learning. They report that the joint and full-parameter alternatives perform worse, and propose conflicting optimization demands as an explanation. Figure 3 is empirical support for the chosen training arrangement in the reported setting; the explanation about optimization conflict is the authors' interpretation, not a separately demonstrated causal mechanism. [Figure 3 and Section 3.2, pp. 8–9](https://arxiv.org/pdf/2505.18962v3#page=8)

The Coconut-style ablation uses six epochs in its initial curriculum stage and three in subsequent stages. These numbers describe that comparison's schedule. They should not be promoted into a complete training recipe for the proposed method. The PDF does not provide a complete specification of optimization hyperparameters, annotation construction, serving behavior, or hardware needed to reproduce the headline speedups. [Section 3.2, p. 8](https://arxiv.org/pdf/2505.18962v3#page=8)

## Check your understanding

1. **What is frozen in stage 2?** The inherited underlying Transformer. The newly introduced router-adapter parameters are trained.
2. **Where does Equation 6 apply its MSE?** To last-layer states at answer positions; teacher reasoning states are also supplied as student inputs, which is a separate mechanism.
3. **Does stop-gradient freeze every teacher parameter throughout stage 1?** The target feature is detached for consistency loss, while Equation 9 still includes the teacher's own language-model objective.
4. **Why discuss teacher forcing separately from inference?** A supplied trajectory avoids some sequential training dependencies; deployment must continue from the model's own states and shortcut decisions.
5. **What must be clarified before faithfully implementing Equation 10?** Whether the reference target should be the student's same-layer state, as displayed, or final-layer state, as described in prose.
