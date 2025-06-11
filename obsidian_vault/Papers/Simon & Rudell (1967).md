---
tags:
  - paper
  - simon_effect
  - s_r_compatibility
  - attention
  - auditory_processing
aliases:
  - Simon & Rudell 1967
---
###### Core Goal
Simon & Rudell (1967) aimed to demonstrate the existence of a strong auditory S-R compatibility effect, where an irrelevant directional cue (the ear in which an auditory command was presented) would influence the speed of responding to the semantic content of that command. They investigated whether this effect, later known as the Simon effect, persisted even when uncertainty about the stimulus source was removed.

###### Paradigm & Key Manipulations

*   **Paradigm:** Auditory [[Simon Task]].
*   **Task:** Participants performed a two-choice reaction time task, pressing a right-hand key in response to the spoken word "right" and a left-hand key in response to the spoken word "left."
*   **Stimulus Presentation:** Verbal commands ("right" or "left") were presented monaurally (to either the right or left ear) through earphones.
*   **Irrelevant Cue:** The ear of presentation was irrelevant to determining the correct key press (which depended solely on the word's meaning).

**Key Independent Variables & Experimental Conditions:**

1.  **Congruency (Command Meaning vs. Ear of Presentation):**
    *   **Congruent:** The semantic content of the command corresponded spatially with the ear of presentation (e.g., word "right" presented to the Right Ear; word "left" presented to the Left Ear).
    *   **Incongruent:** The semantic content of the command conflicted spatially with the ear of presentation (e.g., word "right" presented to the Left Ear; word "left" presented to the Right Ear).
2.  **Certainty of Stimulus Source (Experiment I vs. Experiment II):**
    *   **Experiment I:** The ear of presentation for each command was random and unpredictable to the participant.
    *   **Experiment II:** Trials were blocked by ear of presentation; participants knew in advance which ear would receive the command for an entire block.

###### Key Findings

1.  **Simon Effect (Experiment I - Uncertain Source):**
    *   RT was significantly faster when the (irrelevant) ear of presentation was congruent with the semantic content of the command and the required response hand, compared to when it was incongruent.
    *   For example, responding to "right" was faster when heard in the right ear than in the left ear.
2.  **Persistence of Simon Effect (Experiment II - Certain Source):**
    *   The Simon effect (faster RTs for congruent ear-command pairings) remained significant even when participants knew in advance which ear would be stimulated.
    *   However, the magnitude of the Simon effect was reduced in Experiment II (26ms difference between compatible and incompatible) compared to Experiment I (42ms difference).
3.  **Overall RT Reduction with Certainty:** Participants responded significantly faster overall in Experiment II (certain source) compared to Experiment I (uncertain source).

###### Authors' Conclusions & Interpretations

1.  **Strong Natural Tendency (Population Stereotype):** There is a robust natural tendency to associate right-ear stimulation with a right-hand response and left-ear stimulation with a left-hand response.
2.  **Interference from Irrelevant Cue:** When conflict exists between the symbolic cue (word meaning) and the irrelevant directional cue (ear stimulated), a marked delay in responding occurs. This suggests participants must inhibit the stereotypic directional response before reacting to the symbolic content.
3.  **Potency of the Irrelevant Cue:** The irrelevant ear cue is influential, particularly when the source is uncertain. Removing this uncertainty reduces, but does not eliminate, the effect, indicating the automaticity of this S-R compatibility.
4.  **Implications for Auditory Displays:** The findings highlight the importance of considering inherent S-R compatibilities in the design of auditory displays, as irrelevant spatial cues can significantly impact information processing.

###### Relevance to Thesis & Mapping Notes

*   **Foundational Simon Effect Study:** This paper is a key early demonstration of the Simon effect, illustrating interference from an irrelevant spatial stimulus feature on a non-spatial task.
*   **[[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]]:** Provides a clear example of `Bivalent-Congruent` and `Bivalent-Incongruent` conditions based on the alignment of the irrelevant spatial cue (ear) with the relevant semantic cue (word meaning).
*   **Mapping to SE:**
    *   [[Dimensions/N_Tasks|N_Tasks]]: 1.
    *   [[Dimensions/SOA (Stimulus Onset Asynchrony)|SOA]]: 0 (conceptual, as ear and word are part of the same auditory event) or N/A.
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0.
    *   Relevant dimension (word meaning) maps to one SE pathway (e.g., `mov`). Irrelevant dimension (ear of presentation) maps to the other SE pathway (e.g., `or`).
    *   Congruency in SE arises if `stim_mov_1` (e.g., representing "word right" -> "respond right") and `stim_or_1` (e.g., representing "right ear" -> "respond right") map to the same response. Incongruency occurs if they map to different responses. Both pathways would have `coh=1.0`.
    *   The RSI was reported as 6 seconds.
    *   Task 1 Difficulty: Low (e.g., '2' for 2-choice auditory word discrimination).
*   **Effect of Uncertainty:** The comparison between Exp I and Exp II demonstrates how task parameter predictability (here, of an irrelevant feature's source) can modulate the magnitude of an interference effect. While SE doesn't directly model "uncertainty" as a parameter, the different outcomes for Exp I vs. Exp II would be noted as behavioral results linked to this contextual factor.