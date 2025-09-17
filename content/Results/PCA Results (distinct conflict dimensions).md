---
tags:
  - results
  - analysis
  - pca
  - robustness_check
---

# PCA Results (Distinct Conflict Dimensions)

This note summarizes a secondary Principal Component Analysis conducted as a robustness check on the main [[PCA Results (merged conflict dimensions)]]. In this version, the `Stimulus-Stimulus Congruency` and `Stimulus-Response Congruency` dimensions were kept separate instead of being merged into a single `Stimulus Bivalence & Congruency` feature.

### Key Finding: High Structural Stability

The main finding is that the overall structure of the latent space is **remarkably stable** compared to the primary analysis.

-   **Variance Explained:** The first two components explain **36.5%** of the variance (PC1: 20.4%, PC2: 16.1%), which is nearly identical to the 36.9% explained in the merged analysis.
-   **Component Interpretation:** The interpretation of the top four principal components remains unchanged. The same features dominate the loadings, leading to the same conceptual labels:
    -   **PC1:** Procedural Flexibility vs. Stable Task Execution
    -   **PC2:** Proactive Preparation vs. Reactive Dual-Task Coordination
    -   **PC3:** Overall Task Complexity and Preparation
    -   **PC4:** Intrinsic Task Difficulty vs. Temporal Separation

### Difference: The Role of Conflict Dimensions

The main purpose of this analysis was to see if separating the conflict dimensions would reveal a distinct "conflict axis" that was previously obscured.

-   **Result:** Even when treated as separate features, neither `Stimulus-Stimulus Congruency` nor `Stimulus-Response Congruency` emerged as high-loading variables on any of the top four principal components. Their influence on the overall variance structure remained minimal.

### Conclusion

This secondary analysis serves as a strong validation of the primary approach. The stability of the results demonstrates that the decision to merge the two conflict dimensions into a single, more parsimonious feature was justified. It simplifies the model without obscuring the primary structural axes of the experimental design space, which are driven by task architecture, timing, and difficulty rather than the specific type of conflict.
