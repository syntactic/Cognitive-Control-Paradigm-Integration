#dimension

Definition: Stimulus Onset Asynchrony (SOA) is the time interval between the onset of two distinct stimuli or stimulus features to which a participant must potentially respond or from which they must resolve conflict.

---
###### Relevance in Dual-Task (`N_Tasks=2`) Paradigms

This is the classic definition and the primary independent variable in [[Dual-Task Performance & PRP|PRP]] studies.

*   **Formula:** `SOA = Onset(S2) - Onset(S1)`
*   **Effect:** Short SOA leads to maximal [[PRP Effect]]. Long SOA transitions towards a [[Task Switching]] regime. `SOA=0` is a full dual-task.

---
###### Relevance in Single-Task (`N_Tasks=1`) Paradigms

In single-task paradigms (like Stroop, Flanker, Task Switching with bivalent stimuli), SOA defines the temporal relationship between the **Target feature (S1)** and the **Distractor feature (S2)**.

*   **Rule:** SOA is only applicable if the stimulus is **Bivalent** (i.e., has both a target and a distractor dimension). If the stimulus is **Univalent**, `SOA = N/A`.
*   **Standard Case (SOA = 0):** In most interference and task-switching tasks, the target and distractor features are attributes of a single object presented simultaneously.
    *   *Examples:* Standard [[Canonical Tasks/Stroop Task|Stroop]] (color and word are simultaneous), standard [[Canonical Tasks/Flanker Task|Flanker]] (target and flankers appear at once).
*   **Asynchronous Case (SOA ≠ 0):** Some designs deliberately introduce a delay to study priming or preparation.
    *   **Negative SOA (Distractor First):** `SOA < 0`. The distractor appears *before* the target, priming a response.
        *   *Example:* [[Kopp et al. (1996)]] presented flankers 100ms before the target, resulting in `SOA = -100ms`.
    *   **Positive SOA (Target First):** `SOA > 0`. The target appears *before* the distractor.
        *   *Example:* [[Yeung & Monsell (2003)]] presented a color patch (target) 160ms before the word (distractor), resulting in `SOA = +160ms`.

###### PCA Coding
*   Numerical values are used directly.
*   `N/A` is coded as a distinct placeholder (e.g., **-1**) to differentiate it from `SOA = 0`.