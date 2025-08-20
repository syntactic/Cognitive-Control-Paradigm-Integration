---
tags:
  - methodology
  - data_processing
  - guide
  - canonical_schema
---

## 1. Purpose and Rationale

Guidelines for the `Super_Experiment_Mapping_Notes` JSON column serving two functions:

1. **`convert.py` overrides:** Trial-level timing calculation adjustments for literature fidelity
2. **`viewer.js` metadata:** Between-trial sequencing and randomization for simulations

Keeps main CSV clean for analysis while capturing operationalization nuances in JSON.

## 2. The RSI vs. ITI Abstraction: A Methodological Note

A core challenge is translating literature concepts to the framework's capabilities. A prime example is the **Response-Stimulus Interval (RSI)**.
*   **Conceptual RSI:** A dynamic interval that begins after a participant's response.
*   **Operational ITI:** A static, pre-defined Inter-Trial Interval (`regen` time in `super-experiment`) that begins at the end of a trial's fixed duration.

The framework **implements an ITI**. However, to maintain fidelity with the task-switching literature, we code the conceptual interval in the main CSV under the `RSI` column. The JSON configuration below uses `ITI` prefixes to make it clear that we are controlling the *implemented* parameter in the viewer. This is a deliberate, documented abstraction.

## 3. JSON Schema Overview

The JSON object has a nested structure to clearly separate concerns. For any given experimental condition (row), a key should only be included if its value deviates from the project's standard defaults.

```json
{
  "block_id": "unique_string_identifier_for_the_block",
  "description": "A brief, human-readable note about this condition's role.",
  
  "convert_overrides": {
    "t1_stim_duration": 300,
    "t2_stim_duration": 5000,
    "t1_cue_go_duration": 5000
  },

  "viewer_config": {
    "sequence_type": "AABB",
    "ITI_distribution": "uniform",
    "ITI_range": [1000, 1500],
    "SOA_distribution": "uniform",
    "SOA_range": [-1000, 1000]
  }
}
```

---

## 4. Top-Level Keys: Identification and Context

These keys exist at the root of the JSON object.

*   **`block_id`** (string)
    *   **Purpose:** The most critical key for grouping. It uniquely identifies an experimental block. All trial conditions (rows) that are part of the same mixed-task block **must share the exact same `block_id` string.** This solves the grouping problem efficiently and without redundancy.
    *   **Pipeline Role:** `convert.py` will propagate this value to a `Block_ID` column in `resolved_design_space.csv`. `viewer.js` will then use this column to assemble complete blocks for simulation.
    *   **Example ID:** `"rogers_monsell_1995_exp2_random_rsi"`

*   **`description`** (string, optional but recommended)
    *   **Purpose:** A brief, human-readable note to clarify the specific nature of the condition. Invaluable for debugging and context.
    *   **Pipeline Role:** Propagated to a `Description` column for display in the viewer.
    *   **Example:** `"Incongruent trials within the 75% congruent block."`

## 5. `convert_overrides` Section (for `convert.py`)

This section contains keys that are parsed exclusively by the `convert.py` script. They are used to **override default within-trial timing calculations** when a paper specifies non-standard durations that cannot be captured by the main derived dimensions alone.

*   **`t1_stim_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the Task 1 stimulus (or the target in a single-task paradigm).
    *   **Example:** `300` (for the short auditory tone in [[Hazeltine et al. (2006)]]).

*   **`t2_stim_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the Task 2 stimulus (or the distractor in a single-task paradigm).
    *   **Example:** `5000` (to approximate "visible until response").

*   **`t1_cue_go_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the cue and go-signal intervals for Task 1. *Note: The current `super-experiment` framework assumes cue and go signals have identical timing. This override affects both.*
    *   **Example:** `5000` (for a long response window).

*   **`t2_cue_go_duration`** (integer, in ms)
    *   **Purpose:** Sets the duration of the cue and go-signal intervals for Task 2.

## 6. `viewer_config` Section (for `viewer.js`)

This section contains keys that are propagated by `convert.py` into the `resolved_design_space.csv` and are used by the `viewer.js` client to **structure the sequence of trials and handle randomization** during an interactive simulation.

### 6.1. Task Sequencing

*   **`sequence_type`** (string)
    *   **Purpose:** Defines a non-random task sequence for task-switching paradigms, overriding the simple `Switch Rate` percentage from the main CSV.
    *   **Values:** `"AABB"`, `"ABAB"`, `"AAAABBBB"`. Defaults to `"Random"` if not present.

### 6.2. Inter-Trial Interval (ITI) Randomization

These keys control the `regen` time between trials. They are used when a study randomizes the interval *between* trials, as in [[Rogers & Monsell (1995)]] Exp. 2.

*   **`ITI_distribution`** (string)
    *   **Purpose:** Specifies how the ITI should be determined on each trial. The main `RSI` column in the CSV should contain the *mean* of this distribution for analysis.
    *   **Values:** `"uniform"`, `"choice"`. Defaults to `"fixed"`.

*   **`ITI_range`** (array of 2 numbers)
    *   **Purpose:** Used with `"uniform"` distribution. Defines the `[min, max]` values.
    *   **Example:** `[150, 1200]`

*   **`ITI_values`** (array of numbers)
    *   **Purpose:** Used with `"choice"` distribution. Defines the discrete set of possible values.
    *   **Example:** `[600, 1600]`

### 6.3. Stimulus Onset Asynchrony (SOA) Randomization

These keys are used for dual-task paradigms where the `Inter-task SOA` is randomized on a trial-by-trial basis.

*   **`SOA_distribution`** (string)
    *   **Purpose:** Specifies how the Inter-task SOA should be determined. The main `Inter-task SOA` column should contain the *mean* of this distribution.
    *   **Values:** `"uniform"`, `"choice"`. Defaults to `"fixed"`.

*   **`SOA_range`** (array of 2 numbers)
    *   **Purpose:** Used with `"uniform"` distribution for SOA.
    *   **Example:** `[-1000, 1000]` (from [[Sigman & Dehaene (2006)]])

*   **`SOA_values`** (array of numbers)
    *   **Purpose:** Used with `"choice"` distribution for SOA.

## 7. A Note on RSI-Driven Dual Tasks

A small but theoretically important class of paradigms, notably [[Allport et al. (1994)]] Exp. 5, are structured as dual-tasks where the primary independent variable is the **Response-Stimulus Interval (RSI)** between R1 and S2. This is parametrically distinct from classic SOA-driven PRP, where the interval is between S1 and S2.

The framework identifies these unique paradigms using a specific three-part rule. The `convert.py` script applies special timing logic if and only if a condition meets all of the following criteria:

1.  `Task 2 Response Probability` is `1`.
2.  `Inter-task SOA` is `N/A`.
3.  `RSI` has a numerical value.

**Implementation Logic in `convert.py`:**

Because the start time of S2 in these paradigms depends on a dynamic event (R1), which `convert.py` cannot know, we must use a principled approximation. The script will calculate the start time of S2 as follows:

`start_S2 = start_S1 + assumed_RT1 + RSI`

An `assumed_RT1` of **600ms** will be used as a reasonable placeholder for a standard choice-reaction time. This is a documented abstraction within the framework. This logic ensures these unique designs are correctly operationalized based on their conceptual structure, without requiring a special JSON override.
