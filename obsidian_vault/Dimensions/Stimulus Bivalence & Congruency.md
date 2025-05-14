---
tags:
  - dimension
  - stimulus_property
---
Definition: Describes properties of a stimulus object, particularly its relevance to multiple potential task rules and the relationship between those interpretations.

- **Bivalence:** A stimulus is **bivalent** if it possesses features relevant to the rules of two or more tasks that could potentially be active. A stimulus is **univalent** if its features are only relevant to one task.
    
    - Example (Bivalent): In Stroop, a colored word (e.g., "RED" in blue ink) is bivalent; it has word identity (for reading task) and ink color (for color-naming task).
    - Example (Univalent): A pure color patch is univalent for color naming; a black-and-white word is univalent for reading.
- **Congruency:** Applies to **bivalent** stimuli when the response mappings of the multiple tasks it affords lead to:
    
    - **Congruent:** The same response decision or category (e.g., word "RED" in red ink).
    - **Incongruent:** Different/conflicting response decisions (e.g., word "RED" in blue ink).
    - **Neutral:** The irrelevant dimension does not map to a response in the current task's response set (e.g., word "TABLE" in blue ink, for color naming). This is "Bivalent-Neutral."

**Values:** Categorical {Univalent, Bivalent-Congruent, Bivalent-Neutral, Bivalent-Incongruent}. NA if N_Tasks=1 and no distractor.

**Relevance to Design Space:**

- Central to all [[Interference Control]] paradigms (Stroop, Flanker, Simon).
- Important for understanding [[Mixing Cost]] and some aspects of [[Switch Cost]] in [[Task Switching]] when bivalent stimuli are used.

Super Exp. Mapping: Requires configuring stimuli with multiple relevant features (e.g., a triangle that is both moving and oriented) and, for congruency, using overlapping movementKeyMap and orientationKeyMap.