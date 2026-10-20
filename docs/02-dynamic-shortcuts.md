# 2. Dynamic shortcuts: depth and decoding steps

[Back to the guide](../README.md) · [Next: training and objectives](03-training-and-objectives.md)

**Reading target:** understand what the two shortcuts change, how their training equations differ from inference, and which details v3 leaves open. The primary evidence is [Section 2.1, pp. 4–5, Equations 1–5](https://arxiv.org/pdf/2505.18962v3#page=4), with budget controls discussed in [Section 3.2, p. 9](https://arxiv.org/pdf/2505.18962v3#page=9).

## Start with a grid of computation

A Transformer reasoning run has at least two useful coordinates: the layer being computed and the decoding step being processed. Standard autoregressive decoding repeatedly starts from an input embedding and traverses the model's layers. Earlier latent reasoning approaches can replace emitted intermediate words with hidden states, but a latent step can still require a full layer traversal. The paper proposes changing the route through this grid. [Section 2.1, pp. 4–5](https://arxiv.org/pdf/2505.18962v3#page=4)

| Symbol | Meaning in this module |
| --- | --- |
| `l`, `L` | Current layer and total number of Transformer layers |
| `t` | Sequence or decoding-step index, following the paper's notation |
| `h[l,t]` | Hidden state at layer `l` and step `t` |
| `f[l]` | Standard Transformer layer computation |
| `g[l]` | Lightweight adapter branch |
| `R[l]` | Router implemented with a feed-forward layer and sigmoid |
| `w` | Router output used to mix paths during training |
| `lambda_depth` | Inference threshold for taking a depth shortcut |
| `lambda_step` | Fixed latent-step budget before final-answer generation |

**Guide interpretation:** picture an elevator moving between floors and a corridor connecting adjacent time steps on the same floor. The elevator is depth computation; the corridor is reuse across steps. This analogy explains the two coordinates, but it does not specify an implementation or imply that a hidden state is a readable, self-contained thought.

## Depth shortcut: choose a cheaper branch

The depth shortcut lets a router choose between a lightweight adapter and further standard-layer computation. During training, Equation 1 uses a soft combination: the adapter output receives weight `w`, while the standard path receives `1-w`. Equation 2 computes `w` from the preceding-layer state. A training mixture therefore evaluates a combination of paths; it should not be mistaken for the hard branch choice used at inference. [Equations 1–3, p. 4](https://arxiv.org/pdf/2505.18962v3#page=4)

At inference, Equation 3 takes the adapter branch when the router score is **strictly greater than** `lambda_depth`; otherwise it uses the standard Transformer operation. Increasing the threshold makes early exits harder to trigger. The paper states that `lambda_depth = 1` forces traversal to the final layer. This direction matters: a larger threshold means more depth computation, rather than a more aggressive shortcut policy. [Equation 3, p. 4](https://arxiv.org/pdf/2505.18962v3#page=4); [Section 3.2, p. 9](https://arxiv.org/pdf/2505.18962v3#page=9)

**Original illustrative example:** if an imagined router returns `0.7`, a threshold of `0.6` selects the shortcut, while `0.8` does not. These values explain the rule; they are not measurements or recommended settings.

## Step shortcut: continue from an intermediate state

Early exit alone does not eliminate the next decoding step's restart from the bottom of the model. The step shortcut adds a connection across decoding steps at the same layer. Equation 4's training mixture combines an adapter applied to the previous step's same-layer state with the standard current-step computation. The paper excludes this shortcut at `t = 0`, where no previous step exists. [Equation 4, p. 5](https://arxiv.org/pdf/2505.18962v3#page=5)

For inference, the text describes passing an early-exited state directly to the next step at that layer. Upon reaching the last layer, the model completes a reasoning cycle; it can feed the final state into another cycle or proceed to the answer. The latent-step budget is fixed by `lambda_step`. The router dynamically allocates depth within that budget; this is not a claim that the model independently learns when the entire problem is solved. [Section 2.1, p. 5](https://arxiv.org/pdf/2505.18962v3#page=5)

The authors argue that this reuse avoids omitting a newly arriving language token because the intermediate process already runs through latent states. Treat the stronger claim that crucial information is preserved as the authors' motivation and empirical hypothesis, not as a mathematical guarantee that every shortcut is lossless. [Section 2.1, p. 5](https://arxiv.org/pdf/2505.18962v3#page=5)

## Read Equation 5 carefully

The combined training equation places **the sum of the depth-adapter and step-adapter terms** under the shared weight `w`, then adds the standard path weighted by `1-w`. It is not written as a normalized three-way probability distribution over depth, step, and standard routes. The notation also uses adapter transformations in the training formulas while the inference narrative describes copying states. Both descriptions belong to v3; a reading guide should not silently replace them with a more detailed algorithm. [Equation 5 and accompanying text, p. 5](https://arxiv.org/pdf/2505.18962v3#page=5)

**Guide interpretation:** the intended contribution is joint flexibility across the layer and step axes. Translating that intent into a serving system would require explicit decisions about state scheduling, attention caches, batching, and adapter computation. The equations and schematic alone do not resolve those engineering choices.

## What the two budget controls do

| Change | Intended computational effect | Evidence boundary |
| --- | --- | --- |
| Raise `lambda_depth` | Permit fewer depth exits and use deeper processing | The threshold rule specifies direction; accuracy need not improve at every setting |
| Raise `lambda_step` | Allow more intermediate latent steps | This is an externally selected budget, not a learned stop decision |
| Adjust both | Explore a range of quality and computation settings | Figure 4 reports accuracy over a grid; it is not a complete latency measurement for every cell |

The paper presents this as controllable test-time scaling. Its [Figure 4 and Section 3.2, pp. 8–9](https://arxiv.org/pdf/2505.18962v3#page=8) support examining both axes. They do not establish a hardware-independent conversion from a particular threshold to milliseconds or energy.

## Check your understanding

1. **Why does a depth shortcut not make the step shortcut redundant?** A shallow exit reduces layer work for one step; the next step could still restart from the bottom. Same-layer reuse addresses that restart.
2. **Does a latent step mean a generated word?** No. Intermediate computation uses hidden representations; the final answer is still generated in language.
3. **Is a router score proof that a reasoning step is unimportant?** No. It is a learned routing signal trained with the paper's criticality-based supervision, whose assumptions are discussed in the next module.
4. **Can this guide's grid analogy be executed as pseudocode?** No. It explains the proposal while retaining the source's unresolved implementation details.
