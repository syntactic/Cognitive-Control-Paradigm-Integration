---
tags:
  - paper
  - task_switching
  - cognitive_control
  - residual_switch_cost
  - preparation
aliases:
  - De Jong (2000)
---

### Core Goal
To explain the origin of the **[[Effects/Switch Cost|Residual Switch Cost]]**—the performance cost that persists in task switching even with long preparation intervals. De Jong challenges existing theories by proposing and testing the **"Failure-to-Engage" (FTE) hypothesis**. This account posits that residual costs do not arise from a fundamental inability to complete [[Theoretical Concepts/Task-Set Reconfiguration|reconfiguration]] in advance, but rather from **intermittent, strategic failures to engage in advance preparation at all**.

### Paradigm & Key Manipulations
The chapter describes experiments using a classic [[Paradigm Classes/Task Switching|Task-Switching]] paradigm.

*   **Paradigm:** An implicit-cue task-switching design.
*   **Tasks:** Letter classification (Vowel/Consonant) vs. Color classification (Red/Blue).
*   **Stimuli:** Colored letters, which are inherently `Bivalent-Neutral` as the features are orthogonal.
*   **Task Cueing:** The task was cued implicitly by the stimulus's spatial location, which cycled predictably through a 2x2 grid, creating an **AABB task sequence**. This maps to `[[Dimensions/Task Cue Type|Task Cue Type]]: Implicit`.
*   **General Method:** Performance on `Switch` trials was compared to `Repeat` trials (referred to as "nonswitch" trials). The primary evidence comes from fitting mixture models to reaction time distributions (CDFs).

**Key Independent Variables:**

1.  **[[Dimensions/RSI (Response Stimulus Interval)|Response-Stimulus Interval (RSI)]]:** The main preparation interval was manipulated. Critically, in some experiments it was **unpredictable**, randomly chosen from a set of values (e.g., 150, 600, 1500 ms). This maps to `[[Dimensions/RSI Is Predictable|RSI Is Predictable]]: No`.
2.  **Block Length:** Manipulated between short (e.g., 12 trials) and long (e.g., 48 or 96 trials) blocks to investigate strategic pacing and sustained effort.

### Key Findings & Conclusions
*   **Residual Costs Replicated:** Confirmed that substantial switch costs remain even at very long RSIs.
*   **Mixture Model Evidence:** The primary finding is that the RT distribution on long-RSI switch trials is best described as a mixture of two underlying distributions: 1) the fast distribution from repeat trials (reflecting successful preparation) and 2) the slow distribution from short-RSI switch trials (reflecting no preparation).
*   **Strategic Failures are the Cause:** The model fit suggests that participants simply fail to engage in advance preparation on a significant proportion of trials (~50% in one analysis). The author concludes that residual switch costs have a **strategic origin**, stemming from an optional process, rather than a mandatory but incomplete one.
*   **Explicit Cues Prompt Preparation:** The chapter notes that the failure to prepare is more common with implicit cues than with explicit cues, suggesting explicit cues are a more powerful trigger for engaging the intention to prepare.

### Relevance to Thesis & Mapping Notes
This chapter is theoretically crucial because it introduces a major alternative explanation for a key phenomenon in task switching, and its methodology provides an excellent test case for our coding framework.

*   **A Third Major Theory:** This paper establishes the **Failure-to-Engage (FTE) hypothesis** as a distinct account of the residual switch cost. This refines the central debate in our framework, which is currently dominated by the tension between incomplete [[Theoretical Concepts/Task-Set Reconfiguration|Task-Set Reconfiguration]] ([[Rogers & Monsell (1995)]]) and persistent [[Theoretical Concepts/Task-Set Inertia|Task-Set Inertia]] ([[Allport el al. (1994)]]). Our notes on these concepts must be updated to reflect this third, strategic viewpoint.

*   **Dimensional Relevance & Validation:**
    *   `[[Dimensions/RSI Is Predictable]]`: This paper's use of an *unpredictable* RSI provides the perfect counterpoint to the predictable RSI in [[Rogers & Monsell (1995)]]. It empirically validates our decision to include `RSI Is Predictable` as a critical binary dimension, as it's central to testing theories of preparation.
    *   `[[Dimensions/RSI (Response Stimulus Interval)|RSI]]`: Serves as the primary manipulated preparation interval.
    *   `[[Dimensions/Trial Transition Type|Trial Transition Type]]`: Clearly maps `Switch`, `Repeat` ("nonswitch"), and `Pure` trials.
    *   `[[Dimensions/Task Cue Type|Task Cue Type]]`: The AABB sequence is a classic example of an `Implicit` cue.

*   **Mapping to Super Experiment & Overrides:**
    *   The paradigm is highly mappable. The random RSI manipulation is a perfect application of our JSON override system. For example, for Exp 1 in the chapter, the main `RSI` column would contain the mean (717ms), while the `Super_Experiment_Mapping_Notes` column would contain: `{"RSI_distribution": "choice", "RSI_values": [150, 600, 1500]}`.
    *   The AABB sequence is also handled by an override: `{"sequence_type": "AABB"}`. This ensures the viewer can simulate the experiment faithfully while the derived `Switch Rate` of 33% is used for PCA.

*   **Framework Limitations:**
    *   De Jong's "Block Length" manipulation probes strategic effort/pacing, a factor our current dimensional space does not explicitly capture. While we can code the short- and long-block conditions as separate rows, our framework doesn't have a parameter for "Strategic Pacing."
    *   The reliance on CDF and mixture model analysis highlights a difference in analytical approach. Our project maps the *design space*, while De Jong models the *behavioral output*. This is not a contradiction, but a complementary perspective.
