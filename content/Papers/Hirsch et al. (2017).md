---
tags:
  - paper
  - dual_task
  - prp
  - task_switching
  - cognitive_control
  - structure
  - bridge_paradigm
aliases:
  - Hirsch et al. 2017
---
###### Core Goal
To investigate whether two tasks performed in rapid succession in a [[Dual-Task Performance & PRP|PRP paradigm]] are represented as a single, higher-order "task-pair" at a global level of control. The study also aimed to determine the cognitive control mechanism (persisting activation vs. inhibition) used to select these global task-pair representations.

###### Paradigm & Key Manipulations
The study combined a standard [[Dual-Task Performance & PRP|PRP paradigm]] with a novel **task-pair switching logic**.
- **Tasks:** Three distinct visual tasks were available for Task 1 (T1), and one auditory task was used for Task 2 (T2). This created three unique task-pairs (e.g., Task-Pair 1 = Visual Task A + Auditory Task C; Task-Pair 2 = Visual Task B + Auditory Task C).
- **Core Innovation:** The "task-pair switching" logic was designed to isolate global effects from local sub-task effects. Because T2 was the same across all pairs, the sub-task transition from the end of trial N-1 (T2) to the beginning of trial N (T1) was *always a task switch*, regardless of whether the task-pair repeated or switched. This method controls for local switch costs, allowing for a pure measurement of the global task-pair switching cost.
- **Key Comparisons:**
    1.  **N-1 Transition:** Compared performance on `n-1` task-pair repetition trials (e.g., Pair 2 -> Pair 2) with `n-1` task-pair switch trials (e.g., Pair 1 -> Pair 2).
    2.  **N-2 Transition:** Compared performance in `n-2` task-pair repetition sequences (e.g., Pair 3 -> Pair 2 -> Pair 3) with `n-2` task-pair switch sequences (e.g., Pair 1 -> Pair 2 -> Pair 3) to test for backward inhibition.
- **Other Manipulations:**
    - Experiment 1 used conceptually overlapping responses.
    - Experiment 2 used physically overlapping responses to increase between-task [[Crosstalk|crosstalk]].
    - Experiment 3 removed immediate repetitions to test the robustness of the n-2 effect.

###### Key Findings
1.  **Evidence for Global Task-Pairs (Task-Pair Switch Costs):** The study found significant `n-1` task-pair switch costs. Performance was reliably worse on trials where the task-pair switched compared to when it repeated. This demonstrates that switching the global task-pair entity incurs a performance cost, providing strong evidence that T1 and T2 are cognitively grouped into a single, hierarchical representation.
2.  **Evidence for Activation over Inhibition (N-2 Repetition *Benefit*):** In contrast to the prediction of an inhibitory account (which would predict `n-2` repetition *costs*), the study found a consistent `n-2` repetition *benefit*. Performance was better when returning to the task-pair from two trials back (an A-B-A sequence) compared to switching to a novel third pair (a C-B-A sequence). This suggests that activation of the task-pair from trial `n-2` persists, providing a positive priming effect on trial `n`.

###### Authors' Main Conclusions
The findings provide strong evidence for a hierarchical organization of cognitive control in dual tasks.
1.  Simultaneously performed sub-tasks are grouped into a single, higher-level mental representation (a "task-pair").
2.  The crucial selection mechanism at this global level appears to be **persisting activation** (positive priming) of the relevant higher-order task, rather than inhibition of irrelevant ones.

###### Relevance to Thesis & Mapping Notes
This paper is a quintessential **"bridge" study** that provides a crucial link between [[Paradigm Classes/Dual-Task Performance & PRP|dual-tasking]] and [[Paradigm Classes/Task Switching|task-switching]].
- **Hierarchical Control:** It offers direct empirical evidence for hierarchical task representations, a core concept in advanced models of [[Cognitive Control]].
- **Methodological Innovation:** Its task-pair switching logic is a significant methodological advance for disentangling levels of control, resolving confounds present in earlier work (e.g., Luria & Meiran, 2003).
- **Theoretical Implications:** The finding of an `n-2` repetition *benefit* challenges theories that posit inhibition as a primary mechanism for resolving between-task conflict at a global level, instead favoring accounts based on [[Task-Set Inertia|task-set inertia]] or activation.
- **Mapping to Design Space:** This paradigm is a unique hybrid and a valuable test case for the coding framework.
    - It is a dual-task paradigm (`[[Dimensions/Task 2 Response Probability]]`=1.0) with a manipulated `[[Dimensions/Inter-task SOA (Stimulus Onson Asynchrony)|SOA]]`.
    - However, because the trial *procedure* (the identity of the task-pair) changes unpredictably from trial to trial, it has a `[[Dimensions/Switch Rate]]` > 0%. This places it in a unique region of the design space between classic, stable PRP (`Switch Rate`=0%) and classic task-switching.
    - The `[[Dimensions/Trial Transition Type]]` dimension would be applied to the sequence of *task-pairs* to distinguish the switch vs. repeat conditions at the `n-1` and `n-2` levels.
