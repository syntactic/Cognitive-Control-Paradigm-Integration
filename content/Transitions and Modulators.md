---
tags:
  - thesis_concept
  - design_space
---

The power of the parametric design space is in its ability to show how canonical paradigms are not isolated islands, but are regions connected by the systematic manipulation of core parameters. The two most powerful dimensions for revealing these connections are **[[Dimensions/Task 2 Response Probability]]** and **[[Dimensions/Inter-task SOA (Stimulus Onset Asynchrony)|Stimulus Onset Asynchrony (SOA)]]**. The key transitions can be understood by how these dimensions are manipulated.

---
### Transition 1: Within Task 2 Response Probability=1.0 Space (The PRP-Task Switching Continuum)

This transition occurs entirely within the dual-task domain and is governed by the temporal separation of two **required tasks**.
- **Core Change:** Manipulating the temporal overlap between two full S-R episodes.
- **Key Parameter:** [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]].
- **The Continuum:**
    - At **short SOA**, the paradigm is quintessentially a [[Paradigm Classes/Dual-Task Performance & PRP|PRP]] task. The cognitive challenge is managing a central processing bottleneck and parallel processing capacity.
    - At **very long SOA** (e.g., > 2000ms), the first task (T1) is fully completed before the second stimulus (S2) even appears. The challenge is no longer about concurrent processing, but about disengaging from the T1 context and engaging the T2 context. It becomes functionally equivalent to a predictable [[Paradigm Classes/Task Switching]] trial with a long preparation interval. [[Allport el al. (1994)|Allport et al. 1994]]'s experiment 5 could be viewed as an experiment that lies at this boundary. It's framed as a task-switching experiment, but [[RSI (Response Stimulus Interval)|RSI]] is manipulated in a way similar to how SOA would be manipulated, except it is meant to explore the hypothesis that performance deficiencies are due to a need to do post-execution decay or cleanup and advance preparation for the next task rather than a central bottleneck inhibiting concurrent processing.
- **Literature:** The relationship between PRP and task switching is a foundational concept discussed in reviews like [[Pashler (1994)]] and [[Kiesel et al. (2010)]].

---
### Transition 2: From Task 2 Response Probability=1.0 to 0.0 (The Dual-Task to Distractor-Filtering Transition)

This transition represents a fundamental change in the participant's goal set, moving across the boundary of the Task 2 Response Probability dimension.
- **Core Change:** Changing the status of the second stimulus (S2) from requiring a response to being irrelevant.
- **Key Parameter:** This is not a simple numerical parameter like SOA, but a change in the **task rules**, often manipulated via instructions or [[Dimensions/Task Cue Type|Task Cue Type]].
- **The Continuum:**
    - In a **Dual-Task** (Task 2 Response Probability=1.0) setting, the participant must coordinate and execute two responses.
    - If we keep the stimuli the same but change the instructions to "respond to S1 and ignore S2," the paradigm becomes a **Single-Task with a Distractor** (Task 2 Response Probability=0.0). The cognitive challenge shifts from coordination to selective attention and filtering.

---
### Transition 3: Within Single-Task Space (The Interference-PRP-like Continuum)

This transition occurs entirely within the single-task domain and demonstrates how PRP-like principles apply even when only one response is required per trial.
- **Core Change:** Manipulating the temporal separation of the **target and distractor features** of a single, Bivalent stimulus.
- **Key Parameter:** [[Distractor SOA]].
- **The Continuum:**
    - At **SOA=0**, the paradigm is a standard [[Paradigm Classes/Interference Control]] task (e.g., Stroop, Flanker). The challenge is to resolve conflict between simultaneously presented competing information.
    - At **SOA ≠ 0**, the paradigm takes on a PRP-like quality. The first-arriving feature (be it target or distractor) acts as a "mini-S1," priming a response that creates interference for the processing of the second-arriving feature (the "mini-S2").
- **Literature:** [[Kopp et al. (1996)]] is a perfect example of a negative SOA (-100ms) where the distractor primes a response before the target arrives. [[Yeung & Monsell (2003)]] shows a positive SOA (+160ms) where the target arrives first, but the delayed distractor can still cause interference.

- **Effect of [[Preparation and Pre-cuing|Preparation]] (CSI):** Varying [[CSI (Cue-Stimulus Interval)]] modulates costs within paradigms (reduces [[Switch Cost]], may reduce [[PRP Effect]] at short SOA). Links proactive control to online performance limits. See [[Meiran (1996)]].

---
### A Key Modulatory Dimension: Preparation Time (CSI)

While N_Tasks and SOA define the fundamental structure of a paradigm, the **Cue-Stimulus Interval (CSI)** is a primary dimension for modulating performance within that structure. It does not typically create a transition between paradigm types, but instead probes the effectiveness of proactive cognitive control.

- **Core Function:** CSI represents the time available for **advance preparation** after a task is cued but before the stimulus appears. It directly measures the ability to engage in task-set reconfiguration.
- **Primary Effect:** Varying CSI modulates the magnitude of performance costs.
    - **In [[Paradigm Classes/Task Switching]]:** Increasing the CSI significantly reduces the [[Effects/Switch Cost]]. The amount of cost that remains even with a long CSI is known as the residual switch cost.
    - **In [[Paradigm Classes/Dual-Task Performance & PRP]]:** While less common, pre-cuing T1 or T2 with a variable CSI can be used to study preparation for one of the two tasks, potentially modulating the [[Effects/PRP Effect]].
- **Why it's a Modulator, Not a Transition:** Changing CSI makes a given task easier or harder by affording more or less time for preparation, but it does not change the fundamental nature of the task (e.g., it does not change a Task 2 Response Probability=0.0 paradigm to a Task 2 Response Probability=1.0 paradigm).
