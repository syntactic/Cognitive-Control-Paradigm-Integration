---
tags:
  - review_paper
  - dual_task
  - prp
  - bottleneck_theory
  - cognitive_control
aliases:
  - Pashler 1994
---
###### Core Goal
To provide a comprehensive review of dual-task interference, primarily using the [[Dual-Task Performance & PRP|Psychological Refractory Period (PRP)]] paradigm, and to argue for a specific, structural model of cognitive limitation. The paper's central thesis is that dual-task costs in simple, speeded tasks are not primarily caused by a graded sharing of limited "attentional resources," but rather by a serial, structural **[[Theoretical Concepts/Bottleneck Theories|processing bottleneck]]** at a central cognitive stage.

###### Paradigm(s) Discussed
*   **Primary Focus:** The [[Dual-Task Performance & PRP|Psychological Refractory Period (PRP) paradigm]]. This involves two speeded choice-RT tasks (T1 and T2) presented in close temporal succession, with the [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]] being the key manipulated variable.
*   **Other Paradigms (for contrast/extension):** The review also discusses how the bottleneck model relates to:
    *   Probe RT tasks.
    *   Concurrent memory load tasks.
    *   Continuous dual-task performance.
    *   Single-task interference phenomena like the [[Canonical Tasks/Flanker Task|Flanker Task]] and stop-signal task.

###### Key Concepts & Arguments

1.  **The Central Bottleneck Model:**
    *   Pashler argues that the robust [[Effects/PRP Effect|PRP effect]] (RT2 slowing at short SOA with a slope of -1) is strong evidence for a stage of processing that can only handle one task at a time.
    *   **Locus of the Bottleneck:** Through a systematic application of the "locus-of-slack" logic, the bottleneck is localized to a central stage that includes **[[Response Selection Bottleneck (RSB)|response selection]]**, memory retrieval, and other complex cognitive operations.
    *   **Parallel Stages:** Critically, early perceptual stages (stimulus identification) and late motor stages (response execution) are *not* part of the bottleneck and can operate in parallel with the bottleneck processing of the other task.

2.  **The "Locus-of-Slack" Logic:**
    *   This is the key methodological tool used to test the model. The model predicts:
        *   Slowing a **pre-bottleneck** stage of T2 (e.g., reducing stimulus contrast) will have its effect "absorbed" into the slack period at short SOA, meaning RT2 will not be delayed.
        *   Slowing a **bottleneck** stage of T1 (e.g., increasing S-R mapping complexity) will cause that delay to "propagate" to T2, slowing RT2 by an equal amount at short SOA.
        *   Slowing a **post-bottleneck** stage of T1 (e.g., requiring more keypresses) will not delay T2 at all.

3.  **Challenge to Capacity/Resource Sharing Models:**
    *   The all-or-none pattern of the PRP effect and the results from the locus-of-slack logic are inconsistent with models where a limited pool of "capacity" is flexibly and gradually shared between two tasks. Such models would predict graded performance trade-offs, not the sharp bottleneck pattern observed.

4.  **Preparatory Limitations:**
    *   The paper acknowledges that the bottleneck is not the *only* source of dual-task interference. There is also a general cost associated with preparing for two possible tasks versus just one. This "preparatory limitation" slows performance on both T1 and T2, even at long SOAs, compared to single-task baselines.

###### Author's Main Conclusions
*   The primary source of interference in dual-task situations is a central, structural bottleneck that prevents more than one response selection (and other related cognitive operations) from occurring at the same time.
*   This bottleneck is distinct from perceptual limitations and motor execution limitations.
*   The concept of a vague, general-purpose "attentional capacity" is less useful for explaining these data than a more specific, mechanistic bottleneck model.
*   Many phenomena attributed to "automaticity" or "attention" can be better understood through the lens of specific processing mechanisms and their structural limitations.

###### Relevance to Thesis & Mapping Notes
*   **Foundational Review:** This paper is a cornerstone for the [[Dual-Task Performance & PRP]] section of the [[Parametric Design Space]]. It provides one of the most influential theoretical frameworks (the RSB model) and summarizes the key empirical evidence for it.
*   **Dimensional Relevance:**
    *   **[[Number of Tasks|Number of Tasks]]:** Defines the N_Tasks=2 paradigm space.
    *   **[[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]]:** The central independent variable for the entire PRP paradigm.
    *   **[[Dimensions/Task Difficulty|Task Difficulty]]:** Crucial for the locus-of-slack methodology. Manipulating difficulty at different stages (perceptual, central, motor) is how the bottleneck is identified.
    *   **[[Dimensions/Response Set Overlap|Response Set Overlap]]:** The paper notes that the PRP effect is robust across different stimulus and response modalities, suggesting the bottleneck is a general central mechanism, not one tied to specific effectors.
*   **Theoretical Keystone:** Establishes the **[[Response Selection Bottleneck (RSB)|Response Selection Bottleneck (RSB)]]** model, which is a fundamental theoretical position the project must account for. It stands in contrast to capacity-sharing models and provides a strong, testable hypothesis about the architecture of cognitive control.
*   **Mapping to Super Experiment:** The PRP paradigm is highly mappable to the SE framework.
    *   Set `N_Tasks=2`.
    *   The `SOA` column in the CSV directly maps to the `interTaskInterval` parameter in the Super Experiment.
    *   `Task Difficulty` can be mapped to SE's `coh_` parameters to simulate perceptual difficulty (pre-bottleneck) or to changes in the S-R mapping rules to simulate central difficulty (bottleneck).