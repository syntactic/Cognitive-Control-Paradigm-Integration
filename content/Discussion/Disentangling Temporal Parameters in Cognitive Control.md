---
tags:
  - concept
  - thesis_concept
  - temporal_dynamics
---
## 1. The Challenge: A "Conceptual Soup" of Time

A significant challenge in unifying the cognitive control literature is the overlapping and sometimes ambiguous terminology used to describe temporal parameters. Key variables like Stimulus Onset Asynchrony (SOA), Response-Stimulus Interval (RSI), Cue-Stimulus Interval (CSI), and Inter-Trial Interval (ITI) are often used in paradigm-specific ways, obscuring their functional relationships. This project's parametric approach reveals that these are not always orthogonal concepts but can be seen as different ways of partitioning the time within and between cognitive episodes.

## 2. Unpacking the Definitions

*   **SOA (Stimulus Onset Asynchrony):** The time between the onset of two *stimuli*.
    *   **[[Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]]:** Between S1 and S2 in a dual-task trial. Probes the limits of *concurrent processing* and bottlenecks.
    *   **[[Dimensions/Distractor SOA|Distractor SOA]]:** Between a target and distractor feature in a single-task trial. Probes *distractor priming and filtering*.

*   **RSI (Response-Stimulus Interval):** The time between a *response* and the next *stimulus*.
    *   **Inter-Trial RSI:** The classic definition in task-switching ([[Rogers & Monsell (1995)]]). Time from R_n-1 to S_n. It represents a period for *post-trial processing* (e.g., decay of [[Task-Set Inertia]]) and *pre-trial preparation* (e.g., [[Task-Set Reconfiguration]]).
    *   **Intra-Trial RSI:** As seen in [[Allport et al. (1994)]] Exp. 5. Time from R1 to S2 in a dual-task trial. It functions as a post-response preparation interval for the second part of a larger task.

*   **CSI (Cue-Stimulus Interval):** The time between a *cue* and a *stimulus*. Represents a "pure" preparation interval for an explicitly instructed task.

*   **ITI (Inter-Trial Interval):** The time between the end of one trial's events and the start of the next trial's events. This is the operational parameter the `super-experiment` framework actually implements.

## 3. Key Conceptual Overlaps Revealed by the Framework

### Overlap 1: Long SOA becomes an Intra-Trial RSI

When `Inter-task SOA` becomes very long, the first task is completed (S1 -> R1) before S2 appears. The interval `SOA - RT1` becomes a de facto preparation period. This transforms a paradigm that tests concurrent processing bottlenecks into one that tests sequential task-set engagement, blurring the line between PRP and a specific kind of task-switching.

### Overlap 2: CSI is a component of RSI

In a cued task-switching paradigm, the RSI can be decomposed:
`RSI = (Time from R_n-1 to Cue_n) + (Time from Cue_n to S_n)`
`RSI = Response-Cue Interval (RCI) + CSI`

This shows that these parameters are not independent. Manipulating one often affects the other, and different theories place emphasis on different sub-intervals as being critical for control. The parametric space forces us to be explicit about how the entire timeline is structured.

### Overlap 3: The RSI vs. ITI Abstraction

The framework's inability to implement a true, dynamic RSI forces an abstraction: we model the conceptual RSI from the literature using a static, pre-defined ITI. This highlights a common idealization in cognitive modeling and experimental design, and the documentation of this choice adds to the project's transparency.
