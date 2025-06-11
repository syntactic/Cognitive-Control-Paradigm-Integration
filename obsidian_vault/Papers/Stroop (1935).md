---
tags:
  - paper
---
**Full Title:** Studies of Interference in Serial Verbal Reactions

**Author:** J. Ridley Stroop

**Year:** 1935

**Journal:** Journal of Experimental Psychology

**Core Goal:**
To investigate and quantify the interference effects observed when there is a conflict between the name of a color and the ink color in which that name is printed. The study primarily aimed to:
1.  Measure the interference of conflicting color stimuli upon reading color names.
2.  Measure the interference of conflicting word stimuli upon naming ink colors.
3.  Examine the effect of practice on these interference effects.

**Paradigm(s) Used & Key Manipulations:**

**Experiment 1: Effect of Interfering Color Stimuli Upon Reading Names of Colors Serially**
*   **Task:** Read a list of color names (red, blue, green, brown, purple).
*   **Stimuli:**
    *   **Condition 1 (RCNd - Reading Color Names different):** Color names printed in an ink color *different* from the color named (e.g., word "RED" printed in blue ink).
    *   **Condition 2 (RCNb - Reading Color Names black):** Color names printed in black ink (control).
*   **Dependent Variable:** Time taken to read 100 color names.
*   **Derived Dimensions (for mapping this condition):**
    *   [[Dimensions/N_Tasks|N_Tasks]]: 1 (Reading words)
    *   [[Dimensions/SOA (Stimulus Onset Asynchrony)|SOA]]: N/A (or 0, if considering the ink color as an attribute presented simultaneously with the word form)
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0
    *   [[Dimensions/Switch Rate|Switch Rate]]: 0
    *   [[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence]]:
        *   RCNd: **Bivalent-Incongruent** (word form + conflicting ink color attribute)
        *   RCNb: **Univalent** (word form + neutral black ink)
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]]: N/A (single task)
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: None/Implicit

**Experiment 2: Effect of Interfering Word Stimuli Upon Naming Colors Serially**
*   **Task:** Name the ink color of presented stimuli.
*   **Stimuli:**
    *   **Condition 1 (NCWd - Naming Color Word different):** Words (names of colors) printed in an ink color *different* from the color named by the word (e.g., word "RED" printed in blue ink – subject should say "blue").
    *   **Condition 2 (NC - Naming Color):** Solid squares of color (control – later revised to swastikas in Exp 3 to better match visual complexity).
*   **Dependent Variable:** Time taken to name 100 ink colors.
*   **Derived Dimensions (for mapping this condition):**
    *   [[Dimensions/N_Tasks|N_Tasks]]: 1 (Naming colors)
    *   [[Dimensions/SOA (Stimulus Onset Asynchrony)|SOA]]: N/A (or 0)
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0
    *   [[Dimensions/Switch Rate|Switch Rate]]: 0
    *   [[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence]]:
        *   NCWd: **Bivalent-Incongruent** (ink color + conflicting word attribute)
        *   NC: **Univalent** (color patch/swastika only)
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]]: N/A (single task)
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: None/Implicit

**Experiment 3: The Effects of Practice upon Interference**
*   **Tasks & Stimuli:** Similar to Exp 1 (RCNd) and Exp 2 (NCWd, NC with swastikas).
*   **Manipulation:** Participants underwent 8 days of practice naming the ink colors of conflicting color words (NCWd task).
*   **Measures:** Performance on NCWd, NC, and RCNd tests before, during, and after the practice period.

**Key Findings:**

1.  **Interference of Color on Word Reading (Exp 1):**
    *   Reading color names printed in conflicting colors (RCNd) took slightly longer (average 2.3 seconds more per 100 words, ~5.6% increase) than reading them in black ink (RCNb).
    *   Stroop notes this difference was not statistically reliable in his main group but Peterson's prediction suggested it might be. (Modern replications often find a small but significant reverse Stroop effect).

2.  **Interference of Words on Color Naming (Exp 2):**
    *   Naming the ink color of words that named a different color (NCWd) took significantly longer (average 47.0 seconds more per 100 items, ~74.3% increase) than naming the color of solid squares/swastikas (NC).
    *   This is the **classic, robust Stroop effect.**

3.  **Practice Effects (Exp 3):**
    *   Practice on the NCWd task (naming ink color of conflicting words) decreased the interference effect (i.e., speeded up performance on NCWd), but did *not* eliminate it.
    *   Practice on NCWd also led to a small improvement in naming colors of squares/swastikas (NC task - transfer).
    *   Critically, practice on NCWd *increased* the interference of color on word reading (i.e., performance on RCNd worsened; the reverse Stroop effect became larger). This suggests that practice in attending to color and suppressing word reading strengthens the color-processing pathway, making it a more potent distractor when word reading is required.

**Authors' Main Conclusions/Interpretations:**

*   The association between a printed word and the act of reading it is significantly stronger and more habitual than the association between a color and naming it.
*   This difference in associative strength (due to extensive lifelong practice with reading) accounts for the large interference of words on color naming and the relatively small interference of colors on word reading.
*   Practice can modify these interference effects, but the fundamental asymmetry due to differential learning history persists. Practicing the weaker task (color naming in the presence of word distractors) can strengthen its pathway, but this may, in turn, increase its potential to interfere with the stronger task (word reading).

**Relevance to Thesis:**

*   **Foundational Interference Study:** This is the seminal paper defining the [[Effects/Stroop Effect|Stroop effect]], a cornerstone phenomenon in [[Interference Control]] and [[Attention]].
*   **[[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]]:** Perfectly exemplifies Bivalent-Incongruent stimuli and their comparison to Univalent (control) stimuli.
*   **Mapping to Super Experiment:**
    *   Both Exp 1 and Exp 2 are [[Dimensions/N_Tasks|N_Tasks]]=1 paradigms.
    *   SE can model these by using one task channel for the "target" dimension (e.g., 'mov' for word form, 'or' for ink color) and the other channel to present the "distractor" dimension simultaneously (`start_mov_1 = start_or_1`, `dur_mov_1 = dur_or_1`).
    *   For the target task, `coh_` would be 1. For the distractor dimension, `coh_` would also be 1 (to represent its presence) in incongruent conditions, and `coh_` = 0 (or stimulus set to neutral) in univalent/control conditions.
    *   The SOA would be 0 here, as attributes are simultaneous.
*   **Task Strength/Automatization:** Highlights how differential practice/automatization of tasks (reading vs. color naming) leads to asymmetrical interference. This is a key concept when considering why some tasks interfere more than others.
*   **Practice Effects & Plasticity:** Experiment 3 provides data on how [[Cognitive Control]] processes and interference effects can be modified (but not entirely overcome) by practice.