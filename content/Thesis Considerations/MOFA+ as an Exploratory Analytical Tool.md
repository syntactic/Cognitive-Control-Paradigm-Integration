---
tags:
  - methodology
  - mofa
  - thesis_consideration
---

# MOFA+ as an Exploratory Analytical Tool

While Principal Component Analysis (PCA) serves as the primary analytical method for this thesis, we also employed Multi-Omics Factor Analysis (MOFA+) as a complementary, exploratory tool. MOFA+ offers a more theory-driven approach to dimensionality reduction that allows us to test specific hypotheses about the relationships between our conceptual dimensions.

### 1. What is MOFA+?

MOFA+ is an unsupervised statistical method for dimensionality reduction, based on a flexible framework of matrix factorization. Like PCA, its goal is to identify a small number of latent "factors" that capture the main sources of variation in a complex dataset. However, it differs from PCA in several key ways relevant to this project:

*   **Theory-Guided:** Its most powerful feature is the ability to group input features into predefined "views," allowing the model to be guided by our theoretical assumptions.
*   **Non-Orthogonal Factors:** Unlike PCA's principal components, the factors discovered by MOFA+ are not constrained to be mathematically orthogonal. This can lead to more interpretable factors that better reflect potentially correlated underlying cognitive processes.
*   **Probabilistic Framework:** It uses a variational Bayesian framework, which provides a generative model of the data. A practical benefit of this is its native ability to handle missing data without requiring imputation, a key difference from our PCA pipeline.
*   **Sparsity:** The model encourages sparsity in its factor loadings, meaning each factor is defined by a small, interpretable set of core features.

### 2. The Concept of "Views"

The central advantage of MOFA+ for this project is its use of **views**. A view is a collection of features that are conceptually related. Before running the analysis, we group our derived dimensions based on the cognitive function they are thought to represent.

This grouping is not arbitrary; it is an explicit operationalization of our theoretical framework, defined in the `VIEW_MAPPING_UNIFIED` dictionary within `analysis_utils.py`:

```python
VIEW_MAPPING_UNIFIED = {
    'Temporal': ['Inter-task SOA', 'Distractor SOA', 'Task 1 CSI', 'Task 2 CSI', 'RSI'],
    'Context': ['Switch Rate', 'RSI is Predictable', 'Trial_Transition_Type'],
    'Task_Properties': ['Task 1 Difficulty', 'Task 2 Difficulty'],
    'Conflict': ['Stimulus-Stimulus Congruency', 'Stimulus-Response Congruency'],
    'Rules': ['Task 1 Stimulus-Response Mapping', 'Task 2 Stimulus-Response Mapping', 'Response Set Overlap'],
    'Structure': ['Task 2 Response Probability', 'Task_1_Cue_Type', 'Task_2_Cue_Type', '...NA flags...']
}
```

By providing the model with this structure, we enable it to discover factors that may explain variance *across* multiple conceptual domains. For example, a single MOFA+ factor could have high weights on features in both the **'Conflict'** view and the **'Context'** view. This would provide evidence for a latent process that links contextual cues (like `Switch Rate`) to the processing of conflict, a core prediction of the [[Theoretical Concepts/Conflict Monitoring Theory]].

### 3. How MOFA+ Finds Factors

At its core, MOFA+ works by decomposing our data matrix (where rows are experimental conditions and columns are features) into two smaller matrices: a matrix of **factor scores** (Z) and a matrix of **weights** (W).

The model uses a variational Bayesian algorithm to find the factors and weights that are most likely to have generated the observed data, while also prioritizing solutions where the weights are sparse. This means it tries to explain the data using factors that are driven by a small number of highly influential features, which aids in interpretation.

The output allows us to analyze:
*   The **weights** of each feature on each factor, telling us what the factor represents.
*   The **factor scores** for each experimental condition, telling us where each paradigm is located on that factor's axis.
*   The amount of variance explained by each factor, both overall and *within each view*.

### 4. Role in This Thesis

For this thesis, MOFA+ serves as a secondary, confirmatory, and exploratory tool. Its primary purpose is not to replace the global, variance-driven map provided by PCA, but to provide a more nuanced, theory-informed perspective. We use it to ask more specific questions about how different conceptual domains of experimental design co-vary. While its results may be more complex, they offer a powerful way to test if the latent structure of the design space aligns with established theories of cognitive control.