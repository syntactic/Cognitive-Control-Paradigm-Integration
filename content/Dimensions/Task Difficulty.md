#dimension 

**Definition:** An inclusive measure reflecting the overall processing demands required to successfully perform a single task instance, encompassing perceptual load, cognitive load (e.g., rule complexity, working memory, transformations), and response selection demands.

**Directionality for Coding:**
*   Higher numerical values indicate **higher** difficulty.
*   Lower numerical values indicate **lower** difficulty.

**Ordinal Scale (1-5) for Literature Coding:**

*   **1: Very Low Difficulty**
    *   Description: Simple detection of highly salient stimuli; minimal cognitive/response load.
    *   Examples: Simple RT to clear stimulus.
    *   Typical SE Coherence (if applicable): ~0.9-1.0 (after transformation)
*   **2: Low Difficulty**
    *   Description: Simple discrimination (e.g., 2-AFC) of clear stimuli; low cognitive load.
    *   Examples: Standard 2-AFC with distinct options; Go/No-Go with simple rule; Word Reading in Stroop.
    *   Typical SE Coherence: ~0.7-0.85
*   **3: Moderate Difficulty**
    *   Description: Discrimination among a few alternatives (3-4) or more complex 2-AFC; some rule complexity/WM load; common level for many experimental tasks.
    *   Examples: Typical task-switching tasks (e.g., letter/digit); Color Naming in Stroop; PRP tasks with two 2-AFCs; Flanker/Simon tasks.
    *   Typical SE Coherence: ~0.4-0.65 (default for instantiation often 0.5)
*   **4: High Difficulty**
    *   Description: Discrimination among many alternatives (>4); significant S-R mapping complexity or rule transformation; higher WM load; potentially degraded/ambiguous stimuli.
    *   Examples: N-back (2+); mental rotation; categorization with fuzzy boundaries.
    *   Typical SE Coherence: ~0.15-0.35
*   **5: Very High Difficulty**
    *   Description: Tasks approaching perceptual/cognitive limits; very complex rules; near-threshold discriminations.
    *   Examples: Fine psychophysical discriminations; extremely complex, poorly learned S-R maps.
    *   Typical SE Coherence: ~0.0-0.1

**Criteria for Assignment:**
1.  Author's explicit manipulations/labels of difficulty.
2.  Number of S-R alternatives.
3.  Inferred cognitive load (rule complexity, WM, transformations, inhibition needs).
4.  Perceptual discriminability/stimulus clarity.
5.  (Secondary) Baseline error rates/RTs.

**PCA-Compatible Representation (Level 2):**
*   The 1-5 ordinal scale can be used directly.
*   For PCA, these values should be **normalized** (e.g., min-max scaling to 0-1 range, or z-score standardization) if other variables in the PCA are on different scales or if the interval assumption of the ordinal scale is a concern.
    *   Min-Max Scaling Example (if 1-5 is used): `Normalized_Difficulty = (Original_Difficulty - 1) / (5 - 1)`
        *   1 -> 0
        *   2 -> 0.25
        *   3 -> 0.5
        *   4 -> 0.75
        *   5 -> 1
*   "Not Specified" or "N/A" requires a specific strategy (e.g., placeholder like -1, imputation, or exclusion from PCA).

**Super Experiment Instantiation (Level 3 - `coh_` parameter):**
*   SE `coherence` parameter (0 to 1, where 1 is easiest/clearest).
*   Transformation: `SE_coherence = 1 - Normalized_Difficulty` (assuming Normalized_Difficulty is 0 for easiest, 1 for hardest).
    *   Example (using the 0-1 normalized difficulty from above):
        *   Difficulty Level 1 (Normalized 0) -> SE Coherence = 1.0
        *   Difficulty Level 2 (Normalized 0.25) -> SE Coherence = 0.75
        *   Difficulty Level 3 (Normalized 0.5) -> SE Coherence = 0.5
        *   Difficulty Level 4 (Normalized 0.75) -> SE Coherence = 0.25
        *   Difficulty Level 5 (Normalized 1.0) -> SE Coherence = 0.0
*   If original paper specifies coherence, use that directly. If not, use this transformation from the coded difficulty level.
*   If Task Difficulty coded as "Not Specified," a default SE coherence (e.g., 0.5) can be used for instantiation, with this assumption noted.

**Notes:**
*   This "Task Difficulty" dimension is an abstraction. SE's `coherence` primarily models perceptual difficulty. Using it as a stand-in for broader cognitive difficulty for SE instantiation is a practical simplification and should be acknowledged.
*   Distinguish between difficulty of *executing a single task instance* vs. *managing multiple tasks/switching* (which is captured by other dimensions like Switch Rate, Mixing Cost effect, etc.).