---
tags:
  - paper
  - stroop_task
  - neutral_condition
  - interference
  - matching_task
aliases:
  - Schroeter et al. 2002
---
###### Core Goal
The primary goal was methodological: to test the feasibility of using near-infrared spectroscopy (NIRS) to measure brain activity in a cognitive paradigm using an event-related design. The study used a color-word matching Stroop task to elicit interference effects.

###### Paradigm & Key Manipulations

*   **Paradigm:** A variant of the [[Canonical Tasks/Stroop Task|Stroop Task]], specifically a **color-word matching task**.
*   **Task:** Participants were shown two rows of letters and had to decide if the ink color of the top row corresponded to the color name written in the bottom row. They made a "Yes" or "No" response via a two-choice button press.
*   **Stimulus Timing:** The top row was presented 100ms before the bottom row to shift visual attention. The inter-stimulus interval (RSI) was 12 seconds.

*   **Key Conditions & Stimulus Operationalization:**
    *   **Congruent:** The top row was a color word printed in its corresponding color (e.g., 'RED' in red ink). The bottom row was the same color word in black ink (e.g., 'RED').
        *   *Example Yes Trial:* Top: 'RED' (in red); Bottom: 'RED' (in black).
    *   **Incongruent:** The top row was a color word printed in a conflicting color (e.g., 'GREEN' in blue ink). The bottom row was the word 'GREEN' in black ink. The participant's task is to evaluate the ink color of the top row (blue) against the word of the bottom row (GREEN). The irrelevant, conflicting information is the word 'GREEN' in the top row.
        *   *Example No Trial:* Top: 'GREEN' (in blue); Bottom: 'GREEN' (in black).
    *   **Neutral:** The top row was a string of 'XXXX' printed in a color (e.g., red). The bottom row was a color word in black (e.g., 'BLUE'). This removes the semantic interference from the top row.
        *   *Example No Trial:* Top: 'XXXX' (in red); Bottom: 'BLUE' (in black).

###### Key Findings

*   The NIRS data successfully showed stronger hemodynamic responses (interpreted as stronger brain activation) for incongruent trials compared to neutral and congruent trials, validating its use.
*   **Behavioral Results (RTs):** The reaction times showed a standard interference effect but an unusual congruency effect:
    *   Incongruent: 882 ms
    *   Congruent: 800 ms
    *   Neutral: 740 ms
*   **Key Observation:** Neutral trials were significantly **faster** than congruent trials. This is a "reverse facilitation" or "congruent cost," likely because in congruent trials, the top stimulus itself ('RED' in red) primes the matching response, but the task still requires a complex comparison of top ink color to bottom word meaning, which may be more complex than the simple neutral condition (color patch vs. word).
*   **R-Value:** The relative position of the neutral RT is R = (RTN - RTC) / (RTI - RTN) = (740 - 800) / (882 - 740) = -60 / 142 ≈ **-0.42**. This confirms the R < 0 pattern noted by [[Smith & Ulrich (2024)]].

###### Authors' Conclusions & Interpretations

The authors concluded that NIRS is a feasible and valuable tool for studying cognitive processes in an event-related manner. The behavioral results, while secondary to their main goal, were in accordance with literature showing robust Stroop interference. The specific matching-task design likely accounts for the neutral condition being faster than the congruent one.

###### Relevance to Thesis & Mapping Notes

*   **Crucial Example of Task Design:** This study is a powerful example of how the specific task instructions (matching vs. naming) fundamentally alter the nature of the "neutral" and "congruent" conditions and the resulting RT patterns.
*   **[[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]]:** It provides a clear operationalization of a neutral condition using a non-word stimulus ('XXXX'), which maps well to the `Bivalent-Neutral` category in the framework. The unusual RT pattern highlights that facilitation/interference is not just about stimulus features but their relationship to the required task.
*   **SE Mapping Considerations:**
    *   [[Dimensions/N_Tasks|N_Tasks]]: 1.
    *   The core manipulation between the three conditions maps directly to the `Stimulus Valency` dimension.
    *   SE cannot directly model the complex **matching** logic of this task. The mapping must abstract this away, treating it as a single S-R event whose type is defined by the congruency condition.
    *   The 100ms onset asynchrony between stimulus components within a single trial is a nuance that the SE framework is not designed to capture easily for a single-task event.
    *   For SE instantiation, the incongruent condition involves a target (top ink color) and a conflicting distractor (top word meaning). The neutral condition has a target and a non-competing distractor ('XXXX').