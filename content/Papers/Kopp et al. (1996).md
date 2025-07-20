---
tags:
  - paper
  - flanker_task
  - neutral_condition
  - interference
  - erp
  - soa
aliases:
  - Kopp et al. 1996
---
###### Core Goal
To investigate executive control, specifically response priming and inhibition, using a modified [[Canonical Tasks/Flanker Task|Flanker Task]] while recording event-related potentials (ERPs). The study aimed to isolate the neural correlates (particularly the N200 component) of resolving response conflict induced by incongruent flankers.

###### Paradigm & Key Manipulations

*   **Paradigm:** An arrow-based Flanker task with ERP recording.
*   **Task:** Participants responded with their left or right hand to the direction of a centrally presented target arrowhead.
*   **Key Manipulations:**
    1.  **Flanker-Target SOA:** A critical design choice was that the flanker stimuli appeared 100ms *before* the target stimulus. This creates a -100ms [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]] between the distractor and target, designed to maximize response priming from the flankers.
    2.  **Flanker Compatibility (Stimulus-Stimulus Congruency):**
        *   **Congruent:** Flanker arrows pointed in the same direction as the target.
        *   **Incongruent:** Flanker arrows pointed in the opposite direction.
        *   **Neutral:** Flankers were squares, which have no associated directional response.
    3.  **Spatial Distance:** The distance between the flankers and the target was varied: Short (1° of visual angle) or Large (3°).
*   **Procedure:** The intertrial interval (RSI) was approximately 2000ms.

###### Key Findings (Behavioral RTs from Table 1)

*   A standard Flanker effect (Congruent < Neutral < Incongruent) was observed for reaction times.
*   **Short Distance RTs:**
    *   Congruent: 306 ms
    *   Neutral: 350 ms
    *   Incongruent: 415 ms
*   **Large Distance RTs:**
    *   Congruent: 321 ms
    *   Neutral: 351 ms
    *   Incongruent: 395 ms
*   **Key Observation:** The interference effect (Incongruent - Neutral) was larger at the short distance (65ms) than the large distance (44ms), confirming that closer flankers cause more conflict.
*   **R-Value Calculation:**
    *   **Short Distance:** R = (RTN - RTC) / (RTI - RTN) = (350 - 306) / (415 - 350) = 44 / 65 ≈ **0.68**. This is a clear R < 1 pattern.
    *   **Large Distance:** R = (RTN - RTC) / (RTI - RTN) = (351 - 321) / (395 - 351) = 30 / 44 ≈ **0.68**. The R-value is highly consistent across spatial distances.
*   **ERP Findings:** The main finding of the paper was that a specific ERP component (N2c) was present only in the incongruent condition and its amplitude scaled with the strength of the incorrect response, suggesting it reflects the active inhibition of erroneously primed responses.

###### Authors' Conclusions & Interpretations

The authors concluded that the N2c component is a neurobehavioral marker of executive control, specifically reflecting the detection and inhibition of inappropriate response tendencies automatically triggered by the flankers. The 100ms SOA was effective in inducing this erroneous priming before the target was processed.

###### Relevance to Thesis & Mapping Notes

*   **Blurring Paradigm Boundaries:** This study is a perfect example of a [[Transitions and Modulators|transition case]]. While it is a single-response [[Canonical Tasks/Flanker Task|Flanker task]] ([[Number of Tasks|Number of Tasks]]=1), it uses a non-zero [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]], a manipulation that is the hallmark of [[Dual-Task Performance & PRP|PRP]] paradigms. This highlights that SOA can be used to modulate distractor processing, not just second-task processing.
*   **Neutral Stimulus:** Provides another clear example of a neutral stimulus (squares) that is visually distinct and has no inherent mapping to the left/right responses.
*   **Spatial Distance as Difficulty:** The manipulation of flanker-target distance serves as a good proxy for task difficulty, as closer spacing increases interference and demands more cognitive control. This can be mapped to the [[Dimensions/Task Difficulty]] dimension.
*   **SE Mapping Considerations:**
    *   This paradigm is highly mappable to the [[Super Experiment Framework]].
    *   The flanker would be modeled as the distractor (e.g., `or` pathway) and the target as the main task stimulus (e.g., `mov` pathway).
    *   The -100ms SOA is modeled by setting `start_or_1 = 0` and `start_mov_1 = 100`.
    *   The neutral condition (squares) is modeled by having the distractor stimulus map to a non-competing response.
    *   The spatial distance manipulation can be abstracted and mapped to the `coh_mov_1` parameter (as part of `Task 1 Difficulty`), where lower coherence represents higher difficulty/interference from the closer flankers.
