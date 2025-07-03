#dimension

Definition: Stimulus Onset Asynchrony (SOA) is the time interval between the onset of two distinct stimuli or stimulus features to which a participant must potentially respond or from which they must resolve conflict.

---
###### Relevance in Dual-Task (`N_Tasks=2`) Paradigms

This is the classic definition and the primary independent variable in [[Dual-Task Performance & PRP|PRP]] studies.

*   **Formula:** `SOA = Onset(S2) - Onset(S1)`
*   **Effect:** Short SOA leads to maximal [[PRP Effect]]. Long SOA transitions towards a [[Task Switching]] regime. `SOA=0` is a full dual-task.

***Exception: RSI-Driven Dual-Task Paradigms***
In some dual-task designs, particularly those focused on preparation effects after the first response, the primary temporal manipulation is the **[[Dimensions/RSI (Response Stimulus Interval)|RSI]]**—the interval between the response to Task 1 (R1) and the stimulus for Task 2 (S2). This is notably used in [[Allport el al. (1994)|Allport et al. 1994]] Exp. 5.

*   In these cases, the SOA is not a fixed, independent variable but rather a *consequence* of performance (`SOA = RT1 + RSI`).
*   **Coding Rule:** For such paradigms, the `SOA` column should be coded as **`N/A`** to distinguish them from classic PRP designs. The critical timing information is captured in the `RSI` column.

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
#### PCA Coding and Applicability
In the design space, the applicability of SOA is a critical feature. For PCA, this is handled by two features:
- **SOA_is_NA (Binary: 0 or 1):** This feature indicates whether SOA is the primary, manipulated temporal variable between the critical stimulus events.
     - **SOA_is_NA = 0 (SOA is Applicable):** This is the standard case for classic [[Dual-Task Performance & PRP]] paradigms and for single-task [[Interference Control]] paradigms with asynchronous bivalent features.
     - **SOA_is_NA = 1 (SOA is Not Applicable):** This occurs in two distinct situations:
         1. **Single-Task Univalent:** The paradigm involves only one task with univalent stimuli, so there is no second stimulus event to measure an asynchrony against (e.g., a "target alone" Flanker trial).
         2. **RSI-Driven Dual-Task:** The paradigm involves two S-R episodes (N_Tasks=2), but the key temporal manipulation is the **[[Dimensions/RSI (Response Stimulus Interval)|RSI]]**, which is the interval from the response of T1 to the stimulus of T2 (e.g., [[Allport el al. (1994)]] Exp. 5). In these cases, SOA is a dependent variable, not the manipulated one. 
 - **SOA_ms (Numeric):** The numerical value of the SOA. When SOA_is_NA is 1, this is imputed to 0 for the analysis.