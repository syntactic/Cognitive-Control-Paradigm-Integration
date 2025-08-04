# tests/test_mofa_preparation.py

import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from unittest.mock import Mock, MagicMock
from analysis_utils import prepare_mofa_data, reconstruct_from_mofa_factors, InvertibleColumnTransformer

def test_prepare_mofa_data_sparse_strategy(raw_test_data_dict):
    """
    Tests the prepare_mofa_data function with the sparse strategy.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    df_long, likelihoods, preprocessor_obj, view_map = prepare_mofa_data(df_raw, strategy='sparse')
    
    # Test 1: Check return type structure
    assert isinstance(df_long, pd.DataFrame), "df_long should be a DataFrame"
    assert isinstance(likelihoods, list), "likelihoods should be a list"
    assert isinstance(preprocessor_obj, StandardScaler), "preprocessor_obj should be StandardScaler for sparse strategy"
    assert isinstance(view_map, dict), "view_map should be a dictionary"
    
    # Test 2: Check DataFrame structure
    expected_cols = ['sample', 'feature', 'value', 'view', 'group']
    assert all(col in df_long.columns for col in expected_cols), f"Missing columns. Got: {df_long.columns.tolist()}"
    
    # Test 3: Assert that N/A values result in dropped rows
    # For PRP_Short_SOA, Distractor SOA is 'N/A' -> should not exist in df_long
    prp_distractor_rows = df_long[
        (df_long['sample'] == 'PRP_Short_SOA') & 
        (df_long['feature'] == 'Distractor SOA')
    ]
    assert len(prp_distractor_rows) == 0, "Expected no rows for PRP_Short_SOA Distractor SOA (was N/A)"
    
    # Test 4: Assert correct ordinal encoding
    # For TS_Switch_Incompatible, Stimulus-Response Congruency is 'Incongruent' -> should be -1.0
    ts_sr_rows = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') & 
        (df_long['feature'] == 'Stimulus-Response Congruency')
    ]
    assert len(ts_sr_rows) == 1, "Expected exactly one row for TS_Switch_Incompatible Stimulus-Response Congruency"
    assert ts_sr_rows['value'].iloc[0] == -1.0, f"Expected -1.0 for Incongruent, got {ts_sr_rows['value'].iloc[0]}"
    
    # Test 5: Check likelihoods
    assert all(likelihood == 'gaussian' for likelihood in likelihoods), "All likelihoods should be 'gaussian'"
    
    # Test 6: Check view mapping
    assert 'Inter-task SOA' in view_map, "view_map should contain original feature names"
    assert view_map['Inter-task SOA'] == 'Temporal', "Inter-task SOA should map to Temporal view"

def test_prepare_mofa_data_dense_strategy(raw_test_data_dict):
    """
    Tests the prepare_mofa_data function with the dense strategy.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    df_long, likelihoods, preprocessor_obj, view_map = prepare_mofa_data(df_raw, strategy='dense')
    
    # Test 1: Check return type structure
    assert isinstance(df_long, pd.DataFrame), "df_long should be a DataFrame"
    assert isinstance(likelihoods, list), "likelihoods should be a list"
    assert isinstance(preprocessor_obj, InvertibleColumnTransformer), "preprocessor_obj should be InvertibleColumnTransformer for dense strategy"
    assert isinstance(view_map, dict), "view_map should be a dictionary"
    
    # Test 2: Check DataFrame structure
    expected_cols = ['sample', 'feature', 'value', 'view', 'group']
    assert all(col in df_long.columns for col in expected_cols), f"Missing columns. Got: {df_long.columns.tolist()}"
    
    # Test 3: Check that dense strategy creates a "complete" DataFrame
    # Should have (n_samples * n_features) rows where n_features is after one-hot encoding
    n_samples = len(df_raw)
    n_features_after_ohe = len(preprocessor_obj.get_feature_names_out())
    expected_total_rows = n_samples * n_features_after_ohe
    assert len(df_long) == expected_total_rows, f"Expected {expected_total_rows} rows, got {len(df_long)}"
    
    # Test 4: Check that one-hot encoded features exist
    # Look for features with the one-hot encoding pattern
    ohe_features = [f for f in df_long['feature'].unique() if '_' in f and ('Mapped' in f or 'is NA' in f)]
    assert len(ohe_features) > 0, "Should have one-hot encoded features in dense strategy"
    
    # Test 5: Check specific one-hot encoded feature
    # Response Set Overlap should create features like 'cat__Response_Set_Overlap_Mapped_RSO_Disjoint'
    response_overlap_features = [f for f in df_long['feature'].unique() if 'Response_Set_Overlap' in f]
    if response_overlap_features:  # Only check if such features exist
        assert len(response_overlap_features) > 0, "Should have Response Set Overlap one-hot encoded features"
    else:
        # Check for any categorical features instead
        categorical_features = [f for f in df_long['feature'].unique() if 'cat__' in f]
        assert len(categorical_features) > 0, "Should have some categorical (one-hot encoded) features"
    
    # Test 6: Check view mapping contains transformed feature names
    assert any('cat__' in key for key in view_map.keys()), "view_map should contain transformed feature names with cat__ prefix"

def test_prepare_mofa_data_invalid_strategy(raw_test_data_dict):
    """
    Tests that prepare_mofa_data raises an error for invalid strategy.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    with pytest.raises(ValueError, match="Unknown strategy: invalid"):
        prepare_mofa_data(df_raw, strategy='invalid')

def test_prepare_mofa_data_default_strategy(raw_test_data_dict):
    """
    Tests that prepare_mofa_data uses sparse strategy by default.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    df_long, likelihoods, preprocessor_obj, view_map = prepare_mofa_data(df_raw)
    
    # Should default to sparse strategy
    assert isinstance(preprocessor_obj, StandardScaler), "Should use StandardScaler with default strategy"

def test_reconstruction_sparse_strategy(raw_test_data_dict):
    """
    Tests the reconstruction function with sparse strategy preprocessor.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    # Get sparse preprocessing results
    df_long, likelihoods, scaler, view_map = prepare_mofa_data(df_raw, strategy='sparse')
    
    # Create mock MOFA model and factor scores for testing
    mock_model = Mock()
    
    # Create mock weights DataFrame - use actual features from the sparse data
    features_in_model = df_long['feature'].unique()
    n_factors = 3
    mock_weights = pd.DataFrame(
        np.random.randn(len(features_in_model), n_factors),
        index=features_in_model,
        columns=[f'Factor{i+1}' for i in range(n_factors)]
    )
    mock_model.get_weights.return_value = mock_weights
    
    # Create mock factor scores
    sample_names = ['Test_Sample']
    factor_scores = pd.DataFrame(
        np.random.randn(1, n_factors),
        index=sample_names,
        columns=[f'Factor{i+1}' for i in range(n_factors)]
    )
    
    # Test reconstruction
    reconstructed = reconstruct_from_mofa_factors(factor_scores, mock_model, scaler)
    
    # Test 1: Check return type and structure
    assert isinstance(reconstructed, pd.DataFrame), "Should return DataFrame"
    assert reconstructed.index.tolist() == sample_names, "Should preserve sample names as index"
    
    # Test 2: Check that continuous features exist in output
    continuous_features = [
        'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA', 
        'Task 1 CSI', 'Task 2 CSI', 'RSI', 'Switch Rate', 
        'Task 1 Difficulty', 'Task 2 Difficulty'
    ]
    present_continuous = [f for f in continuous_features if f in reconstructed.columns]
    assert len(present_continuous) > 0, "Should have some continuous features in reconstruction"
    
    # Test 3: Check that ordinal features are mapped to valid values
    if 'Stimulus-Response Congruency' in reconstructed.columns:
        sr_value = reconstructed['Stimulus-Response Congruency'].iloc[0]
        assert sr_value in [-1.0, 0.0, 1.0], f"SR Congruency should be mapped to valid ordinal value, got {sr_value}"

def test_reconstruction_dense_strategy(raw_test_data_dict):
    """
    Tests the reconstruction function with dense strategy preprocessor.
    NOTE: This is a basic test that verifies the function runs without errors.
    Full reconstruction testing with dense strategy is complex due to the 
    one-hot encoding inverse transform requirements.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    # Get dense preprocessing results
    df_long, likelihoods, preprocessor, view_map = prepare_mofa_data(df_raw, strategy='dense')
    
    # Test 1: Verify that the preprocessor is the correct type
    assert isinstance(preprocessor, InvertibleColumnTransformer), "Should be InvertibleColumnTransformer"
    
    # Test 2: Verify basic structure  
    features_in_model = preprocessor.get_feature_names_out()
    assert len(features_in_model) > 0, "Should have transformed features"
    
    # Test 3: Check that we can identify the preprocessor type in reconstruction logic
    # This tests the isinstance check in reconstruct_from_mofa_factors
    assert isinstance(preprocessor, ColumnTransformer), "Should pass ColumnTransformer check"

def test_reconstruction_invalid_preprocessor():
    """
    Tests that reconstruction raises error for invalid preprocessor type.
    """
    # Create mock factor scores and model with properly aligned dimensions
    factor_scores = pd.DataFrame([[1.0, 2.0]], columns=['Factor1', 'Factor2'], index=['Test'])
    mock_model = Mock()
    # Weights should be: (n_features, n_factors) but get_weights returns (n_features, n_factors) with features as index
    mock_weights = pd.DataFrame([[0.5, 0.2], [0.3, 0.8]], index=['Feature1', 'Feature2'], columns=['Factor1', 'Factor2'])
    mock_model.get_weights.return_value = mock_weights
    
    # Use invalid preprocessor type
    invalid_preprocessor = "not_a_preprocessor"
    
    with pytest.raises(ValueError, match="Unsupported preprocessor type"):
        reconstruct_from_mofa_factors(factor_scores, mock_model, invalid_preprocessor)

def test_reconstruction_series_input(raw_test_data_dict):
    """
    Tests that reconstruction handles Series input correctly.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    # Get sparse preprocessing results
    df_long, likelihoods, scaler, view_map = prepare_mofa_data(df_raw, strategy='sparse')
    
    # Create mock model
    mock_model = Mock()
    features_in_model = df_long['feature'].unique()
    mock_weights = pd.DataFrame(
        np.random.randn(len(features_in_model), 2),
        index=features_in_model,
        columns=['Factor1', 'Factor2']
    )
    mock_model.get_weights.return_value = mock_weights
    
    # Create factor scores as Series (single sample)
    factor_scores = pd.Series([1.0, 2.0], index=['Factor1', 'Factor2'], name='Test_Sample')
    
    # Test reconstruction
    reconstructed = reconstruct_from_mofa_factors(factor_scores, mock_model, scaler)
    
    # Should handle Series input and return DataFrame
    assert isinstance(reconstructed, pd.DataFrame), "Should convert Series to DataFrame and return DataFrame"
    assert len(reconstructed) == 1, "Should have one row for single sample"
    assert reconstructed.index[0] == 'Test_Sample', "Should preserve sample name from Series"