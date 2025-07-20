---
tags:
  - methodology
  - data_processing
  - conflict
  - guide
aliases:
  - Conflict Coding
---
# Conflict Coding Guide

### Purpose
This document provides the canonical guidelines for coding conflict-related dimensions in the `super_experiment_design_space.csv` dataset. It formalizes the use of two precise, orthogonal dimensions to capture conflict: **`Stimulus-Stimulus (S-S) Congruency`** and **`Stimulus-Response (S-R) Congruency`**. Adherence to this guide is mandatory to ensure the logical consistency of the parametric design space.

### The Core Principle: Semantic vs. Structural Priming

The distinction between S-S and S-R conflict is determined by whether an irrelevant stimulus feature primes a response via a **learned, semantic association** or via a **direct, structural correspondence**. To determine the conflict type, we analyze the relationship between the irrelevant stimulus feature (`S_irrelevant`) and the response.

#### **1. Stimulus-Stimulus (S-S) Congruency: Conflict via Semantic Association**

This conflict occurs when `S_irrelevant` has a learned, semantic relationship with an item in the abstract **Response Set** (the set of possible answers, e.g., the words {"blue", "red"}).

*   **Mechanism:** `S_irrelevant` -> (primes) -> **Conceptual Response Category**
*   **Rule of Thumb:** Does the irrelevant part of the stimulus *mean* the same thing as one of the possible answers?
*   **Applies To:** Stroop/Flanker tasks (perceptual conflict) and task-switching with bivalent stimuli (operational conflict).

#### **2. Stimulus-Response (S-R) Congruency: Conflict via Structural Correspondence**

This conflict occurs when `S_irrelevant` has a direct, structural (e.g., spatial, directional) correspondence with the physical **Response Effector** or action.

*   **Mechanism:** `S_irrelevant` -> (primes) -> **Physical Motor Action**
*   **Rule of Thumb:** Does the irrelevant part of the stimulus directly map onto the physical action, bypassing its meaning?
*   **Applies To:** Simon and Simon-like tasks (e.g., pitch-height, affective congruency).

### The N/A vs. Neutral Litmus Test

To distinguish between a functionally univalent stimulus (coded as S-S Congruency: N/A) and a truly bivalent but neutral stimulus (coded as S-S Congruency: Neutral), apply the following two-question test to the irrelevant stimulus attribute:

**Question 1: Does the stimulus possess a second, potentially interfering attribute?**

- If **No** (e.g., a simple color patch in a color-naming task), the stimulus is univalent. Code as S-S Congruency: N/A.
- If **Yes** (e.g., a colored word, a numeral with value and count), proceed to Question 2.

**Question 2: Is this second attribute "response-relevant"?**

- An attribute is response-relevant if, and only if, it maps onto a response within the competing task's response set.
- If **No** (e.g., the ink color "black" when the competing task's response set is {red, blue, green}; or the word "XXXXX" when the competing task's response set is {red, blue, green}), the stimulus is **functionally univalent**. The irrelevant attribute is inert. **Code as S-S Congruency: N/A**.
- If **Yes** (e.g., the word "BLUE" when the competing task is word-reading; the value '4' when the competing task is parity judgment), the stimulus is **truly bivalent**. You must then determine if the trial is Congruent, Incongruent, or **Neutral** (if the attribute is response-relevant but orthogonal on this trial, e.g. the word "TABLE").

### The Pragmatic Coding Rule: Prioritizing the Source of Conflict

To avoid ambiguity, we apply a clear rule of precedence:

**If a paradigm involves S-S conflict, it should be coded under `S-S Congruency`, and `S-R Congruency` should be marked as `N/A`, *unless both are being factorially manipulated* (as in [[Egner et al. (2007)]]).**

This prioritizes the conflict at its origin—the competition between stimulus representations or afforded operations.
#### A Critical Test Case: Modeling the Stroop Asymmetry
Both classic Stroop (naming the ink color) and Reverse Stroop (reading the word) are structurally **Type 4B ensembles** under the Kornblum et al. (1990) model, as both the relevant and irrelevant dimensions pertain to color concepts. Therefore, incongruent trials in both tasks are coded as **`S-S Congruency: Incongruent`**.

The famous empirical asymmetry in the magnitude of the interference effect is not captured by this dimension alone. Instead, the framework models it as an **interaction between `S-S Congruency` and `Task Difficulty`**:

*   **Classic Stroop:** An easy irrelevant task (Word Reading, Difficulty=`2`) interferes strongly with a harder relevant task (Color Naming, Difficulty=`3`), producing a large congruency effect.
*   **Reverse Stroop:** A harder irrelevant task (Color Naming, Difficulty=`3`) interferes weakly with an easy relevant task (Word Reading, Difficulty=`2`), producing a small congruency effect.

This approach ensures that the *type* of conflict is coded consistently, while the *behavioral outcome* is explained by the interplay of multiple parameters in the design space.

---
## Worked Examples

#### Example A: Classic Stroop (Bivalent-Incongruent)
*   **Stimulus:** Word "BLUE" in red ink, centered.
*   **Task:** Name the ink color.
*   **Analysis:** The conflict is between two semantic features (word vs. color). This is primary S-S conflict.
*   **New Coding:**
    *   `S-S Congruency`: **`Incongruent`**
    *   `S-R Congruency`: **`N/A`** (Following the pragmatic rule)

#### Example B: Classic Simon Task (Univalent Stimulus, S-R Conflict)
*   **Stimulus:** A red dot appears on the left.
*   **Task:** Press the "red" key (e.g., a right-hand key).
*   **Analysis:** The stimulus itself is simple (univalent). The conflict is between its irrelevant spatial location and the required response location. This is pure S-R conflict.
*   **New Coding:**
    *   `S-S Congruency`: **`N/A`** (No irrelevant semantic feature).
    *   `S-R Congruency`: **`Incongruent`**

#### Example C: Neutral Stroop (Bivalent-Neutral)
*   **Stimulus:** Word "TABLE" in red ink, centered.
*   **Analysis:** There is an irrelevant stimulus feature (the word), but it doesn't map to the response set. This is a neutral S-S relationship.
*   **New Coding:**
    *   `S-S Congruency`: **`Neutral`**
    *   `S-R Congruency`: **`N/A`**

#### Example D: Semantic Simon Task (Non-Spatial S-R Conflict)
*   **Stimulus:** The word "UP" appears centrally, printed in red.
*   **Task:** Respond to the *ink color* (red) with a spatially mapped key (e.g., a left/right keypress).
*   **Analysis:** The relevant feature is color. The irrelevant feature is the word meaning "UP". "UP" is orthogonal to color, but it has a strong, automatic mapping to an up/down response. If the response keys were up/down, this would create S-R conflict. Since the response keys are left/right, there is no dimensional overlap.
*   **New Coding:**
    *   `S-S Congruency`: **`Neutral`** (The word "UP" is neutral with respect to a red/blue color judgment).
    *   `S-R Congruency`: **`N/A`** (The irrelevant dimension, "up-ness", does not map to the left/right response dimension).
    *   **Insight:** This example shows how the system correctly identifies no conflict if the irrelevant feature and the response dimension do not overlap. If the responses *were* up/down keys, the coding would become `S-R Congruency: Incongruent` (assuming the "red" rule mapped to the down key).

#### Example E: Multi-Level Conflict (The "French Noun" Paradigm)

This hypothetical task-switching paradigm demonstrates how the dimensions interact to capture complex designs.

*   **Stimulus:** The French noun "la souris" (the mouse).
*   **Tasks:** Switch between "determine animacy" and "determine gender."
*   **Response Mapping:** `Left Key` = animate / masculine; `Right Key` = inanimate / feminine.
*   **Analysis of a Switch Trial for "la souris":**
    1.  **Stimulus Ambiguity:** The stimulus is bivalent because it affords two operations (animacy and gender judgment). This is a potential S-S conflict.
    2.  **Apply Task Rules:**
        *   Animacy: "souris" is *animate* -> `Left Key`.
        *   Gender: "la souris" is *feminine* -> `Right Key`.
    3.  **Determine Congruency:** The two afforded operations lead to conflicting motor responses (Left vs. Right). This is an Incongruent S-S relationship.
*   **New Coding:**
    *   `S-S Congruency`: **`Incongruent`**
    *   `S-R Congruency`: **`N/A`** (The conflict is not spatial or structural).
    *   **Insight:** This shows how `S-S Congruency` captures not just perceptual conflict (Stroop), but also "post-operational" conflict that emerges after applying competing task rules to a bivalent stimulus. If the stimulus were "le chien" (the dog), it would be `S-S Congruency: Congruent`.

---

## Summary of Coding for Canonical Paradigms

| Paradigm Example | New `S-S Congruency` | New `S-R Congruency` | Rationale for New Coding |
| :--- | :--- | :--- | :--- |
| **Classic Stroop Task** | `Incongruent` | `N/A` | Conflict is S-S. By rule, S-R is N/A. |
| **Classic Simon Task** | `N/A` | `Incongruent` | No S-S conflict. Conflict is purely S-R (spatial). |
| **Classic Flanker Task** | `Incongruent` | `N/A` | Conflict is between identities (S-S). By rule, S-R is N/A. |
| **Egner et al. (2007) Factorial** | `Incongruent` | `Congruent` | This is the exception that proves the rule. The paradigm explicitly manipulates both, so both are coded. This is a rare "bridge" case. |
| **Semantic Simon Task** | `Neutral` | `Incongruent` | The relevant task (e.g., color) is orthogonal to the irrelevant semantic direction ("UP"), making this a pure S-R conflict. |
