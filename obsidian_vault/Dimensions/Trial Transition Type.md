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
    *   **Description:** The trial occurs within a single-task or single-procedure block, where the same cognitive set is applied repeatedly without any possibility of switching to another task.
    *   **Relevance:**
        *   In **[[Task Switching]]**, these trials form the "pure block" baseline used to calculate the [[Effects/Mixing Cost]]. Coded with `Switch Rate = 0%`.
        *   In standard **[[Dual-Task Performance & PRP|PRP/dual-task]]** paradigms (e.g., [[McCann & Johnston (1992)|McCann & Johnston 1992]]), the high-level procedure ("do T1, then do T2") is identical on every trial. This procedural stability is analogous to a pure task-switching block. **Therefore, these conditions are coded as `Pure`**.

*   **`N/A` (Not Applicable)**
    *   **Description:** Used for conditions where the concept of a trial-to-trial transition is not the primary manipulation or is ambiguous.
    *   **Relevance:**
        *   The very first trial of any block.
        *   Paradigms with a block-level manipulation of uncertainty, where the distinction between a transition "repeat" and "switch" is not the focus of the analysis. The primary example is **[[Sigman & Dehaene (2006)]]**, where the block-level uncertainty is already captured by `Number of Tasks = 2` and `Switch Rate = 50%`.

### Rationale and Importance

The introduction of this dimension is critical for several reasons:

1.  **Captures the Core of Task Switching:** It makes the fundamental comparison of task-switching research (`Switch` vs. `Repeat` trials) an explicit feature in the design space. Without it, the [[Effects/Switch Cost]] cannot be represented.
2.  **Enables Measurement of Mixing Cost:** It allows for the explicit coding of `Pure` block trials, which are the necessary baseline for measuring the [[Effects/Mixing Cost]] (`RT_repeat - RT_pure`).
3.  **Provides a Consistent Framework:** By using `Pure` to describe the procedural stability of standard PRP paradigms, it creates a powerful theoretical link between the stable cognitive set of a single-task block and the stable procedural set of a dual-task block. This strengthens the unified nature of the design space.
4.  **Improves Granularity:** It enforces the "one row per experimental condition" principle, ensuring that distinct psychological events (`Switch` and `Repeat` trials) are represented as distinct points in the space, which is essential for a meaningful [[PCA]].

This dimension, in conjunction with `Switch Rate`, allows for a nuanced description of the temporal dynamics of an experiment, distinguishing between the *probability* of a switch occurring in a block (`Switch Rate`) and the *actual outcome* of that probability on a given trial transition (`Trial Transition Type`).