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
  - Hirsch et al. 2018
---
### Core Goal
To directly investigate the relationship between cognitive control processes in [[Paradigm Classes/Task Switching|task-switching]] and [[Paradigm Classes/Dual-Task Performance & PRP|dual-tasking]]. The study uses highly comparable paradigms to measure the respective performance costs (mixing costs, switch costs, dual-task costs, PRP effect) within the same participants and analyzes their correlations to identify shared underlying mechanisms.

### Paradigm(s) & Manipulations
The study is a within-subjects comparison of two major paradigm classes, designed to be as similar as possible in terms of stimuli, tasks, and responses.

**Tasks:** Letter classification (Vowel/Consonant) vs. Digit classification (Odd/Even). Stimuli were univalent (a letter or a digit).

**1. Task-Switching Paradigm:**
*   **Structure:** `Number of Tasks = 1`. Participants performed in pure blocks and mixed blocks.
*   **Manipulations:**
    *   **[[Dimensions/Trial Transition Type|Trial Transition Type]]:** Compared `Pure` trials vs. `Repeat` and `Switch` trials in mixed blocks to measure mixing and switch costs.
    *   **[[Dimensions/RSI (Response Stimulus Interval)|RSI]]:** The preparation interval was randomly varied (`100ms` or `600ms`), making it unpredictable.

**2. Dual-Task (PRP) Paradigm:**
*   **Structure:** `Number of Tasks = 2`. Participants performed two tasks (T1 and T2) in rapid succession.
*   **Manipulations:**
    *   **[[Dimensions/Inter-task SOA (Stimulus Onson Asynchrony)|SOA]]:** Randomly varied (`100ms` or `600ms`) to measure the PRP effect.
    *   **Intra-Trial Task Transition:** A novel manipulation where the task required for T1 could be the same as T2 (`Repeat`) or different from T2 (`Switch`) within a single dual-task trial.

### Key Findings & Conclusions
The study's main findings are based on the correlations between performance costs across the two paradigms:
1.  **Mixing Cost & Dual-Task Cost Correlate:** A significant positive correlation was found between the mixing cost (from task-switching) and the dual-task cost (from PRP). The authors suggest this points to a shared mechanism related to working memory updating and maintaining multiple active task sets.
2.  **Switch Cost & PRP Effect Correlate:** A surprisingly strong positive correlation was found between the switch cost and the PRP effect. This challenges the view that the PRP effect arises solely from passive queuing in a bottleneck, suggesting instead that active cognitive control processes (i.e., shifting) contribute significantly to the PRP effect.
3.  **Additive Switch Costs in T2:** The switch cost within the dual-task (T1-T2 Switch vs. Repeat) was additive with SOA, suggesting the shifting process occurs after T1 response selection but before T2 response selection.

*   **Authors' Main Conclusion:** The results provide strong evidence for shared cognitive control mechanisms underlying performance in both task-switching and dual-task contexts, bridging two traditionally separate fields of research.

### Relevance to Thesis & Mapping Notes
This paper is a quintessential "bridge-builder" and a cornerstone for the thesis, as its entire purpose is to empirically link the [[Paradigm Classes/Task Switching|Task Switching]] and [[Paradigm Classes/Dual-Task Performance & PRP|Dual-Task]] regions of the design space.

*   **A Critical Test of the Framework's Definitions:** This study's innovative dual-task design provides a crucial test case for the definition of the dimensions. The solution requires applying the most rigorous, abstract definitions.
*   **Coding the Dual-Task Block:**
    1.  We define a **"trial procedure"** as the ordered pair of tasks to be performed, e.g., `(T1_Task, T2_Task)`.
    2.  In this experiment's dual-task block, the trial procedure is unpredictable, varying randomly between four possibilities: `(Letter, Letter)`, `(Digit, Digit)`, `(Letter, Digit)`, and `(Digit, Letter)`.
    3.  According to the formal definition in `[[Dimensions/Switch Rate]]`, a block with between-trial procedural variability is coded with a `Switch Rate > 0%`. Therefore, we code this block with **`Switch Rate = 50%`**. This correctly captures the block-level context of unpredictability, distinguishing it from standard, procedurally stable PRP experiments (which have `Switch Rate = 0%`).
    4. The [[Dimensions/Intra-Trial Task Relationship]] dimension is then used to describe the within-trial relationship, allowing us to code the "Same" (e.g., Letter, Letter) and "Different" (e.g., Letter, Digit) trials as distinct conditions.
    5. Because the sequence is randomized, [[Dimensions/Trial Transition Type]] is coded as N/A.
*   This principled approach ensures the paradigm's hybrid nature is made visible in the analysis, correctly positioning it between pure PRP and pure task-switching paradigms. This contrasts with the coding of `[[Sigman & Dehaene (2006)]]`, where a more direct and precise dimension (`Inter-task SOA`) was available to represent its specific form of procedural variability (task order).
