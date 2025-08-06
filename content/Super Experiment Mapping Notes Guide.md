---
tags:
  - methodology
  - data_processing
  - guide
---
## 1. Purpose and Rationale

This document provides the canonical guidelines for using the `Super_Experiment_Mapping_Notes` column in the `super_experiment_design_space.csv` dataset. This column contains a JSON object that serves two critical functions:

1.  **It allows for precise overrides** of default within-trial timing calculations performed by `convert.py`, ensuring maximum fidelity to the source literature.
2.  **It provides essential metadata** about between-trial sequencing and randomization for the `viewer.js` client, enabling high-fidelity interactive simulations.

The principle is to keep the main CSV columns clean and optimized for quantitative analysis (PCA, MOFA+) while using this JSON object to capture the necessary nuances for accurate operationalization.

## 2. JSON Schema Overview

The JSON object has a flat structure with several optional keys. For any given experimental condition (row), a key should only be included if its value deviates from the project's standard defaults.
```json
{
  "block_id": "string",
  "description": "string",
  "convert_overrides": {
    "t1_stim_duration": integer,
    "t2_stim_duration": integer,
    "t1_cue_go_duration": integer,
    "t2_cue_go_duration": integer
  },
  "viewer_config": {
    "sequence_type": "string",
    "RSI_distribution": "string",
    "RSI_range": [min, max],
    "RSI_values": [val1, val2],
    "SOA_distribution": "string",
    "SOA_range": [min, max],
    "SOA_values": [val1, val2]
  }
}
```

---

## 3. Detailed Key Definitions

### 3.1. Block and Condition Identifiers

*   **`block_id`** (string)
    *   **Purpose:** The most critical key for grouping. It uniquely identifies an experimental block. All trial conditions (rows) that are part of the same mixed-task block **must share the exact same `block_id` string.** This solves the grouping problem efficiently and without redundancy.
    *   **Example:** For all conditions in Rogers & Monsell's (1995) Experiment 2, the ID could be `"rogers_monsell_1995_exp2"`.

*   **`description`** (string)
    *   **Purpose:** A brief, human-readable note to clarify the specific nature of the condition. Invaluable for debugging and context.
    *   **Example:** `"Switch trial with incongruent distractor, short RSI block."`

### 3.2. Within-Trial Timing Overrides (for `convert.py`)

These keys are parsed by `convert.py` to override its default timing calculations. They are only needed when a paper specifies non-standard durations.

*   **`t1_stim_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the Task 1 stimulus (or the target in a single-task paradigm).
    *   **Example:** `300` (for the auditory tone in [[Hazeltine et al. (2006)]]).

*   **`t2_stim_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the Task 2 stimulus (or the distractor in a single-task paradigm).
    *   **Example:** `5000` (to approximate "visible until response").

*   **`t1_cue_go_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the cue and go-signal intervals for Task 1. *Note: As you correctly observed, the current `convert.py` script assumes cue and go signals have identical timing. This override affects both.*
    *   **Example:** `5000` (for a long response window).

*   **`t2_cue_go_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the cue and go-signal intervals for Task 2.
    *   **Example:** `5000`

### 3.3. Between-Trial Sequence Configuration (for `viewer.js`)

These keys are propagated by `convert.py` into the `resolved_design_space.csv` and are used by `viewer.js` to structure the sequence of trials during simulation.

*   **`sequence_type`** (string)
    *   **Purpose:** Defines a non-random task sequence for task-switching paradigms, overriding the simple `Switch Rate` percentage.
    *   **Values:** `"AABB"`, `"ABAB"`, `"AAAABBBB"`. Defaults to `"Random"` if not present.

*   **`RSI_distribution`** (string)
    *   **Purpose:** Specifies how the RSI/ITI should be determined on each trial. The main `RSI` column in the CSV should contain the *mean* of this distribution for PCA.
    *   **Values:** `"uniform"`, `"choice"`. Defaults to `"fixed"` if not present.

*   **`RSI_range`** (array of 2 numbers)
    *   **Purpose:** Used with `"uniform"` distribution. Defines the `[min, max]` values.
    *   **Example:** `[150, 1200]`

*   **`RSI_values`** (array of numbers)
    *   **Purpose:** Used with `"choice"` distribution. Defines the discrete set of possible values.
    *   **Example:** `[600, 1600]`

*   **`SOA_distribution`** (string)
    *   **Purpose:** Specifies how the Inter-task SOA should be determined on each trial in dual-task paradigms. The main `Inter-task SOA` column should contain the *mean* of this distribution.
    *   **Values:** `"uniform"`, `"choice"`. Defaults to `"fixed"`.

*   **`SOA_range`** (array of 2 numbers)
    *   **Purpose:** Used with `"uniform"` distribution for SOA.
    *   **Example:** `[-1000, 1000]` (from [[Sigman & Dehaene (2006)]])

*   **`SOA_values`** (array of numbers)
    *   **Purpose:** Used with `"choice"` distribution for SOA.

## 4. Worked Example: Coding a Mixed Block from [[De Jong (2002)]]

This experiment used an AABB sequence with a random RSI chosen from three values. Let's code the "Switch Congruent" and "Repeat Incongruent" conditions from a short block.

**Condition 1: Switch Congruent**
*   **CSV Row:** `Experiment`: `De Jong (2000) Exp2 Short Block Switch Congruent`, `Trial Transition Type`: `Switch`, `Stimulus-Stimulus Congruency`: `Congruent`, `RSI`: `750` (mean), `RSI is Predictable`: `No`...
*   **JSON in Notes Column:**
    ```json
    {
      "block_id": "dejong_2000_exp2_short",
      "viewer_config": {
        "sequence_type": "AABB",
        "RSI_distribution": "choice",
        "RSI_values":
      }
    }
    ```

**Condition 2: Repeat Incongruent**
*   **CSV Row:** `Experiment`: `De Jong (2000) Exp2 Short Block Repeat Incongruent`, `Trial Transition Type`: `Repeat`, `Stimulus-Stimulus Congruency`: `Incongruent`, `RSI`: `750`, `RSI is Predictable`: `No`...
*   **JSON in Notes Column:**
    ```json
    {
      "block_id": "dejong_2000_exp2_short",
      "viewer_config": {
        "sequence_type": "AABB",
        "RSI_distribution": "choice",
        "RSI_values":
      }
    }
    ```
By using the same `block_id`, `viewer.js` knows these two conditions (and the other two from that block) belong together in a single simulation.
