---
tags:
 - paper
 - task_switching
 - dual_task
 - prp
 - cognitive_control
 - structure
 - bridge_paradigm
aliases:
 - Lien et al. 2003
---
### Core Goal
To examine the effects of task switching and response correspondence within a [[Paradigm Classes/Dual-Task Performance & PRP|PRP paradigm]], systematically manipulating the participant's foreknowledge of the upcoming task sequence. This study directly investigates the boundary between task-switching and dual-task processes.

### Paradigm & Manipulations
The study used a PRP design with a Letter task (vowel/consonant) and a Digit task (odd/even).
*   **Core Manipulation:** Foreknowledge was varied across three experiments.
    *   **Experiment 1 (No Foreknowledge):** The four possible dual-task pairs (DD, LL, DL, LD) were randomly intermixed. Participants had no ability to predict the upcoming trial's structure.
    *   **Experiment 2 (Partial Foreknowledge):** Trials were blocked. In "repeat" blocks, only DD and LL trials occurred. In "switch" blocks, only DL and LD trials occurred. Participants knew the *type* of relationship (Same/Different) but not the specific task identities.
    *   **Experiment 3 (Full Foreknowledge):** Each block contained only one task pair (e.g., a block of only DD trials). This is a standard, procedurally stable PRP design.
*   **Other Manipulations:** `Inter-task SOA` and `S-S Congruency` were manipulated within all experiments.

### Relevance to Thesis & Mapping Notes
This paper is a perfect "trajectory" through the design space, demonstrating how increasing procedural knowledge parametrically changes the nature of the paradigm. It is a primary validation case for the `Switch Rate` and `Intra-Trial Task Relationship` dimensions.

**Coding Trajectory Across Experiments:**

| Experiment | Foreknowledge | Block Context | `Switch Rate` | `Trial Trans. Type` | `Intra-Trial Task Rel.` | Paradigm Type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Exp. 1** | None | Fully Randomized | **50%** | `N/A` | `Same`/`Different` | Procedurally Variable PRP |
| **Exp. 2** | Partial | Blocked by Type | **50%** | `N/A` | `Same`/`Different` | Procedurally Variable PRP |
| **Exp. 3** | Full | Single Task Pair | **0%** | `Pure` | `Same`/`Different` | Standard PRP |

*   **Experiments 1 & 2** are coded with `Switch Rate = 50%` because even within the blocked design of Exp. 2, the specific trial procedure (e.g., DD vs. LL) is unpredictable. This correctly identifies them as "bridge" paradigms with high procedural uncertainty.
*   **Experiment 3** is coded with `Switch Rate = 0%` because the trial procedure is fixed within each block, making it a classic, stable PRP experiment.
*   The new **`Intra-Trial Task Relationship`** dimension is essential for capturing the core manipulation (`Same` vs. `Different` trials) in a way that is consistent across all three experiments.