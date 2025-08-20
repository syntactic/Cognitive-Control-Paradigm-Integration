---
tags:
  - methodology
  - pca
---

PCA input features derived from the master literature coding CSV. Derived dimensions map to reduced categories reflecting distinctions achievable within the Super Experiment (SE) framework.

**I. Numerical Features (Z-scored):**

1.  **`Task 2 Response Probability`**: (0-1) Core single-task/dual-task separator.
2.  **`Inter-task SOA`**: (ms) S1-S2 delay in dual-task paradigms. Median imputation when N/A.
3.  **`Distractor SOA`**: (ms) Target-distractor delay in single-task bivalent paradigms. Median imputation when N/A.
4. **`Task 1 CSI`**: (ms) Cue-Stimulus Interval for first task.
5. **`Task 2 CSI`**: (ms) Cue-Stimulus Interval for second task. Median imputation for single-task.
6.  **`RSI`**: (ms) Response-Stimulus Interval. `Super_Experiment_Mapping_Notes` may specify distributions; CSV value is expected value.
7. **`Switch Rate`**: (0-100) Task switch probability. Default 0 for N/A.
8. **`Task 1 Difficulty`**: (0-1) Normalized from CSV ordinal (1-5) -> (value-1)/4. Default 0.5 for N/A.
9.  **`Task 2 Difficulty`**: (0-1 or -1) Normalized second task difficulty. -1 for true single-task paradigms.

**II. Categorical Features (One-Hot Encoded):**

*`_Mapped` suffix indicates final categories processed by `analysis_utils.py`.*

A. **`Stimulus_Bivalence_Congruency_Mapped`**: Operational dimension combining S-S and S-R conflict. Categories: `SBC_Congruent`, `SBC_Incongruent`, `SBC_Neutral`, `SBC_NA`.

B. **`Response_Set_Overlap_Mapped`**: Categories: `RSO_Identical`, `RSO_Disjoint`.
    *   SE-Mappable Categories:
        *  `RSO_SE_Identical` (Literature: "Identical")
        *  `RSO_SE_Disjoint` (Literature: all disjoint categories - SE maps to different key groups)
        *  `RSO_SE_NA` (Literature: "N/A")

C. **`Task_1_Stimulus-Response_Mapping_Mapped`**: Categories: `SRM_Compatible`, `SRM_Incompatible`, `SRM_Arbitrary`.
    *   `SRM_SE_Compatible`: Spatially/semantically congruent `keyMap`
    *   `SRM_SE_Incompatible`: Crossed/counter-intuitive `keyMap`
    *   `SRM_SE_Arbitrary`: Learned, non-prepotent associations

D. **`Task_2_Stimulus-Response_Mapping_Mapped`**: Categories: `SRM2_Compatible`, `SRM2_Incompatible`, `SRM2_Arbitrary`.

E. **`Task_1_Cue_Type_Mapped`**: Categories: `TCT_Implicit`, `TCT_Arbitrary`
    *   `TCT_SE_None_Implicit`: CSI=0, cue simultaneous with stimulus
    *   `TCT_SE_Info_Precedes_Stim`: CSI > 0, external cue information
    *   `TCT_SE_NA`

F. **`Task_2_Cue_Type_Mapped`**: Categories: `TCT2_Implicit`, `TCT2_Arbitrary`.

G. **`Trial_Transition_Type_Mapped`**: Categories: `TTT_Pure`, `TTT_Switch`, `TTT_Repeat`.

H. **`Inter_task_SOA_is_NA`**: (Binary) Flag for Inter-task SOA relevance.

I. **`Distractor_SOA_is_NA`**: (Binary) Flag for Distractor SOA relevance.

J. **`RSI_Is_Predictable`**: (Binary) Fixed (1) vs variable (0) RSI.

K. **`Task_2_Difficulty_is_NA`**: (Binary) Task 2 difficulty presence.

L. **`Task_2_CSI_is_NA`**: (Binary) Task 2 CSI presence.