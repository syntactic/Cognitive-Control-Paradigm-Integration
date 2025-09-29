---
tags:
  - results
  - analysis
  - pca
---

# Initial Interpretation of the PCA Results

This note provides the initial conceptual interpretation of the Principal Component Analysis (PCA) performed on the coded experimental design space. The analysis reveals a structured space defined by two primary, orthogonal axes that align well with established theoretical distinctions in cognitive control research.

### PCA Summary
- **Variance Explained:** The first two components account for 36.9% of the total variance (PC1: 20.5%, PC2: 16.4%), indicating a high-dimensional design space where the 2D plot is a useful but simplified representation. The first four components explain a total of 57.5%.
- **Component Sparsity:** The Hoyer's Sparseness for the first four components is low (~0.37), meaning each component is a blend of multiple features. This shows the complexity of the design space.


### Principal Component 1: Procedural Flexibility vs. Stable Task Execution

PC1 separates paradigms based on whether they demand flexible, trial-to-trial procedural changes versus stable, repetitive execution.

-   **High PC1 Scores (Positive Loadings):** Characterized by a dominant loading on `Switch Rate` (0.369). This end of the axis is defined by [[Paradigm Classes/Task Switching|Task Switching]] paradigms, representing designs focused on **cognitive flexibility and reconfiguration**.
-   **Low PC1 Scores (Negative Loadings):** Characterized by a strong negative loading on Task 2 Difficulty is NA=1 (-0.248) and features indicating single-task simplicity. This end represents **stable, single-task execution** where the primary challenge is performing a single, repeated task set.

### Principal Component 2: Proactive Preparation vs. Reactive Dual-Task Coordination

PC2 provides a clear division based on the temporal nature of the required cognitive control.

-   **High PC2 Scores (Positive Loadings):** Defined by very high loadings on `Task 1 CSI` (0.43) and `Task 2 CSI` (0.405). This region contains paradigms that provide explicit preparation time, primarily cued [[Paradigm Classes/Task Switching|Task Switching]]. It represents designs that emphasize **proactive, preparatory control**.
-   **Low PC2 Scores (Negative Loadings):** Defined by a dominant negative loading for `Task 2 Response Probability` (-0.424) and other PRP-related features (`Inter-task SOA`, `Task Difficulty`). This region is dominated by [[Paradigm Classes/Dual-Task Performance & PRP|Dual-Task & PRP]] paradigms, which demand **reactive coordination** of two tasks under high temporal and cognitive load.

### Deeper Components: Load and Asynchrony

*   **PC3 (Overall Task Complexity and Preparation):** The interpretation holds, but is more nuanced. It seems to represent an axis of **Prepared Multi-Tasking Complexity**.
    *   It's positively loaded by features related to having multiple, prepared tasks (`CSI`, `RSI`, `Task 2 Response Probability`).
    *   The negative loading from `Distractor SOA` (-0.225) is interesting; it suggests that paradigms defined by asynchronous *distractors* are structurally different from those defined by prepared *dual-tasks*.

*   **PC4 (Intrinsic Task Difficulty vs. Temporal Separation):** This interpretation is now **crystal clear**.
    *   The component is overwhelmingly dominated by positive loadings on `Task 2 Difficulty` (0.683) and `Task 1 Difficulty` (0.476).
    *   The strongest negative loadings are `RSI` (-0.248) and `Inter-task SOA` (-0.177).
    *   This beautifully separates paradigms based on whether their primary challenge comes from the *content* of the tasks themselves or the *timing and separation* between them.

### A Note on the Missing "Conflict Axis"
A critical finding is that none of the top four principal components, which together account for 56.7% of the variance, are primarily driven by the `Stimulus Bivalence & Congruency` dimension. This suggests that while conflict is a crucial *manipulation* within paradigms, it is not a primary driver of the overall *structural variance* across the design space. Task architecture and timing appear to be the dominant organizing principles. This finding motivates a more targeted analysis of conflict's role using other methods.

---
