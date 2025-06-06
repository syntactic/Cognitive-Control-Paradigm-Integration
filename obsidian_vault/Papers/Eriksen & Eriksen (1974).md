---
tags:
  - paper
  - flanker_task
  - interference
  - attention
aliases:
  - Eriksen & Eriksen 1974
---

###### Core Goal
Eriksen & Eriksen (1974) investigated the impact of flanking "noise" letters on reaction time (RT) for identifying a central target letter in a non-search task (target location was fixed and known). The study aimed to determine how noise letter type (response compatible or incompatible) and the spatial separation between letters influence target identification.

###### Paradigm & Key Manipulations

*   **Paradigm:** [[Flanker Task]] (non-search variant).
*   **Task:** Participants performed a two-choice (left/right) lever-press response to a central target letter (H/K vs. S/C).
*   **Target Location:** Consistently 0.5 degrees visual angle above fixation.
*   **Noise Array:** The target was flanked by three noise letters on each side.
*   **Stimulus Exposure:** 1-second tachistoscopic presentation.

**Key Independent Variables:**

1.  **Noise Type (Response Compatibility of Flankers):**
    *   **1. Noise Same as Target:** Flankers identical to the target (e.g., HHHHHHH for target H). *CSV Valency: `Bivalent-Congruent (Identical)`*
    *   **2. Noise Response Compatible:** Flankers were the other letter from the target's response set (e.g., KKKHKKK for target H). *CSV Valency: `Bivalent-Congruent (ResponseSet)`*
    *   **3. Noise Response Incompatible:** Flankers from the opposing response set (e.g., SSSHSSS for target H). *CSV Valency: `Bivalent-Incongruent`*
    *   **4. Noise Heterogeneous-Similar:** Flankers shared visual features with the target's response set but were not members (e.g., N, W, Z for H/K). *CSV Valency: `Bivalent-Neutral (FeatureSimilar)`*
    *   **5. Noise Heterogeneous-Dissimilar:** Flankers shared visual features with the *opposite* target response set. *CSV Valency: `Bivalent-Neutral (FeatureDissimilar)`*
2.  **Between-Letter Spacing:** Varied at three levels: ~0.06 deg (closest), 0.5 deg, and 1.0 deg.
3.  **Control Conditions (Target Alone):**
    *   **Target Alone - Mixed:** Single target presented, intermixed randomly with noise trials. *CSV Valency: `Univalent`*
    *   **Target Alone - Blocked:** Single target presented in dedicated blocks with no expectation of noise. *CSV Valency: `Univalent`*

###### Key Findings

1.  **Spacing Effect:** RT decreased as letter spacing increased across all noise conditions. Differences between noise conditions were most pronounced at the closest spacing.
2.  **Noise Compatibility:** Incompatible noise letters yielded significantly longer RTs than other noise types. "Noise Same as Target" and "Noise Response Compatible" conditions produced similar RTs.
3.  **Heterogeneous Noise Effects:** These conditions resulted in intermediate RTs. At wider spacings, "dissimilar" heterogeneous noise led to longer RTs than "similar" heterogeneous noise.
4.  **Control Condition Performance:** RTs to target-alone presentations were significantly faster (by ~30ms) in the blocked condition compared to the mixed condition.
5.  **Error Patterns:** Error rates generally paralleled RT findings, with the highest error rates for incompatible noise at close spacing.

###### Authors' Conclusions & Interpretations

1.  **Limits of Selective Attention:** Processing of noise letters within ~1 degree of the target cannot be entirely suppressed, even with a known target location.
2.  **Minimum Channel Capacity:** The visual processing channel has a minimum capacity that exceeds what is needed for a single letter; nearby letters are processed concurrently.
3.  **Locus of Interference at Response Selection:** The pronounced effect of noise response compatibility suggests that interference primarily occurs at the response selection stage due to competition from responses activated by the flankers.
4.  **Role of Inhibition and Spatial Discrimination:** An inhibitory mechanism is required to prevent responses to flankers, and response selection depends on spatial discrimination of the target. This discrimination is less efficient at closer spacings and when flankers prime conflicting responses.
5.  **Preparatory Set for Inhibition:** The advantage in the "target alone - blocked" condition indicates that the inhibitory process can be modulated or disengaged when no noise is anticipated.

###### Relevance to Thesis & Mapping Notes

*   **Foundational Study:** Establishes key characteristics of the flanker effect and the impact of flanker-target spacing and response compatibility.
*   **[[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]]:** Provides clear operationalizations of congruent, incongruent, and different types of neutral flanker conditions.
*   **Parameter for Spacing:** Systematically varied letter spacing, a critical physical parameter.
*   **Neutral Condition Varieties:** The "Heterogeneous-Similar" and "-Dissimilar" conditions exemplify early attempts to create neutral flankers based on feature overlap, distinct from simple unrelated symbols.
*   **SE Mapping Considerations:**
    *   [[Dimensions/N_Tasks|N_Tasks]]: 1.
    *   [[Dimensions/SOA (Stimulus Onset Asynchrony)|SOA]]: 0 (conceptual, flankers as simultaneous attribute) or N/A.
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0.
    *   The effect of `Letter Spacing` is coded in the CSV using a float `Task 1 Difficulty`, which is then translated to influence `coh_mov_1` (target pathway coherence) in SE.
    *   Flanker presence and type are mapped to the `or` pathway in SE (`stim_or_1`, with `coh_or_1=1.0`). Congruency/incongruency arises from the S-R mapping of `stim_mov_1` vs. `stim_or_1`.
    *   SE's abstraction means `Bivalent-Neutral (FeatureSimilar)` and `(FeatureDissimilar)` would both likely map to SE's standard "orthogonal/non-competing distractor" configuration, with the specific feature-based distinction noted as a limitation of SE's direct modeling capability.

---