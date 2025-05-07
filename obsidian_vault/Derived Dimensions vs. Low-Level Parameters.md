#methodology #thesis_concept

A key methodological choice in this thesis is how to represent experimental paradigms for mapping and analysis.

- **Low-Level Parameters:** These are the specific parameters required by the [[Super Experiment Framework]] (e.g., start_stim1, dur_cue1, coh_mov1, key maps).
    
    - Pros: Precise, directly implementable/simulatable, suitable for quantitative analysis like [[PCA]].
    - Cons: Too numerous, often specific to stimulus/response types making comparison across diverse literature difficult, may obscure underlying functional similarities.
- **Derived Dimensions:** These are higher-level, conceptual dimensions abstracted from the low-level parameters (e.g., [[SOA (Stimulus Onset Asynchrony)]], [[CSI (Cue-Stimulus Interval)]], [[N_Tasks]], [[Response Set Overlap]]).
    
    - Pros: Capture functional manipulations, align better with how literature describes experiments, facilitate conceptual mapping and identification of transitions/gaps across different specific tasks.
    - Cons: Require careful definition and consistent application, less direct input for simulation or PCA (translation needed).

**Approach in this Thesis:**

1. Use **Derived Dimensions** for the primary conceptual map and literature review.
2. Translate literature examples into **Low-Level Parameters** to populate a dataset.
3. Perform [[PCA]] on the Low-Level Parameter dataset.
4. Compare the structure revealed by PCA with the conceptual map based on Derived Dimensions.