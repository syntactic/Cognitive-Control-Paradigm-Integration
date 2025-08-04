# tests/test_mofa_utils.py

import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from analysis_utils import prepare_mofa_data

def test_preprocess_for_mofa_with_unified_fixture(raw_test_data_dict):
    """
    Tests the prepare_mofa_data function using the unified test fixture.
    Verifies correct numerical encoding and missing value handling.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    df_long, likelihoods, scaler, view_map = prepare_mofa_data(df_raw, strategy='sparse')

    # --- Test 1: Check the output DataFrame structure ---
    expected_cols = ['sample', 'feature', 'value', 'view', 'group']
    assert all(col in df_long.columns for col in expected_cols), f"Missing columns. Got: {df_long.columns.tolist()}"
    assert len(df_long.columns) == len(expected_cols), f"Extra columns found: {df_long.columns.tolist()}"

    # --- Test 2: Assert correct numerical encoding ---
    # For TS_Switch_Incompatible, Stimulus-Response Congruency is 'Incongruent' -> should be -1.0
    ts_sr_rows = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') & 
        (df_long['feature'] == 'Stimulus-Response Congruency')
    ]
    assert len(ts_sr_rows) == 1, "Expected exactly one row for TS_Switch_Incompatible Stimulus-Response Congruency"
    assert ts_sr_rows['value'].iloc[0] == -1.0, f"Expected -1.0 for Incongruent, got {ts_sr_rows['value'].iloc[0]}"

    # --- Test 3: Assert that N/A values result in dropped rows ---
    # For PRP_Short_SOA, Distractor SOA is 'N/A' -> should not exist in df_long
    prp_distractor_rows = df_long[
        (df_long['sample'] == 'PRP_Short_SOA') & 
        (df_long['feature'] == 'Distractor SOA')
    ]
    assert len(prp_distractor_rows) == 0, "Expected no rows for PRP_Short_SOA Distractor SOA (was N/A)"

    # --- Test 4: Assert that valid values are preserved (standardized) ---
    # For PRP_Short_SOA, Inter-task SOA is 100 -> should exist but be standardized (not 100.0)
    prp_inter_task_rows = df_long[
        (df_long['sample'] == 'PRP_Short_SOA') & 
        (df_long['feature'] == 'Inter-task SOA')
    ]
    assert len(prp_inter_task_rows) == 1, "Expected one row for PRP_Short_SOA Inter-task SOA"
    # The value should be standardized, so it should be a float but not the original 100.0
    standardized_inter_task_value = prp_inter_task_rows['value'].iloc[0]
    assert isinstance(standardized_inter_task_value, (float, np.floating)), "Should be a numeric value"
    assert standardized_inter_task_value != 100.0, f"Should be standardized, not raw value. Got {standardized_inter_task_value}"

    # --- Test 5: Check that string cleaning and standardization worked ---
    # For TS_Switch_Incompatible, Switch Rate is '50%' -> should be cleaned and standardized (not 50.0)
    ts_switch_rate_rows = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') & 
        (df_long['feature'] == 'Switch Rate')
    ]
    assert len(ts_switch_rate_rows) == 1, "Expected one row for TS_Switch_Incompatible Switch Rate"
    # Should be standardized, not the raw cleaned value of 50.0
    standardized_switch_rate = ts_switch_rate_rows['value'].iloc[0]
    assert isinstance(standardized_switch_rate, (float, np.floating)), "Should be a numeric value"
    assert standardized_switch_rate != 50.0, f"Should be standardized, not raw cleaned value. Got {standardized_switch_rate}"

    # --- Test 6: Check categorical mappings ---
    # Trial Transition Type: 'Switch' -> -0.5
    ts_ttt_rows = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') & 
        (df_long['feature'] == 'Trial Transition Type')
    ]
    assert len(ts_ttt_rows) == 1, "Expected one row for TS_Switch_Incompatible Trial Transition Type"
    assert ts_ttt_rows['value'].iloc[0] == -0.5, f"Expected -0.5 for 'Switch', got {ts_ttt_rows['value'].iloc[0]}"

    # --- Test 7: Check likelihoods structure ---
    assert isinstance(likelihoods, list), "Likelihoods should be a list"
    assert all(likelihood == 'gaussian' for likelihood in likelihoods), "All likelihoods should be 'gaussian'"
    assert len(likelihoods) == len(df_long['view'].unique()), "Likelihoods length should match number of unique views"
    
    # --- Test 8: Check scaler is returned and properly fitted ---
    assert isinstance(scaler, StandardScaler), "Should return a fitted StandardScaler"
    assert hasattr(scaler, 'scale_'), "Scaler should be fitted (have scale_ attribute)"
    
    # --- Test 9: Verify standardization occurred ---
    # For PRP_Short_SOA, Inter-task SOA is originally 100, but after standardization it should not be 100.0
    prp_inter_task_rows = df_long[
        (df_long['sample'] == 'PRP_Short_SOA') & 
        (df_long['feature'] == 'Inter-task SOA')
    ]
    if len(prp_inter_task_rows) > 0:  # Only test if this feature exists
        standardized_value = prp_inter_task_rows['value'].iloc[0]
        assert standardized_value != 100.0, f"Inter-task SOA should be standardized, not raw value 100.0. Got {standardized_value}"
        assert isinstance(standardized_value, (float, np.floating)), "Standardized value should be float"

def test_preprocess_for_mofa_with_real_data(real_raw_data):
    """
    Integration test for the MOFA preprocessor using real data.
    Ensures the pipeline can handle encoding from the actual CSV.
    """
    df_test = real_raw_data.copy()

    df_long, likelihoods, scaler, view_map = prepare_mofa_data(df_test, strategy='sparse')
    
    # Test 1: Check output structure
    expected_cols = ['sample', 'feature', 'value', 'view', 'group']
    assert all(col in df_long.columns for col in expected_cols)
    
    # Test 2: Check that function handles real data without errors
    assert len(df_long) > 0, "Should have some data after processing"
    assert len(likelihoods) > 0, "Should have some likelihoods"
    
    # Test 3: Verify all values are numeric
    assert df_long['value'].dtype in [np.float64, np.int64], f"Values should be numeric, got {df_long['value'].dtype}"
    
    # Test 4: Check views are assigned
    assert df_long['view'].notna().all(), "All rows should have views assigned"
    
    # Test 5: Check group assignment
    assert (df_long['group'] == 'all_studies').all(), "All rows should have group 'all_studies'"
    
    # Test 6: Check scaler is returned and properly fitted
    assert isinstance(scaler, StandardScaler), "Should return a fitted StandardScaler"
    assert hasattr(scaler, 'scale_'), "Scaler should be fitted (have scale_ attribute)"


def test_mofa_standardization_roundtrip(raw_test_data_dict):
    """
    Tests that standardization is reversible by performing a round-trip transformation.
    This verifies the StandardScaler is working correctly for inverse transformation.
    """
    df_raw = pd.DataFrame(raw_test_data_dict)
    
    df_long, likelihoods, scaler, view_map = prepare_mofa_data(df_raw, strategy='sparse')
    
    # Test round-trip for Inter-task SOA from PRP_Short_SOA sample
    prp_inter_task_rows = df_long[
        (df_long['sample'] == 'PRP_Short_SOA') & 
        (df_long['feature'] == 'Inter-task SOA')
    ]
    
    if len(prp_inter_task_rows) > 0:
        # Get the standardized value
        standardized_value = prp_inter_task_rows['value'].iloc[0]
        
        # Create a mock "reconstructed" data point to test inverse transformation
        # We'll create a single row with this standardized value
        continuous_columns = [
            'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA', 
            'Task 1 CSI', 'Task 2 CSI', 'RSI', 'Switch Rate', 
            'Task 1 Difficulty', 'Task 2 Difficulty'
        ]
        
        # Create a test data point with zeros for most features and our test value for Inter-task SOA
        test_data = pd.DataFrame(
            [[0.0] * len(continuous_columns)], 
            columns=continuous_columns
        )
        test_data.loc[0, 'Inter-task SOA'] = standardized_value
        
        # Apply inverse transformation
        inverse_transformed = scaler.inverse_transform(test_data)
        reconstructed_value = inverse_transformed[0, continuous_columns.index('Inter-task SOA')]
        
        # The reconstructed value should be approximately 100.0 (the original value)
        assert abs(reconstructed_value - 100.0) < 1e-10, f"Round-trip failed: expected ~100.0, got {reconstructed_value}"
