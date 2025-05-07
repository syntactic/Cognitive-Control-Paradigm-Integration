#tool #framework

The Super Experiment library serves as the operational framework for defining and potentially simulating paradigms within the [[Parametric Design Space]].

**Key Features:**

- Allows precise parametric control over trial timing (stimulus onset/duration, cue onset/duration, go signal onset/duration).
    
- Handles definition of tasks (currently 'mov' and 'or' as placeholders for Task 1/Task 2).
    
- Logs responses (keypresses) and reaction times.
    
- Low-level parameters (start_stim1, dur_cue1, coh_mov1, etc.) are used to instantiate configurations based on higher-level [[Derived Dimensions vs. Low-Level Parameters|derived dimensions]].
    
- Requires external code (e.g., createTrialSequence in experiment.js) to manage between-trial structure like [[Switch Cost]].
    

**Current Limitations for Thesis:**

- No built-in mechanism for Cue Validity manipulation (requires sequence-level control and potentially conflicting internal logic based on overlap requirements).
    
- Cannot directly simulate tasks identical to those in some literature (e.g., [[Telford (1931)]]'s tasks, complex Stroop), requiring abstraction to 'Task 1'/'Task 2' based primarily on timing/structure.
    
- Does not inherently model cognitive processes (e.g., memory retrieval, conflict adaptation) but provides the environment to test models or observe behavior.