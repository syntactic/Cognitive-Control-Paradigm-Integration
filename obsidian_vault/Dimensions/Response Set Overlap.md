#dimension #response_property

Definition: Describes the relationship between the sets of possible motor responses required by the two (or more) active tasks in a multi-task context ([[Number of Tasks]] >= 2).

**Values:**

- **Identical:** Both (or all) tasks use precisely the same set of physical responses and abstract response categories (e.g., Task 1 and Task 2 both use Left/Right keypresses, mapped to represent the same underlying decisions like "Yes/No" or "Category A/B").
- **Partially Overlapping:** Tasks share some, but not all, responses or response dimensions. (e.g., T1 uses Left/Middle/Right keys, T2 uses Left/Right keys).
- **Disjoint-Effector (Same Modality):** Tasks use different effectors within the same modality (e.g., T1 = Left Hand keypress, T2 = Right Hand keypress; or T1 = Index Finger, T2 = Middle Finger of same hand).
- **Disjoint-Modality:** Tasks use entirely different response modalities (e.g., T1 = Manual Keypress, T2 = Vocal Response).
- **NA:** Not applicable if [[Number of Tasks]]=1 (no second task for the response set to overlap with).

**Relevance to Design Space:**

- Crucial for determining the potential for **response-level conflict or facilitation** when [[Stimulus Bivalence & Congruency|bivalent stimuli]] are processed. Congruency effects are typically strongest with Identical or Overlapping response sets.
- Can modulate the magnitude of [[PRP Effect]] and [[Switch Cost]].
- [[Yeung & Monsell (2003)]] showed that manipulating response set overlap (making them disjoint) reversed the asymmetry of switch costs.
- Studies on ideomotor compatibility in [[Dual-Task Performance & PRP|PRP]] often rely on disjoint modalities (e.g., manual vs. vocal).

Super Exp. Mapping:
- The `experiment.js` UI provides explicit control via the "Response Set Relationship" setting, which then configures the `movementKeyMap` and `orientationKeyMap` for `superExperiment.block()`:
    - **"Identical":** This selection maps to **Identical** conceptual response sets. Both motion and orientation tasks will use the same keys for the same conceptual responses (e.g., 'a' for left, 'd' for right for both tasks). This allows for meaningful manipulation of stimulus congruency.
    - **"Disjoint":** This selection maps to **Disjoint-Effector (Same Modality - Manual)**. The motion task typically uses 'a'/'d' for left/right responses, while the orientation task uses 'w'/'s' for up/down responses. This makes the response sets distinct.
- The UI in `index.html` enforces an "Disjoint" response set relationship for Dual-Task/PRP paradigms to ensure response ambiguity is avoided.
- The `getKeyMappingsFromConfig()` and `runExperiment()` functions in `experiment.js` implement the logic to pass the appropriate `movementKeyMap` and `orientationKeyMap` to the Super Experiment package.

**Key Literature:**

- [[Yeung & Monsell (2003)]]
- [[Kiesel et al. (2010)]] (Discusses response-based interference)
- [[Koch et al. (2018)]] (Section on modality-specific effects)
