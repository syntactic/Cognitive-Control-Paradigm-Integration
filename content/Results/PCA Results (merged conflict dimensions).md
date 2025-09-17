---
tags:
  - results
  - analysis
  - pca
---

# Initial Interpretation of the PCA Results

This note provides the initial conceptual interpretation of the Principal Component Analysis (PCA) performed on the coded experimental design space. The analysis reveals a structured space defined by two primary, orthogonal axes that align well with established theoretical distinctions in cognitive control research.

### PCA Summary
- **Variance Explained:** The first two components account for 36.9% of the total variance (PC1: 20.7%, PC2: 16.2%), indicating a high-dimensional design space where the 2D plot is a useful but simplified representation. The first four components explain a total of 57.6%.
- **Component Sparsity:** The Hoyer's Sparseness for the first four components is low (~0.36), meaning each component is a blend of multiple features. This shows the complexity of the design space.

### Principal Component 1: "Procedural Flexibility vs. Dynamic Coordination"
PC1, the axis of greatest variance, separates paradigms based on their fundamental structural and load-based demands.

- **High PC1 Scores (Positive Loadings):** Characterized by a very high loading on Switch Rate (0.412). This end of the axis is dominated by [[Paradigm Classes/Task Switching|Task Switching]] paradigms, representing designs focused on **cognitive flexibility and reconfiguration**.
- **Low PC1 Scores (Negative Loadings):** Characterized by features indicating stability, such as Trial Transition Type Mapped_TTT_Pure (-0.225), as well as Task 1 Difficulty (-0.199). This end represents stable, single-task paradigms where the primary challenge is the intrinsic difficulty of the task itself, not procedural changes.
- **Insight:** This component cleanly separates the cognitive demand of changing tasks from the demand of performing a single, potentially difficult, task.

### Principal Component 2: "Single Task-Set vs. Dual Task-Set Repertoire"
PC2 provides a clear, structural division based on the temporal nature of cognitive control required by the paradigm.

- **High PC2 Scores (Positive Loadings):** Characterized by high loadings on Task 1 CSI (0.443) and Task 2 CSI (0.442). This region is populated by paradigms that provide explicit preparation time, primarily cued [[Paradigm Classes/Task Switching|Task Switching]] tasks. It represents designs that emphasize **proactive, preparatory control**.
- **Low PC2 Scores (Negative Loadings):** Characterized by high loadings for Task 2 Response Probability (-0.433), Inter-task SOA (-0.199), Task 1 Difficulty (-0.200), and Task 2 Difficulty (-0.195). This region is dominated by [[Paradigm Classes/Dual-Task Performance & PRP|Dual-Task & PRP]] paradigms, which demand **reactive coordination** of two tasks under high temporal and cognitive load.
- **Insight:** This component makes a powerful distinction not just between single- and dual-tasking, but between control strategies that are anticipatory versus those that are concurrent and reactive.

### Key Insights & Critical Observations
1. **Conflict is Orthogonal to Structure:** As in the previous analysis, key conflict dimensions ([[Dimensions/Stimulus Bivalence & Congruency]]) do not load heavily on the first four principal components. This reinforces the conclusion that the type of conflict is a separate dimension of experimental design, independent of task architecture and timing.
2. **Difficulty's Complex Role:** Task Difficulty is a crucial feature, but it does not define a single axis. It contributes negatively to both PC1 and PC2, suggesting it helps define both the stability of single-task execution and the reactive load in dual-task coordination. Its strong positive loading on PC4 further highlights its role as an independent source of experimental challenge.
---
### Deeper Components: Load and Asynchrony

Analysis of PC3 and PC4 reveals more subtle, yet clear, structural dimensions:
- **PC3 - "Overall Task Complexity and Preparation":** This component is positively loaded by Task 1 CSI (0.445), RSI (0.373), and Task 2 Response Probability (0.356). It appears to capture an axis of overall trial complexity, separating simple, uncued, single-task paradigms from demanding, prepared, multi-task paradigms.
- **PC4 - "Intrinsic Task Difficulty vs. Temporal Separation":** This component is defined by a strong positive loading for Task 2 Difficulty (0.647) and Task 1 Difficulty (0.415), and negative loadings for RSI (-0.242) and Inter-task SOA (-0.223). It cleanly separates paradigms whose primary challenge is the intrinsic difficulty of the tasks from those whose challenge comes from manipulating the temporal intervals between tasks.

### A Note on the Missing "Conflict Axis"
A critical finding is that none of the top four principal components, which together account for 56.7% of the variance, are primarily driven by the `Stimulus Bivalence & Congruency` dimension. This suggests that while conflict is a crucial *manipulation* within paradigms, it is not a primary driver of the overall *structural variance* across the design space. Task architecture and timing appear to be the dominant organizing principles. This finding motivates a more targeted analysis of conflict's role using other methods.
