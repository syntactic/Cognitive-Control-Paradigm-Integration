---
tags:
  - dimension
  - proactive_control
  - temporal_context
  - task_switching
aliases:
  - Predictable RSI
---
### Definition
A binary dimension describing whether the Response-Stimulus Interval (RSI) is constant and predictable within a block of trials, or whether it varies randomly from trial to trial. This dimension captures a critical manipulation of temporal context, determining whether participants can prepare for the *when* of the next stimulus, in addition to the *what* (the task).

### Values

*   **`Yes (Predictable)`**
    *   **Description:** The RSI is a fixed, constant value for all trials within an experimental block.
    *   **Relevance:** A predictable RSI allows participants to form a precise temporal expectation of when the next stimulus will appear. This is a prerequisite for engaging in time-locked, proactive preparation processes like [[Theoretical Concepts/Task-Set Reconfiguration|task-set reconfiguration]].
    *   **Canonical Example:** [[Rogers & Monsell (1995)]] Experiment 3, where different blocks used fixed RSIs (e.g., 150ms, 600ms, 1200ms).

*   **`No (Unpredictable)`**
    *   **Description:** The RSI is randomly drawn from a distribution (either continuous or discrete) on each trial. The participant knows the range of possible RSIs but cannot predict the specific interval on any given trial.
    *   **Relevance:** An unpredictable RSI prevents participants from using the passage of time to prepare for the upcoming stimulus. This manipulation is used to isolate cognitive processes that are not dependent on temporal preparation, such as the passive decay of [[Theoretical Concepts/Task-Set Inertia|task-set inertia]].
    *   **Canonical Examples:** [[Rogers & Monsell (1995)]] Experiment 2 (RSI drawn from a uniform distribution); [[Stephan & Koch (2010)]] Experiment 2 (RSI drawn from a choice of two values).

### Rationale and Importance

The inclusion of `RSI Predictability` as a first-class dimension is theoretically essential:

1.  **Tests Core Theories:** It directly operationalizes the distinction between active preparation and passive decay. Theories based on [[Theoretical Concepts/Task-Set Reconfiguration|Task-Set Reconfiguration]] predict that switch costs should only be reduced when RSI is predictable. In contrast, simple decay-based theories like [[Theoretical Concepts/Task-Set Inertia|Task-Set Inertia]] would predict that any increase in average RSI duration, regardless of predictability, should allow more time for interference to dissipate. The empirical results ([[Rogers & Monsell (1995)]]) strongly support the former, making this dimension a powerful tool for theory testing.

2.  **Disambiguates the `RSI` Dimension:** It adds a crucial qualitative layer to the quantitative `RSI` dimension. Two experiments might both have a mean RSI of 700ms, but if one is predictable and the other is not, they represent vastly different psychological contexts. This binary feature ensures the PCA does not mistakenly treat these distinct conditions as identical.

3.  **Strengthens the Framework:** By explicitly coding for predictability, the design space can more accurately capture the subtle but powerful ways in which temporal context modulates cognitive control.

### PCA Coding

*   This dimension will be treated as a **binary categorical feature** in the PCA pipeline (`RSI_Predictable_Yes` / `RSI_Predictable_No`).
*   It will be one-hot encoded, allowing the analysis to discover how this property covaries with other design choices and contributes to the overall structure of the experimental space.