---
tags:
  - dimension
---

### Core Definition
**`Switch Rate`** is a parameter governing the predictability of the cognitive procedure required on a given trial. It is formally defined as the between-trial probability that the "trial procedure" for the current trial (N) will be different from the "trial procedure" for the immediately preceding trial (N-1).

`Switch Rate = P(Procedure_N ≠ Procedure_{N-1})`

The power of this dimension comes from a consistent, formal definition of "trial procedure" across paradigm classes.

---

### Application in Single-Task Paradigms (`Task 2 Resp. Prob. = 0`)

In the context of [[Paradigm Classes/Task Switching]], the **trial procedure is the identity of the required task-set** (e.g., Task A or Task B).

*   **`Switch Rate = 0%`**: A pure block (e.g., A, A, A, A...). `P(Switch) = 0`.
*   **`Switch Rate = 50%`**: A standard mixed block with two tasks chosen randomly. `P(Switch) = 0.5`.
*   **`Switch Rate = 100%`**: A predictable alternating block (e.g., A, B, A, B...). `P(Switch) = 1`.

---

### Application in Dual-Task Paradigms (`Task 2 Resp. Prob. = 1`)

In the context of [[Paradigm Classes/Dual-Task Performance & PRP]], the **trial procedure is the ordered pair of tasks** assigned to the T1 and T2 processing channels, e.g., `(Task_for_T1, Task_for_T2)`.

*   **`Switch Rate = 0%`**: Defines a **standard, procedurally stable PRP paradigm**. The trial procedure is fixed throughout the block (e.g., it is *always* `(A, B)`). `P(Switch) = 0`. This applies to [[McCann & Johnston (1992)]] and [[Lien et al. (2003)]] Exp. 3.

*   **`Switch Rate > 0%`**: Defines a **procedurally variable PRP paradigm**. The trial procedure is unpredictable and changes from trial to trial.

#### Interpreting Switch Rate in Bridge Paradigms

For bridge paradigms like [[Hirsch et al. (2018)]] and [[Lien et al. (2003)]] (Exp 1 & 2), the trial procedure is drawn **uniformly at random** on each trial from a pool of N possible procedures.

The switch rate for such a design is mathematically determined:
`Switch Rate = (N-1) / N`

*   **The Hirsch/Lien Case:** These experiments draw from a pool of **N=4** procedures: `(A,A)`, `(B,B)`, `(A,B)`, `(B,A)`.
    *   The probability of repeating a procedure is `1/4 = 25%`.
    *   The probability of switching to a different procedure is `3/4 = 75%`.
    *   Therefore, the correct coding for these experiments is **`Switch Rate = 75%`**.

*   **Hypothetical Example (25% Switch Rate):** A `Switch Rate` of `25%` would describe a different hypothetical experiment where the procedure from the previous trial is repeated 75% of the time, and a switch to one of the other three procedures only occurs 25% of the time. This represents a context with a strong bias *towards* procedural stability.
