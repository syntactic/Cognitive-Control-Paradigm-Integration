---
tags:
  - dimension
  - stimulus_property
---
**Stimulus Bivalence & Congruency** describes the relational property between a stimulus and active task-sets. A stimulus is bivalent if it possesses features or affords operations relevant to multiple active task-sets, creating task ambiguity and cognitive conflict.

**Theoretical Basis:** Rooted in "Dimensional Overlap" from [[Kornblum et al. (1990)]] - stimuli create conflict potential when representational dimensions overlap with response dimensions.

**Operational Note:** This dimension is derived by collapsing [[Dimensions/Stimulus-Stimulus Congruency]] and [[Dimensions/Stimulus-Response Congruency]] in convert.py/analysis_utils.py, as both dimensions yield similar PCA results. This unified dimension is used for analysis and visualization.

---
###### Core Concepts:

**Valency:**
- **Univalent:** Affords processing by only one active task rule set
  - Examples: Digit "7" in Letter/Digit switching; pure color patch in Stroop
  - **Rule:** SOA = N/A in single-task paradigms
- **Bivalent:** Affords processing by multiple task rule sets or has irrelevant feature targeting competing task
  - Task-switching: Colored shape for color/shape tasks
  - Interference: Stroop word for color naming  
  - Dual-task: Triangle with motion and orientation features
  - **Rule:** Numerical SOA (typically 0 for simultaneous features)
**Types of Bivalence:**

1. **Attribute-Based (Decomposable):** Multiple separable perceptual attributes
   - Example: Blue circle in color/shape switching
   - Tasks: [[Canonical Tasks/Stroop Task|Stroop]], [[Canonical Tasks/Flanker Task|Flanker]], [[Canonical Tasks/Simon Task|Simon]]

2. **Operation-Based (Non-Decomposable):** Multiple operations on same attribute  
   - Example: Number "64" for add/multiply digits ([[Jersild (1927)]])

*   **Congruency (Stimulus-Response Relationship in Context):** Applies to **bivalent** stimuli when the different features or afforded tasks lead to particular S-R outcomes *within the current task context*.
    *   **Inter-Task Congruency ([[Super Experiment Framework]] Focus):** Arises when two distinct tasks are defined (e.g., SE's 'mov' and 'or'), and the response dictated by one task's processing (e.g., for `stim_mov_1`) aligns or conflicts with the response dictated by the other task's processing (e.g., for `stim_or_1`).
    *   **Intra-Task S-R Congruency (Classic Interference Task Focus):** Arises in single-task contexts (e.g., Flanker, Stroop) where an irrelevant dimension of the stimulus array (e.g., flanker identity, word meaning) would, *if it were the target for the current task rule*, lead to the same or a different response as the actual target.

###### Key Categories for Literature Coding:

*   **Univalent:**
    *   The stimulus (or relevant part of it) only affords one interpretation or maps to only one relevant task/response dimension in the current context.
    *   Often used in control conditions (e.g., "target alone" in Flanker, non-color words or meaningless symbols in Stroop controls).
    *   *SE Mapping:* Typically involves one SE pathway active (`coh_1=1.0`) and the other inactive (`coh_2=0.0`) or presenting unrelated information.

*   **Bivalent-Congruent:**
    *   Multiple relevant features/afforded tasks lead to the *same* response decision or category.
    *   *Example (Stroop):* Word "RED" in red ink for color naming.
    *   *Example (Flanker - Identity):* Target H, Flankers HHHHHHH. (Flanker is identical and affords same response).
    *   *Example (Flanker - ResponseSet):* Target H, Flankers KKKHKKK (where H and K map to the same response key). (Flanker is different but affords same response).
    *   *SE Mapping (Inter-Task Style):* `stim_mov_1` and `stim_or_1` both map to the same response output (e.g., "left").

*   **Bivalent-Incongruent:**
    *   Multiple relevant features/afforded tasks lead to *different/conflicting* response decisions or categories.
    *   *Example (Stroop):* Word "RED" in blue ink for color naming.
    *   *Example (Flanker):* Target H, Flankers SSSHSSS (where H and S map to different response keys).
    *   *SE Mapping (Inter-Task Style):* `stim_mov_1` maps to one response (e.g., "left") and `stim_or_1` maps to a different response (e.g., "right").

*   **Bivalent-Neutral:**
    *   The stimulus is bivalent, but the irrelevant dimension(s) or afforded task(s) do not map to a response within the current task's primary response set, or they prime competing responses equally, resulting in no net bias. This serves as a critical baseline.
    *   **Types of Neutrality observed in literature:**
        *   **Orthogonal/Unrelated Feature:** The irrelevant dimension is unrelated to the response categories of the primary task.
            *   *Example (Stroop):* Word "TABLE" (or "XXXXX") in blue ink, for color naming. The word itself doesn't map to "red," "blue," or "green."
            *   *Example (Task Switching - Meiran 1996):* When judging Left/Right position of a dot, its Up/Down position is an orthogonal, neutral feature.
            *   *Example (Flanker):* Target H, Flankers +++++++.
        *   **Feature-Based Neutrality (e.g., [[Eriksen & Eriksen 1974]]):**
            *   *FeatureSimilar:* Flankers share abstract features with the target's response set but aren't actual members of it (e.g., for target H/K, flankers N,W,Z).
            *   *FeatureDissimilar:* Flankers share abstract features with the *non-target* response set.
        *   **Balanced Priming:** An irrelevant feature primes multiple responses equally (e.g., a double-headed arrow `<-->` as a flanker in a left/right arrow task).
    *   *SE Mapping (Typical for Orthogonal/Unrelated):* Target pathway active (e.g., `mov`). Distractor pathway (e.g., `or`) presents a stimulus whose S-R mapping does not conflict with the target pathway's S-R set (e.g., `stim_or_1` maps to an unused response key, or if SE represented orthogonal dimensions more directly). For E&E's feature-based neutrals, SE mapping is an abstraction (see specific paper notes).

###### Relevance to Design Space & SE Mapping:

*   Central to all [[Interference Control]] paradigms (Stroop, Flanker, Simon).
*   Important for understanding [[Effects/Mixing Cost]] and some aspects of [[Effects/Switch Cost]] in [[Task Switching]] when bivalent stimuli are used.
*   SE models bivalence/congruency primarily through its two task pathways (`mov`, `or`). A single-task interference paradigm (like Flanker) is mapped by assigning the target to one pathway and the distractor/flanker information to the other, with [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]]=0. Congruency then depends on how the stimuli for these two pathways map to responses (often via shared `keyMap`s).
*   The specific *type* of neutrality (orthogonal, feature-based) can be difficult to distinguish with SE's current abstract parameters, often requiring simplification to a general "orthogonal/non-competing distractor" model.