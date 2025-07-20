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
    - **Examples:** Most studies investigating mapping effects fall into this category.
        - **Spatial S-R dimensions:** Morrin and Grant (1955) found that **horizontally aligned stimulus lights mapped directly onto response keys immediately below them** (congruent mapping) yielded the best performance. Schwartz, Pomerantz, and Egeth (1977) observed that subjects were faster when the **side of a button press corresponded to the direction indicated by a left- or right-pointing arrow**. Simon (1967, 1969) showed that when subjects responded to a **monaural tone presented to the left or right ear by pressing a left or right key (or moving a lever)**, performance was faster when the tone's ear of presentation matched the response side.
        - **Nonspatial dimensions:** Sternberg (1969) and Blackman (1975) found an advantage for congruent mapping when subjects were **visually presented with digits and responded with the digit's own name** compared to the name of the next digit. Similarly, Sanders (1970) observed faster reaction times when subjects **named a visually presented vowel** compared to naming the next vowel in the alphabet. These examples illustrate that such effects are not limited to spatial dimensions.
    
- **Type 3 Ensembles**
    - **Definition:** In Type 3 ensembles, the **relevant stimulus dimension has no overlap with any of the response dimensions, whereas the irrelevant stimulus dimension _does_ have dimensional overlap**.
    - **Explanation:** This type is crucial because it provides strong evidence for the **automatic and involuntary nature of the underlying activation mechanism**. Even though a stimulus dimension is irrelevant to the task (it cannot be used to identify the response better than chance), if it shares dimensional overlap with a response dimension, it can still produce mapping effects similar to those observed with relevant dimensions. This indicates that automatic response activation occurs regardless of task relevance.
    - **Examples:**
        - Wallace (1971) instructed subjects to press a left key for a square and a right key for a circle. The figures were presented randomly on the left or right side of a display (making "side" irrelevant). Nevertheless, reaction time was approximately **50 ms faster when the side on which the figure appeared corresponded to the side of the response key**.
        - Simon and Small (1969) had subjects respond to high- or low-pitched monaural tones by pressing left or right keys. The tones were randomly presented to the left or right ear (making "ear identity" irrelevant). Still, reaction time was **65 ms faster when the side of the response key corresponded to the side of the stimulated ear**.
        - Further studies by Simon and colleagues showed that an **irrelevant positional aspect of visual or auditory stimuli** (e.g., presented to the left or right of the body midline) strongly affected lateralized responses.
    
- **Type 4 Ensembles**
    - **Definition:** In this final type, the **stimulus and response sets overlap on both a relevant and an irrelevant dimension**.
    - **Subtypes:**
        - **Type 4A:** The relevant and irrelevant dimensions are **different**.
        - **Type 4B:** The relevant and irrelevant dimensions are the **same or very similar**.
    - **Explanation:** Type 4 ensembles can lead to complex interactions between the various factors involved, including the relative perceptual dominance and degree of overlap of the relevant and irrelevant dimensions.
    - **Examples:**
        - **Type 4A:** Hedge and Marsh (1975) conducted a task where stimuli were **red or green lights presented to the left or right of fixation**, and responses involved pressing a green key on the right or a red key on the left. In this setup, **color was the relevant dimension, and side was the irrelevant dimension**. They reported strong interactions between the mapping conditions for these relevant and irrelevant dimensions.
        - **Type 4B:** This subtype primarily characterizes **Stroop-type tasks**. As discussed previously, in a Stroop task, the task-relevant ink color conflicts with the task-irrelevant word meaning [Egner et al. (2007) summarized in prior conversation]. Both dimensions (ink color and word meaning) pertain to color, making them the same or very similar. Studies on the Stroop effect investigate issues such as the similarity between these relevant and irrelevant dimensions, and the degree of automaticity (or dimensional overlap) associated with them.

### Key Concepts Relevant to The Framework

1.  **Dimensional Overlap as the Basis for Bivalence:** The paper's central concept is **Dimensional Overlap**, the idea that compatibility effects only arise when the stimulus and response sets share common representational dimensions (e.g., both are spatial, both are semantic). This is the direct theoretical justification for the `[[Dimensions/Stimulus-Stimulus Congruency]]` and `[[Dimensions/Stimulus-Response Congruency]]` dimensions. In our terms, a stimulus becomes **bivalent** precisely when such an overlap exists, creating the potential for conflict.

2.  **A Processing Model for the Congruency Effect:** Kornblum et al. propose a two-pathway processing model for stimuli with dimensional overlap: an **automatic activation** of the corresponding response, and a controlled **response identification** based on the instructed rule. The [[Effects/Congruency Effect|congruency effect]] arises from the conflict between these pathways, where an incongruent automatic activation must be "aborted." This model is a clear forerunner to the [[Theoretical Concepts/Conflict Monitoring Theory]] and provides a mechanistic explanation for the phenomena we are mapping.

3.  **A Taxonomy as a Precursor to the Parametric Space:** The authors propose a taxonomy of task ensembles (p. 264, Table 2) based on whether dimensional overlap occurs on relevant or irrelevant dimensions. This taxonomy, which classifies paradigms like the [[Canonical Tasks/Stroop Task|Stroop Task]] (Type 2) and [[Canonical Tasks/Simon Task|Simon Task]] (Type 3) into a common framework, is a powerful early validation of the thesis's core goal: to unify paradigms based on their underlying structural properties in a [[Parametric Design Space]].
