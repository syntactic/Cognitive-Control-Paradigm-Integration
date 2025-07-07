#dimension 

#### Definition
A continuous dimension from 0 to 1 representing the probability that a participant is required to make a response to a second task/stimulus within a trial. It functionally replaces the discrete Number of Tasks dimension to allow for more coherent interpolation in the parametric space.

#### Rationale

**The Core Problem: Interpolation and Interpretability**
The primary goal of the thesis is to map paradigms within a continuous parametric space and explore the "in-between" regions. When using Principal Component Analysis (PCA) to analyze this space, it's possible to identify centroids for canonical paradigms (e.g., Interference, Task-Switching, Dual-Task) and then mathematically interpolate between them to generate novel, hypothetical experimental designs.

However, when Number of Tasks is used as a primary feature, this creates a significant interpretation problem. Interpolating between a single-task paradigm (N_Tasks=1) and a dual-task paradigm (N_Tasks=2) can yield points in the space that correspond to N_Tasks=1.5. This result is conceptually incoherent - an experiment cannot have "one and a half tasks."

**The Solution: A Continuous, Probabilistic Dimension**

The Task 2 Response Probability dimension resolves this issue by reframing the discrete N_Tasks variable into a continuous, meaningful one.
- **Definition:** Task 2 Response Probability is a continuous variable from 0 to 1 that represents the probability that a participant must execute a response to a second stimulus/task event within a trial.
- **Mapping:**
    - **Value = 0:** Corresponds to all single-task paradigms. A second stimulus may be present (as a distractor), but the probability of responding to it is zero. This covers Interference and Task-Switching.
    - **Value = 1:** Corresponds to all dual-task paradigms. A response to the second task is always required. This covers PRP and standard dual-task designs.

**Theoretical and Practical Implications**
This change has several powerful implications for the thesis:
1. **Meaningful Interpolation:** An interpolated value like 0.5 is now perfectly interpretable. It describes a novel "bridge" paradigm where a second stimulus appears, but the participant is only required to respond to it on 50% of the trials. This is an empirically testable design.
2. **Parametric Transition:** It operationalizes the transition from Interference Control (filtering a non-response stimulus) to Dual-Task Performance (coordinating two responses) as a single, continuous parameter. This directly serves the thesis goal of identifying parametric modulators between paradigm classes.
3. **Enhanced Analytical Power:** By replacing a categorical feature with a continuous one, it makes the input for PCA more robust and the interpretation of the resulting components more straightforward. It quantifies the fundamental shift in cognitive demand—from mere filtering to active response coordination—along a single axis.
#### Relevance to the Design Space:

- **Value = 0:** "Characterizes all single-task paradigms, including [[Paradigm Classes/Interference Control]] and [[Paradigm Classes/Task Switching]], where only one S-R mapping must be executed per trial."
- **Value = 1:** "Characterizes all dual-task paradigms, including [[Dual-Task Performance & PRP|PRP]], where two S-R mappings must be executed per trial."
- **Interpolated Values (e.g., 0 < p < 1):** "Represents novel, hypothetical 'bridge' paradigms where a second stimulus appears but only requires a response on a random subset of trials. This creates a continuous transition from pure filtering (p=0) to mandatory dual-task coordination (p=1)."