# Glossary and notation

Definitions are paraphrased from [§2, pp. 3–7](https://arxiv.org/pdf/2505.18962v3#page=3). The explanatory distinctions are guide material.

| Term / symbol | Meaning in this paper | Reading caution |
| --- | --- | --- |
| CoT | Chain-of-thought intermediate language reasoning | A visible trace is not automatically a faithful causal explanation |
| Latent thought | Continuous hidden representation used during intermediate reasoning | Not necessarily one human sentence or atomic proposition |
| DS | Depth shortcut through an adapter rather than continuing deeper | Concerns depth at a reasoning step |
| SS | Step shortcut reusing a state across steps at the same layer | Does not mean dropping question tokens |
| `l`, `L` | Layer index and total number of Transformer layers | Lowercase and uppercase matter for the Eq. 10 ambiguity |
| `t`, `T` | Sequence/decoding position and sequence length in the notation | A latent step and a visible text token are not interchangeable units |
| `h[l,t]` | Hidden state at layer `l` and position `t` | Its teacher/student/model superscript identifies the producing model |
| `f_l` | Standard Transformer layer operation | Not the lightweight adapter |
| `g_l` | Adapter branch operation | The precise adapter dimensions are not specified in v3 |
| `R_l`, `w` | Router and its sigmoid output weight | Soft mixture during training; thresholded selection at inference |
| `lambda_depth` | Depth-exit threshold | Larger values make exits harder; 1 forces full depth under the stated rule |
| `lambda_step` | Fixed latent reasoning budget / decoding step constant | An external inference setting, not a learned answer-correctness stopping rule |
| Reasoning cycle | Traversal reaching the final layer through the dynamic path | See §2.1 rather than assuming every local shortcut is a full cycle |
| `Q`, `R`, `A` | Question, intermediate reasoning, answer segments | Their separate lengths determine the loss masks |
| `sg` | Stop-gradient operator | Stops gradients through the target branch; does not freeze every parameter globally |
| NLL | Negative log-likelihood | Teacher: reasoning + answer; latent student: answer tokens |
| MSE | Mean squared error | State-alignment objective; not directly an accuracy metric |
| `alpha`, `beta` | Consistency and early-exit loss coefficients | Symbolic values are defined, chosen numerical values are not given |
| `c_t` | Binary criticality label | 0 for independent/non-critical DAG nodes; 1 for derived/critical nodes |
| `e[l,t]` | Layer/criticality-dependent weighting in Eq. 11 | A loss weight, not an explicit router target class |
| FLOPs r. | Table 1's multiplicative per-step FLOPs reduction relative to CoT | A factor such as 1.95×, not a percent or overall wall-clock ratio |
| Speedup | Table 1's overall wall-clock inference speedup relative to CoT | Hardware and timing boundaries are not specified |
| Percentage points | Difference between two percentage-valued accuracies | 46.66% − 46.94% = −0.28 points, not −0.28% relative |

[Reading map](00-reading-map.md) · [Dynamic shortcuts](02-dynamic-shortcuts.md) · [Training](03-training-and-objectives.md)
