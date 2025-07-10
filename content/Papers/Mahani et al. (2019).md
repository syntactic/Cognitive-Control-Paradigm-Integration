---
tags:
  - paper
  - simon_task
  - neutral_condition
  - interference
  - multimodal
aliases:
  - Mahani et al. 2019
---
###### Core Goal
The primary goal was to extend the [[Canonical Tasks/Simon Task|Simon Task]] to a multimodal setup to investigate how task-irrelevant spatial information from two different sensory modalities (visual and tactile in Exp 1; visual and auditory in Exp 2) affects performance. A secondary goal was to extend the Diffusion Model for Conflict Tasks (DMC) to account for multiple, superimposed sources of automatic activation.

###### Paradigm & Key Manipulations (Focus on Experiment 2)

*   **Paradigm:** A multimodal [[Canonical Tasks/Simon Task|Simon Task]].
*   **Task (Relevant Dimension):** Participants performed a two-choice keypress response to the *identity* of a visual letter stimulus ('H' or 'S').
*   **Irrelevant Dimensions:** The spatial location of the visual letter (left, right, or center) and the spatial location of a simultaneously presented auditory tone (left ear, right ear, or both ears for central).
*   **Congruency Manipulation:** The spatial location of the visual stimulus and the auditory stimulus were independently varied to be congruent, incongruent, or neutral relative to the location of the required response key.
    *   **Visual Congruency:**
        *   **Congruent:** Letter 'H' (-> left key) appears on the left side of the screen.
        *   **Incongruent:** Letter 'H' (-> left key) appears on the right side of the screen.
        *   **Neutral:** Letter 'H' appears at the center of the screen (at fixation).
    *   **Auditory Congruency:**
        *   **Congruent:** Tone presented to the ear on the same side as the correct response.
        *   **Incongruent:** Tone presented to the ear on the opposite side.
        *   **Neutral:** Tone presented stereophonically to both ears.
*   **Procedure:** Inter-trial delay (RSI) was 1000ms.

###### Key Findings (Focus on Experiment 2 RTs)

*   **Visual Simon Effect:** A robust visual Simon effect was observed. RTs were significantly longer in the visual incongruent condition than in the visual congruent and visual neutral conditions.
*   **Auditory Simon Effect:** The effect of the irrelevant auditory information was much weaker and more complex.
*   **Key RT Pattern for Neutral Condition:**
    *   The paper reports (Fig 4, left panel) that for the auditory dimension, the **neutral condition produced the slowest RTs**. There was no significant difference between auditory congruent and incongruent conditions, but both were faster than auditory neutral.
    *   For the visual dimension, there was no significant difference between congruent and neutral RTs.
    *   Focusing on the auditory congruency effect (averaged across visual conditions), we get the following approximate mean RTs from Figure 4:
        *   Auditory Incongruent (AVIA): ~408 ms
        *   Auditory Congruent (AVCA): ~404 ms
        *   Auditory Neutral (AVNA): ~412 ms
*   **R-Value Calculation:** Using the auditory dimension's RTs: R = (RTN - RTC) / (RTI - RTN) = (412 - 404) / (408 - 412) = 8 / -4 = **-2.0**. While the difference between congruent and incongruent is small, the neutral condition is clearly the slowest, resulting in a large negative R-value. This doesn't match the R > 1 reported in the [[Smith & Ulrich (2024)]] summary for this paper, which might have focused on a different analysis or experiment from the paper. However, the qualitative finding of an unusual neutral condition is clear. *The authors themselves note in the discussion that "no significant difference between the congruent and the incongruent auditory condition was observed," but the neutral was significantly slower than the congruent. This pattern (slowest neutral) is the critical takeaway.*

###### Authors' Conclusions & Interpretations

*   The influence of irrelevant spatial information is dominated by the visual modality when presented alongside auditory information.
*   The authors attribute the weak and unusual auditory effect to the presence of the stronger, simultaneous visual spatial information.
*   The surprising pattern for the neutral condition (slowest RTs) was not fully explained but was a clear empirical finding. The authors' modeling work (FN-MDMC) suggests that foveally presented (neutral) visual stimuli are processed faster, but this does not directly explain the slowness of the *auditory* neutral condition.

###### Relevance to Thesis & Mapping Notes

*   **Complex Neutral Conditions:** This paper is an excellent example of how the definition of "neutral" (central visual stimulus, binaural auditory stimulus) and its interaction with other task-irrelevant dimensions can produce surprising RT patterns. It highlights that neutrality is not a simple absence of conflict.
*   **Multimodal Interference:** Demonstrates the principle of cross-modal interference, but also a clear dominance of one modality (visual) over another (auditory) in a spatial task.
*   **SE Mapping Considerations:**
    *   [[Number of Tasks|Number of Tasks]]: 1.
    *   This is a single task with *two* simultaneous irrelevant dimensions (distractors). The SE framework is built for one target and one distractor. To map this, one would have to run separate, simplified experiments in SE. For example:
        1.  **Visual Simon:** Target=Letter ID (e.g., on `mov` pathway), Distractor=Visual Location (e.g., on `or` pathway).
        2.  **Auditory Simon:** Target=Letter ID (visual), Distractor=Auditory Location (would require SE to handle auditory stimuli, which it does not currently).
    *   The core finding of a slow neutral condition challenges simple models where neutral is a midpoint.
    *   For the purpose of coding into the CSV, we can represent the conditions by focusing on one irrelevant dimension at a time while holding the other constant (e.g., code the visual Simon effect for the neutral auditory condition).