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
A categorical dimension that describes the relationship between the cognitive procedure required on the current trial (N) and the procedure required on the immediately preceding trial (N-1). This dimension's specific meaning is contextualized by `[[Dimensions/Switch Rate]]` and `[[Dimensions/Task 2 Response Probability]]`.

### Values

*   **`Pure`**: This trial occurs within a block where the same cognitive procedure is applied on every single trial. Applies only when `Switch Rate = 0%`.
*   **`Switch`**: The cognitive procedure on trial N is different from the one on trial N-1. Applies only when `Switch Rate > 0%`.
*   **`Repeat`**: The cognitive procedure on trial N is the same as the one on trial N-1. Applies only when `Switch Rate > 0%`.
*   **`N/A`**: Used for conditions where a trial-to-trial procedural comparison is not a controlled variable, such as the first trial of a block or trials within a fully randomized sequence where the analysis averages over trial history.

### Context-Specific Application

#### 1. In Task-Switching (`Task 2 Resp. Prob. = 0`)
The dimension has its canonical meaning, referring to the transition between task rule sets.
*   **`Pure`**: Used in pure blocks (`Switch Rate = 0%`).
*   **`Switch`/`Repeat`**: Used in mixed blocks (`Switch Rate > 0%`) to distinguish the trial types.

#### 2. In Dual-Task (`Task 2 Resp. Prob. = 1`)
This is where the new rules are critical for clarity:

*   **For `[[Hirsch et al. (2018)]]` and `[[Lien et al. (2003)]]` (Exp 1 & 2):**
    *   The `Switch Rate` is `> 0%` to capture the block-level procedural variability.
    *   Because the sequence of trial procedures (e.g., (A,A) -> (A,B)) is randomized, a simple comparison of N vs N-1 is not the primary manipulation. The analyses in these papers average across all trial histories.
    *   Therefore, `Trial Transition Type` is coded as **`N/A`**. The within-trial relationship is now captured by `[[Dimensions/Intra-Trial Task Relationship]]`.

*   **For standard PRP and `[[Lien et al. (2003)]]` (Exp 3):**
    *   The `Switch Rate` is `0%`.
    *   Therefore, all trials are coded as **`Pure`**.
