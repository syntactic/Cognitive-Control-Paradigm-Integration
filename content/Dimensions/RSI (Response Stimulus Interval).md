---
aliases:
  - RSI
---
#dimension 

**Core Definition:** The time interval between the completion of a response in one processing episode and the onset of the critical stimulus (or task cue, if applicable) for the *next* processing episode.

**Relevance to Design Space:**
RSI is a crucial temporal parameter that primarily determines the amount of time available for:
1.  **Dissipation of processing from the previous trial/task.**
2.  **Endogenous preparation for the upcoming trial/task.**
Its manipulation and effects are central to understanding task-set inertia, task-set reconfiguration, and preparation strategies.

**Operationalization Across Paradigm Types:**

*   **In [[Task Switching]] Paradigms (e.g., [[Rogers & Monsell (1995)]], [[Meiran (1996)]] when referring to RCI):**
    *   **Definition:** Typically `RSI = Onset(Cue_Trial_N) - Offset(Response_Trial_N-1)` OR `RSI = Onset(Stimulus_Trial_N) - Offset(Response_Trial_N-1)` if tasks are implicitly cued by stimuli or sequence.
    *   **Function:** Represents the **preparation interval** available after responding to the previous task and before the cue/stimulus for the next task appears.
    *   **Effect:** Longer RSIs generally lead to reduced [[Effects/Switch Cost|Switch Costs]], attributed to more time for advance [[Task-Set Reconfiguration|reconfiguration]] or dissipation of [[Task-Set Inertia|task-set inertia]]. However, this benefit may depend on RSI predictability.
    *   **SE Mapping:** Can be approximated by SE's `regen` parameter (inter-trial interval), assuming the SE trial definition ends promptly after the response. If a task cue is presented first in SE (`start_1=0`), `regen` maps to RCI (Response-Cue Interval), and the full RSI to the imperative stimulus would be `regen (RCI) + CSI`.

*   **In [[Dual-Task Performance & PRP|PRP]] / [[Dual-Task Performance & PRP|Dual-Task]] Paradigms (e.g., [[Telford (1931)]]):**
    *   **Definition (Inter-Trial Context):** `RSI_inter_trial = Onset(S1_Trial_N) - Offset(R2_Trial_N-1)`. This is often referred to as the **Inter-Trial Interval (ITI)**.
    *   **Function:** Represents the time between the completion of one dual-task episode and the beginning of the next.
    *   **Effect:** While not always the primary manipulation in classic PRP (which focuses on intra-trial [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]]), a very short ITI/RSI could lead to carry-over effects or insufficient recovery between complex dual-task trials. Longer ITIs allow for better disengagement and preparation for the next S1.
    *   **Definition (Intra-Trial Context - Less Common as "RSI"):** Sometimes, `RSI_intra_trial = Onset(S2) - Offset(R1)` might be discussed. This is equivalent to `SOA - RT1`. It's an *outcome* measure reflecting processing overlap, not typically a manipulated "RSI" for preparation.
    *   **SE Mapping:** The `RSI_inter_trial` (ITI) maps to SE's `regen` parameter.

*   **In Single-Task Interference Paradigms (e.g., [[Stroop (1935)]] using serial presentation):**
    *   **Definition:** If items are presented serially, RSI would be the time from responding to item N-1 to the presentation of item N.
    *   **Function:** Often very short and self-paced in continuous naming/reading tasks.
    *   **Effect:** Typically not a manipulated variable but reflects the pacing of serial processing.
    *   **SE Mapping:** Less directly applicable as SE defines discrete trials. Would require modeling each item as a "trial" with a very short `regen`.

**Values for Coding:**
*   Milliseconds (ms).
*   **"Not Specified"**: If the paper does not report a controlled ITI or R-S interval between relevant episodes. This will be preprocessed to be imputed with the median before PCA sees it.
*   A derived value, usually expected value of RSI over the conditions: For conditions where RSI was explicitly varied unpredictably within a block (e.g., [[Rogers & Monsell (1995)]] Exp 2; [[Stephan & Koch (2010)]] Exp 2). This distinguishes it from fixed RSI values. The specific range of variation should be in the `Super_Experiment_Mapping_Notes`.

**Relationship to Other Dimensions:**
*   Interacts significantly with [[CSI (Cue-Stimulus Interval)|CSI]]: Total preparation time can be seen as `RSI + CSI` (though they afford different types/stages of preparation).
*   Interacts with `Switch Rate` and `Task Cue Type`: The utility of a long RSI for preparation depends on whether a switch is expected and whether the cue provides timely information.
*   **RSI Predictability (Implicit):** While not a formal dimension currently, the *predictability* of RSI (fixed vs. random) is crucial for its effect on preparation, as highlighted by Rogers & Monsell (1995). This is captured in coding via specific values for fixed RSI vs. placeholders/notes for random RSI.

**Key Literature:**
*   [[Rogers & Monsell (1995)]] (Manipulation of RSI in task switching, predictability effects)
*   [[Meiran (1996)]] (Manipulation of RCI and CSI)
*   [[Stephan & Koch (2010)]] (Manipulation of RSI in task switching with I-O compatibility)

**Note on SE Instantiation:**
When using SE's `regen` parameter as a proxy for RSI/RCI, ensure the SE trial structure accurately reflects the events of the original paradigm (e.g., cue onset being the first event if `regen` is to model RCI).