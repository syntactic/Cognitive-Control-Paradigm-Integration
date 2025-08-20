---
tags:
  - paper
  - dual_task
  - prp
  - interference_control
  - flanker_task
  - bottleneck_theory
  - locus_of_slack
  - semantic_processing
aliases:
  - Fischer & Schubert 2008
---
### Core Goal
To test whether the semantic processing of emotional valence can occur in parallel with the central bottleneck in a dual-task paradigm. Using the locus-of-slack logic, they investigated if a valence-based Flanker effect in Task 2 would be "absorbed" into the slack period at short SOAs, which would suggest that this high-level semantic processing bypasses the bottleneck.

### Paradigm(s) & Manipulations
The study employed a [[Paradigm Classes/Dual-Task Performance & PRP|PRP paradigm]] that embedded a modified interference task as Task 2.

*   **Task 1 (T1):** Auditory tone discrimination (high/low frequency).
*   **Task 2 (T2):** A modified [[Canonical Tasks/Flanker Task|Flanker task]] requiring a valence judgment (pleasant/unpleasant) of a central target word, flanked by emotionally congruent or incongruent words.

**Key Manipulations:**
1.  **[[Dimensions/Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]]:** The primary PRP manipulation, varied between `85ms` (short) and `800ms` (long).
2.  **T2 Flanker Congruency ([[Dimensions/Stimulus-Stimulus Congruency|S-S Conflict]]):** The valence of the flanker words was either `Congruent` (e.g., target 'love', flanker 'smile') or `Incongruent` (e.g., target 'love', flanker 'war') with the target word.
3.  **T2 Internal SOA ([[Dimensions/Distractor SOA|Distractor SOA]]):** A crucial and unusual feature of the design was that the flanker words in T2 were presented `85ms` *before* the target word, creating a negative internal distractor SOA of -85ms.
4.  **Task Load:** Performance in the dual-task conditions was compared to a separate single-task group who performed only the valence-flanker task.

### Key Findings & Conclusions
1.  **Underadditive Interaction:** The study's central finding was a significant **underadditive interaction** between SOA and T2 congruency. The Flanker congruency effect on RT2 was substantially smaller at the short SOA (~29 ms) than at the long SOA (~59 ms).
2.  **Evidence for Parallel Processing:** According to the locus-of-slack logic, this underadditivity demonstrates that a significant portion of the time cost associated with resolving the flanker conflict was "absorbed" into the slack period while T2 was waiting for the T1 bottleneck to clear.
3.  **Valence Processing Bypasses Bottleneck:** The authors conclude that the semantic activation of valence categories is not subject to the central processing bottleneck. This type of high-level semantic processing can occur in parallel with the bottleneck-limited stages of T1, extending previous findings from simpler perceptual tasks to the domain of semantic and emotional processing.

### Relevance to Thesis & Mapping Notes
This paper is a key test case for the limits of [[Theoretical Concepts/Bottleneck Theories|Bottleneck Theory]] and serves as an excellent "bridge" paradigm by embedding a classic [[Paradigm Classes/Interference Control|Interference Control]] task (Flanker) within a [[Paradigm Classes/Dual-Task Performance & PRP|PRP]] structure.

*   **Validates Locus-of-Slack Logic:** It is a perfect example of applying the locus-of-slack methodology to probe the processing locus of a high-level cognitive function (semantic activation).
*   **Challenges Simple Bottleneck Models:** The findings provide strong evidence against a monolithic, content-general central bottleneck, suggesting that some forms of processing can proceed in parallel.
*   **Dimensional Mapping & A Key Abstraction:**
    *   The dual-task conditions are coded with `Number of Tasks = 2` and the appropriate `Inter-task SOA` (`85` or `800`).
    *   The single-task conditions are coded with `Number of Tasks = 1`.
    *   **A critical coding decision:** This paradigm's unique T2-internal temporal structure is captured by setting `Distractor SOA = -85ms` for **both the single-task and dual-task conditions**. While the framework formally reserves `Distractor SOA` for single-task paradigms, retaining this value for the dual-task rows is a deliberate choice to ensure this unique design occupies a distinct position in the PCA space. This abstraction is documented as a `[[Study Limitations|limitation]]`, as the framework cannot simultaneously represent an inter-task SOA and an independent T2-internal distractor SOA.
