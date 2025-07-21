import pytest
import pandas as pd
import numpy as np
import logging
from analysis_utils import (
    preprocess_for_pca,
    create_pca_pipeline,
    find_centroids,
    interpolate_centroids,
    inverse_transform_point,
    get_component_loadings,
    map_ss_congruency,
    map_sr_congruency,
    classify_paradigm
)

# Fixture for test data with the new schema
@pytest.fixture
def new_sample_data():
    return pd.DataFrame({
        'Task 2 Response Probability': ['0.0', '1.0', '0.0', '0.0', '0.0'],
        'Inter-task SOA': ['N/A', '150', 'N/A', 'N/A', 'N/A'],
        'Distractor SOA': ['N/A', 'N/A', 'N/A', 'N/A', '0'],
        'Switch Rate': ['0', '0', '50', '0', '0'],
        'Stimulus-Stimulus Congruency': ['N/A', 'N/A', 'Neutral', 'N/A', 'Incongruent'],
        'Stimulus-Response Congruency': ['N/A', 'N/A', 'N/A', 'Incongruent', 'N/A'],
        'Response Set Overlap': ['N/A', 'Identical', 'Disjoint', 'N/A', 'N/A'],
        'Task 1 Stimulus-Response Mapping': ['Compatible', 'Arbitrary', 'Compatible', 'Arbitrary', 'Compatible'],
        'Task 1 Cue Type': ['None/Implicit', 'Arbitrary (Symbolic)', 'Arbitrary (Symbolic)', 'None/Implicit', 'None/Implicit'],
        'Task 1 CSI': ['0', '50', '200', '0', '0'],
        'RSI': ['1000', '1000', '650', '1200', '1200'],
        'Task 1 Difficulty': ['2', '3', '2', '2', '3'],
        'Task 2 Difficulty': ['N/A', '3', 'N/A', 'N/A', 'N/A'],
        'Task 2 CSI': ['N/A', '50', 'N/A', 'N/A', 'N/A'],
        'Task 2 Stimulus-Response Mapping': ['N/A', 'Compatible', 'N/A', 'N/A', 'N/A'],
        'Task 2 Cue Type': ['N/A', 'Arbitrary (Symbolic)', 'N/A', 'N/A', 'N/A'],
        'Trial Transition Type': ['Pure', 'Pure', 'Switch', 'Pure', 'Pure'],
        'RSI Is Predictable': ['Yes', 'Yes', 'No', 'Yes', 'Yes'],
    })

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

"""def test_classify_paradigm(new_sample_data):
    # Clean the data first as classify_paradigm runs on processed data
    df = new_sample_data.copy()
    df['Task 2 Response Probability'] = pd.to_numeric(df['Task 2 Response Probability'])
    df['Switch Rate'] = df['Switch Rate'].apply(lambda x: float(str(x).replace('%','')))

    # Row 0: Single-Task (no conflict)
    assert classify_paradigm(df.iloc[0]) == 'Single-Task'
    # Row 1: Dual-Task/PRP
    assert classify_paradigm(df.iloc[1]) == 'Dual-Task/PRP'
    # Row 2: Task Switching
    assert classify_paradigm(df.iloc[2]) == 'Task Switching'
    # Row 3: Interference (S-R Conflict)
    assert classify_paradigm(df.iloc[3]) == 'Interference'
    # Row 4: Interference (S-S Conflict)
    assert classify_paradigm(df.iloc[4]) == 'Interference'"""

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
        'Trial Transition Type': ['Pure'], 'RSI Is Predictable': ['Yes']
    })
    preprocess_for_pca(invalid_data.copy())
    assert "Warning: Distractor SOA has a value but neither S-S nor S-R congruency is defined" in caplog.text
    caplog.clear()


"""# Comprehensive integration test for preprocess_for_pca
def test_preprocess_for_pca_integration(new_sample_data):
    df_pca_features, num_cols, cat_cols, df_processed = preprocess_for_pca(new_sample_data)

    # --- Assertions for column lists ---
    assert 'Stimulus_Stimulus_Congruency_Mapped' in cat_cols
    assert 'Stimulus_Response_Congruency_Mapped' in cat_cols
    assert 'Stimulus_Valency_Mapped' not in cat_cols

    # --- Assertions for correct processing in df_processed ---
    expected_paradigms = ['Single-Task', 'Dual-Task/PRP', 'Task Switching', 'Interference', 'Interference']
    assert df_processed['Paradigm'].tolist() == expected_paradigms

    expected_ss_mapped = ['SS_NA', 'SS_NA', 'SS_Neutral', 'SS_NA', 'SS_Incongruent']
    assert df_processed['Stimulus_Stimulus_Congruency_Mapped'].tolist() == expected_ss_mapped

    expected_sr_mapped = ['SR_NA', 'SR_NA', 'SR_NA', 'SR_Incongruent', 'SR_NA']
    assert df_processed['Stimulus_Response_Congruency_Mapped'].tolist() == expected_sr_mapped

    # --- Assertions for the final PCA features DataFrame ---
    assert 'Stimulus_Stimulus_Congruency_Mapped' in df_pca_features.columns
    assert 'Stimulus_Response_Congruency_Mapped' in df_pca_features.columns
    assert 'Stimulus_Valency_Mapped' not in df_pca_features.columns

    # Check shape
    assert df_pca_features.shape[0] == 5 # 5 rows
    assert len(num_cols) + len(cat_cols) == df_pca_features.shape[1]"""

def test_preprocess_for_pca_with_real_data(real_raw_data):
    """
    Integration test for the PCA preprocessor using real data.
    Ensures the pipeline can handle the structure and values from the actual CSV.
    """
    # For the PCA pipeline, we expect 'N/A' as a string.
    # The fixture reads 'N/A' as a string, so no changes are needed.
    df_test = real_raw_data.copy()

    df_pca_features, _, _, df_processed = preprocess_for_pca(df_test)

    # Test 1: Check output shape
    # 3 experiments should result in 3 rows
    assert df_pca_features.shape[0] == 3
    assert df_processed.shape[0] == 3

    # Test 2: Check a specific processed value
    # For Stroop, 'Paradigm' should be classified as 'Interference'
    stroop_row = df_processed[df_processed['Experiment'] == 'Stroop 1935 Color Naming']
    assert stroop_row['Paradigm'].iloc[0] == 'Interference'
    
    # Test 3: Check that T2 Difficulty gets the -1 placeholder for a non-TS/DT task
    stroop_pca_row = df_pca_features.loc[stroop_row.index]
    assert stroop_pca_row['Task 2 Difficulty'].iloc[0] == -1.0

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
    df_pca_features, numerical_cols, categorical_cols, df_processed = preprocess_for_pca(df_raw)

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
        "PRP_Short_SOA": "Dual-Task/PRP",
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

    # Task 2 Difficulty should be imputed with the -1.0 placeholder for a "true single task"
    assert stroop_row_pca_features['Task 2 Difficulty'].iloc[0] == -1.0
    
    # Inter-task SOA should be flagged as N/A and its value imputed to 0
    assert stroop_row_pca_features['Inter_task_SOA_is_NA'].iloc[0] == 1
    assert stroop_row_pca_features['Inter-task SOA'].iloc[0] == 0

    # --- Test 5: Categorical One-Hot Encoding ---
    # Check the mapped column for 'Trial_Transition_Type'
    ttt_column = df_pca_features['Trial_Transition_Type_Mapped']

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
