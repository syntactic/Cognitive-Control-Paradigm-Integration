---
tags:
  - paper
  - task_switching
  - task_set_inertia
  - interference
  - cognitive_control
aliases:
  - Allport et al. 1994
---
### Core Goal
To investigate the behavioral costs of switching tasks and to challenge the prevailing view that these costs reflect the duration of a discrete, executive "shift-of-set" operation. The authors' central argument is that **switch costs do not represent an active reconfiguration process but rather a form of proactive interference from the previously active task set**. They introduce the influential concept of **Task-Set Inertia (TSI)** to explain these findings.

### Paradigm(s) Used
The paper describes a series of experiments using variations of a [[Task Switching]] paradigm with predictable task alternation (ABAB...). This builds on the early work of [[Jersild (1927)]].

*   **Tasks:** A variety of tasks were used across experiments, including:
    *   **Number Judgments (Exp 1, 2):** Responding to the **value** vs. **group size** of numerals, and judging them as **Odd/Even** vs. **More/Less** than five.
    *   **Stroop-like Tasks (Exp 3, 5):** Switching between **word naming** (dominant) and **color naming** (non-dominant).
    *   **RSVP Semantic Monitoring (Exp 6, 7):** Monitoring a rapid stream of words for a shifting semantic category (e.g., from 'Animal' to 'Small Object').

*   **General Procedure:** Participants typically alternated between two tasks in a predictable sequence. Performance on these "alternating" lists/trials was compared to "uniform" (single-task) baseline conditions.

### Key Manipulations
1.  **Task Feature Switched (Exp 1):** Compared the cost of switching the relevant **stimulus dimension** (e.g., Value vs. Group Size) versus switching the **cognitive operation/judgment** (e.g., Odd/Even vs. More/Less).
2.  **Task Difficulty (Exp 2):** Manipulated the difficulty of the number comparison task (Near vs. Far symbolic distance) to see if switching between harder tasks incurred a greater cost.
3.  **Task Cueing (Exp 3):** Compared "uniform lists" (where stimuli were all numbers or all color-words, thus the task was implicitly maintained) with "mixed lists" (where stimulus type alternated, e.g., number -> color-word, providing an external cue for the task switch).
4.  **Task Dominance & Asymmetry (Exp 3, 5):** Used tasks of unequal strength (e.g., word reading vs. color naming) to examine if the cost of switching was symmetrical.
5.  **Response-Stimulus Interval (RSI) (Exp 5):** In a discrete RT version of the task, manipulated the time between the response to the first stimulus and the onset of the second stimulus (20ms, 550ms, 1100ms) to provide variable preparation time.

### Key Findings
1.  **Large and Robust Switch Costs:** Confirmed large performance costs (in list completion time or RT) for alternating tasks compared to repeating them.
2.  **Switch Cost Invariant to Difficulty/Complexity:** The magnitude of the switch cost was **not significantly affected** by the difficulty of the individual tasks (Exp 2) or by whether one vs. two task features were switched concurrently (Exp 1).
3.  **Asymmetrical Switch Costs:** In the Stroop tasks (Exp 5), the switch cost was **larger when switching *to* the stronger, dominant task** (word reading) than when switching to the weaker task (color naming).
4.  **Persistent Switch Costs over RSI:** The [[Effects/Switch Cost|switch cost]] was **not eliminated** by providing a long preparation interval (RSI). A large cost remained even at an RSI of 1100ms, challenging the idea that the cost is due to a preparatory process that can be completed in advance.
5.  **Task-Set Inertia (TSI):** The authors interpret these findings as evidence for TSI. The cost of switching reflects proactive interference from the lingering, "inertial" activation of the previous task set, which must be overcome when the new stimulus arrives.
6.  **Symmetrical Interference with Bivalent Stimuli:** Under alternation, the classic Stroop interference effect became symmetrical. That is, word meaning interfered with color naming, and ink color interfered with word reading to a similar degree, suggesting both task-sets were co-active.

### Authors' Main Conclusions
*   The costs associated with task switching do not reflect the duration of a preparatory, autonomous "shift-of-set" control operation.
*   Instead, switch costs are a direct consequence of **proactive interference from the persisting task-set of the preceding trial (Task-Set Inertia)**.
*   This interference must be resolved after the new stimulus appears, leading to a performance cost that is largely independent of preparation time (RSI).
*   The authors argue against a unitary, limited-capacity central executive for controlling shifts, as their data show costs are insensitive to manipulations (like task difficulty) that should load such a system.

### Notes on CSV Coding
The following experiments were excluded from the mapping to dimensional framework: 2, 4.

### Relevance to Thesis & Mapping Notes
This paper is foundational for the thesis as it establishes one of the major theoretical accounts of task switching.

*   **Theoretical Keystone:** It provides the primary formulation of the **[[Task-Set Inertia]]** hypothesis, which is a direct theoretical competitor to the **Task-Set Reconfiguration** hypothesis of [[Rogers & Monsell (1995)]]. The [[Parametric Design Space]] can be used to frame the conditions under which each account seems more or less plausible.
*   **Dimensional Relevance:**
    *   [[Number of Tasks|Number of Tasks]]: 1
    *   [[Dimensions/Switch Rate|Switch Rate]]: 100% (predictable alternation).
    *   [[Dimensions/Stimulus-Stimulus Congruency]]: The stimuli are bivalent (e.g., a numeral has both value and group size; a colored word has both word and color attributes).
    *   [[Dimensions/Task Difficulty|Task Difficulty]]: This paper provides a crucial data point where manipulating this dimension had **no effect** on the switch cost.
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: Manipulated between `Implicit` (uniform lists) and stimulus-cued (`Transparent_External` via mixed lists).
    *   [[Dimensions/RSI (Response Stimulus Interval)|RSI]]: Explicitly manipulated in Exp 5. This is a critical parameter, but note the [[Study Limitations|SE Limitation]]: RSI is mapped to `regen` in SE, which is an imperfect proxy.
*   **Asymmetrical Switch Cost:** Provides a classic example of this phenomenon and a theoretical account for it based on TSI, which contrasts with the account in [[Yeung & Monsell (2003)]] that focuses on interference levels.
*   **Mapping Challenges:**
    *   The list-completion time method used in Exps 1-4 is different from the discrete trial structure of SE. To map it, each item in the list would be considered a single "trial" with an implicit RSI.
    *   The RSVP paradigms (Exp 6-7) are outside the scope of what SE can directly model. This is a good example for the "SE Limitations" section of the thesis.

#### Mapping Experiment 5: A Parametrically Distinct Paradigm
 
 While Allport et al. frame Experiment 5 in the language of "task shifting," its parametric structure is critically different from the list-based experiments and from modern task-cuing paradigms. It should be coded as a **dual-task paradigm** (Number of Tasks: 2 or Task 2 Response Probability: 1).
 
 **Rationale:**
- Each trial pair (e.g., color naming -> word reading) constitutes two distinct, sequential S-R episodes.
- The core independent variable is the **Response-Stimulus Interval (RSI)** between R1 and S2. This makes it an **RSI-driven dual-task**, which is parametrically distinct from classic PRP (which is SOA-driven).

This paper is essential for coding because it provides clear examples of varying multiple core dimensions and offers a strong theoretical interpretation that has shaped the field for decades.
