---
tags:
  - methodology
  - thesis_concept
---
The process of mapping the existing literature onto the [[Parametric Design Space]] is a core methodological component of this thesis. It involves a systematic procedure for translating published experimental designs into a consistent, analyzable format. This structured approach is similar to the strategy to overcome the "task impurity problem," a challenge identified and tackled with a statistical methodology by [[Miyake et al. (2000)]].

## 1. High-Level Process

1. **Identify Key Studies:** Select foundational and representative studies from the literature using database searches, seminal reviews (e.g., [[Kiesel et al., 2010]], [[Koch et al., 2018]], [[Pashler, 1994]]), and citation tracking.
2. **Define Derived Dimensions:** Establish a set of core conceptual dimensions that capture the primary functional manipulations in cognitive control research (e.g., [[Inter-task SOA (Stimulus Onset Asynchrony)]], [[CSI (Cue-Stimulus Interval)]], [[Task 2 Response Probability]]).
3. **Code Studies at the Condition Level:** For each study, identify its distinct experimental conditions and code each one as a separate entry (a row) in a structured CSV dataset. This involves assigning a value for each derived dimension.
4. **Translate to SE Parameters:** For each coded condition, translate its high-level dimensional representation into the concrete, low-level parameters required by the [[Super Experiment Framework]]. This translation is automated via a script (convert.py) and creates the final dataset (resolved_design_space.csv) for quantitative analysis.
5. **Analyze and Visualize:** Use the resulting dataset to perform a Principal Component Analysis ([[PCA]]) and visualize the structure of the experimental design space.
6. **Identify Gaps and Limitations:** Use the conceptual map and the PCA results to locate under-explored regions in the design space and to identify experimental manipulations from the literature that the SE framework cannot fully capture (see [[Study Limitations]]).

## 2. The Unit of Analysis: Granularity in Coding

A critical methodological decision is the "grain" or "unit of analysis" for coding. The principle guiding this thesis is to **code at the level of the finest experimental condition for which a distinct behavioral effect is reported or intended.**

This means that if a study manipulates a key variable within a block of trials (e.g., congruent vs. incongruent trials), each level of that variable is coded as a separate row in the dataset. This "condition-level" granularity is essential for two reasons:

- **Analytical Fidelity for PCA:** The primary goal of the PCA is to discover the structure of variance in the design space. By coding individual conditions, we expose the variance introduced by key experimental manipulations (like congruency or predictability) to the analysis. Collapsing a mixed block into a single entry would erase this crucial variance, blinding the PCA to the study's core logic.
- **Representing Experimental Comparisons:** Cognitive science advances by comparing performance across closely matched conditions. This coding scheme honors that logic, representing each distinct point of comparison that researchers have explored. A study that systematically explores 10 conditions rightfully occupies more volume in the conceptual space than a study with only two, and the PCA should reflect this.

To manage the reconstruction of mixed-blocks in the viewer.js client, each condition is assigned a unique Condition_ID, and a block_composition_ids key in the Super_Experiment_Mapping_Notes JSON object lists all IDs belonging to a single experimental block.

## 3. Principles for Simplification and Granularity

A central challenge in creating a unified space is deciding the appropriate level of granularity for each dimension. The goal is to maximize fidelity to the source literature while creating a feature set that is meaningful, analyzable, and operationally relevant to the [[Super Experiment Framework]]. This is achieved through a **two-level simplification process**:

1. **Level 1 (Conceptual Coding):** Capture high-fidelity details from the paper into the super_experiment_design_space.csv.
2. **Level 2 (Analytical Processing):** Programmatically apply principled simplifications to create the final feature set for the PCA.

The decision to simplify a dimension at Level 2, or to add a new granular dimension at Level 1, is guided by three principles applied in order:

---
### Principle 1: Theoretical Centrality

- **Question:** Does this distinction represent a fundamental theoretical question or a core manipulation that differentiates major hypotheses in the cognitive control literature?
- **Action:**
    - **If YES (Preserve Granularity):** The distinction must be explicitly represented in the PCA feature set. If it is not already captured by existing dimensions, a new one must be added.
        - **Example:** The distinction between a fixed/predictable [[RSI (Response Stimulus Interval)|RSI]] and a variable/unpredictable RSI is central to the [[Task-Set Reconfiguration]] vs. [[Task-Set Inertia]] debate ([[Rogers & Monsell, 1995]]). It is not captured by any other dimension. **Therefore, a new binary feature, RSI_Predictability, is added to the PCA input.**
    - **If NO (Candidate for Simplification):** The distinction, while potentially interesting, may not be foundational to the broad structure of the design space. It can be considered for simplification if it fails the subsequent principles.

---
### Principle 2: Framework Redundancy

- **Question:** Can this distinction be robustly captured by a unique interaction of existing dimensions, rather than requiring a new, dedicated dimension?
- **Action:**
    - **If YES (Avoid Adding Feature):** Leverage the interaction to represent the concept. This maintains parsimony in the feature set.
        - **Example:** The task-order uncertainty in [[Sigman & Dehaene (2006)]], where SOA is randomized, could have warranted an SOA_Predictability feature. However, this unique paradigm is already perfectly described by the interaction of Number of Tasks = 2 and Switch Rate = 50%. **Therefore, no new feature is needed.**
    - **If NO (Proceed to Next Principle):** If the concept is both theoretically central (Principle 1) and not redundant (Principle 2), we must evaluate if it can be implemented.

---
### Principle 3: Operational Mappability

- **Question:** Can the different conceptual categories from the literature be mapped to functionally distinct implementations within the [[Super Experiment Framework]]? This is the final and most practical filter.
- **Action:**
    - **If YES (Preserve Granularity):** The distinction must be preserved in the PCA feature set to reflect a dimension that can actually be explored parametrically.
        - **Example:** The SRM of Task 1 can be different from Task 2 (e.g., [[McCann & Johnston (1992)]]). SE can implement this with independent keyMap configurations. **Therefore, separate SRM_Task1 and SRM_Task2 features are maintained for the PCA.**
    - **If NO (Simplify/Collapse Categories):** If multiple conceptual categories all map to the same SE implementation, they must be collapsed into a single category for the PCA. To do otherwise would create illusory dimensions of variance that are not operationally real within this project's framework.
        - **Example 1:** The distinction between Disjoint - Modality (Vocal vs. Manual) and Disjoint - Effector (Left vs. Right Hand) cannot be implemented in the keypress-only SE framework. Both map to "different sets of keys." **Therefore, they are collapsed into a single RSO_Disjoint category during analytical processing (analysis_utils.py).**
        - **Example 2:** The fine-grained neutral flanker conditions of [[Eriksen & Eriksen (1974)]] (Feature Similar vs. Feature Dissimilar) are recorded faithfully in the source CSV (Level 1). However, because SE does not model abstract feature similarity, these are **collapsed into a single SBC_Bivalent_Neutral category for the PCA (Level 2).**

By rigorously applying this three-step rubric, we ensure that the final feature set for the PCA is maximally informative, non-redundant, and operationally sound, providing a solid foundation for analyzing the parametric design space.

## Bottom-Up Coding and Consistency Checking

To maintain the integrity and logical coherence of the parametric design space, all experimental conditions must be coded from the "bottom-up." This means the assignment of dimensional values is determined by the fundamental features of a single trial, independent of any high-level, pre-conceived paradigm label. This principle is enforced through the following workflow:

**Step A: Code Trial Features First**
For any given experimental condition, begin by analyzing the properties of a single trial instance. Answer these questions first:
*   How many S-R episodes are required? (Determines `Task 2 Response Probability`).
*   Is the stimulus `Univalent` or `Bivalent`?
*   If `Bivalent`, are the target and distractor features presented simultaneously or asynchronously?
*   Is there a cue? Is it presented before the stimulus?
*   Is the RSI fixed or variable?

**Step B: Assign Dimensional Values Based on Features**
The answers from Step A directly determine the values in the CSV.
*   If a stimulus is `Bivalent` and its features are simultaneous, `Stimulus Valency` must be coded as `Bivalent-*` and `Distractor SOA` **must** be coded as `0`. It cannot be `N/A`.
*   If `Task 2 Response Probability` is `1` and there is a delay between S1 and S2, `Inter-task SOA` **must** have a numerical value.
*   The high-level "Paradigm" label (e.g., Task Switching, Interference) is a descriptive *output* of this coding process, not an input that constrains it.

**Step C: Perform a Consistency Check**
Before finalizing the coding for a new, complex paper, it is mandatory to perform a consistency check.
1.  Identify 2-3 already-coded studies in the vault that are structurally similar (e.g., other task-switching studies with bivalent stimuli, other PRP studies with unusual mappings).
2.  Create a small comparison table, like the one used for the De Jong (2000) analysis, comparing the proposed coding of the new paper against the established coding of the old ones across key, shared dimensions.

**Step D: Resolve Discrepancies**
If the consistency check reveals a discrepancy, it must be resolved before proceeding. The discrepancy signals one of three possibilities:
1.  The proposed coding for the new paper is incorrect and must be revised to align with precedent.
2.  The coding for the older, precedent-setting papers was incorrect and must be revised.
3.  The new paper introduces a genuinely novel manipulation that our current dimensional framework cannot account for, which may require adding a new dimension or making a note in `[[Study Limitations]]`.

By adhering to this bottom-up workflow, we ensure that the design space is built on a foundation of logically consistent, trial-level features, which is essential for the validity of any subsequent analysis.
