---
tags:
  - paradigm
  - canonical_task
  - interference_control
  - selective_attention
  - automaticity
  - inhibition
aliases:
  - Stroop Effect
---
###### Core Concept: The Stroop Task & Effect

The **Stroop Task**, first described by John Ridley Stroop, is a classic paradigm demonstrating interference in reaction time when processing conflicting stimulus attributes. It highlights the difficulty of suppressing a highly learned or automatic process (e.g., word reading) when required to attend to a less automated feature (e.g., ink color).

The **Stroop Effect** is the robust finding that naming the ink color of a color word is significantly slower and more error-prone when the ink color and the word meaning are incongruent (e.g., the word "RED" printed in blue ink) compared to when they are congruent (e.g., "RED" in red ink) or when naming the color of a neutral stimulus (e.g., "XXXXX" in blue ink, or a color patch).

###### Typical Paradigm Structure

1.  **Task Goal:** Participants are most commonly instructed to **name the ink color** of a presented stimulus, while ignoring its semantic content (the word itself).
2.  **Stimuli:** Typically words, often color names, printed in various ink colors.
3.  **Irrelevant Dimension:** The semantic meaning of the word.
4.  **Relevant Dimension:** The physical ink color of the word.
5.  **Responses:** Usually vocal (naming the color), but can be manual (pressing a key corresponding to a color).

###### Key Conditions & How Congruency Arises:

*   **[[Dimensions/Stimulus-Stimulus Congruency]]:** The stimulus (e.g., "RED" in blue ink) is bivalent because it has two salient dimensions: word meaning and ink color.
    *   **Congruent Trials:** The word meaning matches the ink color.
        *   *Example:* Word "BLUE" printed in blue ink. Task: Name ink color (say "blue").
    *   **Incongruent Trials:** The word meaning conflicts with the ink color.
        *   *Example:* Word "BLUE" printed in red ink. Task: Name ink color (say "red").
    *   **Neutral Trials:** The word is irrelevant to color naming, or a non-word/symbol is used.
        *   *Example (Neutral Word):* Word "TABLE" printed in red ink. Task: Name ink color (say "red"). (CSV: `Bivalent-Neutral`)
        *   *Example (Non-Word/Symbol):* String "XXXXX" printed in red ink. Task: Name ink color (say "red"). (CSV: `Bivalent-Neutral` or `Univalent` if word dimension is considered truly absent/uninformative for that stimulus type).
        *   *Example (Color Patch):* A simple red square. Task: Name color (say "red"). (CSV: `Univalent`)
*   **[[Dimensions/Stimulus Response Mapping|Stimulus Response Mapping]]:** Typically `Arbitrary` (though highly learned for color naming, e.g., red color -> "red" vocalization). The conflict arises from the bivalent stimulus features.

###### Key Manipulations & Variations:

*   **Reverse Stroop:** Task is to read the word, ignoring the ink color. Interference is typically much smaller.
*   **Emotional Stroop:** Using emotionally charged words vs. neutral words, measuring interference on color naming.
*   **Spatial Stroop:** Words like "UP" or "DOWN" presented above or below fixation, with task to name location or word.
*   **Number Stroop:** Judging physical size vs. numerical value of digits.

###### Theoretical Interpretations:

- **Dimensional Overlap Model:** In the framework of [[Kornblum et al. (1990)]], the classic Stroop task is a **Type 4B ensemble**. This is because both the relevant dimension (ink color) and the irrelevant dimension (word meaning) have dimensional overlap with the response set (spoken color names). This contrasts with a "Neutral Stroop" (e.g., a neutral word like "TABLE" in colored ink), which would be a **Type 2 ensemble**, as the irrelevant word dimension does not have overlap with the response set.
*   **Speed of Processing Theory:** Word reading is a faster, more automatic process than color naming. The output of the reading process becomes available sooner and interferes with the slower color-naming process.
*   **Automaticity:** Word reading is a highly automatized skill that is difficult to inhibit once initiated by the presence of a word.
*   **Parallel Distributed Processing (PDP) / Connectionist Models:** Both word and color pathways are activated in parallel. Stronger connections for the reading pathway lead to its output dominating or creating conflict with the color pathway. (e.g., [[Cohen et al. (1990)]]).
*   **Selective Attention & Response Competition:** The task requires selectively attending to the ink color dimension and inhibiting the response associated with the word dimension.
*   **Conflict Monitoring:** Modern theories like [[Theoretical Concepts/Conflict Monitoring Theory]] propose that the ACC detects the high level of response conflict on incongruent trials and signals for increased top-down control.

###### Relevance to Cognitive Control:

*   A hallmark task for studying **selective attention** and the ability to filter irrelevant information.
*   Investigates the interplay between **automatic and controlled processing**.
*   Crucial for understanding **inhibitory control** mechanisms.
*   Used to study **conflict monitoring and resolution**.

###### Key Parameters for Design Space Mapping:

*   [[Number of Tasks|Number of Tasks]]: 1.
*   [[Dimensions/Stimulus-Stimulus Congruency]]: Defines congruent/incongruent/neutral conditions.
*   Response Modality (vocal, manual).
*   [[Distractor SOA]]: Typically 0 (or N/A) as word and color are simultaneous attributes of one stimulus.
*   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: Typically 0.
*   [[Dimensions/Switch Rate|Switch Rate]]: Typically 0%.
