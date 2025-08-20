---
tags:
  - dimension
  - deprecated
aliases:
  - N_Tasks
---

## ⚠️ DEPRECATED DIMENSION

**This dimension has been superseded by [[Dimensions/Task 2 Response Probability]] for analytical purposes.**

### Legacy Definition
The number of distinct stimulus-response (S-R) episodes that the participant is instructed to complete **within a single trial presentation** or very close temporal proximity, typically triggered by temporally distinct stimuli (S1, S2).

**Values:** Categorical {1, 2}

### Why This Dimension Was Deprecated
As detailed in GEMINI.md, the discrete Number of Tasks dimension creates interpretability problems for parametric analysis. When using Principal Component Analysis (PCA), interpolating between single-task (N_Tasks=1) and dual-task (N_Tasks=2) paradigms yields mathematically incoherent results like N_Tasks=1.5.

### Replacement Dimension
**[[Dimensions/Task 2 Response Probability]]** provides a continuous (0.0 to 1.0) representation of the same conceptual space:
- **Value = 0.0:** Corresponds to all single-task paradigms (interference, task-switching)
- **Value = 1.0:** Corresponds to all dual-task paradigms (PRP, dual-task)
- **Interpolated values:** Represent coherent "bridge" paradigms where Task 2 response is probabilistic

### Legacy Usage
This dimension may still appear in:
- Historical paper summaries for descriptive purposes
- The CSV column headers for backward compatibility
- Conceptual discussions where the discrete categorization is more intuitive

For all analytical and operational purposes, use [[Dimensions/Task 2 Response Probability]].
