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

The parametric space is defined by a set of core experimental dimensions, grouped by the cognitive function they primarily target. This structure is directly operationalized in our analytical pipeline (see [[Thesis Considerations/MOFA+ as an Exploratory Analytical Tool|MOFA+]]).

*   **Structure & Task Load:**
    *   [[Dimensions/Task 2 Response Probability|Task 2 Response Probability]]: The key dimension differentiating single-task (p=0) from dual-task (p=1) paradigms.
    *   [[Dimensions/Task Difficulty|Task Difficulty]]: An abstraction of the cognitive load required by each task.

*   **Temporal Dynamics:**
    *   [[Dimensions/Inter-task SOA (Stimulus Onset Asynchrony)|Inter-task SOA]]: The primary temporal variable in dual-task research (T1-S1 to T2-S2 onset).
    *   [[Dimensions/Distractor SOA|Distractor SOA]]: The temporal offset between a target and a distractor in a single-task context.
    *   [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]: The time available for advance preparation.
    *   [[Dimensions/RSI (Response Stimulus Interval)|RSI]]: The time between trials, crucial for studying preparation and decay of interference.

*   **Context & Sequence:**
    *   [[Dimensions/Switch Rate|Switch Rate]] & [[Dimensions/Trial Transition Type|Trial Transition Type]]: Parameters that define the dynamics of task-switching.
    *   [[Dimensions/RSI Is Predictable|RSI Is Predictable]]: A critical modulator determining how RSI can be used for preparation.
    *   [[Dimensions/Task Cue Type|Task Cue Type]]: The nature of the information given to the participant to specify the task.

*   **Conflict Sources:**
    *   [[Dimensions/Stimulus-Stimulus Congruency|Stimulus-Stimulus Congruency]]: The source of Stroop-like conflict (semantic/identity).
    *   [[Dimensions/Stimulus-Response Congruency|Stimulus-Response Congruency]]: The source of Simon-like conflict (spatial/structural).

*   **Rules & Mappings:**
    *   [[Dimensions/Response Set Overlap|Response Set Overlap]]: The relationship between the motor outputs of different tasks.
    *   [[Dimensions/Stimulus Response Mapping|Stimulus Response Mapping]]: The compatibility of the instructed rule linking a stimulus to a response.

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

This section details how the conceptual framework is operationalized and analyzed.

*   **[[Super Experiment Framework]]**: The software library used to define and run experimental trials based on low-level parameters.
*   **Analytical Methods**: We use a dual-analysis approach to explore the structure of the design space:
    *   **[[Thesis Considerations/PCA Input Dimensions|Principal Component Analysis (PCA)]]**: Our primary method for identifying the orthogonal axes of maximal variance in the design space. See our notes on [[Thesis Considerations/PCA Feature Selection|feature selection]] and [[Thesis Considerations/PCA Input Dimensions|input dimensions]].
    *   **[[Thesis Considerations/MOFA+ as an Exploratory Analytical Tool|MOFA+]]**: A secondary, theory-driven method used to explore how latent factors are distributed across conceptually-defined "views" of the data.
*   **[[Parameter Overrides and Sequence Metadata]]**: A note on the system used to handle special cases and non-standard timings from the literature.

### Project Status and Open Questions

This research is an ongoing process. These documents track its current state and future directions:

*   **[[Thesis Outline]]**: The planned structure of the final thesis document.
*   **[[Ongoing Questions]]**: A list of unresolved conceptual and methodological issues.
*   **[[Study Limitations]]**: Acknowledged constraints of the current framework and mapping process.
