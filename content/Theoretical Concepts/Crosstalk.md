---
tags:
  - concept
  - mechanism
  - interference
---

Definition: Crosstalk refers to the unwanted transmission of information or processing influence between concurrently active or closely sequential cognitive tasks or processing streams. It occurs when processing intended for one task affects the processing of another task, typically leading to interference but sometimes facilitation.

**Manifestations:**

- In [[Dual-Task Performance & PRP]]: Can contribute to the [[PRP Effect]] and [[Dual-Task Cost]]. [[Backward Crosstalk Effect (BCE)]] specifically refers to Task 2 processing influencing Task 1 performance. Modality effects (less interference between different modalities) are often explained by reduced crosstalk potential (e.g., [[Koch et al. (2018)]]).
- In [[Task Switching]]: Manifests as [[Congruency Effect (CSE)|congruency effects]] when [[Stimulus Bivalence & Congruency|bivalent stimuli]] activate representations relevant to the currently irrelevant task.
- In [[Interference Control]] tasks (Stroop, Flanker, Simon): It is the core phenomenon – processing of the irrelevant dimension interferes with processing of the relevant dimension.

**Levels of Occurrence:** Crosstalk can potentially occur at various processing stages:

- Stimulus Level: Overlapping perceptual features.
- Response Selection Level: Conflict or facilitation between selected response codes (depends on [[Response Set Overlap]]).
- Task-Set Level: Interference from activation of competing task rules.

**Super Experiment Relevance:**
- The `experiment.js` UI, by allowing explicit control over [[Dimensions/Response Set Overlap|Response Set Overlap]] ("Identical" vs. "Disjoint") and [[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]] ("Congruent", "Incongruent", "Neutral"), enables more direct and systematic setup of experimental conditions hypothesized to modulate crosstalk.
- For instance, selecting "Identical" response sets with "Incongruent" stimuli is designed to maximize response-level crosstalk. Selecting "Disjoint" response sets aims to minimize such crosstalk, potentially shifting any observed interference to earlier processing stages.

**Theoretical Relevance:**

- Challenges theories assuming strict modularity or complete encapsulation of processing streams.
- Provides evidence for parallel processing and shared representations.
- Highlights the need for [[Cognitive Control]] mechanisms, such as those proposed by [[Theoretical Concepts/Conflict Monitoring Theory]], to manage and minimize detrimental crosstalk.
- Often modeled via shared connections or spreading activation in computational models.

**Key Literature:**

- [[Hommel (1998)]] (Introduced BCE concept)
- [[Navon & Miller (1987)]] (Outcome conflict)
- [[Logan & Gordon (2001)]] (TVA model incorporates crosstalk)
- [[Koch et al. (2018)]] (Review discussing modality effects/crosstalk)
