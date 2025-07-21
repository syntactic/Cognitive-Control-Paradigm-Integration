# tests/test_mofa_utils.py

import pytest
import pandas as pd
import numpy as np
from mofa_utils import preprocess_for_mofa

def test_preprocess_for_mofa_with_unified_fixture(raw_test_data_dict):
    """
    Tests the main preprocessing function using a unified data source.
    This test ensures the function behaves correctly when fed data with np.nan for missing values.
    """
    # Create the DataFrame and replace string 'N/A' with np.nan, as the notebook would.
    df_raw = pd.DataFrame(raw_test_data_dict).replace('N/A', np.nan)
    
    df_long, likelihoods = preprocess_for_mofa(df_raw)

    # --- Test 1: Check the final DataFrame structure ---
    expected_cols = ['sample', 'feature', 'value', 'view', 'group']
    assert all(col in df_long.columns for col in expected_cols)
    assert len(df_long.columns) == len(expected_cols)

    # --- Test 2: Check a specific categorical encoding ---
    ts_sr_row = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') &
        (df_long['feature'] == 'Stimulus-Response Congruency')
    ]
    assert ts_sr_row['value'].iloc[0] == -1.0 # Incongruent -> -1.0
    assert ts_sr_row['view'].iloc[0] == 'Conflict'

    # --- Test 3: Check cleaning of RSI and Switch Rate ---
    ts_rsi_row = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') &
        (df_long['feature'] == 'RSI')
    ]
    assert ts_rsi_row['value'].iloc[0] == 1100.0 # mean(600, 1600)

    ts_switch_rate_row = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') &
        (df_long['feature'] == 'Switch Rate')
    ]
    assert ts_switch_rate_row['value'].iloc[0] == 50.0

    # --- Test 4: Check that 'RSI Is Predictable' was correctly converted ---
    stroop_rsi_pred_row = df_long[
        (df_long['sample'] == 'Stroop_Incongruent') &
        (df_long['feature'] == 'RSI Is Predictable')
    ]
    assert stroop_rsi_pred_row['value'].iloc[0] == 1.0 # Yes -> 1.0

    ts_rsi_pred_row = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') &
        (df_long['feature'] == 'RSI Is Predictable')
    ]
    assert ts_rsi_pred_row['value'].iloc[0] == 0.0 # No -> 0.0

    # --- Test 5: Check that NaN values were correctly dropped ---
    # For the PRP task, 'Distractor SOA' is NaN and should not be in the final df_long
    prp_distractor_soa_rows = df_long[
        (df_long['sample'] == 'PRP_Short_SOA') &
        (df_long['feature'] == 'Distractor SOA')
    ]
    assert prp_distractor_soa_rows.empty

    # --- Test 6: Check newly added encodings ---
    # For TS_Switch_Incompatible:
    # 'Task 1 Stimulus-Response Mapping' should be 'Incompatible' -> -1.0
    ts_srm_row = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') &
        (df_long['feature'] == 'Task 1 Stimulus-Response Mapping')
    ]
    assert ts_srm_row['value'].iloc[0] == -1.0
    assert ts_srm_row['view'].iloc[0] == 'Rules'

    # 'Trial Transition Type' should be 'Switch' -> -1.0
    ts_ttt_row = df_long[
        (df_long['sample'] == 'TS_Switch_Incompatible') &
        (df_long['feature'] == 'Trial Transition Type')
    ]
    assert ts_ttt_row['value'].iloc[0] == -1.0
    assert ts_ttt_row['view'].iloc[0] == 'Rules'

def test_preprocess_for_mofa_with_real_data(real_raw_data):
    """
    Integration test for the MOFA preprocessor using real data.
    Ensures the pipeline can handle melting and encoding from the actual CSV.
    """
    # For the MOFA pipeline, we expect 'N/A' to be a true NaN.
    df_test = real_raw_data.copy().replace('N/A', np.nan)

    df_long, likelihoods = preprocess_for_mofa(df_test)
    
    # Test 1: Check that missing values are dropped, not included
    # The Telford experiment has 'Distractor SOA' as N/A.
    # This feature should NOT appear for that sample in the long dataframe.
    telford_distractor_soa = df_long[
        (df_long['sample'] == 'Telford 1931 Auditory RT (500ms SOA)') &
        (df_long['feature'] == 'Distractor SOA')
    ]
    assert telford_distractor_soa.empty

    # Test 2: Check a specific retained value
    # The Telford experiment should have an Inter-task SOA of 500.
    telford_intertask_soa = df_long[
        (df_long['sample'] == 'Telford 1931 Auditory RT (500ms SOA)') &
        (df_long['feature'] == 'Inter-task SOA')
    ]
    assert not telford_intertask_soa.empty
    assert telford_intertask_soa['value'].iloc[0] == 500.0
    assert telford_intertask_soa['view'].iloc[0] == 'Temporal'
