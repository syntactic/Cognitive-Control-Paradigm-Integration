#methodology #pca 
This note lists the features intended for input into the Principal Component Analysis (PCA). These features are derived from the master literature coding CSV file. Derived dimensions from the literature are mapped to a reduced set of categories that reflect distinctions achievable or most relevant within the Super Experiment (SE) framework. This mapping is an explicit step in the data processing pipeline.

**I. Numerical PCA Features (Standardized - e.g., Z-scored):**

1.  **`N_Tasks_PCA`** (Numeric: 1 or 2)
    *   Directly from CSV `Number of Tasks`.
2.  **`SOA_ms_PCA`** (Numeric: ms)
    *   From CSV `SOA`.
    * If `Number of Tasks` == 2: this is the standard interpretation for PRP, indicating the delay between stimulus for task 1 and stimulus for task 2.
    *  If `Number of Tasks` == 1: this is a special case for single-task paradigms with interference. A distractor stimulus appears at this SOA but the subject is expected to only perform one task in the trial. This happens in [[Yeung & Monsell (2003)]]. This is `0` for bivalent stimuli with simultaneous features and a `+/-` value for asynchronous features.
    *   Placeholder/Imputation for N/A: Code `N/A` as **-1**. It distinguishes univalent trials (where SOA is not applicable) from bivalent trials with simultaneous distractors (`SOA = 0`)
3.  **`CSI_ms_PCA`** (Numeric: ms)
    *   From CSV `CSI`.
    *   Placeholder/Imputation for N/A: I don't think this would ever occur, so there shouldn't be a need to impute values. (implicit cue = 0 CSI).
4.  **`RSI_ms_PCA`** (Numeric: ms)
    * From CSV `RSI`.
    * The `Super_Experiment_Mapping_Notes` may indicate a more accurate idea of how RSI might have been manipulated in an experiment (see [[Stephan & Koch (2010)]] for example). It might indicate that the RSI is drawn from a distribution. In that case, the CSV's `RSI` value is the expected value of that distribution.
    * Placeholder/Imputation for N/A or "Not Specified": e.g., median of observed RSIs, or a fixed value representing a common ITI.
5.  **`Switch_Rate_percent_PCA`** (Numeric: 0-100)
    *   From CSV `Switch Rate`.
    *   Placeholder/Imputation for N/A: 0. This shouldn't practically be N/A. If we're in a single-task paradigm there either is a switch (mixed block) or never a switch. If we're in a dual-task paradigm then the task order could switch such as in [[Sigman & Dehaene (2006)]].
6.  **`Task1_Difficulty_Normalized_PCA`** (Numeric: 0-1)
    *   Derived from CSV `Task 1 Difficulty` (1-5 ordinal) -> (value-1)/4.
    *   Placeholder/Imputation for N/A: e.g., 0.5 (moderate difficulty).
7.  **`Task2_Difficulty_Normalized_PCA`** (Numeric: 0-1)
    *   Derived from CSV `Task 2 Difficulty` (1-5 ordinal) -> (value-1)/4.
    *   If `Number of Tasks` = 1 (for that row/condition), this feature is set to a distinct placeholder (e.g., -1) or imputed based on context (e.g. if it's a TS paradigm, it's the difficulty of the *other* task in repertoire). *Current preference: Use actual difficulty of T2 in repertoire for TS; use placeholder -1 if truly no T2.*
    *   Placeholder/Imputation for N/A (if N_Tasks=2 but difficulty unspecified): e.g., 0.5.

**II. Categorical PCA Features (One-Hot Encoded from SE-Mappable Categories):**

For each categorical dimension, literature values are first mapped to an SE-Mappable category, then one-hot encoded.

A.  **`Stimulus_Bivalence_Congruency` (from CSV `Stimulus Valency`) -> SE-Mappable for PCA:**
    *   Literature Categories: "Univalent", "Bivalent-Congruent", "Bivalent-Neutral", "Bivalent-Incongruent", "N/A"
    *   SE-Mappable PCA Categories (these are all distinct and SE can generally model the stimulus side; response conflict depends on RSO):
        *   `SBC_Univalent`
        *   `SBC_Bivalent_Congruent`
        *   `SBC_Bivalent_Neutral`
        *   `SBC_Bivalent_Incongruent`
        *   (`SBC_NA` column will exist if NAs are present after mapping, or NAs result in all zeros for other SBC columns).
    *   One-Hot Encoded PCA Features: `SBC_Univalent`, `SBC_Bivalent_Congruent`, `SBC_Bivalent_Neutral`, `SBC_Bivalent_Incongruent`.

B.  **`Response_Set_Overlap` -> SE-Mappable for PCA:**
    *   Literature Categories (examples): "Identical", "Disjoint - Category (Same Modality)", "Disjoint - Effector (Same Modality)", "Disjoint - Modality (Standard/Non-Standard)", "N/A"
    *   SE-Mappable PCA Categories:
        *  `RSO_SE_Identical` (Maps from Lit: "Identical")
        *  `RSO_SE_Disjoint` (Maps from Lit: "`Disjoint - Category (Same Modality)`", "`Disjoint - Effector (Same Modality)`", "`Disjoint - Modality (Standard/Non-Standard)`" (This category acknowledges SE *cannot* do true modality disjoint like vocal vs manual. This PCA category would group all literature cases where responses are fundamentally different in modality/effector beyond simple key choices. For SE instantiation, these would *all* be mapped to different key groups, e.g., `a/d` vs `w/s`). This is a compromise.
        *  `RSO_SE_NA` (Maps from Lit: "N/A")
    *   One-Hot Encoded PCA Features: `RSO_SE_Identical`, `RSO_SE_Disjoint`

C.  **`Task_Cue_Type_External` (from CSV `Task Cue Type`) -> SE-Mappable for PCA:**
    *   Literature Categories: "None/Implicit", "Arbitrary_External", "Transparent_External", "N/A"
    *   SE-Mappable PCA Categories (SE's internal cue is always arbitrary; this focuses on *when* external info is available):
        *   `TCT_SE_None_Implicit` (Lit: "None/Implicit" -> SE: cue likely simultaneous with stim, CSI=0)
        *   `TCT_SE_Info_Precedes_Stim` (Lit: "Arbitrary_External", "Transparent_External" where CSI > 0 -> SE: CSI value respected)
        *   `TCT_SE_NA`
    *   One-Hot Encoded PCA Features: `TCT_SE_None_Implicit`, `TCT_SE_Info_Precedes_Stim`. (If CSI=0 for an external cue, it might fall into `None_Implicit` effectively for SE timing, or a third category `TCT_SE_Info_Simultaneous_Stim`).
        *Given CSI_ms_PCA is a numerical feature, perhaps one-hot encoding Task Cue Type for PCA is less critical if CSI captures the main timing variance. If the *nature* (Arbitrary vs Transparent) of external cues is thought to have effects SE can't model but we want in PCA, then keep more distinct categories.*
D.  **`Stimulus_Response_Mapping` (from CSV `Stimulus Response Mapping`) -> SE-Mappable for PCA:**
    *   **Literature Categories (from CSV):** "`Compatible`", "`Incompatible`", "`Arbitrary`", (potentially "`N/A`")
    *   **SE-Mappable PCA Categories:** These categories are directly SE-mappable as they define how the `keyMap` is configured in the Super Experiment.
        *   `SRM_SE_Compatible` (Lit: "Compatible" -> SE: `keyMap` aligns stimulus with spatially/semantically congruent response)
        *   `SRM_SE_Incompatible` (Lit: "Incompatible" -> SE: `keyMap` forces a crossed or counter-intuitive stimulus-response link)
        *   `SRM_SE_Arbitrary` (Lit: "Arbitrary" -> SE: `keyMap` is based on learned, non-prepotent associations; this is the typical setup for many tasks)
    *   **One-Hot Encoded PCA Features:** `SRM_SE_Compatible`, `SRM_SE_Incompatible`. Arbitrary is represented by 0 values for those two columns.