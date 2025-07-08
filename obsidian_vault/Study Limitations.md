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
    *   **Stimulus Response Mapping:** If there are two tasks, it assumes the mapping type is the same for both tasks. So it is impossible to have one arbitrary mapping for one task and one compatible mapping for another.
    *  **Overloading of the SOA Parameter:** Previously, a limitation was the overloading of the SOA parameter. This has been resolved by separating it into [[Inter-task SOA (Stimulus Onset Asynchrony)]] and [[Dimensions/Distractor SOA]]. This ensures that paradigms like [[Allport el al. (1994)]] Exp. 5 (an RSI-driven dual-task) and [[Kopp et al. (1996)]] (a distractor-SOA interference task) are no longer conflated under a single ambiguous dimension, strengthening the analytical framework.
    *   **Implicit Cues:** Mapping "implicit" cues from literature (e.g., sequence-based) to SE's explicit (though internal) cueing mechanism requires careful interpretation.
    * **Task Difficulty**: The _source_ of difficulty is critical. A task that is difficult due to high perceptual demands may tax the control system differently than a task that is difficult due to a high working memory load. Read Vandierendonck, Liefooghe, and Verbruggen (2010). 

*   **Conceptual Limitations:**
    *   Focus on structural/timing parameters; less on learning, strategy, or individual differences beyond what parameters might induce.