---
tags:
  - dimension
  - conflict
  - interference
  - spatial_compatibility
aliases:
  - S-R Congruency
  - S-R Conflict
  - Simon-like Conflict
---
### Core Definition
**Stimulus-Response (S-R) Congruency** captures conflict arising from a direct, automatic mapping between an **irrelevant stimulus attribute** (often, but not exclusively, spatial) and a **physical feature of the required motor response** (e.g., its location, direction, or valence). The key feature of S-R conflict is that the irrelevant attribute is from a **conceptually orthogonal domain** to the relevant task, and its link to the motor system bypasses semantic interpretation of the response set. This is the quintessential **[[Canonical Tasks/Simon Task|Simon-like]]** conflict.

It addresses the question: "Does an irrelevant, non-semantic feature of the stimulus automatically prime a physical motor action that is the same as, or different from, the one required by the task rule?"

### Theoretical Basis
This dimension is a direct operationalization of the conflict described in "Type 3" ensembles of the Dimensional Overlap Model ([[Kornblum et al. (1990)]]), where an irrelevant stimulus dimension (e.g., location) overlaps with the response dimension, causing automatic response activation. My definition generalizes this to include non-spatial structural correspondences.

### Operationalization in Paradigms
*   **[[Canonical Tasks/Simon Task|Simon Task]]:** The canonical example. The conflict is between the irrelevant **stimulus location** (e.g., left side of screen) and the relevant **response location** (e.g., right keypress).
*   **[[Canonical Tasks/Stroop Task|Stroop]] / [[Canonical Tasks/Flanker Task|Flanker]]:** In their classic forms with centered stimuli, S-R Congruency is **not present**. However, it can be added by presenting the Stroop word or Flanker array to the left or right of fixation, as in [[Egner et al. (2007)]].

### Non-Spatial Examples of S-R Congruency

While spatial location is the canonical example, the principle of a direct, structural correspondence can apply in other domains:

*   **Pitch-Height Effect:** An irrelevant high/low *pitch* of a tone can automatically prime an upward/downward motor response, creating conflict if the response keys are arranged vertically.
*   **Affective Congruency:** An irrelevant positive/negative emotional *valence* of a word (e.g., "PUPPY" vs. "SPIDER") can prime approach/avoidance motor actions (e.g., pulling/pushing a joystick).
*   **Magnitude-Force Effect:** An irrelevant numerical *magnitude* of a digit (e.g., '9') can prime a more forceful keypress, creating conflict if the task requires a soft press.

### Possible Values & Coding Rules
*   **`Congruent`**: The irrelevant stimulus location corresponds to the location of the required response (e.g., a stimulus on the left requires a left-hand response).
*   **`Incongruent`**: The irrelevant stimulus location conflicts with the location of the required response (e.g., a stimulus on the left requires a right-hand response).
*   **`Neutral`**: The stimulus location is non-lateralized or provides no spatial bias (e.g., stimulus is presented at the center of fixation).
*   **`N/A`**: **Used when there is no irrelevant spatial dimension to the stimulus** or when the response is not spatially coded. This applies to all classic, centrally-presented Stroop and Flanker tasks.

### Distinction from Other Dimensions
*   **Orthogonal to S-S Congruency:** `S-R Congruency` is about stimulus location vs. response location. `[[Dimensions/Stimulus-Stimulus Congruency|S-S Congruency]]` is about two semantic features of a stimulus.
*   **CRITICAL: Distinct from SRM:** These two dimensions are orthogonal and must not be confused.
    *   `[[Dimensions/Stimulus Response Mapping|Stimulus Response Mapping (SRM)]]` refers to the **instructed, intentional rule** for the **relevant** stimulus feature (e.g., the rule "respond *away from* the tone").
    *   `S-R Congruency` refers to the **automatic, incidental priming** from an **irrelevant** stimulus feature (e.g., an irrelevant light flashes on the same side as the required response key).
    *   You can have a `Compatible` SRM with an `Incongruent` S-R trial, and vice versa.

### Super Experiment Mapping
This is modeled by having one stimulus pathway (e.g., `mov`) represent the relevant task feature, while another pathway (e.g., `or`) represents the irrelevant spatial location.
*   The S-R mapping for the `mov` pathway is determined by the `[[Dimensions/Stimulus Response Mapping]]` dimension.
*   The `stim_or_1` stimulus (e.g., 'left_location') is then mapped to a response. `S-R Congruency` is defined by whether this automatically primed response is the same as (`Congruent`) or different from (`Incongruent`) the correct response determined by the `mov` pathway and its SRM rule.

### Key Literature
*   `[[Simon & Rudell (1967)]]`
*   `[[Simon (1969)]]`
*   `[[Egner et al. (2007)]]`
*   `[[McCann & Johnston (1992)]]` (Exp 2, which includes a Simon manipulation in T2).
