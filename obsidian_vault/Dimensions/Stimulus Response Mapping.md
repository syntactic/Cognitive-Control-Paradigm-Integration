---
tags:
  - dimension
  - sr_mapping
  - cognitive_control
aliases:
  - S-R Mapping Type
  - Stimulus-Response Compatibility Rule
---
###### Definition
**Stimulus Response Mapping (SRM)** refers to the specific rule set that dictates how a given stimulus (or a feature of it) should be translated into a particular response. This dimension primarily concerns the *nature* of this instructed S-R relationship, particularly whether it aligns with or opposes pre-existing, "natural," or highly learned tendencies.

While related to [[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]] (which deals with conflict/alignment *between stimulus features*), SRM focuses on the compatibility of the *overall instructed S-R rule itself*.

###### Key Values / Categories:

*   **`Compatible`:**
    *  The instructed S-R mapping aligns with a strong natural tendency, a highly overlearned association, or a direct, intuitive relationship between stimulus and response.
    *  Often results in faster and more accurate performance.
    * Compatibility can be defined relative to the proximal motor action (e.g., keypress location) or a distal action goal (e.g., the location of a resulting visual effect, as in [[Hommel (1993)]]). However for this study I'm focusing strictly on the relationship between the relevant attribute of the stimulus and the response in its most proximal form - not a distal action goal / effect of a response.
    *   *Example:* Responding with a right-hand key to a stimulus appearing on the right (spatial compatibility, as in the "Toward" condition of [[Simon (1969)|Simon 1969]]).
    *   *Example:* Pressing an "up arrow" key when the word "UP" is displayed.

*   **`Incompatible`:**
    *   The instructed S-R mapping opposes a strong natural tendency, a highly overlearned association, or requires an counter-intuitive translation between stimulus and response.
    *   Often results in slower RTs, increased errors, and a subjective feeling of difficulty, reflecting the need to overcome the prepotent compatible tendency.
    *   *Example:* Responding with a left-hand key to a stimulus appearing on the right (spatial incompatibility, as in the "Away" condition of [[Simon (1969)|Simon 1969]]).
    *   *Example:* Pressing a "down arrow" key when the word "UP" is displayed.

*   **`Arbitrary`:**
    *   The S-R mapping has no pre-existing intuitive or natural basis; it must be learned explicitly for the task and does not strongly align with or oppose a prepotent tendency. This is common for many experimental tasks.
    *   *Example:* Pressing the 'J' key for a picture of a cat and the 'F' key for a picture of a dog.
    *   *Example:* Mapping colors to arbitrary keypresses in many Stroop or task-switching paradigms.
    *   This is often the default or most common type of mapping in controlled experiments where specific pre-existing compatibilities are not the primary focus.

*   **(Potentially) `Learned/Overlearned`:** A sub-type of `Compatible` or `Arbitrary` that has become highly automatized through extensive specific practice, even if initially arbitrary. This might interact with compatibility effects when switching from/to such tasks. (Consider if this level of detail is needed).

*   **(Potentially) `N/A`:** If the concept isn't applicable (e.g., detection tasks with a single response, or if other dimensions fully capture the S-R relationship without needing this specific classification).

###### Relevance to Design Space & Cognitive Control:

*   **Fundamental Aspect of Task Definition:** The SRM rule is a core component of defining any task.
*   **Source of Conflict/Interference:** Incompatible SRM is a direct source of cognitive conflict, requiring increased cognitive control to suppress the "natural" response and execute the "unnatural" one. This cost is often additive to other sources of conflict (e.g., stimulus incongruency).
*   **Investigating Automaticity and Inhibition:** Comparing performance under compatible vs. incompatible mappings helps reveal the strength of automatic S-R associations and the efficiency of inhibitory control.
*   **Interaction with Other Dimensions:**
    *   Can interact with [[Dimensions/Task Difficulty|Task Difficulty]]: An intrinsically easy task can become difficult if given an incompatible SRM.
    *   Can be the defining feature that differentiates "tasks" in some [[Task Switching]] paradigms (e.g., switch from "respond compatibly" to "respond incompatibly").
*   **Modulating the Simon Effect:** As seen in [[Simon (1969)|Simon 1969]], directly manipulating SRM compatibility (Toward vs. Away) for a *relevant* spatial stimulus produces an effect analogous to the classic Simon effect (where an *irrelevant* spatial stimulus feature influences response).

###### Super Experiment Mapping:

*   This dimension is primarily implemented in the Super Experiment by configuring the **`keyMap`** objects (`movementKeyMap`, `orientationKeyMap`).
*   **Compatible Mapping:** The `keyMap` links stimulus values to responses in a "natural" or direct way (e.g., stimulus 'left_ear_tone' maps to 'left_key').
*   **Incompatible Mapping:** The `keyMap` links stimulus values to responses in a "crossed" or counter-intuitive way (e.g., stimulus 'left_ear_tone' maps to 'right_key').
*   **Arbitrary Mapping:** The `keyMap` links stimulus values to response keys based on arbitrary assignment for the experiment.