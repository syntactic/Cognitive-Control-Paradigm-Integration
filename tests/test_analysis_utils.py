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
    classify_paradigm,
    generate_dynamic_view_mapping,
    VIEW_MAPPING_UNIFIED
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
        'Trial Transition Type': ['Pure'], 'RSI is Predictable': ['Yes'],
        'Task 1 Type': ['Color Naming'], 'Task 2 Type': ['N/A'], 'Intra-Trial Task Relationship': ['N/A']
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

    df_pca_features, _, _, df_processed, _ = preprocess(df_test)

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
    df_pca_features, numerical_cols, categorical_cols, df_processed, _ = preprocess(df_raw)

    # --- Test 1: Shape and Integrity ---
    # The output should have one row per input experiment
    assert df_pca_features.shape[0] == 8  # Updated for expanded test data
    assert df_processed.shape[0] == 8
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
    assert t2_difficulty_norm_mean == 0.4  # Updated for expanded test data
    assert stroop_row_pca_features['Task 2 Difficulty'].iloc[0] == t2_difficulty_norm_mean
    
    # Inter-task SOA should be flagged as N/A and its value imputed to the median
    assert stroop_row_pca_features['Inter-task SOA is NA'].iloc[0] == 1
    inter_task_soa_median = pd.to_numeric(df_raw["Inter-task SOA"], errors="coerce").median()
    assert inter_task_soa_median == 200.0  # Updated for expanded test data
    assert stroop_row_pca_features['Inter-task SOA'].iloc[0] == inter_task_soa_median

    # --- Test 5: Categorical One-Hot Encoding ---
    # Check the mapped column for 'Trial Transition Type'
    ttt_column = df_pca_features['Trial Transition Type Mapped']

    # The first two experiments (Stroop, PRP) are 'Pure'
    assert ttt_column.iloc[0] == 'TTT_Pure'
    assert ttt_column.iloc[1] == 'TTT_Pure'
    # The third experiment (Task Switching) is 'Switch'
    assert ttt_column.iloc[2] == 'TTT_Switch'

    # Check the mapped column for 'Response Set Overlap'
    rso_column = df_pca_features['Response Set Overlap Mapped']

    # Stroop is N/A
    assert rso_column.iloc[0] == 'RSO_NA'
    # PRP is Disjoint
    assert rso_column.iloc[1] == 'RSO_Disjoint'
    # Task Switching is Identical
    assert rso_column.iloc[2] == 'RSO_Identical'

def test_preprocess_merge_conflict_dimensions(raw_test_data_dict):
    """
    Tests that the `merge_conflict_dimensions` flag correctly merges the
    two conflict columns into a single 'Stimulus Bivalence & Congruency' column.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    # Run preprocessing with the merge flag set to True
    df_features, _, _, df_processed, _ = preprocess(df_raw, merge_conflict_dimensions=True)

    # --- Assertions ---
    # 1. The original mapped columns should NOT be in the final feature set
    assert 'Stimulus_Stimulus_Congruency_Mapped' not in df_features.columns
    assert 'Stimulus_Response_Congruency_Mapped' not in df_features.columns

    # 2. The new merged column's mapped version SHOULD be in the feature set
    assert 'SBC_Mapped' in df_features.columns

    # 3. Check the values based on the precedence rule
    # Exp 1 (Stroop): S-S is N/A, S-R is Incongruent -> Merged should be Incongruent
    assert df_processed.loc[0, 'Stimulus Bivalence & Congruency'] == 'Incongruent'
    assert df_features.loc[0, 'SBC_Mapped'] == 'Incongruent'

    # Exp 2 (PRP): S-S is N/A, S-R is N/A -> Merged should be N/A
    assert df_processed.loc[1, 'Stimulus Bivalence & Congruency'] == 'N/A'
    assert df_features.loc[1, 'SBC_Mapped'] == 'N/A'

    # Exp 3 (Task Switching): S-S is Neutral, S-R is Incompatible -> Merged should be Incongruent
    assert df_processed.loc[2, 'Stimulus Bivalence & Congruency'] == 'Incongruent'
    assert df_features.loc[2, 'SBC_Mapped'] == 'Incongruent'

def test_generate_dynamic_view_mapping(raw_test_data_dict):
    """
    Tests that the dynamic view mapping function correctly generates the
    feature-to-view dictionary in both standard and merged-conflict modes.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)

    # --- Case 1: Standard (non-merged) ---
    df_features, _, _, _, preprocessor_std = preprocess(df_raw, merge_conflict_dimensions=False)
    preprocessor_std.fit(df_features) # Fit the preprocessor
    
    view_map_std = generate_dynamic_view_mapping(preprocessor_std, VIEW_MAPPING_UNIFIED)

    # Assertions for standard mode - check for keys that should exist based on test data
    # The test data has SS Congruency = 'Neutral' and SR Congruency = 'Incongruent'
    assert 'cat__Stimulus-Stimulus Congruency Mapped_SS_Neutral' in view_map_std
    assert view_map_std['cat__Stimulus-Stimulus Congruency Mapped_SS_Neutral'] == 'Conflict'
    # Check that at least one SR congruency key exists (could be SR_NA or SR_Incongruent)
    sr_keys = [k for k in view_map_std.keys() if 'Stimulus-Response Congruency Mapped' in k]
    assert len(sr_keys) > 0, f"No SR congruency keys found. Available keys: {list(view_map_std.keys())}"
    assert all(view_map_std[k] == 'Conflict' for k in sr_keys), f"SR keys don't map to Conflict: {[(k, view_map_std[k]) for k in sr_keys]}"
    assert 'num__Inter-task SOA' in view_map_std
    assert view_map_std['num__Inter-task SOA'] == 'Temporal'
    # Make sure the merged key is NOT present
    assert 'cat__SBC_Mapped_Congruent' not in view_map_std

    # --- Case 2: Merged Conflict Dimensions ---
    df_features_merged, _, _, _, preprocessor_merged = preprocess(df_raw, merge_conflict_dimensions=True)
    preprocessor_merged.fit(df_features_merged) # Fit the preprocessor

    view_map_merged = generate_dynamic_view_mapping(preprocessor_merged, VIEW_MAPPING_UNIFIED)

    # Assertions for merged mode - check for SBC keys that should exist
    sbc_keys = [k for k in view_map_merged.keys() if 'SBC_Mapped' in k]
    assert len(sbc_keys) > 0, f"No SBC keys found. Available keys: {list(view_map_merged.keys())}"
    assert all(view_map_merged[k] == 'Conflict' for k in sbc_keys), f"SBC keys don't map to Conflict: {[(k, view_map_merged[k]) for k in sbc_keys]}"
    # Make sure the original keys are NOT present
    ss_keys = [k for k in view_map_merged.keys() if 'Stimulus-Stimulus Congruency Mapped' in k]
    sr_keys = [k for k in view_map_merged.keys() if 'Stimulus-Response Congruency Mapped' in k]
    assert len(ss_keys) == 0, f"SS keys should not be present in merged mode: {ss_keys}"
    assert len(sr_keys) == 0, f"SR keys should not be present in merged mode: {sr_keys}"

def test_pca_pipeline_and_inverse_transform(raw_test_data_dict):
    """
    Tests the full PCA pipeline: fitting, transforming, and inverse transforming.
    This ensures that the data can be reconstructed back to its original form,
    which is crucial for the interpolation functionality.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    df_pca_features, numerical_cols, categorical_cols, _, preprocessor = preprocess(df_raw)

    # Create and fit the pipeline
    pipeline = create_pca_pipeline(numerical_cols, categorical_cols)
    
    # Fit the pipeline and transform the data
    pca_result = pipeline.fit_transform(df_pca_features)
    
    # --- Diagnostic Information ---
    # Get the PCA component from the pipeline
    pca_step = pipeline.named_steps['pca']
    explained_variance_ratio = pca_step.explained_variance_ratio_
    cumulative_variance = explained_variance_ratio.cumsum()
    
    print(f"\n=== PCA Diagnostic Information ===")
    print(f"Original features: {df_pca_features.shape[1]}")
    print(f"PCA components: {pca_result.shape[1]}")
    print(f"Explained variance ratio: {explained_variance_ratio}")
    print(f"Cumulative explained variance: {cumulative_variance}")
    print(f"Total variance explained: {cumulative_variance[-1]:.3f}")
    print(f"Dataset size: {df_pca_features.shape[0]} samples")
    print("=====================================\n")
    
    # --- Test 1: PCA Result Shape ---
    # The number of rows should be the same as the input
    assert pca_result.shape[0] == df_pca_features.shape[0]
    # The number of components should be less than or equal to the number of features
    assert pca_result.shape[1] <= df_pca_features.shape[1]

    # --- Test 2: Inverse Transform ---
    # Transform the PCA result back to the original feature space
    reconstructed_features_arr = pipeline.inverse_transform(pca_result)
    reconstructed_features_df = pd.DataFrame(reconstructed_features_arr, columns=df_pca_features.columns, index=df_pca_features.index)

    # The shape should match the pre-PCA feature matrix
    assert reconstructed_features_df.shape == df_pca_features.shape

    # --- Test 3: Reconstruction Accuracy ---
    # Separate numerical and categorical columns for comparison
    original_numeric = df_pca_features[numerical_cols]
    reconstructed_numeric = reconstructed_features_df[numerical_cols].astype(float)
    
    original_categorical = df_pca_features[categorical_cols]
    reconstructed_categorical = reconstructed_features_df[categorical_cols]

    # Compare numerical columns with a tolerance
    np.testing.assert_allclose(original_numeric.values, reconstructed_numeric.values, rtol=1e-5, atol=1e-5)

    # Compare categorical columns (allowing for type conversion during pipeline processing)
    # The PCA inverse transform may not perfectly reconstruct binary indicator columns
    # since they go through dimensionality reduction, so we'll be more lenient with binary indicators
    for col in categorical_cols:
        original_values = original_categorical[col].values
        reconstructed_values = reconstructed_categorical[col].values
        
        # Handle binary columns that may have been converted to float
        if original_categorical[col].dtype == 'int64' and reconstructed_categorical[col].dtype == 'object':
            # Convert reconstructed back to int for comparison
            reconstructed_values = reconstructed_values.astype(float).astype(int)
        elif original_categorical[col].dtype == 'int64' and reconstructed_categorical[col].dtype == 'float64':
            # Round and convert to int
            reconstructed_values = reconstructed_values.round().astype(int)
        
        # With the fixed OneHotEncoder (drop=None), we should expect much better reconstruction
        if (col.endswith(' is NA') or col == 'RSI is Predictable') and original_categorical[col].dtype == 'int64':
            # Binary columns should now reconstruct perfectly or nearly perfectly
            np.testing.assert_array_equal(original_values, reconstructed_values, 
                                        err_msg=f"Binary column {col} values don't match: Original={original_values}, Reconstructed={reconstructed_values}")
        else:
            # All other categorical columns should also reconstruct well
            np.testing.assert_array_equal(original_values, reconstructed_values, 
                                        err_msg=f"Column {col} values don't match")


def test_interpolation_and_reconstruction(raw_test_data_dict):
    """
    Tests the full workflow of finding centroids, interpolating between them,
    and inverse-transforming the result back to a human-readable format.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    df_pca_features, numerical_cols, categorical_cols, df_processed, _ = preprocess(df_raw)

    # Create and fit the pipeline
    pipeline = create_pca_pipeline(numerical_cols, categorical_cols)
    pca_result = pipeline.fit_transform(df_pca_features)
    
    # Add PCA results and paradigm info to a single DataFrame
    pca_df = pd.DataFrame(pca_result, columns=[f'PC{i+1}' for i in range(pca_result.shape[1])])
    pca_df['Paradigm'] = df_processed['Paradigm'].values

    # --- Step 1: Find Centroids ---
    centroids = find_centroids(pca_df)
    assert 'Interference' in centroids
    assert 'Dual-Task_PRP' in centroids

    # --- Step 2: Interpolate ---
    # Interpolate halfway between an Interference task and a Dual-Task
    interpolated_point_pc = interpolate_centroids(
        centroids['Interference'], 
        centroids['Dual-Task_PRP'], 
        alpha=0.5
    )
    assert interpolated_point_pc.shape == (pca_result.shape[1],)

    # --- Step 3: Inverse Transform ---
    reconstructed_params = inverse_transform_point(interpolated_point_pc, pipeline)
    
    # --- Test 4: Check Reconstructed Values ---
    # The reconstructed parameters should be logically between the two source paradigms.
    
    # The original Interference task (Stroop) has T2RP = 0.
    # The original Dual-Task has T2RP = 1.
    # The interpolated point should have a T2RP of ~0.5.
    assert 0.4 < reconstructed_params['Task 2 Response Probability'] < 0.6

    # The original Interference task has Inter-task SOA imputed to the median (200.0).
    # The original Dual-Task has Inter-task SOA ranging from 100-500.
    # The interpolated point should be in a reasonable range.
    assert 100 <= reconstructed_params['Inter-task SOA'] <= 500

    # The original Interference task has Task 2 Difficulty imputed to the mean (0.4 normalized).
    # The original Dual-Task has varying Task 2 Difficulty values (1-4).
    # The interpolated point should be in a reasonable range.
    assert 1.0 <= reconstructed_params['Task 2 Difficulty'] <= 5.0

    # The original Interference task has S-R Congruency = Incongruent.
    # The original Dual-Task has S-R Congruency = N/A.
    # The inverse transform will pick the most likely category. We can't be too
    # strict here, but we can check that it's a valid category.
    assert reconstructed_params['Stimulus-Response Congruency Mapped'] in ['SR_Incongruent', 'SR_NA']



