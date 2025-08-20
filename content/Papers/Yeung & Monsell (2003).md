---
tags:
  - paper
---
**Full Title:** Switching Between Tasks of Unequal Familiarity: The Role of Stimulus-Attribute and Response-Set Selection

**Authors:** Nick Yeung, Stephen Monsell

**Year:** 2003

**Journal:** Journal of Experimental Psychology: Human Perception and Performance

**Core Goal:**
To investigate the "paradoxical" asymmetry in [[Effects/Switch Cost|Switch Costs]] reported by Allport et al. (1994), where it can be harder to switch to a stronger, well-practiced task than to a weaker one. The authors explore whether this asymmetry is dependent on the level of between-task interference and how manipulations aimed at reducing interference (by facilitating stimulus-attribute selection or separating response sets) affect switch costs.

**Paradigm(s) Used:**
[[Task Switching]] paradigms, primarily using:
-   **Experiment 1:** Stroop-like tasks – switching between color naming (weaker) and word naming (stronger). Stimuli were words on colored rectangles.
-   **Experiments 2a & 2b:** Switching between digit naming (stronger) and a derived digit task (weaker):
    -   Exp 2a: Odd/Even classification.
    -   Exp 2b: Tens-complement naming (e.g., "3" -> "seven").
-   **Experiment 3:** Switching between digit naming (stronger, vocal response) and color naming (weaker, varied response modality/category).

**Key Manipulations:**

1.  **Stimulus Attribute Onset Asynchrony (SOA within stimulus, Exp 1):** The onset of the word attribute was delayed relative to the color patch onset (0ms, 160ms, or 320ms delay). This was *not* a traditional trial-to-trial SOA or a CSI, but a manipulation to make selection of the color attribute easier by giving it a temporal advantage.
2.  **[[Dimensions/Response Set Overlap|Response Set Overlap]] (Exp 2 & 3):**
    *   **Exp 2a (Digit Naming vs. Odd/Even):** Different response categories (digit names vs. "odd"/"even"), same modality (vocal). *Result: Disjoint by category.*
    *   **Exp 2b (Digit Naming vs. Tens-Complement):** Same response categories (digit names), same modality (vocal). *Result: Identical.*
    *   **Exp 3 (Digit Naming vs. Color Naming):** Systematically varied overlap:
        *   **Full Overlap:** Spoken digit names for strong task; spoken digit names (arbitrarily mapped) for weak task.
        *   **Modality Overlap (Category Disjoint):** Spoken digit names (strong); spoken direction words (arbitrarily mapped) for color (weak).
        *   **Category Overlap (Modality Disjoint):** Spoken digit names (strong); manual keypresses 1-4 (arbitrarily mapped) for color (weak).
        *   **No Overlap:** Spoken digit names (strong); manual keypresses for directions (arbitrarily mapped) for color (weak).
3.  **Task Strength/Familiarity:** Inherently manipulated by choosing tasks like word/digit naming (strong) versus color naming, odd/even, or tens-complement (weaker).
4. [[RSI (Response Stimulus Interval)]]: 1000ms (Exp 1), 1200ms (Exp 2), 1000ms (Exp 3)

**Key Findings:**

1. **High Interference Conditions:** Switch costs larger for switching to stronger task (replicating Allport's asymmetry)
2. **Reduced Interference Conditions:** Asymmetry reverses - larger costs to weaker task
   - **Exp 1:** Delayed word onset reversed asymmetry  
   - **Exp 2a:** Disjoint response categories favored stronger task
   - **Exp 3:** Separated response sets reversed asymmetry
3. **Interference Reduction:** Manipulations reduced overall interference but key finding was asymmetry reversal
4. **Model:** Task activation = task strength + control input + task priming. Asymmetrical priming after weak tasks (requiring more control) explains both patterns depending on interference level.

**Main Conclusions:**
- Asymmetrical switch costs (larger to stronger task) occur with high between-task interference
- Reduced interference reverses asymmetry (larger costs to weaker task)  
- Switch costs arise from interaction between task priming and endogenous control
- Separating response sets effectively reduces interference and changes switch cost dynamics

**Relevance to Thesis:**

-   **Critical for [[Dimensions/Response Set Overlap|Response Set Overlap]]:** Provides direct empirical evidence on how different degrees and types of response set overlap (identical, category-disjoint, modality-disjoint, fully disjoint) modulate [[Effects/Switch Cost|Switch Costs]] and their asymmetry.
-   **Informs [[Dimensions/Stimulus-Stimulus Congruency]]:** Experiment 1, by manipulating the temporal distinctiveness of stimulus attributes, addresses a form of stimulus-level interference that impacts congruency and selection.
-   **Nuances Asymmetric Switch Costs:** Moves beyond a simple "stronger task always harder to switch to" by showing this is context-dependent (high interference). This is a key refinement of the Allport et al. (1994) findings.
-   **Interaction of Factors:** Demonstrates the interplay between task strength, interference levels (due to stimulus and response factors), and control processes in determining switching performance.
-   **Mapping to Super Experiment:**
    *   Exp 1's SOA-within-stimulus is tricky for SE. SE's `start_mov_1` vs `start_or_1` could simulate attributes appearing at different times, but SE's cueing is tied to the *task*, not individual attributes within a bivalent stimulus for one task. This might be a limitation or require careful interpretation for SE mapping.
    -   The Super Experiment's client UI (`index.html`, `experiment.js`) allows direct selection of "Identical" or "Disjoint" response set relationships.
    -   **"Identical" in SE** (same keys for same conceptual responses, e.g., 'a'/'d' for left/right for both tasks) can model:
        -   Their "Full Overlap" condition (Exp 3), where both tasks used spoken digit names.
        -   Their "Tens-Complement Naming" vs. "Digit Naming" (Exp 2b), where both used spoken digit names (Identical response categories).
    -   **"Disjoint" in SE** (e.g., 'a'/'d' for movement task, 'w'/'s' for orientation task) can model:
        -   Their "No Overlap" condition (Exp 3: spoken digits vs. manual direction keys). This is a good mapping as SE uses different keys for different conceptual dimensions.
        -   Their "Category Overlap" (Exp 3: spoken digits vs. manual digit keys) can be approximated if one conceptual dimension (e.g., digit identity) is mapped to different effectors/key groups.
        -   Their "Modality Overlap" (Exp 3: spoken digits vs. spoken directions) is harder to map directly since SE is keypress-based, but the "Orthogonal" setting (distinct key groups for distinct conceptual dimensions) captures the essence of disjoint response categories within the same manual modality.
        -   Their "Odd/Even Classification" vs. "Digit Naming" (Exp 2a), though both vocal, used different response categories. "Orthogonal" in SE (mapping to different key groups) is the closest analogy for distinct response categories.
    -   The SE's `movementKeyMap` and `orientationKeyMap` are dynamically configured by `experiment.js` based on the UI selection, allowing these different overlap conditions to be set up more directly.
-   Connects to the literature on task-set inertia, priming, and the strategic allocation of control.