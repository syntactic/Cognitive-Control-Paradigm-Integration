---
tags:
  - paper
  - dual_task
  - prp
  - task_switching
  - crosstalk
  - bottleneck_theory
aliases:
  - Miller & Alderton 2006
---
### Core Goal
To investigate whether the motoric requirements of a second task (T2)—specifically, the force of a required keypress—can influence the motor execution of a first task (T1) in a Psychological Refractory Period (PRP) paradigm. This provides a direct test for "backward response-level crosstalk" and challenges the assumption of strictly serial processing stages in simple [[Theoretical Concepts/Bottleneck Theories|bottleneck models]].

### Paradigm(s) & Manipulations
The paper uses a series of three experiments that systematically transition across the design space. The core tasks remained consistent:
*   **Task 1 (T1):** A 2-choice color discrimination (red/green) with a left-hand finger response (middle vs. index).
*   **Task 2 (T2):** A 2-choice letter identification ('X'/'O') with a right-hand response that was either *hard* or *soft*.

**Key Manipulations Across Experiments:**
1.  **Experiment 1 (Simultaneous Dual-Task):**
    *   **Stimulus:** A single colored letter (e.g., a red 'X').
    *   **Manipulation:** [[Dimensions/Inter-task SOA (Stimulus Onset Asynchrony)|SOA]] was fixed at `0`. The core design was a 2x2 factorial of T1 finger x T2 force.

2.  **Experiment 2 (Sequential PRP):**
    *   **Stimuli:** Two separate, univalent stimuli: a colored rectangle (S1) followed by a white letter (S2).
    *   **Manipulation:** The [[Dimensions/Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]] was the primary independent variable, manipulated at three levels: `50ms`, `150ms`, and `400ms`, randomized within blocks.

3.  **Experiment 3 (Task-Switching with Interference):**
    *   **Stimulus:** A single central target (either a colored rectangle or a letter) was flanked by distractors from the other task set. Only one response was required per trial.
    *   **Manipulations:**
        *   **[[Dimensions/Distractor SOA|Distractor SOA]]:** The flankers appeared `50ms` or `400ms` *after* the target.
        *   **[[Dimensions/Switch Rate|Switch Rate]]:** Varied between-subjects. Exp 3a used predictable `100%` alternation, while Exp 3b used random `50%` switching.

### Key Findings & Conclusions
1.  **Robust Backward Crosstalk:** The central finding from Experiments 1 and 2 was a clear backward response-level crosstalk effect. T1 responses were physically more forceful when the upcoming T2 response was required to be hard, compared to when it was required to be soft.
2.  **SOA Independence:** In Experiment 2, this crosstalk effect was present across all tested SOAs and did not significantly diminish as SOA increased from 50ms to 400ms.
3.  **Crosstalk is Response-Selection Dependent:** The crosstalk effect **disappeared entirely in Experiment 3**. When participants only had to respond to the target and ignore the flankers (i.e., no response selection for the second task's stimulus features), the force requirements associated with the flankers had no influence on the T1 response.
4.  **Locus of Crosstalk:** The authors conclude that the observed crosstalk is not due to automatic stimulus activation or simple motor coupling. Instead, it originates specifically from the **response selection stage of T2**, which must be operating in parallel with the later motor-programming and execution stages of T1.

*   **Authors' Main Conclusion:** The results strongly challenge strictly serial bottleneck models where T2 response selection cannot begin until T1 response selection is complete. They support models that allow for some degree of parallel processing between T1 execution and T2 central stages, leading to content-specific crosstalk.

### Relevance to Thesis & Mapping Notes
This paper is an exemplary "bridge" study, as its three experiments create a clear, motivated trajectory across the [[Parametric Design Space]]. It serves as a powerful validation of the parametric approach.

*   **Bridging Paradigms:** It explicitly demonstrates the transition from:
    1.  A simultaneous dual-task (`N_Tasks=2`, `SOA=0`)
    2.  To a sequential PRP task (`N_Tasks=2`, variable `SOA>0`)
    3.  To a [[Paradigm Classes/Task Switching|Task-Switching]] / [[Paradigm Classes/Interference Control|Interference Control]] hybrid (`N_Tasks=1`, variable `Distractor SOA`).

*   **Refines Core Concepts:**
    *   **[[Theoretical Concepts/Crosstalk|Crosstalk]]:** Provides a clear demonstration of [[Effects/Backward Crosstalk Effect (BCE)|Backward Crosstalk Effect]], and critically, localizes its source to the response selection stage, not just stimulus priming.
    *   **[[Theoretical Concepts/Bottleneck Theories|Bottleneck Theories]]:** Serves as a direct empirical challenge to simple, serial bottleneck models, forcing a consideration of models that allow for parallel central processing or capacity sharing.

*   **Dimensional Mapping Summary:**
    *   **Experiment 1:** Coded as a single condition with `Task 2 Response Probability = 1` and `Inter-task SOA = 0`. The stimulus is `Bivalent-Neutral`.
    *   **Experiment 2:** Coded as three conditions, distinguished by `Inter-task SOA` values of `50`, `150`, and `400`. The stimuli are now `Univalent`, so `Stimulus-Stimulus Congruency` is `N/A`.
    *   **Experiment 3:** Coded as six conditions, defined by `Task 2 Response Probability = 0`. The key dimensions are `Distractor SOA` (`50`, `400`) and the `Switch Rate` / `Trial Transition Type` combination (100% Switch vs. 50% Switch/Repeat).

This paper is invaluable because it doesn't just occupy a point in the design space; it actively moves between distinct regions, illustrating the parametric relationships that connect different canonical paradigms.
