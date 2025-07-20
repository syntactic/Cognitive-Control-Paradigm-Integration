---
tags:
  - paper
---
**Full Title:** The Refractory Phase of Voluntary and Associative Responses

**Author:** C. W. Telford

**Year:** 1931

**Journal:** Journal of Experimental Psychology

**Core Goal:**
To investigate whether a "refractory phase"—a period of decreased excitability or readiness for response immediately following a voluntary action or associative process—exists in complex human behaviors, analogous to that found in simpler physiological systems (like nerve/muscle tissue or reflexes). Telford explored this by examining how the time interval between successive stimuli affects:
1.  Simple reaction time.
2.  Accuracy of judgments.
3.  Tendencies to repeat associative responses.

**Paradigm(s) Used & Key Manipulations:**
Telford conducted three main sets of experiments, all ofwhich can be conceptualized as [[Dual-Task Performance & PRP|PRP-like paradigms]] where [[Number of Tasks|Number of Tasks=2]] (two sequential S-R episodes). The primary manipulation was the [[Inter-task SOA (Stimulus Onset Asynchrony)|Stimulus Onset Asynchrony (SOA)]] between the first stimulus (S1) and the second stimulus (S2).

**Experiment I: Reaction Time to Auditory Stimuli**
*   **Task:** Simple reaction time (keypress) to an auditory click.
*   **S1-R1:** Keypress to first click.
*   **S2-R2:** Keypress to second click.
*   **Manipulation:** SOA between S1 and S2 varied (0.5s, 1s, 2s, 4s).
*   **Other Derived Dimensions:**
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0 (stimulus is the cue)
    *   [[Dimensions/Switch Rate|Switch Rate]]: 0 (same task repeated)
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]]: Identical (same keypress)
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: None/Implicit

**Experiment II: Accuracy in Judging Linear Magnitudes**
*   **Task:** Judge whether the left portion of a divided horizontal line was longer or shorter than a standard right portion (30mm). Vocal response ("long" or "short").
*   **S1-R1:** Judgment of first pair of lines.
*   **S2-R2:** Judgment of second pair of lines.
*   **Manipulation:** SOA (interval between presentation of first line pair and second line pair) varied (stimuli presented on a moving kymograph belt, creating intervals of approx. 0.5, 1, 2, 4 inches, corresponding to time intervals based on belt speed).
*   **Other Derived Dimensions:**
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0
    *   [[Dimensions/Switch Rate|Switch Rate]]: 0
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]]: Identical (same vocal judgment categories)
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: None/Implicit

**Experiment III: Repetitive Tendencies in an Associative Process**
*   **Task:** After hearing a nonsense syllable, write down an associated number (0-9 for adults, 1-10 for children).
*   **S1-R1:** Write number associated with first syllable.
*   **S2-R2:** Write number associated with second syllable.
*   **Manipulation:** SOA (interval between reading of successive syllables) varied.
    *   Adults: 1s, 2s, 4s, 8s, 16s.
    *   Children (preliminary): 1s, 1.5s, 2.5s, 5s, 7.5s, 10s.
*   **Other Derived Dimensions:**
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: 0
    *   [[Dimensions/Switch Rate|Switch Rate]]: 0
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]]: Identical (written digit)
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: None/Implicit

**Key Findings:**

1.  **Reaction Time (Exp I):**
    *   RT to S2 was longest at the shortest SOA (0.5s).
    *   RT decreased significantly from 0.5s to 1s SOA.
    *   RT was minimal and similar for 1s and 2s SOAs.
    *   RT increased again at 4s SOA.
    *   This U-shaped (or inverted-U for performance) curve suggests an optimal inter-stimulus interval for rapid successive responses.

2.  **Judgment Accuracy (Exp II):**
    *   Accuracy was poorest at the shortest interval (0.5 inch / ~0.5s).
    *   Accuracy improved significantly at the 1-inch interval.
    *   Accuracy then *decreased* again at 2-inch and 4-inch intervals.
    *   This also suggests an optimal interval for accuracy in successive judgments, similar to RT.

3.  **Associative Repetition (Exp III):**
    *   The tendency to *avoid* repeating the same number response was highest at the shortest SOAs.
    *   As SOA increased, the percentage of repeated number sequences increased (i.e., avoidance of repetition decreased). This effect was more pronounced in children.
    *   Telford interpreted this as evidence against immediate repetition, consistent with a refractory-like state.

**Authors' Main Conclusions/Interpretations:**

*   Telford concluded that voluntary responses, judgments, and simple associative processes all show evidence of a "refractory phase" immediately after a response, where the system is less ready or less accurate for a subsequent, similar response.
*   This refractory period is followed by a recovery, and for RT and accuracy, potentially a "supernormal phase" (increased readiness/accuracy) around a 1-2 second inter-stimulus interval, before performance may decline again at longer, less "alert" intervals.
*   The findings suggest that these effects in complex human behavior are comparable to refractory phenomena in more elementary physiological systems.
*   He argued against simple "attention" explanations, suggesting these attentional fluctuations themselves might be rooted in such refractory and recovery cycles.
*   The decreased tendency to repeat associations at short intervals was seen as a manifestation of this refractory state.

**Relevance to Thesis:**

*   **Historical Foundation:** One of the earliest systematic investigations into what we now call the [[Effects/PRP Effect|Psychological Refractory Period (PRP)]] across different types of tasks (motor, perceptual judgment, association).
*   **SOA Manipulation:** Provides clear examples of manipulating SOA (the core dimension of PRP studies) and its impact on performance (RT, accuracy, response tendencies).
*   **Task Definition:** Useful for thinking about how to define an "S-R episode" or "task instance" in sequential performance. Each judgment or association here is treated as such.
*   **Mapping to Super Experiment:** All three experimental types are fundamentally mappable to SE by using its two task channels to represent S1-R1 and S2-R2, with SOA being the delay between `start_stim1` and `start_stim2` (and their respective cues/go signals). The tasks themselves (auditory RT, line judgment, number association) would be abstractly represented by SE's 'mov'/'or' placeholders, with the *timing* being the crucial aspect mapped.
*   **Phenomena:** Demonstrates the basic PRP effect on RT, and extends the idea of a "refractory period" to accuracy and response choice, which is conceptually broader than just RT-based bottlenecks.
*   **Dimensions:** Clearly fits [[Number of Tasks]]=2, variable [[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]], [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]=0, [[Dimensions/Switch Rate|Switch Rate]]=0, [[Dimensions/Response Set Overlap|Response Set Overlap]]=Identical, and [[Dimensions/Task Cue Type|Task Cue Type]]=None/Implicit.