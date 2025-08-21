---
tags:
  - results
  - analysis
  - pca
---

# Initial Interpretation of the PCA Results

This note provides the initial conceptual interpretation of the Principal Component Analysis (PCA) performed on the coded experimental design space. The analysis reveals a structured space defined by two primary, orthogonal axes that align well with established theoretical distinctions in cognitive control research.

### PCA Summary
- **Variance Explained:** The first two components account for 35.9% of the total variance (PC1: 19.1%, PC2: 16.8%), indicating a high-dimensional design space where the 2D plot is a useful but simplified representation.
- **Component Sparsity:** The Hoyer's Sparseness for the first three components is low (~0.37), meaning each component is a blend of multiple features. This underscores the complexity of the design space.

### Principal Component 1: "Task-Set Flexibility vs. High-Load Coordination"
PC1, the axis of greatest variance, separates paradigms based on their fundamental structural and load-based demands.

- **High PC1 Scores (Positive Loadings):** Characterized by high `Switch Rate` and `CSI`. This end of the axis is populated by [[Paradigm Classes/Task Switching|Task Switching]] paradigms, representing designs focused on **cognitive flexibility**.
- **Low PC1 Scores (Negative Loadings):** Characterized by high `Task 2 Response Probability` and, crucially, high `Task 1/2 Difficulty`. This end is dominated by demanding [[Paradigm Classes/Dual-Task Performance & PRP|Dual-Task & PRP]] paradigms. It represents designs focused on **high-load concurrent coordination**.
- **Insight:** The location of the low-difficulty Telford (1931) auditory RT tasks on the positive side of this axis reveals that task difficulty is as critical as task structure in defining this primary dimension.

### Principal Component 2: "Single Task-Set vs. Dual Task-Set Repertoire"
PC2 provides a clear, structural division of the space based on the number of task-sets a participant must maintain.

- **High PC2 Scores (Positive Loadings):** Characterized by high loadings on flags indicating the absence of a second task (e.g., `Task_2_Difficulty_is_NA`). This region is populated by all [[Paradigm Classes/Interference Control|Interference Control]] and single-task baseline conditions. It represents paradigms requiring the maintenance of only a **single task-set**.
- **Low PC2 Scores (Negative Loadings):** Characterized by features only applicable when a second task exists (e.g., `Switch Rate`, `Task 2 Response Probability`). This region contains all `Task Switching` and `Dual-Task` paradigms, representing designs that require maintaining a **dual task-set repertoire**.

### Key Insights & Critical Observations
1.  **Conflict is Orthogonal to Structure:** Key conflict dimensions ([[Dimensions/Stimulus-Stimulus Congruency]] and [[Dimensions/Stimulus-Response Congruency]]) do not load heavily on PC1 or PC2. This suggests that the type of conflict is a separate dimension of experimental design, independent of task structure and repertoire size.
2.  **Difficulty is a Core Structural Feature:** The analysis reveals that `Task Difficulty` is not just a modulator but a core feature that, along with `Task 2 Response Probability`, defines the nature of dual-task paradigms in this space.
---
### Deeper Components: Load and Asynchrony

Analysis of PC3 and PC4 reveals more subtle, yet clear, structural dimensions:

*   **PC3 - "General Cognitive Load & Preparation":** This component is positively loaded by `Task Difficulty`, `Task 2 Response Probability`, and `CSI`. It appears to capture an axis of overall trial complexity, separating simple, uncued, single-task paradigms from demanding, prepared, dual-task paradigms.

*   **PC4 - "Asynchronous Distractor vs. Inter-Task Interval":** This component is cleanly defined by a strong positive loading for `Distractor SOA` and a strong negative loading for `Inter-task SOA`. It validates the framework's distinction between these two types of temporal manipulation, effectively isolating asynchronous interference paradigms (like [[Kopp et al. (1996)]]) from classic PRP paradigms.

### A Note on the Missing "Conflict Axis"
A critical finding is that none of the top four principal components, which together account for 56.7% of the variance, are primarily driven by the `Stimulus-Stimulus Congruency` or `Stimulus-Response Congruency` dimensions. This suggests that while conflict is a crucial *manipulation* within paradigms, it is not a primary driver of the overall *structural variance* across the design space. Task architecture and timing appear to be the dominant organizing principles. This finding motivates a more targeted analysis of conflict's role using other methods.
