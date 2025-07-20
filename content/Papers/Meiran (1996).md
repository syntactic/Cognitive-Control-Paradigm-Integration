**Core Goal:**  
To provide strong evidence for an active, time-consuming process of task-set reconfiguration that can occur prior to stimulus presentation (i.e., during preparation) in task switching, distinct from passive carry-over effects (like [[Task-Set Inertia]]). Introduces and validates the explicit task-cuing paradigm with variable [[CSI (Cue-Stimulus Interval)]] for this purpose.

**Experiment Definition:**

- **Explicit Task-Cuing Paradigm:** Participants switched between two spatial judgment tasks (Up/Down vs. Left/Right) based on an explicit cue (arrow direction) presented before the target stimulus (a dot in one of four locations).
- [[Number of Tasks|Number of Tasks=1]] per trial, [[Switch Rate]] typically 50% (random cuing).
- [[Response Set Overlap]] = Identical (Left/Right keypresses for both tasks).
- [[Dimensions/Stimulus-Stimulus Congruency]] = Bivalent-Neutral (Target location affords judgments on both dimensions).
- [[Task Cue Type]] = Arbitrary (arrow direction maps to spatial judgment axis).

**Key Manipulations:**

1. **Cue-Stimulus Interval (CSI):** Systematically varied the time between the onset of the task cue (arrow) and the onset of the target stimulus (dot). Ranges varied across experiments (e.g., 100ms to 1100ms).
2. **Response-Cue Interval (RCI):** The time between the previous response and the current cue was also implicitly varied or controlled in some analyses to disentangle preparation from decay.
3. **Task Shift vs. Task Repeat:** Compared performance on trials where the cued task differed from the previous trial versus trials where it was the same.

**Key Findings:**

- **Robust Switch Costs:** Replicated the standard [[Switch Cost]] effect – RTs were slower on task-switch trials than task-repeat trials, especially at short CSI.
- **CSI Reduces Switch Costs:** Increasing the CSI significantly reduced the magnitude of the switch cost. This reduction followed a negatively accelerating curve, with most benefit gained by ~600ms.
- **Large Residual Switch Cost:** Critically, switch costs were not eliminated even at the longest CSIs used (e.g., 1100ms). A substantial residual cost remained.
- **Preparation Affects Repeats Too:** RTs on repeat trials also decreased with increasing CSI, although typically less than switch trials, indicating general preparation effects beyond switch-specific reconfiguration.
- **RCI Effects Minimal/Dissociated:** The study argued (in later experiments and discussion, though Exp 1 confounds CSI/RCI) that the reduction in switch cost was primarily due to CSI (active preparation), not just increased RCI (passive decay), although decay might play a role.

**Author's Main Conclusions/Interpretations:**

- Task switching involves an active, time-consuming **advance reconfiguration** process that can be engaged during the CSI, reducing switch costs.
- This reconfiguration process cannot typically be fully completed before stimulus onset, resulting in a **residual switch cost**. This residual component might reflect stimulus-triggered completion of reconfiguration or potentially [[Task-Set Inertia]].
- The task-cuing paradigm successfully isolates preparatory reconfiguration effects from simple stimulus/response priming or passive decay effects (when RCI is controlled or accounted for).

### Relevance to Thesis

This is a foundational paper for the [[Paradigm Classes/Task Switching]] domain, as it introduces the explicit **task-cuing paradigm** and provides some of the cleanest evidence for an active, preparatory **[[Theoretical Concepts/Task-Set Reconfiguration|Task-Set Reconfiguration]]** process by manipulating the [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]].

**A Key Case Study for Conflict Dimensions:** This paper is a particularly valuable test case for the orthogonal conflict dimensions, as it unintentionally instantiates different types of conflict across its experiments:

- **Exp 1 & 2 (Spatial Tasks):** These experiments involve two distinct sources of conflict. The first is **[[Dimensions/Stimulus-Stimulus Congruency|S-S Congruency]]**, arising because the bivalent stimulus (a dot in a quadrant) affords two competing task rules (Up/Down vs. Left/Right) that can map to the same or different responses. The second is **[[Dimensions/Stimulus-Response Congruency|S-R Congruency]]**, arising because the irrelevant spatial location of the stimulus can correspond to the physical location of the response key. As Meiran himself notes (p. 1427), these two forms of conflict were **perfectly confounded** in his design. The coding in super_experiment_design_space.csv reflects this by assigning identical values to both S-S Congruency and S-R Congruency for these conditions.
- **Exp 5 (Object Tasks):** This experiment successfully isolates **pure [[Dimensions/Stimulus-Stimulus Congruency|S-S Congruency]]**. By switching between non-spatial color and shape tasks, the conflict is entirely about the competing semantic interpretations of the bivalent stimulus. There is no irrelevant spatial feature to prime a response, so S-R Congruency is correctly coded as N/A.
- **Dimensional Mapping Summary:**
    - [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: The primary manipulated variable.
    - [[Dimensions/Trial Transition Type|Trial Transition Type]]: Switch vs. Repeat.
    - [[Dimensions/Stimulus Response Mapping|Stimulus Response Mapping]]: Arbitrary for all tasks, as the mappings (e.g., Up -> Key 7) are learned.
**Exclusions**:
- Experiment 4 intended to see the effect of practice effects - both the experiment length was longer and the warm-up procedure was emphasized to improve accuracy. Because these are not necessarily manipulations we can make in the SE, I have excluded experiment 4.
