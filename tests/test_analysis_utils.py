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
    get_component_loadings
)

# Fixture for test data with the new schema
@pytest.fixture
def new_sample_data():
    """
    A fixture representing the new data schema with various paradigm types,
    using strings to mimic raw CSV data.
    - Row 0: Univalent single-task (e.g., simple RT).
    - Row 1: Dual-task, compatible mappings.
    - Row 2: Task-switching, incompatible mappings.
    - Row 3: Univalent single-task, different RSI.
    """
    return pd.DataFrame({
        # --- Existing Columns ---
        'Task 2 Response Probability': ['0.0', '1.0', '0.0', '0.0'],
        'Inter-task SOA': ['N/A', '150', 'N/A', 'N/A'],
        'Distractor SOA': ['N/A', 'N/A', 'N/A', 'N/A'],
        'Stimulus Valency': ['Univalent', 'Univalent', 'Univalent', 'Univalent'],
        'Switch Rate': ['0', '0', '50', '0'],
        'Response Set Overlap': ['N/A', 'Identical', 'Disjoint', 'N/A'],
        'Stimulus Response Mapping': ['Compatible', 'Arbitrary', 'Compatible', 'Incompatible'], # This is now T1 SRM
        'Task Cue Type': ['None/Implicit', 'Arbitrary (Symbolic)', 'Arbitrary (Symbolic)', 'None/Implicit'], # This is now T1 Cue Type
        'CSI': ['0', '50', '200', '0'], # This is now T1 CSI
        'RSI': ['1000', '1000', '650', '2000'],
        'Task 1 Difficulty': ['2', '3', '2', '4'],
        'Task 2 Difficulty': ['N/A', '3', 'N/A', 'N/A'],

        # --- Add NEW Columns ---
        'Task 2 CSI': ['N/A', '50', 'N/A', 'N/A'],
        'Task 2 Stimulus-Response Mapping': ['N/A', 'Compatible', 'N/A', 'N/A'],
        'Task 2 Cue Type': ['N/A', 'Arbitrary (Symbolic)', 'N/A', 'N/A'],
        'Trial Transition Type': ['Pure', 'Pure', 'Switch', 'Pure'],
        'RSI Is Predictable': ['Yes', 'Yes', 'No', 'Yes'],
    })

def test_data_validation_logging(caplog):
    """
    Tests that the new validation function logs appropriate warnings for
    inconsistent data.
    """
    caplog.set_level(logging.WARNING)

    # Test Case 1: T2 info present when it shouldn't be (T2RP=0)
    invalid_data_1 = pd.DataFrame({
        'Experiment Name': ['TestExp1'],
        'Task 2 Response Probability': [0.0],
        'Task 2 Difficulty': [3], # Should be N/A
        'Task 2 CSI': [50], # Should be N/A
        'Task 2 Stimulus-Response Mapping': ['Compatible'], # Should be N/A
        'Task 2 Cue Type': ['Arbitrary (Symbolic)'], # Should be N/A
        # Fill in other required columns to avoid unrelated errors
        'Inter-task SOA': ['N/A'], 'Distractor SOA': ['N/A'], 'Stimulus Valency': ['Univalent'],
        'Switch Rate': [0], 'Response Set Overlap': ['N/A'], 'Stimulus Response Mapping': ['Compatible'],
        'Task Cue Type': ['None/Implicit'], 'CSI': [0], 'RSI': [1000], 'Task 1 Difficulty': [1],
        'Trial Transition Type': ['Pure'], 'RSI Is Predictable': ['Yes']
    })
    preprocess_for_pca(invalid_data_1.copy())
    assert "Warning: Task 2 Difficulty is present for a single-task condition" in caplog.text
    assert "Warning: Task 2 CSI is present for a single-task condition" in caplog.text
    assert "Warning: Task 2 Stimulus-Response Mapping is present for a single-task condition" in caplog.text
    assert "Warning: Task 2 Cue Type is present for a single-task condition" in caplog.text
    caplog.clear()

    # Test Case 2: Switch Rate is 0% for a Switch trial
    invalid_data_2 = pd.DataFrame({
        'Experiment Name': ['TestExp2'],
        'Trial Transition Type': ['Switch'],
        'Switch Rate': [0], # Should be > 0
        # Fill in other required columns
        'Task 2 Response Probability': [0.0], 'Task 2 Difficulty': ['N/A'], 'Task 2 CSI': ['N/A'],
        'Task 2 Stimulus-Response Mapping': ['N/A'], 'Task 2 Cue Type': ['N/A'], 'Inter-task SOA': ['N/A'],
        'Distractor SOA': ['N/A'], 'Stimulus Valency': ['Univalent'], 'Response Set Overlap': ['Identical'],
        'Stimulus Response Mapping': ['Compatible'], 'Task Cue Type': ['Arbitrary (Symbolic)'],
        'CSI': [200], 'RSI': [1000], 'Task 1 Difficulty': [2], 'RSI Is Predictable': ['No']
    })
    preprocess_for_pca(invalid_data_2.copy())
    assert "Warning: Trial Transition is 'Switch' or 'Repeat' but Switch Rate is 0%" in caplog.text
    caplog.clear()


# Comprehensive integration test for preprocess_for_pca
def test_preprocess_for_pca_integration(new_sample_data):
    df_pca_features, num_cols, cat_cols, df_processed = preprocess_for_pca(new_sample_data)

    # Create and fit the pipeline to access the fitted preprocessor
    pipeline = create_pca_pipeline(num_cols, cat_cols)
    pipeline.fit(df_pca_features)

    # Get the preprocessor and the correct one-hot encoded feature names
    preprocessor = pipeline.named_steps['preprocessor']
    ohe_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols)
    all_feature_names = num_cols + list(ohe_feature_names)

    # Transform the data using ONLY the preprocessor to check its output
    preprocessed_data = preprocessor.transform(df_pca_features)
    df_transformed = pd.DataFrame(preprocessed_data, columns=all_feature_names)

    # --- Assertions ---

    # Assert that the new numeric columns are present and correctly processed
    assert 'Task 2 CSI' in num_cols
    assert 'RSI_Is_Predictable' in num_cols
    assert df_processed['Task 2 CSI'].tolist() == [0.0, 50.0, 0.0, 0.0]
    assert df_processed['RSI_Is_Predictable'].tolist() == [1, 1, 0, 1]

    # --- Robust check for Trial Transition Type ---
    # 1. Find all columns generated from the 'Trial_Transition_Type_Mapped' feature.
    ttt_cols = [col for col in df_transformed.columns if col.startswith('Trial_Transition_Type_Mapped_')]
    
    # 2. Assert that exactly one column was created due to drop='if_binary'.
    assert len(ttt_cols) == 1, "Expected exactly one column for the binary TTT feature."
    
    # 3. Get the name of the single column that was kept.
    kept_ttt_col = ttt_cols[0]

    # 4. Verify the values are correct for known trial types.
    # Original data: row 1 is 'Pure', row 2 is 'Switch'.
    # This logic works regardless of which column ('..._Pure' or '..._Switch') was kept.
    if 'Switch' in kept_ttt_col:
        assert df_transformed.loc[2, kept_ttt_col] == 1, "Row 2 (Switch) should be 1 in the 'Switch' column."
        assert df_transformed.loc[1, kept_ttt_col] == 0, "Row 1 (Pure) should be 0 in the 'Switch' column."
    elif 'Pure' in kept_ttt_col:
        assert df_transformed.loc[2, kept_ttt_col] == 0, "Row 2 (Switch) should be 0 in the 'Pure' column."
        assert df_transformed.loc[1, kept_ttt_col] == 1, "Row 1 (Pure) should be 1 in the 'Pure' column."
    else:
        pytest.fail(f"Unexpected TTT column found: {kept_ttt_col}")

    # --- Other Assertions ---
    # Robustly check other potentially binary categorical features
    srm2_cols = [col for col in df_transformed.columns if col.startswith('Task_2_Stimulus-Response_Mapping_Mapped_')]
    assert len(srm2_cols) > 0 # Ensure at least one column was created

    tct2_cols = [col for col in df_transformed.columns if col.startswith('Task_2_Cue_Type_Mapped_')]
    assert len(tct2_cols) > 0 # Ensure at least one column was created

    # Check that the final DataFrame for PCA has the expected shape
    assert df_pca_features.shape[0] == 4 # 4 rows
    assert df_transformed.shape[1] > 15 # Check for a reasonable number of columns

