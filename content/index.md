---
title: Home
---
Master's thesis project unifying human cognitive control research. Demonstrates that disparate paradigms (Stroop, Task Switching, PRP) are distinct regions within a single, continuous [[Parametric Design Space]].

This vault contains the theoretical framework, literature notes, data definitions, and open questions guiding this research.

## Navigation

### Core Concepts

*   **[[Parametric Design Space]]**: Central thesis concept mapping paradigms onto a continuous space.
*   **[[Cognitive Control]]**: Overview of the psychological construct under investigation.
*   **[[Literature Mapping Process]]**: Methodology translating published experiments into structured format.
*   **[[Derived Dimensions vs. Low-Level Parameters]]**: Distinction between conceptual variables and implementation parameters.

### Derived Dimensions

Core experimental dimensions grouped by cognitive function, operationalized in the analytical pipeline (see [[Thesis Considerations/MOFA+ as an Exploratory Analytical Tool|MOFA+]]):

*   **Structure & Task Load:**
    *   [[Dimensions/Task 2 Response Probability|Task 2 Response Probability]]: Differentiates single-task (p=0) from dual-task (p=1) paradigms.
    *   [[Dimensions/Task Difficulty|Task Difficulty]]: Cognitive load abstraction.

*   **Temporal Dynamics:**
    *   [[Dimensions/Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]]: Primary dual-task temporal variable.
    *   [[Dimensions/Distractor SOA|Distractor SOA]]: Target-distractor temporal offset.
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: Advance preparation time.
    *   [[Dimensions/RSI (Response Stimulus Interval)|RSI]]: Inter-trial interval.

*   **Context & Sequence:**
    *   [[Dimensions/Switch Rate|Switch Rate]] & [[Dimensions/Trial Transition Type|Trial Transition Type]]: Task-switching dynamics.
    *   [[Dimensions/RSI Is Predictable|RSI Is Predictable]]: RSI preparation modulator.
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: Task specification information.

*   **Conflict Sources:**
    *   [[Dimensions/Stimulus Bivalence & Congruency|Stimulus Bivalence & Congruency]]: Operational dimension combining S-S and S-R conflict sources.

*   **Rules & Mappings:**
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]]: The relationship between the response outputs of different tasks.
    *   [[Dimensions/Stimulus Response Mapping|Stimulus Response Mapping]]: The compatibility of the instructed rule linking a stimulus to a response.

### Paradigm Classes

*   **[[Paradigm Classes/Interference Control|Interference Control]]**: Stroop, Flanker, Simon - selective attention testing.
*   **[[Paradigm Classes/Task Switching|Task Switching]]**: Cognitive flexibility via rule set switching.
*   **[[Paradigm Classes/Dual-Task Performance & PRP|Dual-Task Performance & PRP]]**: Concurrent processing limits via sequential responses.

### Key Literature

*   `[[Stroop (1935)]]`: Seminal interference paper.
*   `[[Rogers & Monsell (1995)]]`: Alternating-runs paradigm and [[Theoretical Concepts/Task-Set Reconfiguration|Task-Set Reconfiguration]].
*   `[[Allport el al. (1994)]]`: [[Theoretical Concepts/Task-Set Inertia|Task-Set Inertia]] theory.
*   `[[McCann & Johnston (1992)]]`: Dual-task [[Theoretical Concepts/Bottleneck Theories|bottleneck]] identification.
*   `[[Sigman & Dehaene (2006)]]`: Bridges dual-task and task-switching paradigms.

### Implementation and Analysis

*   **[[Super Experiment Framework]]**: Software library for trial definition and execution.
*   **Analytical Methods**:
    *   **[[Thesis Considerations/PCA Input Dimensions|PCA]]**: Primary method identifying orthogonal variance axes. See [[Thesis Considerations/PCA Feature Selection|feature selection]].
    *   **[[Thesis Considerations/MOFA+ as an Exploratory Analytical Tool|MOFA+]]**: Theory-driven latent factor exploration across conceptual "views".
*   **[[Super Experiment Mapping Notes Guide]]**: System for handling literature special cases and non-standard timings.

### Project Status

*   **[[Thesis Outline]]**: Planned thesis structure.
*   **[[Ongoing Questions]]**: Unresolved conceptual and methodological issues.
*   **[[Study Limitations]]**: Framework and mapping constraints.
