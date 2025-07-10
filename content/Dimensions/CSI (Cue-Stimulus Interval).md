#dimension

Definition: The time interval between the onset of a cue indicating the upcoming task/stimulus and the onset of the imperative stimulus itself.

Relevance: Represents the time available for [[Preparation and Pre-cuing|advance preparation]].

- Critical manipulation in cued [[Task Switching]] paradigms. Longer CSI generally reduces [[Switch Cost]].
- Can be manipulated in [[Dual-Task Performance & PRP|PRP]] or [[Interference Control]] tasks if explicit cues are used.
- CSI = 0 implies simultaneous cue and stimulus presentation.

Super Exp. Mapping (Client-side - experiment.js): The conceptual CSI (preCueDuration parameter in generateTrialParams or dualPreCue in generateDualTaskParams) is used to calculate the low-level start_1 (cue onset for Task 1) by subtracting it from start_mov_1 (or start_or_1). Thus, the derived CSI is the difference between the effective stimulus onset (start_mov_X or start_or_X) and the cue onset (start_X).