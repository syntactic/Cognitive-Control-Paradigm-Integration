---
tags:
- paper
- dual_task
- prp
- bottleneck_theory
- cognitive_control
aliases:
- Pashler 1984
---

### Core Goal
To use the "locus-of-slack" logic within the [[Paradigm Classes/Dual-Task Performance & PRP|overlapping tasks (PRP) paradigm]] to precisely locate the central processing bottleneck. The study tests whether the bottleneck occurs before, during, or after specific stages of a visual search task by observing how the effects of different difficulty manipulations on the second task (T2) are modulated by the presence of a first task (T1).

### Paradigm Used
A standard [[Paradigm Classes/Dual-Task Performance & PRP|PRP paradigm]] where participants performed two tasks in rapid succession.
*   **Task 1 (T1):** A simple 2-choice reaction time task (judging if a bar of light appeared above or below fixation).
*   **Task 2 (T2):** A visual search task (determining if a target letter was present or absent in a small array).

### Key Manipulations
The study systematically varied factors thought to influence different processing stages of Task 2 and observed their effects alone versus in the dual-task context.
1.  **Task Overlap:** The main comparison was between performing the visual search task in isolation (single-task) versus as T2 (dual-task).
2.  **[[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]]:** The time between S1 and S2 was manipulated across experiments (e.g., 100ms in Exp. 1 & 2; 300ms in Exp. 3; 0ms in Exp. 5).
3.  **T2 Perceptual/Encoding Difficulty (Pre-Bottleneck):**
    *   **Stimulus Contrast (Exp. 1):** The letter array was presented in either high or low contrast.
    *   **Display Size (Exp. 2, 3, 4):** The number of letters in the search array was varied (2, 4, or 6).
4.  **T2 Decision/Selection Difficulty (Central Stage):**
    *   **Target Presence/Absence (All Exp.):** Compared trials where the target was present ("yes" response) versus absent ("no" response). This is assumed to affect later stages of comparison or decision.
5.  **Task Order (Exp. 5):** The roles were reversed, with the visual search task as T1 and the bar-judgment task as T2.

### Key Findings (The "Locus of Slack" Logic)
*   **Underadditivity for Early Stages:** The effects of factors influencing early processing (stimulus contrast and display size) were **significantly reduced** in the dual-task condition at short SOAs. The extra processing time they required was "absorbed" into the slack period where T2 was waiting for T1 to clear the bottleneck.
*   **Additivity for Later Stages:** In contrast, the effect of target presence/absence was **fully additive**. Its impact on RT2 was the same in both single-task and dual-task conditions. This indicates the stage affected by this factor occurs *after* the slack period and is therefore part of or subsequent to the bottleneck itself.
*   **SOA Modulates Underadditivity:** At a longer SOA of 300ms (Exp. 3), there was less slack time available, and the underadditive interaction for display size was eliminated, as the model would predict.

### Author's Main Conclusions
*   The results provide strong evidence for a **central processing bottleneck**.
*   This bottleneck is located **after** the early perceptual encoding and comparison stages (which are affected by contrast and display size) but **at or before** the final decision/selection stage (which is affected by target presence/absence).
*   This pattern strongly supports a **[[Theoretical Concepts/Response Selection Bottleneck (RSB)|Response Selection Bottleneck]]** model, where the critical limitation is in choosing and programming a response, while perceptual analysis can proceed in parallel.
*   The findings argue against general capacity-sharing models, which would likely predict overadditive interactions, not the specific pattern of underadditivity and additivity observed.

### Relevance to Thesis & Mapping Notes
*   **Foundational Study:** This is a cornerstone paper for the [[Paradigm Classes/Dual-Task Performance & PRP|PRP]] paradigm and the [[Theoretical Concepts/Bottleneck Theories|bottleneck theory]] of dual-task interference.
*   **Dimensional Relevance:**
    *   **`Number of Tasks` / `Task 2 Response Probability`:** The central comparison between single- and dual-task blocks is a direct manipulation of this dimension.
    *   **`Inter-task SOA`:** Systematically manipulated across experiments, making it a perfect case study for this dimension.
    *   **`Task Difficulty`:** The use of contrast and display size provides a clear example of how to operationalize and code this dimension. The different outcomes for "early" (perceptual) vs. "late" (decision) difficulty are key theoretical points.
*   **Theoretical Keystone:** This paper provides some of the cleanest and most cited evidence for the **Response Selection Bottleneck (RSB)** model, a fundamental theory that the parametric design space aims to situate.
*   **Mapping to Super Experiment:** The paradigm is highly mappable. `N_Tasks=2`, `interTaskInterval` (for SOA), and `coh_1`/`coh_2` (as an abstraction for Task Difficulty) can directly instantiate the conditions explored in these experiments.
