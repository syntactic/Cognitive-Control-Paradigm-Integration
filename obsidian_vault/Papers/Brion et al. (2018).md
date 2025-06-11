---
tags:
  - paper
  - flanker_task
  - neutral_condition
  - interference
  - emotional_flanker
aliases:
  - Brion et al. 2018
---
###### Core Goal
To investigate the interaction between reflective (inhibitory) and automatic (attentional bias) systems in alcohol-dependent (ALC) and Korsakoff syndrome (KS) individuals compared to healthy controls (CP). The study used a modified "Alcohol Flanker Task" to measure inhibitory control in the presence of alcohol-related stimuli.

###### Paradigm & Key Manipulations

*   **Paradigm:** A modified [[Canonical Tasks/Flanker Task|Flanker Task]] with an integrated Go/No-Go component, using pictorial stimuli.
*   **Task:** Participants were instructed to respond ("Go," spacebar press) to a central target image and withhold response ("No-Go") to another. The analysis here focuses on the **Go-trial reaction times** for the healthy control group, as these are most comparable to a standard Flanker task.
*   **Stimuli:** Images of beer cans (alcohol-related) and soda cans (non-alcohol-related). In a separate block, these roles were reversed. For simplicity, we can consider one block type (e.g., target = soda, distractor = beer).
*   **Flanker Conditions (Operationalization):**
    *   **Target:** A central image (e.g., a soda can).
    *   **Congruent:** The target was flanked by identical images (e.g., SSS**S**SSS, where S=soda).
    *   **Incongruent:** The target was flanked by images from the competing category (e.g., BBB**S**BBB, where B=beer).
    *   **Neutral:** The target was flanked by neutral images (gray cans, "N") (e.g., NNN**S**NNN).
*   **Procedure:** A trial started with a variable fixation cross (400-800ms). The stimulus array was then presented for a maximum of 900ms. The inter-trial interval was 490ms (blank screen).

###### Key Findings (RTs for Control Group, Non-alcohol block)

*   The primary findings related to differences between ALC, KS, and CP groups in terms of errors (false alarms, omissions).
*   For the reaction time data of the **Control Participants (CP)** in the **non-alcohol-related stimuli block** (Table 2), the pattern is:
    *   Incongruent: 466.01 ms
    *   Congruent: 459.16 ms
    *   Neutral: 453.13 ms
*   **Key Observation:** For the healthy controls, RTs followed the pattern: **Neutral < Congruent < Incongruent**. Neutral trials were the fastest.
*   **R-Value Calculation:** R = (RTN - RTC) / (RTI - RTN) = (453.13 - 459.16) / (466.01 - 453.13) = -6.03 / 12.88 ≈ **-0.47**. This shows a clear R < 0 pattern, consistent with the [[Smith & Ulrich (2024)]] summary.

###### Authors' Conclusions & Interpretations

The authors' main conclusions focused on the clinical populations, suggesting different inhibitory subcomponents are affected in ALC (prepotent response inhibition) vs. KS (distractor interference). The task successfully revealed an interaction between executive load and stimulus type. The RT pattern in the control group confirms a standard Flanker effect, with the gray cans serving as an effective neutral condition that produces less interference than the incongruent flankers and less facilitation (or possibly slight interference) than the congruent flankers.

###### Relevance to Thesis & Mapping Notes

*   **Operationalization of Neutral:** This study provides a clear example of using a visually matched but semantically neutral stimulus (gray cans) as the neutral condition in a pictorial Flanker task.
*   **[[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]]:** The study clearly operationalizes congruent, incongruent, and neutral conditions, making it a good candidate for coding. The `Bivalent-Neutral (Feature Similar)` classification from [[Eriksen & Eriksen (1974)]] could be argued for, as the gray cans are featurally similar (cans) but lack the specific identity of the target/distractor sets.
*   **Go/No-Go Component:** The integration of a Go/No-Go logic is a common modification to interference tasks. While our framework focuses on the choice RT aspect, it's important to note this design feature.
*   **SE Mapping Considerations:**
    *   [[Dimensions/N_Tasks|N_Tasks]]: 1.
    *   The core Flanker task (Go trials) can be mapped. The target identity (e.g., soda) would be represented on one SE pathway (e.g., `mov`), and the flanker identity (soda, beer, or gray can) would be on the other pathway (`or`), with [[Dimensions/SOA (Stimulus Onset Asynchrony)|SOA]]=0.
    *   The neutral condition (gray can flankers) would be modeled in SE by having the `or` pathway present a stimulus that does not map to either of the competing responses.