---
tags:
  - methodology
  - data_processing
  - super_experiment
aliases:
  - JSON Overrides
---
# Parameter Overrides and Sequence Metadata in Super_Experiment_Mapping_Notes

## 1. Purpose and Rationale

While the primary goal of the thesis is to map literature to a set of high-level [[Derived Dimensions vs. Low-Level Parameters|derived dimensions]] (like [[Dimensions/SOA (Stimulus Onset Asynchrony)|SOA]] and [[Dimensions/CSI (Cue-Stimulus Interval)|CSI]]), some experimental designs in the literature have specific timing characteristics that cannot be captured by these dimensions alone. The `Super_Experiment_Mapping_Notes` column in the `super_experiment_design_space.csv` file provides a mechanism to handle these exceptions and special cases through a structured JSON object.

This system allows the Python conversion script (`convert.py`) to apply specific, hard-coded values for certain parameters on a per-condition basis, overriding the script's default calculations. This ensures maximum fidelity in translating a specific paper's methodology into the [[Super Experiment Framework]], especially when default assumptions (like a standard 2000ms stimulus duration) do not apply.

The primary use case is to define non-standard **durations** for stimulus, cue, or "go" signal intervals that are explicitly mentioned in a paper (e.g., a stimulus lasting only 300ms, or a go-signal lasting until the end of a trial). A secondary use case is to define structural information (e.g., "AABB" trial sequences or variable RSI distributions) that is used by the viewer client to simulate the experiment faithfully, while the main CSV columns contain a simplified, PCA-compatible value (e.g., average switch rate or mean RSI).

## 2. JSON Structure

The metadata is placed within a single JSON object in the `Super_Experiment_Mapping_Notes` column. All keys are optional.

```json
{
  "sequence_type": "AABB",
  "RSI_distribution": "uniform",
  "RSI_range": [150, 1200],
  "param_overrides": {
    "t1_stim_duration": 300,
    "t1_cue_go_duration": 5000
  },
  "description": "A human-readable note for the viewer client."
}
```

## 3. List of Overrideable Parameters

The following parameters can be defined within the `param_overrides` dictionary. These values directly influence the calculation of the `effective_start_*` and `effective_end_*` columns in the `resolved_design_space.csv`.

#### Duration Overrides

These control the length of specific events in the trial.

-   **`base_stim_duration`**
    -   **Description:** Overrides the script's default stimulus duration (e.g., 2000ms) for **both** Task 1 and Task 2 stimuli, unless a more specific override (`t1_stim_duration` or `t2_stim_duration`) is also present.
    -   **Effect on Resolved CSV:** Modifies the calculation of `effective_end_stim...` columns.

-   **`t1_stim_duration`**
    -   **Description:** Specifically sets the duration for the Task 1 stimulus. In a dual-task context, this is the first task; in a single-task context, it's the target stimulus.
    -   **Effect on Resolved CSV:** Overrides `base_stim_duration` for calculating `effective_end_stim1_mov` or `effective_end_stim1_or`.

-   **`t2_stim_duration`**
    -   **Description:** Specifically sets the duration for the Task 2 stimulus. In a dual-task context, this is the second task; in a single-task context, it's the distractor stimulus.
    -   **Effect on Resolved CSV:** Overrides `base_stim_duration` for calculating `effective_end_stim1_or` (in dual-task) or `effective_end_stim2...` (in sequential tasks, currently unused).

-   **`base_cue_go_duration`**
    -   **Description:** Overrides the default duration for **all** cue and "go" signal intervals. This is useful for setting a long response window that extends well beyond stimulus offset.
    -   **Effect on Resolved CSV:** Modifies `effective_end_cue1`, `effective_end_go1`, `effective_end_cue2`, and `effective_end_go2`.

-   **`t1_cue_go_duration`**
    -   **Description:** Specifically sets the duration for the cue and "go" signal associated with Task 1.
    -   **Effect on Resolved CSV:** Overrides `base_cue_go_duration` for `effective_end_cue1` and `effective_end_go1`.

-   **`t2_cue_go_duration`**
    -   **Description:** Specifically sets the duration for the cue and "go" signal associated with Task 2.
    -   **Effect on Resolved CSV:** Overrides `base_cue_go_duration` for `effective_end_cue2` and `effective_end_go2`.

#### Trial Format Overrides

These keys provide structural information for the viewer client to use when generating a trial sequence.

-   **`sequence_type`** (String)
    -   **Description:** Defines a non-random trial sequence structure for task-switching paradigms. If this key is present, it overrides the simple `Switch_Rate_Percent`.
    -   **Possible Values:** `"AABB"`, `"ABAB"`, etc.
    -   **Default (if not present):** `"Random"`. The client will use `Switch_Rate_Percent` to generate trials.
#### RSI Distribution Overrides
These keys are used to document experiments where RSI is randomized on a trial-by-trial basis. For PCA compatibility, the main CSV column (RSI) should contain the expected value of this distribution (e.g., 0 for a symmetric range), while this metadata preserves the full experimental design for the viewer or deeper analysis.
-   **`RSI_distribution`** (String)
    -   **Description:** Specifies the distribution from which the inter-trial interval (ITI/RSI) should be drawn. This works in conjunction with `RSI_range` or `RSI_values`.
    -   **Possible Values:** `"fixed"`, `"uniform"`, `"choice"`.
    -   **Default (if not present):** `"fixed"`. The client will use the single numerical value from the `ITI_ms` column.

-   **`RSI_range`** (Array of 2 numbers)
    -   **Description:** Used when `RSI_distribution` is `"uniform"`. Defines the `[min, max]` values for the uniform distribution.
    -   **Example:** `[150, 1200]`

-   **`RSI_values`** (Array of numbers)
    -   **Description:** Used when `RSI_distribution` is `"choice"`. Defines the discrete set of values from which to randomly sample.
    -   **Example:** `[600, 1600]`
#### SOA Distribution Overrides
These keys are used to document experiments where SOA is randomized on a trial-by-trial basis. For PCA compatibility, the main CSV column (SOA) should contain the expected value of this distribution (e.g., 0 for a symmetric range), while this metadata preserves the full experimental design for the viewer or deeper analysis.
* **`SOA_distribution`** (String)
	* **Description:** Specifies the distribution from which the SOA should be drawn.
	* **Possible Values:** "uniform", "choice".
	* **Default (if not present):** "fixed". The client will use the single numerical value from the SOA column.
* **`SOA_range`** (Array of 2 numbers)
	* **Description:** Used when SOA_distribution is "uniform". Defines the [min, max] values for the uniform distribution.
	- **Example (from [[Sigman & Dehaene (2006)]]):** [-1000, 1000]
- **`SOA_values`** (Array of numbers)
	- **Description:** Used when `SOA_distribution` is "`choice`". Defines the discrete set of values from which to randomly sample.
## 4. Example Application: [[Hazeltine et al. (2006)]]

In Hazeltine et al. (2006), the auditory tone stimulus (Task 1) lasted for **300ms**, while the visual word stimulus (Task 2) remained visible until a response was made. We can model this with overrides:

-   **Goal:** Set T1 stimulus duration to 300ms and ensure the "go" signal for T2 lasts a very long time to approximate "until response."
-   **JSON in Notes Column:**
    ```json
    {
      "param_overrides": {
        "t1_stim_duration": 300,
        "t2_stim_duration": 5000, 
        "t2_cue_go_duration": 5000
      }
    }
    ```
-   **Effect on Conversion Script:**
    -   When processing this row, the script will use `300` instead of the default `2000` to calculate `effective_end_stim1_mov`.
    -   It will use `5000` to calculate `effective_end_stim1_or` (T2 stimulus).
    -   It will use `5000` to calculate `effective_end_cue2` and `effective_end_go2`, ensuring the response window for T2 is very long.
## Example Application 2: [[Rogers & Monsell (1995)]] Exp 2

-   **Description:** A task-switching experiment with an "AABB" sequence and a random RSI drawn uniformly from 150ms to 1200ms.
-   **Main CSV Columns:**
    -   `Switch Rate`: `33%`
    -   `RSI`: `675` (the mean)
-   **JSON in Notes Column:**
    ```json
    {
      "sequence_type": "AABB",
      "RSI_distribution": "uniform",
      "RSI_range": [150, 1200]
    }
    ```
-   **Effect:** The PCA script uses the simple `675` value from the `RSI` column. The viewer client reads the JSON and knows to generate an AABB sequence where the ITI for each trial is a new random number between 150 and 1200.

This override system provides the necessary flexibility to accurately map the specific temporal details of diverse experimental literature into a consistent, analyzable format.