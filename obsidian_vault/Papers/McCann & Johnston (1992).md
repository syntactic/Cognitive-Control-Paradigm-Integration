---
tags:
  - paper
  - dual_task
  - prp
  - bottleneck_theory
  - sr_compatibility
aliases:
  - McCann & Johnston 1992
---
### Core Goal
To pinpoint the location of the [[Theoretical Concepts/Bottleneck Theories|single-channel bottleneck]] in dual-task performance using the locus-of-slack logic. Specifically, the authors tested whether the bottleneck occurs *before* or *after* the **response selection** stage by manipulating the difficulty of Task 2's Stimulus-Response (S-R) mapping and observing its interaction with [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]].

### Paradigm(s) Used
A standard [[Dual-Task Performance & PRP|PRP paradigm]] across two experiments, where participants performed two choice-RT tasks in rapid succession.

#### Experiment 1
*   **Task 1:** Auditory tone judgment (high vs. low frequency). Response was **vocal** ("high" or "low").
*   **Task 2:** Manual 6-choice shape/size judgment. Response was a **manual keypress** with one of three fingers on one of two hands.
*   **Primary Manipulation:** The S-R mapping rule for Task 2 was varied based on the stimulus shape.
    *   **Compatible Mapping:** For one shape (e.g., triangle), size (small, medium, large) mapped compatibly to finger position (e.g., left, middle, right).
    *   **Arbitrary Mapping:** For the other shape (e.g., rectangle), size mapped arbitrarily to finger position.
*   **SOA Manipulation:** 4 levels (50, 150, 300, 800 ms).

#### Experiment 2
*   **Task 1:** Auditory tone judgment (same as Exp 1).
*   **Task 2:** Manual 2-choice symbolic/spatial judgment. A stimulus (arrow or letter) appeared on the left or right side of the screen. Response was a **manual keypress** (left/right forefinger).
*   **Manipulations:**
    *   **Symbolic S-R Compatibility:** Arrows (`Compatible`) vs. Letters (`Arbitrary`).
    *   **Spatial S-R Compatibility (Simon Effect):** Stimulus location was congruent or incongruent with response location.
    *   **SOA Manipulation:** 4 levels (50, 150, 300, 800 ms).
    *   **Practice:** Performance was measured across 3 days.

### Key Findings

1.  **Additive Effect of S-R Mapping Difficulty and SOA (Exp 1 & 2):**
    *   The performance cost for the more difficult S-R mapping (Arbitrary vs. Compatible) in Task 2 was **additive** with the effect of SOA. The RT difference between the easy and hard mapping conditions remained constant across all SOAs.
    *   This was true for both the complex 6-choice mapping in Exp 1 and the simpler symbolic mapping (letters vs. arrows) in Exp 2.
    *   The additive pattern persisted across three sessions of practice in Exp 2.

2.  **Underadditive Effect of Simon Effect and SOA (Exp 2):**
    *   In contrast, the spatial compatibility (Simon) effect was **strongly underadditive** with SOA. The RT cost for incongruent stimulus locations was largest at long SOAs and was almost completely eliminated at the shortest SOA (50 ms).

### Authors' Main Conclusions/Interpretations

*   The results strongly support a **central bottleneck model** where the bottleneck is located **at or before response selection**.
*   The additivity of S-R mapping difficulty (a core component of response selection) with SOA means this stage is not being "absorbed into slack." It must occur *after* the slack period, and is therefore part of, or subsequent to, the bottleneck itself.
*   The underadditivity of the Simon effect suggests it arises from a process that occurs *before* the bottleneck. The authors discuss two possibilities: 1) the Simon effect is a pre-bottleneck stimulus identification process, or 2) it's an automatic response activation tendency that dissipates during the slack period created by the bottleneck. Both accounts place the Simon effect's locus before the bottlenecked response selection stage.
*   The results argue against late-bottleneck models (where only response execution is bottlenecked) and capacity-sharing models (which would predict overadditive interactions).

### Relevance to Thesis & Mapping Notes

This paper is a cornerstone for testing the interaction between key dual-task dimensions.

*   **Dimensional Relevance:**
    *   [[Number of Tasks|Number of Tasks]]: 2
    *   [[Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]]: Primary independent variable.
    *   **[[Dimensions/Stimulus Response Mapping|SRM]]**: This is the critical manipulation. You must code `SRM_Task1` and `SRM_Task2` separately.
        *   For all experiments, T1 (vocal tone judgment) has a `Compatible` SRM.
        *   For Exp 1, there will be conditions where `SRM_Task2` is `Compatible` and others where it's `Arbitrary`.
        *   For Exp 2, there will be conditions where `SRM_Task2` is `Compatible` (arrows) and others where it's `Arbitrary` (letters).
    *   **[[Dimensions/Response Set Overlap|Response Set Overlap]]**: `Disjoint - Modality` for all conditions (Vocal vs. Manual).
    *   **[[Dimensions/Task Difficulty|Task Difficulty]]**:
        *   T1 (Tone Judgment): `3` (non-trivial 2-AFC).
        *   T2 (Exp 1, 6-choice mapping): `4` (complex, >4 alternatives).
        *   T2 (Exp 2, arrows/letters): `3` (standard 2-AFC).
    *   **[[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]**: `0` for all conditions (stimuli are the cues).
    *   **[[Dimensions/RSI (Response Stimulus Interval)|RSI]]**: **1000 ms** (The paper states the intertrial interval was "approximately 1 s").

*   **Coding Granularity:**
    *   **Experiment 1** will be coded as 4 (SOA levels) x 2 (T2 SRM types) = **8 rows**.
    *   **Experiment 2** will be coded as 4 (SOA levels) x 2 (Symbolic Compatibility) x 2 (Spatial Compatibility) = **16 rows**. This correctly captures the full factorial design and allows analysis of the different interaction patterns.