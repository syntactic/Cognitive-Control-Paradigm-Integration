---
title: Home
---
Welcome to the digital home of a Master's thesis project focused on unifying the study of human cognitive control. For decades, researchers have investigated our ability to manage thoughts and actions using a variety of seemingly disparate paradigms like the Stroop Task, Task Switching, and the Psychological Refractory Period (PRP). This project's central goal is to demonstrate that these are not isolated islands of research, but rather distinct regions within a single, continuous [[Parametric Design Space]].

This vault serves as the living knowledge base and conceptual backbone for this research. It contains the theoretical framework, literature notes, data definitions, and open questions that have guided the work.

## How to Navigate This Space

This vault is organized to allow exploration from multiple starting points, from high-level concepts to the specific parameters of individual experiments.

### Core Concepts

To understand the project's foundation, start with these key ideas:

*   **[[Parametric Design Space]]**: The central thesis concept of mapping paradigms onto a continuous space.
*   **[[Cognitive Control]]**: A brief overview of the psychological construct being investigated.
*   **[[Literature Mapping Process]]**: The methodology used to translate published experiments into a structured, analyzable format.
*   **[[Derived Dimensions vs. Low-Level Parameters]]**: The distinction between the conceptual variables used in the literature and the concrete parameters used for implementation.

### The Building Blocks: Derived Dimensions

The parametric space is defined by a set of core experimental dimensions. Understanding these is key to understanding how paradigms relate to one another.

*   **Temporal & Structural Factors:**
    *   `[[Task 2 Response Probability]]`: The key dimension differentiating single-task from dual-task paradigms.
    *   `[[Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]]`: The primary variable in dual-task research.
    *   `[[Distractor SOA]]`: The SOA between a target and distractor in a single-task context.
    *   `[[CSI (Cue-Stimulus Interval)]]`: The time available for advance preparation.
    *   `[[RSI (Response Stimulus Interval)]]`: The time between trials, crucial for studying preparation and decay.
    *   `[[RSI Is Predictable]]`: A critical modulator determining how RSI can be used for preparation.
    *   `[[Switch Rate]]` & `[[Trial Transition Type]]`: Parameters that define the dynamics of task-switching.

*   **Stimulus & Task Properties:**
    *   `[[Stimulus Bivalence & Congruency]]`: The source of conflict in interference tasks.
    *   `[[Task Cue Type]]`: The nature of the information given to the participant.
    *   `[[Task Difficulty]]`: An abstraction of the cognitive load of a task.

*   **Response Properties:**
    *   `[[Response Set Overlap]]`: The relationship between the motor outputs of different tasks.
    *   `[[Stimulus Response Mapping]]`: The compatibility of the rule linking a stimulus to a response.

### Canonical Paradigm Classes

Explore how these dimensions combine to form the classic paradigms of cognitive control:

*   **[[Paradigm Classes/Interference Control|Interference Control]]**: Paradigms like Stroop, Flanker, and Simon that test selective attention.
*   **[[Paradigm Classes/Task Switching|Task Switching]]**: Paradigms that investigate cognitive flexibility by having participants switch between different rule sets.
*   **[[Paradigm Classes/Dual-Task Performance & PRP|Dual-Task Performance & PRP]]**: Paradigms that probe the limits of concurrent processing by requiring two distinct responses in close succession.

### Key Literature & Theoretical Concepts

The vault contains notes on foundational papers and theories. Here are a few examples:

*   `[[Stroop (1935)]]`: The seminal paper on interference.
*   `[[Rogers & Monsell (1995)]]`: A foundational task-switching study introducing the alternating-runs paradigm and the concept of [[Theoretical Concepts/Task-Set Reconfiguration|Task-Set Reconfiguration]].
*   `[[Allport el al. (1994)]]`: A key task-switching paper introducing the influential theory of [[Theoretical Concepts/Task-Set Inertia|Task-Set Inertia]].
*   `[[McCann & Johnston (1992)]]`: A classic dual-task study using the locus-of-slack logic to identify the [[Theoretical Concepts/Bottleneck Theories|processing bottleneck]].
*   `[[Sigman & Dehaene (2006)]]`: A modern study that explicitly bridges dual-task and task-switching paradigms.

### Implementation and Analysis

This section details how the conceptual framework is operationalized.

*   **[[Super Experiment Framework]]**: The software library used to define and run experimental trials based on low-level parameters.
*   **[[Thesis Considerations/PCA Feature Selection|PCA Feature Selection]]** & **[[Thesis Considerations/PCA Input Dimensions|PCA Input Dimensions]]**: The rationale and methodology for the Principal Component Analysis used to analyze the structure of the design space.
*   **[[Parameter Overrides and Sequence Metadata]]**: A note on the system used to handle special cases and non-standard timings from the literature.

### Project Status and Open Questions

This research is an ongoing process. These documents track its current state and future directions:

*   **[[Thesis Outline]]**: The planned structure of the final thesis document.
*   **[[Ongoing Questions]]**: A list of unresolved conceptual and methodological issues.
*   **[[Study Limitations]]**: Acknowledged constraints of the current framework and mapping process.