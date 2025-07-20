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

def test_classify_paradigm(new_sample_data):
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
    assert classify_paradigm(df.iloc[4]) == 'Interference'

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


# Comprehensive integration test for preprocess_for_pca
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
    assert len(num_cols) + len(cat_cols) == df_pca_features.shape[1]

