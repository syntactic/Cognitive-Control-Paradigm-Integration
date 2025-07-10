---
tags:
  - paper
  - simon_task
  - neutral_condition
  - interference
  - sr_compatibility
  - ideomotor_theory
aliases:
  - Hommel 1993
---
###### Core Goal
To test an "intentional approach" to the [[Canonical Tasks/Simon Task|Simon effect]], proposing that the direction of the effect is determined not by the physical location of the response key or hand, but by the spatial code of the *intended action goal*. The study aimed to show that by manipulating instructions, an identical physical action could produce either a standard or an inverted Simon effect.

###### Paradigm & Key Manipulations

*   **Paradigm:** A variant of the [[Canonical Tasks/Simon Task|Simon task]] where the action (a keypress) produces a distal effect (a light turning on).
*   **Task:** Participants responded to high or low pitched tones with a left or right keypress.
*   **Physical Setup:** The response keys and the feedback lights could be in a parallel (left key -> left light) or inverse (left key -> right light) mapping.
*   **Key Manipulation (Instructional Framing / Stimulus-Response Mapping):** The critical manipulation was the instruction given to participants, which framed their action goal differently.
    *   **Key Instruction (KI):** Participants were told to "press the left/right key." Here, the intended action goal is the proximal keypress. The location of the feedback light is irrelevant to the goal.
    *   **Light Instruction (LI):** Participants were told to "produce the left/right light." Here, the intended action goal is the distal light effect. The location of the key is merely a means to an end.
*   **Congruency Conditions:**
    *   **Congruent (S=Key):** Tone location matched the location of the *correct response key*.
    *   **Incongruent (S≠Key):** Tone location was opposite to the location of the *correct response key*.
    *   **Neutral (N):** Tone was presented from both speakers simultaneously, creating a fused central percept.

###### Key Findings (Experiment 1)

*   **Standard Simon Effect (Key Instruction):** When instructed to press keys (Group KI-IM), participants showed a standard Simon effect. RTs were faster when stimulus location corresponded to key location (S=Key) and slower when it was opposite (S≠Key), relative to neutral.
    *   RTs: S=Key (406ms) < Neutral (440ms) < S≠Key (458ms).
*   **Inverted Simon Effect (Light Instruction):** When instructed to produce lights (Group LI-IM), with an *inverse* key-light mapping (left key -> right light), the Simon effect was inverted. RTs were now faster when the stimulus location corresponded to the *light location*, not the key location. This meant responses were fastest when the tone was on the opposite side of the required key (S≠Key).
    *   RTs: S≠Key (399ms) < Neutral (409ms) < S=Key (429ms).
*   **Conclusion:** The direction of the Simon effect depended entirely on the instructed action goal (key vs. light), not the physical movement itself. This supports the intentional approach.
*   **R-Value Calculation:**
    *   For KI-IM (standard): R = (RTN - RTC) / (RTI - RTN) = (440-406)/(458-440) = 34 / 18 ≈ **1.89**. This is a classic R > 1 pattern for a Simon task.
    *   For LI-IM (inverted): Here, "congruent" is S≠Key and "incongruent" is S=Key. R = (RTN - RTC) / (RTI - RTN) = (409-399)/(429-409) = 10 / 20 = **0.5**. This is an R < 1 pattern.

###### Authors' Conclusions & Interpretations

*   The Simon effect is not tied to an invariant response feature like effector location but is determined by the "goal-defining response feature" – whatever the participant intends to do.
*   Actions are coded in the cognitive system in terms of their intended, perceivable effects (a core idea of ideomotor theory).
*   The irrelevant stimulus location automatically primes actions whose intended effects are spatially congruent with it.
*   The results support an "intentional-coding approach" where the cognitive representation of an action is flexible and dependent on the actor's goals.

###### Relevance to Thesis & Mapping Notes

*   **Crucial for [[Dimensions/Stimulus Response Mapping|Stimulus Response Mapping]]:** This paper is a cornerstone for the SRM dimension. It provides one of the clearest demonstrations that the S-R compatibility rule is not fixed but can be defined by instruction and intention, leading to `Compatible` or `Incompatible` effects for the same physical action.
*   **Refines "Response":** Challenges a simple view of "response" as just a keypress and forces consideration of distal action effects as part of the response representation.
*   **Neutral Condition:** The use of binaural tones for a neutral condition is a standard and effective method. The fact that the RT pattern (R>1 vs R<1) changes with instruction is a powerful finding.
*   **SE Mapping Considerations:**
    *   [[Number of Tasks|Number of Tasks]]: 1.
    *   The core manipulation between groups is not a parameter within a single SE trial but a difference in the *interpretation* of the task, which maps to our `Stimulus Response Mapping` dimension.
    *   For SE instantiation, the **physical setup is identical** for the KI-IM and LI-IM groups. The difference lies in what defines "congruent" vs. "incongruent" for analysis.
    *   In SE, the task would be modeled as Target=Tone Pitch, Distractor=Tone Location.
    *   For the KI-IM group (`SRM=Compatible` relative to the keypress), an SE stimulus on the left (`stim_or=left`) is congruent with a left keypress (`keyMap`).
    *   For the LI-IM group (`SRM=Incompatible` relative to the keypress), an SE stimulus on the left (`stim_or=left`) is now congruent with a *right* keypress, because that keypress produces the intended *left light*. This is a compatibility between the stimulus and the *distal goal*.