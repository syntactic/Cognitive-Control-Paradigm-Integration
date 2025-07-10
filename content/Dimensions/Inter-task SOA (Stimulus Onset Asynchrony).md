---
aliases:
  - SOA
---
#dimension

Definition: The time interval between the onset of the stimulus for Task 1 (S1) and the onset of the stimulus for Task 2 (S2). It is the primary independent variable in classic [[Dual-Task Performance & PRP|PRP]] studies.

---
###### Relevance in Dual-Task (`Number of Tasks=2`) Paradigms

This is the classic definition and the primary independent variable in [[Dual-Task Performance & PRP|PRP]] studies.

*   **Formula:** `SOA = Onset(S2) - Onset(S1)`
*   **Effect:** Short SOA leads to maximal [[PRP Effect]]. Long SOA transitions towards a [[Task Switching]] regime. `SOA=0` is a full dual-task.

***Exception: RSI-Driven Dual-Task Paradigms***
In some dual-task designs, particularly those focused on preparation effects after the first response, the primary temporal manipulation is the **[[Dimensions/RSI (Response Stimulus Interval)|RSI]]**—the interval between the response to Task 1 (R1) and the stimulus for Task 2 (S2). This is notably used in [[Allport el al. (1994)|Allport et al. 1994]] Exp. 5.

*   In these cases, the SOA is not a fixed, independent variable but rather a *consequence* of performance (`SOA = RT1 + RSI`).
*   **Coding Rule:** For such paradigms, the `SOA` column should be coded as **`N/A`** to distinguish them from classic PRP designs. The critical timing information is captured in the `RSI` column.

---
#### PCA Coding and Applicability
In the design space, the applicability of SOA is a critical feature. For PCA, this is handled by two features:
 - **SOA_ms (Numeric):** The numerical value of the SOA. When SOA is N/A, this is imputed to -1 for the analysis.