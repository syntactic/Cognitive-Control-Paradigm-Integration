---
tags:
  - dimension
---

### Core Definition
**`Switch Rate`** is a parameter governing the **predictability of the cognitive procedure** required on a given trial. It refers to the between-trial probability that the "trial procedure" for the current trial (N) will be different from the "trial procedure" for the previous trial (N-1).

The precise operationalization of a "trial procedure" depends on the `[[Dimensions/Number of Tasks|Number of Tasks]]`, giving this dimension a powerful but clearly defined role in differentiating paradigms.

### Values
**Continuous (%)**, typically ranging from 0% to 100%.
*   **`0%`**: A procedurally stable block. The trial procedure is constant.
*   **`50%`**: A procedurally variable block with random sequencing (for two main procedure types).
*   **`100%`**: A procedurally variable block with predictable alternation.

---

### Application in `Number of Tasks = 1` Paradigms (Canonical Meaning)

In the context of [[Paradigm Classes/Task Switching|task-switching]], where only one task is performed per trial, the "trial procedure" is simply the identity of the required task set (e.g., "Color Task" or "Shape Task").

*   **`Switch Rate` here retains its classic meaning:** the probability of switching task rule sets from one trial to the next.
*   A `Switch Rate` of `0%` defines a **pure task block**.
*   A `Switch Rate > 0%` defines a **mixed-task block**, which is the necessary context for measuring a [[Effects/Switch Cost|Switch Cost]].

---

### Application in `Number of Tasks = 2` Paradigms (Procedural Variability)

In the context of [[Paradigm Classes/Dual-Task Performance & PRP|dual-task]] paradigms, the "trial procedure" is the **ordered pair of tasks** assigned to the T1 and T2 processing channels, e.g., `(Task_for_T1, Task_for_T2)`. `Switch Rate` here becomes a measure of **between-trial procedural variability**, capturing how predictable this ordered pair is from one trial to the next.

*   **`Switch Rate = 0%`**: Defines a **standard, procedurally stable PRP paradigm**. The trial procedure is fixed throughout the block (e.g., it is *always* `(Task A, Task B)`). The participant knows exactly what to expect. This applies to classic studies like [[McCann & Johnston (1992)|McCann & Johnston 1992]].

*   **`Switch Rate > 0%`**: Defines a **procedurally variable "bridge" paradigm**. The trial procedure is unpredictable and changes from trial to trial, forcing the participant to actively monitor and maintain a more flexible cognitive set. This is the key feature that distinguishes these paradigms from standard PRP.

### Resolving the Key "Bridge" Paradigms

This definition allows us to cleanly and unambiguously code the complex bridge paradigms that test the limits of our framework.

1.  **[[Hirsch et al. (2018)]]:**
    *   **The Challenge:** A dual-task block where the task for T1 and T2 could be the same or different on any given trial.
    *   **The Solution:** The repertoire of trial procedures `(T1, T2)` includes `(A,A)`, `(B,B)`, `(A,B)`, and `(B,A)`, which are chosen randomly. Because the procedure varies from trial to trial, this is a procedurally variable block.
    *   **Coding:** `Switch Rate = 50%`. The `[[Dimensions/Trial Transition Type|Trial Transition Type]]` dimension is then repurposed to describe the *within-trial* relationship (`Switch` for `(A,B)` trials, `Repeat` for `(A,A)` trials). This correctly captures both the block-level unpredictability and the condition-level manipulation.

2.  **[[Sigman & Dehaene (2006)]]:**
    *   **The Challenge:** A dual-task block where the *order* of the two tasks was randomized, leading to a wide distribution of SOAs from negative to positive.
    *   **The Solution:** While this could be coded as a procedurally variable block (`Switch Rate = 50%` as the procedure switches between `(A,B)` and `(B,A)`), we have a **more precise and less abstract dimension available**: [[Dimensions/Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]].
    *   **Coding:** We choose the more precise representation. `Switch Rate` is coded as `0%`. The task order uncertainty is captured directly by coding two representative conditions: one with a positive mean SOA (`500ms`) and one with a negative mean SOA (`-500ms`). This avoids redundancy and uses the most powerful feature for the job.

### Super Experiment Mapping
In the `viewer.js` client, the logic within `generateTaskAssignmentSequence()` implements this dimension.
*   For `N_Tasks=1`, it determines the sequence of task types based on the switch probability.
*   For `N_Tasks=2` and `Switch Rate > 0%`, it correctly interprets this as a mandate to randomize the assignment of the two available task types to the T1 and T2 channels on each trial, thus simulating the procedural variability of bridge paradigms like Hirsch et al.
