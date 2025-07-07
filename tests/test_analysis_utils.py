import pytest
import pandas as pd
import numpy as np
from analysis_utils import (
    clean_rsi,
    clean_switch_rate,
    classify_paradigm,
    map_valency,
    map_rso,
    map_srm,
    map_tct,
    preprocess_for_pca,
    create_pca_pipeline,
    find_centroids,
    interpolate_centroids,
    inverse_transform_point,
    get_component_loadings
)

# Fixtures for test data with the new schema
@pytest.fixture
def new_sample_data():
    """
    A fixture representing the new data schema with various paradigm types,
    using strings to mimic raw CSV data.
    - Row 0: Univalent single-task (e.g., simple RT). No SOAs apply.
    - Row 1: Bivalent single-task (e.g., Stroop). Only Distractor SOA applies.
    - Row 2: Dual-task (e.g., PRP). Only Inter-task SOA applies.
    - Row 3: Dual-task with a distractor (theoretical). Both SOAs apply.
    - Row 4: Task-switching paradigm.
    """
    return pd.DataFrame({
        'Task 2 Response Probability': ['0.0', '0.0', '1.0', '1.0', '0.0'],
        'Inter-task SOA': ['N/A', 'N/A', '150', '200', 'N/A'],
        'Distractor SOA': ['N/A', '50', 'N/A', '75', 'N/A'],
        'Stimulus Valency': ['Univalent', 'Bivalent', 'Univalent', 'Bivalent', 'Univalent'],
        'Switch Rate': ['0', '0', '0', '0', '50'],
        'Response Set Overlap': ['N/A', 'N/A', 'Identical', 'Disjoint', 'Identical'],
        'Stimulus Response Mapping': ['Compatible', 'Incompatible', 'Compatible', 'Arbitrary', 'Compatible'],
        'Task Cue Type': ['None/Implicit', 'None/Implicit', 'None/Implicit', 'Arbitrary (Symbolic)', 'Arbitrary (Symbolic)'],
        'CSI': ['0', '50', '0', '50', '200'],
        'RSI': ['1000', '1000', '1000', '1000', '1000'],
        'Task 1 Difficulty': ['1', '4', '2', '3', '2'],
        'Task 2 Difficulty': ['N/A', 'N/A', '2', '4', '2']
    })

# Tests for classify_paradigm with new logic
def test_classify_paradigm_new():
    # Manually create a sample for this specific test
    test_df = pd.DataFrame({
        'Task 2 Response Probability': [1.0, 0.0, 0.0, 0.5, 0.0],
        'Switch Rate': [0, 0, 0, 0, 50],
        'Stimulus Valency': ['Univalent', 'Univalent', 'Bivalent', 'Univalent', 'Univalent']
    })
    paradigms = test_df.apply(classify_paradigm, axis=1)
    assert paradigms.tolist() == ['Dual-Task/PRP', 'Other', 'Interference', 'Other', 'Task Switching']

# Comprehensive integration test for preprocess_for_pca
def test_preprocess_for_pca_integration(new_sample_data):
    df_pca, num_cols, cat_cols, df_processed = preprocess_for_pca(new_sample_data)

    # 1. Assert correct generation of _is_NA flags, including the new task-switching row
    assert df_processed['Inter_task_SOA_is_NA'].tolist() == [1, 1, 0, 0, 1]
    assert df_processed['Distractor_SOA_is_NA'].tolist() == [1, 0, 1, 0, 1]

    # 2. Assert correct imputation of main SOA columns to 0
    assert not df_processed['Inter-task SOA'].hasnans
    assert not df_processed['Distractor SOA'].hasnans
    assert df_processed.loc[0, 'Inter-task SOA'] == 0
    assert df_processed.loc[1, 'Distractor SOA'] == 50 # This one was not NaN

    # 3. Assert correct paradigm classification
    assert df_processed['Paradigm'].tolist() == ['Other', 'Interference', 'Dual-Task/PRP', 'Dual-Task/PRP', 'Task Switching']

# New tests for PCA analysis helper functions
def test_find_centroids():
    pc_data = pd.DataFrame({
        'PC1': [1, 2, 8, 9],
        'PC2': [1, 1, 8, 8],
        'Paradigm': ['A', 'A', 'B', 'B']
    })
    centroids = find_centroids(pc_data)
    assert 'A' in centroids
    assert 'B' in centroids
    assert np.allclose(centroids['A']['PC1'], 1.5)
    assert np.allclose(centroids['A']['PC2'], 1.0)
    assert np.allclose(centroids['B']['PC1'], 8.5)
    assert np.allclose(centroids['B']['PC2'], 8.0)

def test_interpolate_centroids():
    c1 = {'x': 0, 'y': 0}
    c2 = {'x': 10, 'y': 20}
    
    # Test halfway point
    halfway = interpolate_centroids(c1, c2, alpha=0.5)
    assert np.allclose(halfway, [5, 10])
    
    # Test endpoint
    at_c2 = interpolate_centroids(c1, c2, alpha=1.0)
    assert np.allclose(at_c2, [10, 20])

def test_get_component_loadings(new_sample_data):
    df_pca_features, numerical_cols, categorical_cols, _ = preprocess_for_pca(new_sample_data)
    pipeline = create_pca_pipeline(numerical_cols, categorical_cols)
    pipeline.fit(df_pca_features)
    
    loadings = get_component_loadings(pipeline, numerical_cols, categorical_cols)
    
    # Assert that the output is a DataFrame
    assert isinstance(loadings, pd.DataFrame)
    
    # Assert that the index contains the original feature names
    assert 'Inter-task SOA' in loadings.index
    # Assert that the index contains a one-hot encoded feature.
    assert 'Stimulus_Valency_Mapped_SBC_Univalent' in loadings.index
    
    # Assert that columns are named PC1, PC2, etc.
    assert all(f'PC{i+1}' in loadings.columns for i in range(pipeline.named_steps['pca'].n_components_))


# New test for pipeline invertibility and interpolation
# def test_pipeline_invertibility_and_interpolation(new_sample_data):
#     # --- Part A: Invertibility ---
#     df_pca_features, numerical_cols, categorical_cols, df_processed = preprocess_for_pca(new_sample_data)
    
#     pipeline = create_pca_pipeline(numerical_cols, categorical_cols)
#     pipeline.fit(df_pca_features)
    
#     # Transform to PC space and back
#     pc_space = pipeline.transform(df_pca_features)
#     reconstructed_space = pipeline.inverse_transform(pc_space)
    
#     # Create DataFrames to compare
#     df_reconstructed = pd.DataFrame(reconstructed_space, columns=df_pca_features.columns)
    
#     # Check that the numerical data is close (allowing for float precision errors)
#     assert np.allclose(df_pca_features[numerical_cols], df_reconstructed[numerical_cols])
    
#     # --- Part B: Interpolation ---
#     # Add PC components and Paradigm labels to a new DataFrame for analysis
#     df_pc_results = pd.DataFrame(pc_space, columns=[f'PC{i+1}' for i in range(pc_space.shape[1])])
#     df_pc_results['Paradigm'] = df_processed['Paradigm']
    
#     # Calculate centroids for the two most different paradigms in the sample
#     centroids = find_centroids(df_pc_results, paradigm_col='Paradigm')
#     centroid_dt = centroids.get('Dual-Task/PRP')
#     centroid_int = centroids.get('Interference')
    
#     assert centroid_dt is not None, "Dual-Task/PRP centroid not found"
#     assert centroid_int is not None, "Interference centroid not found"

#     # Interpolate a point halfway between them
#     interpolated_pc_point = interpolate_centroids(centroid_dt, centroid_int, alpha=0.5)
    
#     # Inverse-transform the point back to the original feature space
#     final_params = inverse_transform_point(interpolated_pc_point, pipeline)
    
#     # Assert that the resulting values are sensible
#     # It should be halfway between a single task (T2RP=0) and a dual task (T2RP=1)
#     assert 0.4 < final_params['Task 2 Response Probability'] < 0.6
    
#     # It's halfway between a state where Inter-task SOA is NOT applicable (1) and IS applicable (0)
#     assert 0.4 < final_params['Inter_task_SOA_is_NA'] < 0.6
    
#     # It's halfway between a state where Distractor SOA IS applicable (0) and NOT applicable (1)
#     assert 0.4 < final_params['Distractor_SOA_is_NA'] < 0.6

# Keep old tests for basic helpers to ensure no regressions
def test_clean_rsi_numeric():
    assert clean_rsi(200) == 200.0
def test_map_valency():
    assert map_valency('Univalent') == 'SBC_Univalent'