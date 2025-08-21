---
tags:
  - dimension
  - dual_task
  - structure
aliases:
  - Tasks Are Identical
  - T1-T2 Relationship
---
### Definition
**`Intra-Trial Task Relationship`** is a categorical dimension that describes the relationship between the cognitive task-set required for Task 1 and the task-set required for Task 2 **within a single dual-task trial**.

### Values

*   **`Same`**: The task for T1 is identical to the task for T2.
    *   *Example:* In [[Telford (1931)]], T1 is a simple auditory RT and T2 is also a simple auditory RT.
*   **`Different`**: The task for T1 is different from the task for T2.
    *   *Example:* In a standard PRP experiment like [[McCann & Johnston (1992)]], T1 might be an auditory tone judgment while T2 is a visual shape judgment.
*   **`N/A` (Not Applicable)**: This value is used for all single-task paradigms where `[[Dimensions/Task 2 Response Probability]]` is 0, as there is no second task for the relationship to be defined.

### Rationale and Importance

This dimension was created to provide a more precise and orthogonal framework for describing experimental designs, particularly novel "bridge" paradigms. Its key functions are:

1.  **Precision in Dual-Task Design:** It explicitly captures a core design choice in dual-task studies that was previously implicit. It allows us to distinguish PRP paradigms that repeat the same task (like Telford) from those that use two different tasks.
2.  **Orthogonality to Inter-Trial Effects:** This dimension is strictly **intra-trial** (within a trial). It is orthogonal to the `Inter-Trial Transition` dimension, which is strictly **inter-trial** (between trials). This separation eliminates the ambiguity of the previously overloaded `Trial Transition Type` dimension.
3.  **Modeling Novel Paradigms:** The primary power of this dimension is revealed in its **interaction with `Switch Rate`**. This interaction is what allows us to uniquely identify the innovative designs of studies like [[Hirsch et al. (2018)]] and Lien et al. (2003), distinguishing them from classic PRP.

### The Critical Interaction with `Switch Rate`

The core contribution of paradigms like Lien et al. is the introduction of **procedural uncertainty** (a block-level property) into a dual-task structure that also varies the **intra-trial task relationship** (a trial-level property). Our framework captures this distinction perfectly:

| Paradigm Example | `Switch Rate` (Block Context) | `Intra-Trial Task Relationship` (Trial Property) | Key Distinction |
| :--- | :--- | :--- | :--- |
| **Telford (1931)** | **0%** | `Same` | The `Same` relationship occurs in a **stable, predictable** block. |
| **Standard PRP** | **0%** | `Different` | The `Different` relationship occurs in a **stable, predictable** block. |
| **Lien/Hirsch "Same" Trial** | **> 0%** | `Same` | The `Same` relationship occurs in a **variable, unpredictable** block. |
| **Lien/Hirsch "Different" Trial** | **> 0%** | `Different` | The `Different` relationship occurs in a **variable, unpredictable** block. |

As shown above, the `Switch Rate` dimension successfully encodes the block-level context, allowing the PCA to distinguish between a Telford trial and a Lien/Hirsch "same" trial, even though their `Intra-Trial Task Relationship` is identical.

### PCA Coding

This dimension will be treated as a categorical feature and one-hot encoded for the PCA (e.g., `ITTR_Same`, `ITTR_Different`, `ITTR_NA`).

### Key Literature

*   [[Telford (1931)]]
*   [[Hirsch et al. (2018)]]
*   Lien, Schweickert, & Proctor (2003)
