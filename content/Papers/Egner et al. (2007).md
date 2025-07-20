---
tags:
  - paper
  - interference_control
  - conflict_adaptation
  - stroop_task
  - simon_task
  - cognitive_control
aliases:
  - Egner et al. 2007
---
### Core Goal
To determine whether cognitive control relies on a single, central resource for resolving all types of conflict, or if it employs independent, conflict-specific mechanisms. The authors tested this by factorially combining two distinct sources of conflict—Stroop conflict and Simon conflict—within a single task and examining whether resolving one type of conflict influenced the resolution of the other.

### Paradigm & Manipulations

*   **Paradigm:** A modified color-naming [[Canonical Tasks/Stroop Task|Stroop task]] combined with a [[Canonical Tasks/Simon Task|Simon task]].
*   **Task:** Participants identified the ink color of a word stimulus presented to the left or right of a central fixation point.
*   **Key Manipulations (2x2 Factorial Design):**
    1.  **Stroop Compatibility ([[Dimensions/Stimulus-Stimulus Congruency|S-S Conflict]]):** The word's meaning could be `Congruent` or `Incongruent` with its ink color.
    2.  **Simon Compatibility ([[Dimensions/Stimulus-Response Congruency|S-R Conflict]]):** The stimulus's spatial location could be `Congruent` or `Incongruent` with the required response hand.
*   **Analytical Manipulation:** The primary analysis was of **conflict adaptation** (sequential effects), examining how the congruency on the previous trial (N-1) modulated the congruency effect on the current trial (N), both within and across conflict types.

### Key Findings & Conclusions

1.  **Behavioral Independence:**
    *   Both a standard Stroop effect and a standard Simon effect were observed (main effects).
    *   Crucially, these two effects did not interact, suggesting they operate independently at a behavioral level.
2.  **Conflict-Specific Adaptation:**
    *   **Within-Domain:** Resolving Stroop conflict on trial N-1 significantly reduced Stroop conflict on trial N. Likewise, resolving Simon conflict on trial N-1 reduced Simon conflict on trial N.
    *   **Across-Domain:** Resolving Stroop conflict had **no effect** on the subsequent Simon conflict, and vice versa.
3.  **Neural Dissociation:**
    *   The resolution of Stroop conflict (stimulus-based) was specifically associated with modulated activity in the **parietal cortex**.
    *   The resolution of Simon conflict (response-based) was specifically associated with modulated activity in the **premotor cortex**.

*   **Authors' Main Conclusion:** The human brain employs separate, conflict-specific cognitive control mechanisms rather than a single, global control resource. The control system flexibly recruits distinct neural circuits to resolve conflict depending on its specific source (stimulus-level vs. response-level).

### Relevance to Thesis & Mapping Notes

This paper is a quintessential "bridge" study in the design space, as it directly integrates two canonical types of [[Paradigm Classes/Interference Control|Interference Control]].

*   **Validates Dimensional Orthogonality:** This paper's findings provide strong empirical support for the decision to treat `[[Dimensions/Stimulus-Stimulus Congruency]]` and `[[Dimensions/Stimulus-Response Congruency]]` as precise, orthogonal dimensions. It demonstrates that these two types of conflict are behaviorally and neurologically dissociable.

*   **Dimensional Mapping:**
    *   [[Task 2 Response Probability]]: `0`.
    *   [[Stimulus-Stimulus Congruency]]: Manipulated (`Congruent`, `Incongruent`).
    *   [[Stimulus-Response Congruency]]: Manipulated (`Congruent`, `Incongruent`).
    *   [[Dimensions/Stimulus Response Mapping|Stimulus Response Mapping]]: `Arbitrary` (for the relevant ink-color-to-key-press rule).
    *   [[RSI (Response Stimulus Interval)]]: `4000` (mean), but [[RSI Is Predictable]]: No (as it was jittered).

*   **Mapping Decision & Framework Limitation:**
    *   In line with the "Sufficient MVP" decision, we are coding the **four core factorial conditions** of this study into the `super_experiment_design_space.csv`.
    *   This explicitly **abstracts away the paper's core dynamic finding** on conflict-specific adaptation. This choice is documented in `[[Study Limitations.md]]`, where I note the framework's inability to currently model such sequential and contextual effects. This paper serves as the primary example of that limitation.
