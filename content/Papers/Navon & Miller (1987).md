---
tags:
  - paper
  - dual_task
  - crosstalk
  - outcome_conflict
  - cognitive_control
aliases:
  - Navon & Miller 1987
---

### Core Goal
To challenge the traditional explanation of dual-task interference, which posits competition for scarce processing resources, and to introduce and provide evidence for an alternative explanation: **outcome conflict**. The authors argue that interference arises when the processing required for one task produces outputs or side effects (i.e., crosstalk) that are harmful to the processing of a concurrent task.

### Paradigms & Key Manipulations
The study used two concurrent visual search experiments, where performance in dual-task conditions was compared to single-task (focused attention) baselines.

**Experiment 1: Semantic Relatedness**
*   **Tasks:** Concurrently search for a boy's name in one channel (e.g., horizontal words) and a city's name in another channel (vertical words).
*   **Key Manipulation:** The semantic nature of the *nontarget* words was varied. A nontarget in one channel could be:
    *   **Off-Channel Target:** A word that was a target for the *other* task (e.g., "Chicago" appearing in the channel being searched for boys' names).
    *   **Off-Channel Associate:** A word semantically related to the other task's category (e.g., "France" in the boys' name channel).
    *   **Neutral:** A word unrelated to either category.

**Experiment 2: Alphanumeric Category**
*   **Tasks:** Search for specific target letters in one channel and specific target digits in another.
*   **Key Manipulation:** Nontargets in a channel could be from the same alphanumeric category as that channel's targets (e.g., other letters) or from the opposite category (e.g., digits).

### Key Findings
1.  **Semantic Crosstalk (Exp 1):** Responses were significantly delayed when a nontarget in one channel belonged to, or was even just semantically related to, the target category of the other channel. These "off-channel" effects were not present when the tasks were performed in isolation, demonstrating a true dual-task interaction.
2.  **Category-Based Crosstalk (Exp 2):** In single-task conditions, it was more efficient to search for a target among distractors of a different category (e.g., find a letter among digits). However, in the dual-task condition, this advantage was eliminated or even reversed; performance was less efficient when the two tasks involved different categories, suggesting that categorical distinctiveness, which helps in single tasks, creates interference in dual tasks.
3.  **Cross-Response Conflict:** In both experiments, a strong congruency effect was found for target presence/absence. Responses were much faster when both tasks required the same decision (both targets present or both absent) compared to when the decisions were different (one present, one absent).

### Authors' Main Conclusions
*   The results provide strong evidence that a substantial portion of dual-task interference stems from **outcome conflict**, a form of content-specific crosstalk, rather than solely from competition for a general, limited pool of resources.
*   This conflict occurs at multiple levels:
    *   **Perceptual/Semantic Conflict:** When nontargets in one task activate representations relevant to the other task.
    *   **S-R Mapping Conflict:** Confusion in mapping stimuli to their correct response sets.
    *   **Cross-Response Conflict:** Interference or facilitation based on the congruence of the ultimate response decisions.
*   The authors conclude that the difficulty of individual tasks is not the only factor determining interference; the specific relationship between the content of the two tasks is critical.

### Relevance to Thesis & Mapping Notes
*   **Foundational for Crosstalk:** This paper is a cornerstone for the concept of [[Theoretical Concepts/Crosstalk|Crosstalk]] and content-dependent interference in multitasking.
*   **Challenges Simple Bottleneck/Resource Models:** It demonstrates that interference is not just about a structural bottleneck but is highly sensitive to the *content* being processed, a key idea for the [[Parametric Design Space]].
*   **Mapping to Super Experiment:**
    *   **Paradigm Type:** [[Paradigm Classes/Dual-Task Performance & PRP|Dual-Task]] (`Number of Tasks`=2), with simultaneous stimulus presentation (`Inter-task SOA`=0).
    *   **Stimulus-Stimulus Congruency:** The core manipulation can be mapped to this dimension. The "off-channel target" condition is a clear instance of a `Incongruent` trial, where a stimulus in one stream maps to the competing task's response. The "off-channel associate" and "neutral" conditions represent different levels of `Neutral` interference.
    *   **Response Set Overlap:** The tasks used different conceptual responses (boy vs. city), which would be abstracted as `Disjoint-Effector` in the SE framework.
    *   **SE Limitations:** The SE framework cannot directly model the rich semantic relationships (e.g., city vs. state) used in Experiment 1. The mapping must abstract this to the general principle of interference from a competing category, which SE can represent via its `mov` and `or` pathways. This is a good example for the [[Study Limitations]] section.
