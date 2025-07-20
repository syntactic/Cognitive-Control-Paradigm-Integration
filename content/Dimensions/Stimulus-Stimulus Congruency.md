---
tags:
  - dimension
  - conflict
  - interference
aliases:
  - S-S Congruency
  - S-S Conflict
  - Stroop-like Conflict
---
### Core Definition
**Stimulus-Stimulus (S-S) Congruency** captures conflict that originates from the stimulus itself, arising when two or more of its attributes **or afforded cognitive operations** prime competing responses within the active task sets. The core of S-S conflict is a clash of *meaning* or *interpretation* triggered by a single stimulus event.

This is the source of **Stroop-like** conflict and **task-based ambiguity** in task-switching.

It addresses the question: "Does an irrelevant feature *or afforded operation* of the stimulus, after applying the relevant task rules, prime the same or a different response as the currently relevant feature/operation?"

### Theoretical Basis
This dimension is a direct operationalization of the conflict described in "Type 4" ensembles of the Dimensional Overlap Model ([[Kornblum et al. (1990)]]). We generalize this to include "operation-based bivalence" (e.g., a single stimulus affording two different tasks), where the conflict still originates from resolving two potential processing pathways tied to the stimulus itself.

### Operationalization in Paradigms
*   **[[Canonical Tasks/Stroop Task|Stroop Task]]:** The canonical example. The conflict is between the irrelevant **word meaning** and the relevant **ink color**.
*   **[[Canonical Tasks/Flanker Task|Flanker Task]]:** The conflict is between the irrelevant **flanker identity** and the relevant **target identity**.
*   **[[Canonical Tasks/Simon Task|Simon Task]]:** In a classic Simon task with a simple, non-semantic stimulus (e.g., a colored dot), S-S Congruency is **not present**. The stimulus lacks a second, conflicting semantic attribute.

### Possible Values & Coding Rules
*   **`Congruent`**: The irrelevant stimulus attribute primes the same response as the relevant attribute (e.g., the word "RED" in red ink).
*   **`Incongruent`**: The irrelevant stimulus attribute primes a different response than the relevant attribute (e.g., the word "BLUE" in red ink).
*   **`Neutral`**: Used when a stimulus is **truly bivalent**, but the irrelevant, response-relevant attribute has no specific congruent or incongruent relationship to the required response on a given trial. This occurs when the irrelevant attribute is orthogonal to the relevant attribute's required response (e.g., the word "TABLE" in red ink). This coding explicitly acknowledges that the stimulus is capable of creating S-S conflict, distinguishing it from a functionally univalent (N/A) stimulus.
*   **`N/A`**: Used when the stimulus is **functionally univalent**. A stimulus is functionally univalent if it lacks a second attribute that is **response-relevant** within the context of the overall experiment's task repertoire. An attribute is only response-relevant if it has a learned or instructed mapping to the response set of another active or competing task. This applies even if the stimulus possesses a second physical attribute (e.g., the black ink on a word in a word-reading task), if that attribute is inert with respect to the competing task's response set.

### Distinction from Other Dimensions
*   **Orthogonal to S-R Congruency:** S-S Congruency is about the relationship *between two stimulus features*. [[Dimensions/Stimulus-Response Congruency|S-R Congruency]] is about the relationship *between an irrelevant stimulus location and the response location*. A paradigm can have one, the other, both, or neither, as demonstrated by [[Egner et al. (2007)]].
*   **Distinct from SRM:** `S-S Congruency` describes conflict from an *irrelevant* feature, while `[[Dimensions/Stimulus Response Mapping]]` describes the nature of the *instructed rule* for the *relevant* feature.

### Super Experiment Mapping
This is typically modeled by presenting a bivalent stimulus (activating both `mov` and `or` pathways) with an `[[Inter-task SOA (Stimulus Onset Asynchrony)|SOA]]=0`.
*   **Congruent:** `stim_mov_1` and `stim_or_1` map to the same response key.
*   **Incongruent:** `stim_mov_1` and `stim_or_1` map to different response keys.
*   **Neutral:** The distractor pathway's stimulus (`stim_or_1`) does not map to any key in the active response set.

### Key Literature
*   `[[Stroop (1935)]]`
*   `[[Eriksen & Eriksen (1974)]]`
*   `[[Egner et al. (2007)]]`
