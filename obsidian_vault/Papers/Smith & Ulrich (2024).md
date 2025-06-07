---
tags:
  - paper
  - literature_review_source
  - interference_tasks
  - neutral_condition
  - cognitive_modeling
aliases:
  - Smith & Ulrich 2024
---

###### Core Goal & Contribution to Thesis Project
Smith & Ulrich (2024), in "The neutral condition in conflict tasks: On the violation of the midpoint assumption in reaction time trends," served as a key resource for this thesis project, primarily by:
1.  Highlighting the theoretical importance and often-overlooked informative nature of the **neutral condition** in conflict tasks ([[Flanker Task]], [[Stroop Task]], [[Simon Task]]).
2.  Providing a **curated list of existing studies (Table 1)** that include neutral conditions, which directly informed the selection of interference task literature for coding and analysis in this project's [[Parametric Design Space]] mapping.
3.  Discussing the **"midpoint assumption"** (that neutral RT should be the average of congruent and incongruent RTs) and presenting evidence for its frequent violation, particularly showing that neutral RT is often closer to congruent RT (R < 1).
4.  Evaluating how current **diffusion models of conflict processing** (DSTP, SSP, DMC) account for, or fail to account for, the observed patterns of neutral RTs.

The paper's central arguments are that the neutral condition is more than just a baseline; its specific characteristics can reveal nuances about conflict processing and provide critical tests for cognitive models.

###### Key Arguments & Findings of Smith & Ulrich (2024)

1.  **Violation of the Midpoint Assumption:**
    *   The authors argue that empirical evidence often shows the average neutral reaction time (RTN) is *not* evenly placed between congruent (RTC) and incongruent (RTI) RTs.
    *   Their literature search (Table 1) and their own experiments largely support that the ratio **R = (RTN - RTC) / (RTI - RTN)** is typically **less than 1**, indicating RTN is closer to RTC.
    *   This violation challenges models that implicitly or explicitly assume symmetrical facilitation and interference effects around a neutral midpoint.

2.  **Informative Nature of the Neutral Condition:**
    *   The position of RTN can differentiate between facilitation (RTN - RTC) and interference (RTI - RTN) components of the overall congruency effect.
    *   Different ways of operationalizing the neutral stimulus can lead to different RTN values, suggesting that "neutrality" itself is not a monolithic concept and can be parametrically varied.

3.  **Modeling Implications:**
    *   Current diffusion models like DSTP and SSP tend to predict R ≈ 1.
    *   The Diffusion Model of Conflict (DMC) can predict R > 1 but struggles with the commonly observed R < 1.
    *   The authors suggest that violations of the midpoint assumption, particularly the R < 1 pattern, necessitate elaborations of existing models, possibly by incorporating non-linear controlled process trajectories or biased automatic processes.

4.  **Experimental Investigations:**
    *   The paper presents experiments using Flanker, Stroop, and Simon tasks with two different stimulus sets (linguistic vs. symbolic) to test the robustness of the midpoint assumption violation.
    *   Their results generally confirm the R < 1 pattern for Flanker and Stroop tasks, though Simon task results were more varied and sometimes showed R > 1, consistent with their literature review.

###### Relevance to Thesis & How It Was Used

*   **Literature Identification:** Table 1 was a primary source for identifying empirical studies of Flanker, Stroop, and Simon tasks that included neutral conditions, allowing for a more targeted literature search for the CSV coding.
*   **Conceptualization of Neutrality:** Deepened the understanding of the neutral condition and its role in dissecting congruency effects, informing the `Stimulus Bivalence & Congruency` dimension.
*   **R-Value as a Metric:** Introduced the R-value as a useful descriptive metric for quantifying the relative position of the neutral RT, which could be a potential variable to extract or calculate for coded studies.
*   **Model Evaluation Context:** Provided context on how different conflict models make predictions regarding the neutral condition, which is relevant for the broader theoretical discussion of the [[Parametric Design Space]].
*   **Highlighting Gaps/Challenges:** Underscored the challenge in consistently defining and modeling "neutral" stimuli and the implications for theoretical accounts of cognitive control.

This paper was instrumental in shaping the approach to selecting and analyzing interference tasks for this thesis, particularly by emphasizing the diagnostic value of the neutral condition.