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
A categorical dimension that describes the relationship between the cognitive procedure required on the current trial (N) and the procedure required on the immediately preceding trial (N-1). This dimension's specific meaning is contextualized by `[[Dimensions/Switch Rate|Switch Rate]]` and `[[Dimensions/Number of Tasks|Number of Tasks]]`.

### Values

*   **`Pure`**
    *   **Description:** This trial occurs within a block where the same cognitive procedure is applied on every single trial.
    *   **Relevance:** This is the defining feature of blocks with a `Switch Rate = 0%`. It applies to single-task pure blocks (the baseline for [[Effects/Mixing Cost]]) and to standard, procedurally stable [[Paradigm Classes/Dual-Task Performance & PRP|PRP]] paradigms where the `(T1, T2)` assignment is fixed.

*   **`Switch`**
    *   **Description:** The cognitive procedure on trial N is different from the one on trial N-1.
    *   **Relevance:** This is the critical condition for measuring costs of change. It can only exist in blocks where `Switch Rate > 0%`.

*   **`Repeat`**
    *   **Description:** The cognitive procedure on trial N is the same as the one on trial N-1.
    *   **Relevance:** This is the intra-block baseline for calculating the [[Effects/Switch Cost]]. It can only exist in blocks where `Switch Rate > 0%`.

*   **`N/A` (Not Applicable)**
    *   **Description:** Used for conditions where the concept of a trial-to-trial procedural switch is either not the primary manipulation or is confounded by other, more dominant experimental variables.
    *   **Rule:** This value is used in two specific cases:
        1.  The very first trial of any block, as it has no preceding trial.
        2.  For paradigms where the primary manipulation is a **randomized temporal parameter** (like `Inter-task SOA` or `RSI`) that makes a simple trial-to-trial procedural comparison (`Switch` vs. `Repeat`) meaningless or misleading.

### Context-Specific Application

#### 1. In `Number of Tasks = 1` Paradigms
The dimension has its canonical meaning, referring to the transition between task rule sets.
*   **`Pure`:** Used in pure blocks (`Switch Rate = 0%`).
*   **`Switch`/`Repeat`:** Used in mixed blocks (`Switch Rate > 0%`) to distinguish the trial types.

#### 2. In `Number of Tasks = 2` Paradigms

This is where the new rules are critical:

*   **For `[[Hirsch et al. (2018)]]`:**
    *   The `Switch Rate` is `50%` to capture the block-level procedural variability.
    *   `Trial Transition Type` is then repurposed to describe the **within-trial relationship** between T1 and T2. A trial where T1 and T2 use different tasks is coded as `Switch`, and a trial where they use the same task is coded as `Repeat`. This is a deliberate, documented abstraction to capture the study's unique factorial design.

*   **For `[[Sigman & Dehaene (2006)]]`:**
    *   The core manipulation is the randomization of `Inter-task SOA` across a wide positive and negative range, captured by coding two representative conditions (`SOA=500ms`, `SOA=-500ms`). `Switch Rate` is `0%` because we are using the more precise `SOA` dimension.
    *   Because the SOA is randomized, a trial with `SOA=500ms` could be followed by one with `SOA=-500ms`. Is this a "switch"? Is a `500ms` trial followed by another `500ms` trial a "repeat"? The question becomes meaningless. The dominant variable is the SOA, not the trial-to-trial sequence.
    *   Therefore, `Trial Transition Type` is coded as **`N/A`**. This signals that the primary axis of variation in this experiment is temporal, not sequential.

### Summary Rationale

This refined definition creates a clear hierarchy:
1.  Is the block procedurally stable or variable? (`Switch Rate`)
2.  If it's stable, all trials are `Pure`. (`TTT`)
3.  If it's variable, are the transitions meaningful to compare?
    *   Yes -> `Switch`/`Repeat`. (`TTT`)
    *   No (confounded by a randomized temporal variable) -> `N/A`. (`TTT`)
