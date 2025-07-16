---
tags:
  - methodology
  - pca
---

This note lists the features intended for input into the Principal Component Analysis (PCA). These features are derived from the master literature coding CSV file. Derived dimensions from the literature are mapped to a reduced set of categories that reflect distinctions achievable or most relevant within the Super Experiment (SE) framework. This mapping is an explicit step in the data processing pipeline.

**I. Numerical PCA Features (Standardized - e.g., Z-scored):**

1.  **`Task 2 Response Probability`**: (Numeric: 0-1) The core dimension separating single-task from dual-task paradigms.
2.  **`Inter-task SOA`**: (Numeric: ms) The delay between S1 and S2 in `N_Tasks=2` paradigms. Imputed to 0 when not applicable.
3.  **`Distractor SOA`**: (Numeric: ms) The delay between target and distractor features in `N_Tasks=1`, bivalent paradigms. Imputed to 0 when not applicable.
4.  **`Inter_task_SOA_is_NA`**: (Binary: 0 or 1) A flag indicating if `Inter-task SOA` is the relevant temporal variable for the paradigm.
5.  **`Distractor_SOA_is_NA`**: (Binary: 0 or 1) A flag indicating if `Distractor SOA` is the relevant temporal variable for the paradigm.
6.  **`Task 1 CSI`**: (Numeric: ms) The Cue-Stimulus Interval for the first task.
7. **`Task 2 CSI`**: (Numeric: ms) The Cue-Stimulus Interval for the second task. Imputed to 0 for single-task paradigms.
8.  **`RSI`**: (Numeric: ms) The Response-Stimulus Interval.
    * The `Super_Experiment_Mapping_Notes` may indicate a more accurate idea of how RSI might have been manipulated in an experiment (see [[Stephan & Koch (2010)]] for example). It might indicate that the RSI is drawn from a distribution. In that case, the CSV's `RSI` value is the expected value of that distribution.
    * Placeholder/Imputation for N/A or "Not Specified": e.g., median of observed RSIs, or a fixed value representing a common ITI.
9.  **`RSI_Is_Predictable`**: (Binary: 0 or 1) Captures whether the RSI is fixed (`1`) or variable (`0`), a critical distinction for preparation theories.
10. **`Switch Rate`**: (Numeric: 0-100) The probability of a task switch.
    *  Placeholder/Imputation for N/A: 0. This shouldn't practically be N/A. If we're in a single-task paradigm there either is a switch (mixed block) or never a switch. If we're in a dual-task paradigm then the task order could switch such as in [[Sigman & Dehaene (2006)]].
11. **`Task 1 Difficulty`**: (Numeric: 0-1) Normalized difficulty score for the first task.
    *   Derived from CSV `Task 1 Difficulty` (1-5 ordinal) -> (value-1)/4.
    *   Placeholder/Imputation for N/A: e.g., 0.5 (moderate difficulty).
12.  **`Task 2 Difficulty`**: (Numeric: 0-1 or -1) Normalized difficulty for the second task in the repertoire. A value of `-1` is used as a placeholder for true single-task paradigms where no alternative task exists.
    *   Derived from CSV `Task 2 Difficulty` (1-5 ordinal) -> (value-1)/4.
    *   If `Number of Tasks` = 1 (for that row/condition), this feature is set to a distinct placeholder (e.g., -1) or imputed based on context (e.g. if it's a TS paradigm, it's the difficulty of the *other* task in repertoire). *Current preference: Use actual difficulty of T2 in repertoire for TS; use placeholder -1 if truly no T2.*
    *   Placeholder/Imputation for N/A (if N_Tasks=2 but difficulty unspecified): e.g., 0.5.

**II. Categorical PCA Features (One-Hot Encoded from SE-Mappable Categories):**

*Note: The `_Mapped` suffix indicates that these are the final categories used by the PCA pipeline after being processed by the mapping functions in `analysis_utils.py`.*

A. **`Stimulus_Valency_Mapped`**: Derived from `Stimulus Valency`. Categories: `SBC_Univalent`, `SBC_Bivalent_Congruent`, `SBC_Bivalent_Incongruent`, `SBC_Bivalent_Neutral`.

B. **`Response_Set_Overlap_Mapped`**: Derived from `Response Set Overlap`. Categories: `RSO_Identical`, `RSO_Disjoint`.
    *   Literature Categories (examples): "Identical", "Disjoint - Category (Same Modality)", "Disjoint - Effector (Same Modality)", "Disjoint - Modality (Standard/Non-Standard)", "N/A"
    *   SE-Mappable PCA Categories:
        *  `RSO_SE_Identical` (Maps from Lit: "Identical")
        *  `RSO_SE_Disjoint` (Maps from Lit: "`Disjoint - Category (Same Modality)`", "`Disjoint - Effector (Same Modality)`", "`Disjoint - Modality (Standard/Non-Standard)`" (This category acknowledges SE *cannot* do true modality disjoint like vocal vs manual. This PCA category would group all literature cases where responses are fundamentally different in modality/effector beyond simple key choices. For SE instantiation, these would *all* be mapped to different key groups, e.g., `a/d` vs `w/s`). This is a compromise.
        *  `RSO_SE_NA` (Maps from Lit: "N/A")

C.  **`Task_1_Stimulus-Response_Mapping_Mapped`**: Derived from `Task 1 Stimulus-Response Mapping`. Categories: `SRM_Compatible`, `SRM_Incompatible`, `SRM_Arbitrary`.
	*   **SE-Mappable PCA Categories:** These categories are directly SE-mappable as they define how the `keyMap` is configured in the Super Experiment.
        *   `SRM_SE_Compatible` (Lit: "Compatible" -> SE: `keyMap` aligns stimulus with spatially/semantically congruent response)
        *   `SRM_SE_Incompatible` (Lit: "Incompatible" -> SE: `keyMap` forces a crossed or counter-intuitive stimulus-response link)
        *   `SRM_SE_Arbitrary` (Lit: "Arbitrary" -> SE: `keyMap` is based on learned, non-prepotent associations; this is the typical setup for many tasks)

D.  **`Task_2_Stimulus-Response_Mapping_Mapped`**: Derived from `Task 2 Stimulus-Response Mapping`. Categories: `SRM2_Compatible`, `SRM2_Incompatible`, `SRM2_Arbitrary`.

E.  **`Task_1_Cue_Type_Mapped`**: Derived from `Task 1 Cue Type`. Categories: `TCT_Implicit`, `TCT_Arbitrary`
    *   Literature Categories: "None/Implicit", "Arbitrary_External", "Transparent_External", "N/A"
    *   SE-Mappable PCA Categories (SE's internal cue is always arbitrary; this focuses on *when* external info is available):
        *   `TCT_SE_None_Implicit` (Lit: "None/Implicit" -> SE: cue likely simultaneous with stim, CSI=0)
        *   `TCT_SE_Info_Precedes_Stim` (Lit: "Arbitrary_External", "Transparent_External" where CSI > 0 -> SE: CSI value respected)
        *   `TCT_SE_NA`
F.  **`Task_2_Cue_Type_Mapped`**: Derived from `Task 2 Cue Type`. Categories: `TCT2_Implicit`, `TCT2_Arbitrary`.
G. **`Trial_Transition_Type_Mapped`**: Derived from `Trial Transition Type`. Categories: `TTT_Pure`, `TTT_Switch`, `TTT_Repeat`.