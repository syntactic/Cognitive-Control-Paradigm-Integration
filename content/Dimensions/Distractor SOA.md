---
tags:
  - dimension
---

### Definition
**Distractor SOA** is the time interval between the onset of a task-relevant **target feature** and the onset of a task-irrelevant **distractor feature** within a single, complex stimulus object or array. This dimension is primarily used to study priming and interference dynamics by manipulating the temporal availability of conflicting information.

`Distractor SOA = Onset(Distractor Feature) - Onset(Target Feature)`

*   A **negative SOA** means the distractor appears *before* the target.
*   A **positive SOA** means the distractor appears *after* the target.
*   A **zero SOA** is the standard for most interference tasks where features are presented simultaneously.

### Application Across Paradigms

While `Distractor SOA` is most common in single-task paradigms, its application depends on the stimulus properties, not strictly on the number of required responses.

#### In Single-Task Paradigms (`Task 2 Response Probability = 0`)

This is the canonical application, used in Interference Control and some Task-Switching designs with bivalent stimuli.

*   **Standard Case (SOA = 0):** In most Stroop and Flanker tasks, the target and distractor features are presented simultaneously.
*   **Asynchronous Case (SOA ≠ 0):** Some designs deliberately introduce a delay to study priming effects.
    *   **Distractor First (Negative SOA):** In Kopp et al. (1996), flankers were presented 100ms before the target arrow, resulting in a `Distractor SOA = -100ms`, maximizing response priming from the distractors.
    *   **Target First (Positive SOA):** In Yeung & Monsell (2003), the target color patch was presented before the distractor word, creating a positive `Distractor SOA` to facilitate target selection.

#### In Dual-Task Paradigms (`Task 2 Response Probability = 1`)

A `Distractor SOA` can be defined in a dual-task (PRP) context if **one of the tasks (e.g., Task 2) is itself an interference task with asynchronous components**.

*   **Distinction from Inter-task SOA:** It is critical to distinguish this from `Inter-task SOA`, which measures the time between the onset of the entire Stimulus 1 and the entire Stimulus 2.
*   **A "Bridge" Case:** In Fischer & Schubert (2008), the paradigm was dual-task (PRP), but Task 2 was a Flanker task where the flankers appeared 85ms *before* the target. This is coded with:
    *   An `Inter-task SOA` (e.g., 85ms or 800ms) to define the relation between Task 1 and Task 2.
    *   A `Distractor SOA` of `-85ms` to define the internal timing of Task 2.
*   **Coding Rule:** This dual-coding is a deliberate choice to capture the unique, hierarchical timing of such "bridge" paradigms. However, as noted in `Study Limitations.md`, the framework's primary temporal dimension in dual-tasks is `Inter-task SOA`, and the ability to model a Task 2-internal SOA is a specific, noted exception. If both tasks in a trial have different target-distractor offsets, this single dimension is not sufficient to capture both.

---
