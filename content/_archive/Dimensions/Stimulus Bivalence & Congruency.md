---
tags:
  - dimension
  - stimulus_property
---
NOTE: This dimension is being phased out in favor of the more granular [[Stimulus-Stimulus Congruency]] and [[Stimulus-Response Congruency]].
Definition: Describes the **relational property between a stimulus and the set of tasks currently active in an experimental block.** A stimulus is bivalent if it possesses features or affords operations that are relevant to **more than one** of the active task-sets. This property is the source of task ambiguity and is fundamental to creating cognitive conflict.

The theoretical basis for bivalence is rooted in the concept of "Dimensional Overlap" proposed by [[Kornblum et al. (1990)]]. They argued that a stimulus creates the potential for conflict when its representational dimensions overlap with the dimensions of the response set, which is the precondition for what we term bivalence.

---
###### Core Concepts:

*   **Valency (in the context of a task pool):**
    *   **Univalent Stimulus:** A stimulus that affords processing by only *one* of the active task rule sets.
        *   *Example:* In a block switching between a "Letter Task" and a "Digit Task," the stimulus "7" is univalent.
        *   *Inference Task Example:* A pure color patch in a Stroop experiment where word reading is also a possible task. The patch has no word feature, so it only affords the color-naming task.
        *   **Rule:** Univalent stimuli in an `Number of Tasks=1` paradigm have `SOA = N/A`.
    *   **Bivalent (or Multivalent) Stimulus:** A stimulus that either 1) affords processing by *two or more* of the active task rule sets, or 2) has an irrelevant feature that is the target for another highly-practiced or experimentally-relevant task. This feature **affords** the activation of the competing task-set, even if that set is not explicitly instructed for the current block. This is the case for classic interference paradigms where baseline blocks instruct participants to only do one task.
	    *  Classic Example 1: A task-switching paradigm where the participant sees a colored shape and must switch between naming the color or naming the shape. (`Number of Tasks=1`, `Switch_Rate=100%`, `Task_1_Type=Color Naming`, `Task_2_Type=Shape Naming`)
	    *  Classic Example 2: A task-switching paradigm of a Stroop task where the participant switches between ink color naming and color word reading. (`Number of Tasks=1`, `Switch_Rate=100%`, `Task_1_Type=Word Reading`, `Task_2_Type=Color Naming`)
	    *  Super Experiment Example: A dual-task paradigm where triangles are primarily moving to the left or right, and are primarily oriented up or down, and the participant must concurrently determine the motion of the triangles and their orientation. (`Number of Tasks=2`, `Task_1_Type=Movement Identification`, `Task_2_Type=Orientation Identification`)
	    *  Pure Block With Interference Example: A baseline Stroop task where the participant must only name the ink color of color words. (`Number of Tasks=1`, `Switch_Rate=0%`, `Task_1_Type=Color Naming`, `Task_2_Type=N/A`, `Response_Set_Overlap=N/A`)
        *   **Rule:** Bivalent stimuli in an `Number of Tasks=1` paradigm have a numerical `SOA` value (typically `0` for simultaneous feature presentation).
###### Types of Bivalence:

*   **1. Attribute-Based Bivalence (Decomposable Stimulus):** Conflict arises from multiple, separable perceptual attributes of a single object.
    *   *Example:* A **blue circle** when switching between a Color Task and a Shape Task. The `color` attribute is relevant to one task, and the `shape` attribute is relevant to the other. This maps cleanly to a "target vs. distractor" model.
    *   *Examples:* [[Canonical Tasks/Stroop Task|Stroop]], [[Canonical Tasks/Flanker Task|Flanker]], [[Canonical Tasks/Simon Task|Simon]].

*   **2. Operation-Based Bivalence (Non-Decomposable Stimulus):** Conflict arises when multiple task rules/operations can be applied to the *same single attribute*.
    *   *Example:* The number **"64"** when switching between an "Add the Digits" task and a "Multiply the Digits" task. The single attribute (number identity) affords two different transformations. The conflict is at a higher level of rule selection.
    *   *Example:* [[Jersild (1927)]]'s calculation tasks.

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