## Study Limitations & SE Framework Constraints

*   **[[Super Experiment Framework|Super Experiment]] Intrinsic Limitations:**
    *   **RSI (Response-Stimulus Interval):** Cannot be directly set as an independent parameter. SE's trial structure is stimulus-onset driven. (e.g., affects mapping [[Rogers & Monsell (1995)]], some [[Stephan & Koch (2010)]] conditions). Map to ITI.
    *   **Cue Validity:** SE doesn't have native inter-trial probabilistic cue validity. Cues are 100% valid for the task they signal within a trial. 
    *   **N > 2 Task Pools:** SE is designed for 2 tasks per trial. Mapping experiments with >2 available task sets (e.g., [[Rubin & Meiran (2005)]] Exp2) requires abstraction to pairwise interactions.
    *   **Specific Stimulus/Task Types:** SE uses generic 'mov'/'or'. Abstraction needed for literature tasks (Stroop, Simon, calculations, line judgments). Fidelity of mapping complex cognitive operations is limited.
    *   **Complex Response Modalities:** SE is keypress-based. Literature with vocal responses requires abstraction.

*   **Mapping & Coding Limitations:**
    *   **Literature Scope:** Cannot be exhaustive; selection bias possible.
	    * In Task-Switching, I did not look into Voluntary Task Switching by Arrington & Logan (2004). In such a case, there's no way of defining a SE parameter override to do voluntary task switching, and I don't know how I'd code it in the dimensions other than creating a new [[Task Cue Type]]. 
    *  **Overloading of the SOA Parameter:** Previously, a limitation was the overloading of the SOA parameter. This has been resolved by separating it into [[Inter-task SOA (Stimulus Onset Asynchrony)]] and [[Dimensions/Distractor SOA]]. This ensures that paradigms like [[Allport el al. (1994)]] Exp. 5 (an RSI-driven dual-task) and [[Kopp et al. (1996)]] (a distractor-SOA interference task) are no longer conflated under a single ambiguous dimension, strengthening the analytical framework.
    *   **Implicit Cues:** Mapping "implicit" cues from literature (e.g., sequence-based) to SE's explicit (though internal) cueing mechanism requires careful interpretation.
    * **Task Difficulty**: The _source_ of difficulty is critical. A task that is difficult due to high perceptual demands may tax the control system differently than a task that is difficult due to a high working memory load. Read Vandierendonck, Liefooghe, and Verbruggen (2010). 
### Exclusion of Sequential and Contextual Effects

The parametric design space is primarily concerned with the static, structural parameters that define an individual experimental condition. It deliberately abstracts away from dynamic, trial-to-trial modulations of performance that arise from sequential context or trial history. This limitation means that key phenomena related to cognitive control adaptation are not directly modeled. Two foundational studies illustrate this exclusion:

1.  **Block-Level Contextual Probability:** In **[[Gratton, Coles, and Donchin (1992)]]**, the global probability of congruent vs. incongruent flanker trials was manipulated across blocks. They found that the magnitude of the Flanker effect on a given trial was modulated by this block-level statistical context. The framework lacks a dimension for "Contextual Expectancy" or "Trial-Type Probability," and therefore cannot distinguish between two physically identical trials that produce different results due to the block they are in.

2.  **Trial-to-Trial Sequential Effects:** In **[[Egner et al. (2007)]]**, the core finding was that **conflict adaptation** is domain-specific: the Stroop effect was reduced following a Stroop-incongruent trial, but not a Simon-incongruent trial. Capturing this requires modeling the specific sequence of congruency across trials (e.g., Incongruent-Congruent vs. Congruent-Congruent). The `Trial Transition Type` dimension is designed to capture task-rule switches, not these finer-grained congruency-based transitions.

#### Abstraction of Stimulus Ambiguity Source
 
In task-switching paradigms, stimulus ambiguity can arise from two distinct sources, which may engage different cognitive control mechanisms:
 
- **Attribute-Based Bivalence:** A stimulus has multiple, separable perceptual features, each relevant to a different task (e.g., a "blue circle" in a color-shape switching task). Resolving this conflict may rely on attentional selection.
- **Operation-Based Bivalence:** A single, non-decomposable stimulus affords multiple, competing transformations or rules (e.g., the number "64" in a task switching between "add the digits" and "multiply the digits," as in [[Jersild (1927)]]). Resolving this conflict may rely more on rule maintenance and inhibition.

For the sake of a parsimonious design space, this framework does not currently have a dedicated dimension to distinguish between these two sources of ambiguity. Both are coded with S-S Congruency: N/A and S-R Congruency: N/A, with the core conflict being captured by the Trial Transition Type (Switch vs. Repeat). This is a deliberate abstraction that should be considered when interpreting the results.

In both cases, physically identical trials yield different behavioral outcomes based on the context in which they are embedded. To maintain a tractable and comparable feature set across dozens of studies for the primary PCA, we have made the methodological decision to focus on the properties of the trial types themselves, acknowledging that this excludes the rich and important domain of sequential trial dynamics from the main analysis.

*   **Conceptual Limitations:**
    *   Focus on structural/timing parameters; less on learning, strategy, or individual differences beyond what parameters might induce.
    *   The framework primarily describes *what* experimental conditions are, not *how* the mind implements the required control. There is a risk of conflating a parameter-level description (e.g., a high value on a "Conflict" dimension derived from PCA) with a true mechanism-level theory (e.g., the feedback loop proposed by [[Theoretical Concepts/Conflict Monitoring Theory|Conflict Monitoring Theory]], see [[Botvinick et al. (2001)]]).
