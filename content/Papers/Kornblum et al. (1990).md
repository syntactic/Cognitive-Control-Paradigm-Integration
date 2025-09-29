---
tags:
  - theory
  - foundational_paper
  - cognitive_control
  - src
aliases:
  - Kornblum et al. 1990
---
### Core Contribution to Thesis Project

This paper provides a foundational theoretical framework for stimulus-response compatibility (SRC) that serves as a direct intellectual precursor to this thesis project's goal of creating a unified design space. It argues that many disparate SRC phenomena can be explained by a single model based on the concept of "Dimensional Overlap." This paper is not coded in the CSV as its value is purely theoretical and its experimental details are superseded by more modern paradigms we have included.

The Dimensional Overlap Model suggests that SRC effects arise when stimulus and response sets share properties, which leads to the automatic activation of corresponding elements in the response set. This commonality is termed **dimensional overlap**. The model classifies S-R ensembles into different types based on whether this dimensional overlap exists for **relevant** (systematically related to the required response) or **irrelevant** (no systematic relationship to the required response) dimensions.

Here is a summary of each ensemble type:

- **Type 1 Ensembles**
    - **Definition:** These ensembles are characterized by **the absence of dimensional overlap in either the relevant or the irrelevant dimensions**.
    - **Explanation:** In Type 1 ensembles, there are no automatic response activation processes or rule-based response identification, which are the fundamental basis for SRC effects. Consequently, any stimulus-response mapping is expected to be as effective as any other.
    - **Example:** A study by Fitts and Deininger (1954) included a condition where a set of **spatially oriented movements was paired with a set of proper names as stimuli**. For this ensemble, **all S-R mappings were found to be equivalent**, demonstrating the lack of compatibility effects. These types of ensembles are useful as neutral or control conditions in experiments investigating dimensional overlap effects.
    
- **Type 2 Ensembles**
    - **Definition:** This type of ensemble is characterized by the **presence of dimensional overlap, and therefore automatic activation processes, in the relevant dimension**.
    - **Explanation:** Because the relevant stimulus dimension overlaps with the response dimension, Type 2 ensembles satisfy the requirements for obtaining **mapping effects**. This means that congruent mappings (where the automatically activated response matches the required response) will produce facilitation, while incongruent mappings will produce interference. The greater the dimensional overlap, the larger the reaction time difference between congruent and incongruent mappings.
    - **Examples:** 
        - **Spatial:** Stimulus lights aligned with response keys (Morrin & Grant, 1955); arrow direction matching button press side (Schwartz et al., 1977); monaural tone ear matching response key side (Simon, 1967, 1969)
        - **Non-spatial:** Digit naming vs. next-digit naming (Sternberg, 1969; Blackman, 1975); vowel naming vs. next-vowel naming (Sanders, 1970)
    
- **Type 3 Ensembles**
    - **Definition:** In Type 3 ensembles, the **relevant stimulus dimension has no overlap with any of the response dimensions, whereas the irrelevant stimulus dimension _does_ have dimensional overlap**.
    - **Explanation:** This type is crucial because it provides strong evidence for the **automatic and involuntary nature of the underlying activation mechanism**. Even though a stimulus dimension is irrelevant to the task (it cannot be used to identify the response better than chance), if it shares dimensional overlap with a response dimension, it can still produce mapping effects similar to those observed with relevant dimensions. This indicates that automatic response activation occurs regardless of task relevance.
    - **Examples:**
        - Wallace (1971): 50ms faster when figure side matched response key side
        - Simon & Small (1969): 65ms faster when tone ear matched response key side  
        - Simon studies: Irrelevant stimulus position affects lateralized responses
    
- **Type 4 Ensembles**
    - **Definition:** In this final type, the **stimulus and response sets overlap on both a relevant and an irrelevant dimension**.
    - **Subtypes:**
        - **Type 4A:** The relevant and irrelevant dimensions are **different**.
        - **Type 4B:** The relevant and irrelevant dimensions are the **same or very similar**.
    - **Explanation:** Type 4 ensembles can lead to complex interactions between the various factors involved, including the relative perceptual dominance and degree of overlap of the relevant and irrelevant dimensions.
    - **Examples:**
        - **Type 4A:** Hedge & Marsh (1975) - red/green lights left/right of fixation with color-position key mapping
        - **Type 4B:** Stroop tasks - ink color (relevant) vs. word meaning (irrelevant) both pertaining to color

### Key Concepts Relevant to The Framework

1.  **Dimensional Overlap as the Basis for Bivalence:** The paper's central concept is **Dimensional Overlap**, the idea that compatibility effects only arise when the stimulus and response sets share common representational dimensions (e.g., both are spatial, both are semantic). This is the direct theoretical justification for the `[[Dimensions/Stimulus-Stimulus Congruency]]` and `[[Dimensions/Stimulus-Response Congruency]]` dimensions. A stimulus becomes **bivalent** precisely when such an overlap exists, creating the potential for conflict.

2.  **A Processing Model for the Congruency Effect:** Kornblum et al. propose a two-pathway processing model for stimuli with dimensional overlap: an **automatic activation** of the corresponding response, and a controlled **response identification** based on the instructed rule. The [[Effects/Congruency Effect|congruency effect]] arises from the conflict between these pathways, where an incongruent automatic activation must be "aborted." This model is a clear forerunner to the [[Theoretical Concepts/Conflict Monitoring Theory]] and provides a mechanistic explanation for the phenomena we are mapping.

3.  **A Taxonomy as a Precursor to the Parametric Space:** The authors propose a taxonomy of task ensembles (p. 264, Table 2) based on whether dimensional overlap occurs on relevant or irrelevant dimensions. This taxonomy, which classifies paradigms like the [[Canonical Tasks/Stroop Task|Stroop Task]] (Type 4, Type 2 for Neutral) and [[Canonical Tasks/Simon Task|Simon Task]] (Type 3) into a common framework, is a powerful early validation of the thesis's core goal: to unify paradigms based on their underlying structural properties in a [[Parametric Design Space]].
