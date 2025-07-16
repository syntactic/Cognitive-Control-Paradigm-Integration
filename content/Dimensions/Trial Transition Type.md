---
tags:
  - dimension
  - proactive_control
  - context
aliases:
  - Trial-to-Trial Transition
  - Switch vs Repeat
---
### Definition
A categorical dimension that describes the relationship between the cognitive procedure required on the current trial (N) and the procedure required on the immediately preceding trial (N-1). This dimension is essential for capturing the core manipulations of [[Paradigm Classes/Task Switching|task-switching]] paradigms and for describing the procedural stability of other paradigms.

### Values

*   **`Switch`**
    *   **Description:** The task rule set required on trial N is different from the one used on trial N-1 (e.g., a "Color" task trial following a "Shape" task trial).
    *   **Relevance:** These are the critical trials for measuring the cost of cognitive reconfiguration or overcoming interference. This condition only exists in blocks where `Switch Rate > 0%`.

*   **`Repeat`**
    *   **Description:** The task rule set required on trial N is the same as the one used on trial N-1 (e.g., a "Color" task trial following another "Color" task trial).
    *   **Relevance:** These trials serve as the intra-block baseline for calculating the [[Effects/Switch Cost]]. This condition also only exists in blocks where `Switch Rate > 0%`.

*   **`Pure`**
    *   **Description:** The trial occurs within a block where the same cognitive procedure is applied repeatedly without any possibility of switching to another.
    *   **Relevance:**
        * In **[[Task Switching]]**, these trials form the "pure block" baseline (Switch Rate = 0%) used to calculate the [[Effects/Mixing Cost]].
        * In standard **[[Dual-Task Performance & PRP|PRP]]** paradigms (e.g., [[McCann & Johnston (1992)]]), the high-level procedure ("do Task 1, then do Task 2") is identical on every trial. This procedural stability is conceptually analogous to a pure task-switching block. **Therefore, these conditions are also coded as Pure**, creating a crucial bridge between the paradigm classes.

*   **`N/A` (Not Applicable)**
    *   **Description:** Used for conditions where the concept of a trial-to-trial procedural switch is not the primary manipulation.
    *   **Relevance:**
        *  The very first trial of any block.
        *  Paradigms like **[[Sigman & Dehaene (2006)]]**. Here, while the task order is uncertain (Switch Rate = 50%), the set of two tasks is constant. The core manipulation is Inter-task SOA, not the cost of switching task rules. Coding this as N/A prevents conflating task-order uncertainty with task-rule switching.

### Rationale and Importance

The introduction of this dimension is critical for several reasons:

1.  **Captures the Core of Task Switching:** It makes the fundamental comparison of task-switching research (`Switch` vs. `Repeat` trials) an explicit feature in the design space. Without it, the [[Effects/Switch Cost]] cannot be represented.
2.  **Enables Measurement of Mixing Cost:** It allows for the explicit coding of `Pure` block trials, which are the necessary baseline for measuring the [[Effects/Mixing Cost]] (`RT_repeat - RT_pure`).
3.  **Provides a Consistent Framework:** By using `Pure` to describe the procedural stability of standard PRP paradigms, it creates a powerful theoretical link between the stable cognitive set of a single-task block and the stable procedural set of a dual-task block. This strengthens the unified nature of the design space.
4.  **Improves Granularity:** It enforces the "one row per experimental condition" principle, ensuring that distinct psychological events (`Switch` and `Repeat` trials) are represented as distinct points in the space, which is essential for a meaningful [[PCA]].

This dimension, in conjunction with `Switch Rate`, allows for a nuanced description of the temporal dynamics of an experiment, distinguishing between the *probability* of a switch occurring in a block (`Switch Rate`) and the *actual outcome* of that probability on a given trial transition (`Trial Transition Type`).