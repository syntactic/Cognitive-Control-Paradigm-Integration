import pytest
import pandas as pd
import numpy as np
import logging
from analysis_utils import (
    preprocess,
    create_pca_pipeline,
    find_centroids,
    interpolate_centroids,
    inverse_transform_point,
    get_component_loadings,
    map_ss_congruency,
    map_sr_congruency,
    classify_paradigm
)

def test_map_ss_congruency():
    assert map_ss_congruency('Congruent') == 'SS_Congruent'
    assert map_ss_congruency('Incongruent') == 'SS_Incongruent'
    assert map_ss_congruency('Neutral') == 'SS_Neutral'
    assert map_ss_congruency('N/A') == 'SS_NA'
    assert map_ss_congruency(np.nan) == 'SS_NA'

def test_map_sr_congruency():
    assert map_sr_congruency('Congruent') == 'SR_Congruent'
    assert map_sr_congruency('Incongruent') == 'SR_Incongruent'
    assert map_sr_congruency('Neutral') == 'SR_Neutral'
    assert map_sr_congruency('N/A') == 'SR_NA'
    assert map_sr_congruency(np.nan) == 'SR_NA'

def test_data_validation_logging(caplog):
    """
    Tests that the validation function logs appropriate warnings for
    inconsistent data, including the new Distractor SOA heuristic.
    """
    caplog.set_level(logging.WARNING)

    # Test Case: Distractor SOA has a value, but both congruency columns are N/A
    invalid_data = pd.DataFrame({
        'Experiment': ['TestExp_Distractor'],
        'Distractor SOA': ['-100'],
        'Stimulus-Stimulus Congruency': ['N/A'],
        'Stimulus-Response Congruency': ['N/A'],
        # Fill in other required columns to avoid unrelated errors
        'Task 2 Response Probability': ['0.0'], 'Inter-task SOA': ['N/A'], 'Switch Rate': ['0'],
        'Response Set Overlap': ['N/A'], 'Task 1 Stimulus-Response Mapping': ['Compatible'],
        'Task 1 Cue Type': ['None/Implicit'], 'Task 1 CSI': ['0'], 'RSI': ['1000'],
        'Task 1 Difficulty': ['1'], 'Task 2 Difficulty': ['N/A'], 'Task 2 CSI': ['N/A'],
        'Task 2 Stimulus-Response Mapping': ['N/A'], 'Task 2 Cue Type': ['N/A'],
        'Trial Transition Type': ['Pure'], 'RSI is Predictable': ['Yes']
    })
    preprocess(invalid_data.copy())
    assert "Warning: Distractor SOA has a value but neither S-S nor S-R congruency is defined" in caplog.text
    caplog.clear()


def test_preprocess_for_pca_with_real_data(real_raw_data):
    """
    Integration test for the PCA preprocessor using real data.
    Ensures the pipeline can handle the structure and values from the actual CSV.
    """
    # For the PCA pipeline, we expect 'N/A' as a string.
    # The fixture reads 'N/A' as a string, so no changes are needed.
    df_test = real_raw_data.copy()

    df_pca_features, _, _, df_processed = preprocess(df_test)

    # Test 1: Check output shape
    # 3 experiments should result in 3 rows
    assert df_pca_features.shape[0] == 3
    assert df_processed.shape[0] == 3

    # Test 2: Check a specific processed value
    # For Stroop, 'Paradigm' should be classified as 'Interference'
    stroop_row = df_processed[df_processed['Experiment'] == 'Stroop 1935 Color Naming']
    assert stroop_row['Paradigm'].iloc[0] == 'Interference'
    
    # Test 3: Check that T2 Difficulty gets the mean placeholder for a non-TS/DT task
    stroop_pca_row = df_pca_features.loc[stroop_row.index]

    t2_difficulty_norm_mean = ((pd.to_numeric(real_raw_data["Task 2 Difficulty"], errors="coerce") - 1) / 4).mean()
    assert t2_difficulty_norm_mean == 0.125
    assert stroop_pca_row['Task 2 Difficulty'].iloc[0] == t2_difficulty_norm_mean

def test_preprocess_for_pca_with_unified_fixture(raw_test_data_dict):
    """
    A comprehensive integration test for the entire PCA preprocessing pipeline,
    using a unified, realistic data fixture.
    
    This test verifies:
    - Correct handling of 'N/A' strings.
    - Proper paradigm classification.
    - Numerical cleaning and normalization.
    - Final structure of the feature matrix for PCA.
    """
    # Create the DataFrame. For the PCA pipeline, 'N/A' must remain a string.
    df_raw = pd.DataFrame(raw_test_data_dict)

    # Run the entire preprocessing pipeline
    df_pca_features, numerical_cols, categorical_cols, df_processed = preprocess(df_raw)

    # --- Test 1: Shape and Integrity ---
    # The output should have one row per input experiment
    assert df_pca_features.shape[0] == 3
    assert df_processed.shape[0] == 3
    # The number of PCA features should be greater than the original number of columns due to one-hot encoding
    assert df_pca_features.shape[1] > len(df_raw.columns)

    # --- Test 2: Paradigm Classification (replaces the old test_classify_paradigm) ---
    # Check the 'Paradigm' column added by the preprocessor
    expected_paradigms = {
        "Stroop_Incongruent": "Interference",
        "PRP_Short_SOA": "Dual-Task_PRP",
        "TS_Switch_Incompatible": "Task Switching"
    }
    for exp, paradigm in expected_paradigms.items():
        assert df_processed.loc[df_processed['Experiment'] == exp, 'Paradigm'].iloc[0] == paradigm

    # --- Test 3: Numerical Cleaning and Transformation ---
    # Retrieve the processed row for the Task Switching experiment
    ts_row_processed = df_processed[df_processed['Experiment'] == 'TS_Switch_Incompatible']
    ts_row_pca_features = df_pca_features.loc[ts_row_processed.index]

    # Check Switch Rate cleaning ('50%' -> 50.0)
    assert ts_row_processed['Switch Rate'].iloc[0] == 50.0
    
    # Check RSI cleaning ('Varied (choice: 600, 1600)' -> 1100.0)
    assert ts_row_processed['RSI'].iloc[0] == 1100.0

    # Check Task Difficulty normalization (3 -> (3-1)/4 -> 0.5)
    assert ts_row_pca_features['Task 1 Difficulty'].iloc[0] == 0.5

    # --- Test 4: Handling of 'N/A' and Placeholders ---
    # For Stroop, T2-related features should be handled correctly
    stroop_row_processed = df_processed[df_processed['Experiment'] == 'Stroop_Incongruent']
    stroop_row_pca_features = df_pca_features.loc[stroop_row_processed.index]

    # Task 2 Difficulty should be imputed with the mean difficulty placeholder for a "true single task"
    t2_difficulty_norm_mean = ((pd.to_numeric(df_raw["Task 2 Difficulty"], errors="coerce") - 1) / 4).mean()
    assert t2_difficulty_norm_mean == 0.375
    assert stroop_row_pca_features['Task 2 Difficulty'].iloc[0] == t2_difficulty_norm_mean
    
    # Inter-task SOA should be flagged as N/A and its value imputed to the median
    assert stroop_row_pca_features['Inter_task_SOA_is_NA'].iloc[0] == 1
    inter_task_soa_median = pd.to_numeric(df_raw["Inter-task SOA"], errors="coerce").median()
    assert inter_task_soa_median == 100
    assert stroop_row_pca_features['Inter-task SOA'].iloc[0] == inter_task_soa_median

    # --- Test 5: Categorical One-Hot Encoding ---
    # Check the mapped column for 'Trial Transition Type'
    ttt_column = df_pca_features['Trial Transition Type_Mapped']

    # The first two experiments (Stroop, PRP) are 'Pure'
    assert ttt_column.iloc[0] == 'TTT_Pure'
    assert ttt_column.iloc[1] == 'TTT_Pure'
    # The third experiment (Task Switching) is 'Switch'
    assert ttt_column.iloc[2] == 'TTT_Switch'

    # Check the mapped column for 'Response_Set_Overlap'
    rso_column = df_pca_features['Response_Set_Overlap_Mapped']

    # Stroop is N/A
    assert rso_column.iloc[0] == 'RSO_NA'
    # PRP is Disjoint
    assert rso_column.iloc[1] == 'RSO_Disjoint'
    # Task Switching is Identical
    assert rso_column.iloc[2] == 'RSO_Identical'
