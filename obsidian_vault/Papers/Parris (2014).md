---
tags:
  - paper
  - stroop_task
  - neutral_condition
  - interference
  - rsi
aliases:
  - Parris 2014
---
###### Core Goal
The study aimed to demonstrate that Stroop interference and facilitation can be dissociated by manipulating the level of "task conflict." Specifically, it tested the prediction that decreasing the Response-Stimulus Interval (RSI) would increase focus on the color-naming goal, thereby simultaneously *decreasing* interference and *increasing* facilitation. This finding would challenge single-mechanism models where interference and facilitation are expected to change in tandem.

###### Paradigm & Key Manipulations

*   **Paradigm:** A standard manual [[Canonical Tasks/Stroop Task|Stroop task]].
*   **Task:** Participants identified the font color of a word by pressing one of four keys, ignoring the word's meaning.
*   **Key Manipulation:** [[Dimensions/RSI (Response Stimulus Interval)|Response-Stimulus Interval (RSI)]] was manipulated between blocks.
    *   **Long RSI block:** 3500 ms. Hypothesized to create a low-focus, high task conflict context.
    *   **Short RSI block:** 200 ms. Hypothesized to induce a high-focus, low task conflict context.
*   **Stimulus Conditions:**
    *   **Congruent:** Color words printed in their corresponding color (e.g., "GREEN" in green ink).
    *   **Incongruent:** Color words printed in a conflicting color (e.g., "BROWN" in green ink).
    *   **Neutral:** Non-color words (e.g., "stage," "plenty") printed in one of the task colors. This is a crucial feature, as it provides a baseline that still involves a word form, ensuring "task conflict" (reading vs. color naming) is present, unlike an "XXXXX" neutral.

###### Key Findings

*   **Crossover Interaction:** The study found the predicted crossover interaction. Moving from the long RSI to the short RSI condition:
    *   **Interference (Incongruent - Neutral) decreased:** from 45ms to 15ms.
    *   **Facilitation (Neutral - Congruent) increased:** from 8ms to 46ms.
*   **Neutral RTs were Stable:** Critically, the RTs for neutral trials did not differ significantly between the long RSI (745ms) and short RSI (739ms) conditions. This stability provides a solid baseline against which to measure the changes in interference and facilitation.
*   **R-Value Calculation:**
    *   **Long RSI:** R = (RTN - RTC) / (RTI - RTN) = (745 - 737) / (790 - 745) = 8 / 45 ≈ **0.18**. This is a clear R < 1 pattern.
    *   **Short RSI:** R = (RTN - RTC) / (RTI - RTN) = (739 - 693) / (754 - 739) = 46 / 15 ≈ **3.07**. This is a clear R > 1 pattern.
*   The fact that R-value changes so dramatically as a function of RSI is a powerful finding, suggesting the relative contributions of facilitation and interference are context-dependent.

###### Authors' Conclusions & Interpretations

*   The results support a "task conflict" account of Stroop effects, where interference and facilitation can be affected in opposing directions.
*   A short RSI induces a proactive control state, increasing the focus on the color-naming task set. This enhanced focus more effectively suppresses the influence of the irrelevant word dimension (reducing interference) and allows the converging color information on congruent trials to have a stronger facilitatory effect.
*   The findings are problematic for single-mechanism models that assume any change in the processing of the word dimension should affect interference and facilitation in the same way (e.g., both should decrease).
*   The stable neutral baseline is key, as it shows the RSI manipulation specifically targeted the processing of congruent and incongruent information, not general arousal or processing speed.

###### Relevance to Thesis & Mapping Notes

*   **[[Dimensions/RSI (Response Stimulus Interval)|RSI]] as a Key Dimension:** This study is a prime example of how a temporal parameter between trials (RSI) can be used to parametrically modulate cognitive control and the resulting behavioral effects.
*   **Dissociation of Interference & Facilitation:** Provides one of the cleanest demonstrations of a dissociation between Stroop interference and facilitation, underlining the importance of including a neutral condition to measure them separately.
*   **Dynamic R-Value:** Shows that the R-value is not a fixed property of a task but can be systematically modulated by control context (here, induced by RSI). This is a critical nuance for the theoretical map.
*   **SE Mapping Considerations:**
    *   [[Dimensions/N_Tasks|N_Tasks]]: 1.
    *   The core Stroop task is mappable: Target=Ink Color (`or` pathway), Distractor=Word Meaning (`mov` pathway), [[Dimensions/SOA (Stimulus Onset Asynchrony)|SOA]]=0. The three valency conditions are directly mappable.
    *   The central manipulation of `RSI` is a major limitation for direct SE instantiation. SE's trial structure is stimulus-onset driven, and the interval after a response is not an independent parameter. We would map RSI to the `regen` (ITI) parameter in SE, but acknowledge this is an approximation and SE is not designed to study RSI effects *per se*. This is a critical point for the [[Study Limitations]] section.