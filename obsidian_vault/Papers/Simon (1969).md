---
tags:
  - paper
  - simon_effect
  - s_r_compatibility
  - spatial_compatibility
  - attention
aliases:
  - Simon 1969
---
###### Core Goal
Simon (1969) aimed to investigate the fundamental nature of spatial stimulus-response (S-R) compatibility, specifically testing the hypothesis that there is a "natural" tendency to react *toward* the source of stimulation. This study sought to isolate this tendency by removing semantic content from the stimulus and directly manipulating the compatibility of the required S-R mapping.

###### Paradigm & Key Manipulations

*   **Paradigm:** A variant of the [[Simon Task]], focusing directly on spatial S-R mapping rules.
*   **Task:** Participants used their right hand to move a control handle to the right or left from a central midline position.
*   **Stimulus:** A 1000-cps monaural tone presented to either the right or left ear. The ear of presentation was the *relevant* cue for determining response direction.
*   **[[Stimulus Response Mapping|Stimulus Response Mapping]] (Key Manipulation):** Participants performed under two different instructional blocks:
    *   **"Toward" Condition (Compatible S-R Mapping):** Instructed to move the handle *toward* the side of the ear stimulated (e.g., tone in Right Ear → move handle Right; tone in Left Ear → move handle Left).
    *   **"Away" Condition (Incompatible S-R Mapping):** Instructed to move the handle *away* from the side of the ear stimulated (e.g., tone in Right Ear → move handle Left; tone in Left Ear → move handle Right).
*   **Procedure:** Each participant performed in both "Toward" and "Away" blocks (order counterbalanced). Within each block, tones were presented randomly to the right or left ear.

###### Key Findings

1.  **Effect of S-R Mapping Rule on Reaction Time (RT):** RT was significantly faster when participants were instructed to move the handle *toward* the source of stimulation (Compatible S-R mapping) compared to when instructed to move *away* from it (Incompatible S-R mapping).
    *   Mean RT Toward: 292 ms
    *   Mean RT Away: 351 ms
2.  **Movement Time (MT):** While RT was affected by the mapping rule, MT was not significantly different between the "Toward" and "Away" conditions. (There were other MT effects, e.g., leftward movements faster, males faster, but not related to the Toward/Away rule).
3.  **Robustness of Effect:** The effect of S-R mapping compatibility on RT was clear and significant, indicating a processing cost associated with overriding the "natural" tendency to respond toward the stimulus source.

###### Authors' Conclusions & Interpretations

1.  **Natural Tendency to Respond Toward Stimulus Source:** The results strongly support the existence of a "natural" tendency to orient or react spatially congruently with the source of stimulation.
2.  **Cost of Overriding Stereotype:** The slower RTs in the "Away" (incompatible) condition reflect the cognitive effort or time required to override this prepotent "Toward" tendency and execute the instructed, less natural response.
3.  **Mechanism for Simon Effect:** This inherent spatial S-R compatibility is proposed as a key mechanism underlying the classic Simon effect (as seen in [[Simon & Rudell (1967)]]), where an *irrelevant* stimulus location interferes with responses to a non-spatial feature. The 1969 study demonstrates the cost of violating this compatibility even when location *is* relevant.
4.  **Orienting Reflex Manifestation:** The interference observed could be a manifestation of the orienting reflex (OR), which can involve a molar reaction of turning toward a stimulus.

###### Relevance to Thesis & Mapping Notes

*   **Clarifies S-R Compatibility Mechanism:** This study provides strong evidence for the direct impact of spatial S-R mapping rules on performance, isolating it from semantic stimulus content.
*   **Informs [[Stimulus Response Mapping]] Dimension:** A prime example for coding the  `Stimulus Response Mapping` column in the CSV (with values "Compatible" for "Toward" and "Incompatible" for "Away").
*   **Distinction from Classic Simon Effect Paradigm:** While related, this design differs from [[Simon & Rudell (1967)]] in that stimulus location is *task-relevant*. The interference arises from the *rule* rather than an *irrelevant stimulus dimension*.
*   **Mapping to SE:**
    *   [[Number of Tasks|Number of Tasks]]: 1.
    *   [[Stimulus Bivalence & Congruency|Stimulus Valency]]: `Univalent` (the tone itself doesn't have conflicting features; the conflict is rule-based).
    *   The core manipulation is modeled in SE by altering the `keyMap` (e.g., `movementKeyMap`) between blocks.
        *   "Toward": `stim_LeftEar` maps to `left_response_key`; `stim_RightEar` maps to `right_response_key`.
        *   "Away": `stim_LeftEar` maps to `right_response_key`; `stim_RightEar` maps to `left_response_key`.
    *   [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]]: N/A. [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0. [[Dimensions/Switch Rate|Switch Rate]]: 0%.
    *   [[Dimensions/Task Difficulty|Task 1 Difficulty]]: Low (e.g., '1' or '2' for simple tone localization determining a 2-choice response).
*   Supports the idea that some forms of "conflict" or "incongruency" in cognitive tasks are not solely stimulus-driven but can be induced by the demands of the S-R mapping rule itself.

---