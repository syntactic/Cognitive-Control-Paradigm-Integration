---
tags:
  - dimension
  - cue_property
---

Definition: Describes the nature of the signal provided to the participant (if any) that specifies which task rule set should be active for an upcoming imperative stimulus.

**Possible Values (for classifying literature):**

- **None/Implicit:** The task is constant for a block, implied by the context (e.g., only one type of stimulus/response is possible), or determined solely by the arrival/nature of the imperative stimulus itself. No explicit within-trial cue is presented to select a task.
    
    - [[Super Experiment Framework|SE Mapping]]: The internal SE border cue appears simultaneously with the imperative stimulus ([[CSI (Cue-Stimulus Interval)|CSI]]=0).

- **Arbitrary Cue:** A cue whose physical form has no pre-existing semantic link to the task it signals. The association must be learned or instructed (e.g., a colored border, a symbol like "%").
    
    - [[Super Experiment Framework|SE Mapping]]: This is the default cueing mechanism in Super Experiment (e.g., orange/blue borders). The SE border cue's timing (onset and duration) is set to match the arbitrary cue's timing in the original study, defining the [[CSI (Cue-Stimulus Interval)|CSI]].

- **Transparent/Direct Cue:** A cue whose form directly and meaningfully indicates the task (e.g., the word "COLOR", "MOTION", or a highly iconic symbol directly representing the task operation).
    
    - [[Super Experiment Framework|SE Mapping]]: The literature's transparent cue presentation and duration defines the [[CSI (Cue-Stimulus Interval)|CSI]]. The internal SE border cue still appears with the imperative stimulus after this CSI, to trigger SE's internal task pathway selection. The functional preparation time is what's mapped.

- **Partial Cue:** (Likely outside SE direct mapping) A cue providing incomplete information about the upcoming task (e.g., "respond spatially" without specifying which spatial dimension, or "a switch will occur" without specifying the target task).
- **Predictive/Contextual Cue:** (Overlaps with Cue Validity and Switch Rate/Sequence Structure) A cue whose informational value is probabilistic or determined by sequence, rather than a direct instruction.

**Relevance to Design Space:**

- Determines the nature of information available for [[Preparation and Pre-cuing|task preparation]].
- Influences the speed and efficiency of [[Task Switching|task-set reconfiguration]].
- Transparent cues generally lead to faster preparation and smaller [[Switch Cost]]s than arbitrary cues.
- The transition from a cued Task 2 to an uncued distractor in dual-task settings involves changing the Task 2 cue type from (e.g.) Arbitrary to None.

**Key Literature:**

- [[Kiesel et al. (2010)]] (Discusses cue effects)
    
- [[Grange & Houghton (2010)]] (Transparent vs. arbitrary cue-switch costs)
    
- [[Dreisbach et al. (2002)]] (Probabilistic/Validity cues)
