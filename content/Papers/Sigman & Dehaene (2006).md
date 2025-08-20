---
tags:
  - paper
---
**Full Title:** Dynamics of the Central Bottleneck: Dual-Task and Task Uncertainty
**Authors:** Mariano Sigman, Stanislas Dehaene
**Year:** 2006
**Journal:** PLoS Biology
**DOI:** 10.1371/journal.pbio.0040220

**Core Goal:** Reconcile "passive structural bottleneck" ([[Dual-Task Performance & PRP|PRP]]) with "active executive control" ([[Task Switching]]) views by investigating task uncertainty and simultaneity interactions.

## Paradigm Used:
A [[Dual-Task Performance & PRP|dual-task]] paradigm where participants responded to two tasks:
1.  **Number Comparison Task (Visual, T_num):** Indicate if a two-digit number (Arabic or spelled-out) was larger/smaller than 45 (right-hand response).
2.  **Tone Discrimination Task (Auditory, T_tone):** Indicate if a tone was high/low frequency (left-hand response).

## Key Manipulations & Design Features:

1.  **[[Inter-task SOA (Stimulus Onset Asynchrony)|SOA:]]** Varied randomly from -1000ms (T_num first) to +1000ms (T_tone first), including SOA=0ms (simultaneous). This means S2 could precede S1.
2.  **Task Order Unpredictability:** The order of stimulus presentation was random, so participants could not prepare for a specific task to be T1.
3.  **Free Response Order:** Participants were instructed to respond to each stimulus as fast as possible and could *freely choose* which task to respond to first.
4.  **Number Task Difficulty (within T_num):**
    *   **Notation:** Arabic digits vs. spelled-out words.
    *   **Distance:** Numerical distance from 45 (close vs. far).
5.  **Single-Task Trials:** Included for baseline.

## Key Dependent Variables:
*   Choice of first response (which task was responded to first).
*   RT1 (reaction time to the first chosen response).
*   RT2 (reaction time to the second chosen response).
*   RT2-RT1 interval.

## Key Findings:

1.  **Task Selection:**
    *   The probability of responding first to a task followed a sigmoidal function of SOA (biased towards responding to the number task first).
    *   The **notation** of the number (perceptual factor) significantly shifted the SOA point of equal choice, indicating task selection is influenced by early processing.
    *   The **numerical distance** (central factor) did *not* significantly affect the choice point.
2.  **RT1 Performance:**
    *   **RT1 was significantly slowed at short SOAs** (< ~300-400ms) compared to long SOAs or single-task performance. This is a key deviation from classic PRP where RT1 is often stable.
3.  **RT2 Performance:**
    *   RT2 showed a classic [[Effects/PRP Effect|PRP effect]]: RT2 was longest at short SOAs (stimuli close in time) and decreased as the temporal separation between S1 and S2 onsets increased.
    *   Number task manipulations (notation, distance) propagated to RT2 when the number task was responded to first.
4.  **Response Inter-relations:**
    *   A strong positive correlation was found between RT1 and RT2, especially at short SOAs, which persisted even at SOAs of 1000ms.
    *   The RT2-RT1 interval was less variable than RT1 or RT2 alone.
5.  **Model Proposed:**
    *   A simple passive bottleneck model could not account for all findings (especially RT1 slowing and RT1-RT2 correlations).
    *   They proposed a hierarchical model incorporating:
        *   **Task Setting Stage:** An initial, time-consuming central decision process to select which task to perform first. Its duration is longer at short SOAs (higher conflict/uncertainty), explaining RT1 slowing.
        *   **Central Bottleneck:** For the execution of the central stages of T1 and then T2.
        *   **Task Disengagement Stage:** A process required after T1 central processing/response before T2 response can be fully executed. Explains RT1-RT2 linkage and some absorption patterns.

## Authors' Main Conclusions/Interpretations:

*   Dual-task processing under uncertainty involves active executive control processes beyond a simple passive bottleneck.
*   **Task Setting:** The planning and selection of task order is an active, time-consuming process that impacts RT1.
*   **Task Disengagement:** A distinct process is needed to switch from processing T1 to T2, linking their execution.
*   These executive components operate alongside a central processing bottleneck.
*   The study provides a synthesis by demonstrating how task uncertainty (typical of task switching) interacts with concurrent processing demands (typical of PRP).

## Relevance to Thesis:

*   **Directly Bridges Paradigms:** Explicitly designed to merge PRP and task-switching concepts ([[Transitions and Modulators]]).
*   **Highlights Task Uncertainty:** Demonstrates that task order uncertainty significantly impacts dual-task processing, introducing costs usually associated with task switching (e.g., affecting RT1).
*   **Informs SE Mapping:**
    * **Coding as a Bridge Paradigm:** This study is uniquely coded as a single experimental condition with Number of Tasks=2 and Switch_Rate=50%. This is a crucial abstraction:
	    - The 50% switch rate doesn't represent a switch between task types (which are fixed) but the **trial-to-trial uncertainty of task presentation order**.
	    - This coding creates a unique point in the design space that explicitly bridges the Dual-Task/PRP and Task Switching domains, highlighting the study's novel contribution.
    *   [[Dimensions/Task Cue Type|Task Cue Type]] = None/Implicit (stimuli are the cues).
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]] = Disjoint-Effector (left/right hands for different tasks).
    * **Handling Randomized SOA:** Since SOA was randomized trial-to-trial from -1000ms to +1000ms, the condition is coded using the mean SOA (0ms) in the main CSV column for PCA compatibility. The full distribution is documented in the Super_Experiment_Mapping_Notes JSON override.
    * **Leveraging viewer.js Logic:** The viewer.js client's generateTaskAssignmentSequence function is designed to handle this exact case. When it sees Number of Tasks=2 and Switch_Rate > 0, it correctly interprets this as randomizing the assignment of the two tasks to the two Super Experiment channels on each trial, thus simulating the task order uncertainty.
*   **Challenges Simple Bottleneck Models:** Shows that RT1 is not always immune in PRP contexts, especially with added uncertainty.
*   **Introduces Control Stages:** The concepts of "task setting" and "task disengagement" are important for understanding the executive components of multitasking.

## Open Questions / Points for Consideration:
*   How does the "free response order" map to SE, where trial parameters pre-define T1 and T2 roles (even if stimuli are simultaneous)? The critical aspect is the *uncertainty* for the participant.
*   The disengagement stage (~600ms) is a substantial component. How might this relate to RSI effects in task switching?
*   The model suggests task selection happens *after* perceptual processing but *before* central decision of the first task.