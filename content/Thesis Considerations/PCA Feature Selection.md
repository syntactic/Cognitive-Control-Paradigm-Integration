---
tags:
  - methodology
  - pca
---

Derived Conceptual Dimensions vs. Low-Level SE Parameters

A critical decision in preparing data for Principal Component Analysis (PCA) within this thesis is the level of abstraction for the input features. The choice is between using:
1.  **Low-Level Super Experiment (SE) Parameters:** These are the direct, numerous parameters required by the SE framework to instantiate a trial (e.g., `start_1`, `dur_1`, `start_mov_1`, `dur_mov_1`, `coh_mov_1`, `start_go_1`, `keyMap` settings, etc.).
2.  **Higher-Level Derived Dimensions:** These are conceptual parameters abstracted from the literature and SE parameters, reflecting functional experimental manipulations (e.g., [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]], [[CSI (Cue-Stimulus Interval)|CSI]], [[Number of Tasks]], [[Response Set Overlap]], [[Task Difficulty]]).

**Justification for using Higher-Level Derived Dimensions as the primary features for PCA:**

1.  **Interpretability of Principal Components:**
    *  **Derived Dimensions:** PCA components derived from these features are more directly interpretable in cognitive terms. For example, a component heavily loading on `Inter-task SOA`, `Task 2 Response Probability`, and `Task 2 Difficulty` could be readily understood as representing "Dual-Task Load & Temporal Coordination." This aligns with how cognitive psychologists conceptualize experimental designs.
    *  **Low-Level SE Parameters:** Components based on numerous, fine-grained SE parameters would be significantly harder to interpret. A component loading on `dur_mov_1`, `start_go_2`, and `coh_or_1` lacks immediate psychological meaning and would require reverse-engineering to understand its functional significance.

2.  **Alignment with Thesis Goals:**
    *  The primary aim is to map the *conceptual design space* of cognitive control paradigms as understood in the literature and to identify *parametric transitions* between them. Derived dimensions represent these conceptual manipulations.
    *  PCA on derived dimensions helps to understand how these known conceptual design choices co-vary, cluster, and differentiate experimental paradigms in the surveyed literature.

3.  **Abstraction and Generalizability:**
    *  Derived dimensions allow for the comparison of studies that implement the same conceptual manipulation (e.g., a 500ms SOA) using different absolute SE timings. For instance, an SOA of 500ms is functionally the same whether S1 starts at SE's 1000ms (and S2 at 1500ms) or S1 starts at SE's 2000ms (and S2 at 2500ms). Using derived `SOA_ms_PCA` captures this crucial functional equivalence.
    *  Low-level SE parameters would treat these as distinct, potentially obscuring fundamental similarities in experimental logic.

4.  **Reduced Dimensionality and Noise:**
    *  While SE has many parameters, several are often fixed, zero, or highly correlated for specific paradigm types (e.g., all `_2` parameters for single-task designs). Derived dimensions inherently perform a level of meaningful dimensionality reduction.
    *  PCA on raw SE parameters might be susceptible to noise or structure arising from SE's specific implementation details (e.g., how `mov2Interval` timing is calculated) rather than fundamental design principles in the literature.

5.  **Focus on Functional Design Choices:**
    *  Researchers manipulate functional aspects like SOA, CSI, or Switch Rate. The absolute start time of a stimulus on the screen (a raw SE parameter) is often arbitrary as long as relative timings are maintained. PCA on derived dimensions reflects these salient design choices.

**Tradeoffs Acknowledged:**

*   **Interpretive Step:** The mapping from literature to derived dimensions involves an interpretive step. The PCA results will reflect the structure of this *coded representation*. This necessitates careful and consistent coding, which is a core part of this project's methodology.
*   **Loss of Fine-Grained Detail (Potentially):** By abstracting to derived dimensions, some very specific SE parameter combinations that might differentiate studies subtly could be collapsed. However, for the primary goal of understanding the broader conceptual space, this is a necessary and beneficial simplification.
