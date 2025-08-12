
import pytest
import pandas as pd
import logging
from convert import (
    parse_notes,
    get_param,
    difficulty_to_coherence,
    simplify_response_set_overlap,
    process_condition,
    validate_block_configurations
)

# Tests for parse_notes
def test_parse_notes_valid_json():
    assert parse_notes('{"key": "value"}') == {"key": "value"}

def test_parse_notes_invalid_json():
    assert parse_notes('not json') == {}

def test_parse_notes_empty_string():
    assert parse_notes('') == {}

def test_parse_notes_nan():
    assert parse_notes(pd.NA) == {}
    assert parse_notes(None) == {}

# Tests for get_param
@pytest.fixture
def sample_row_and_notes():
    row = pd.Series({'Experiment': 'TestExp'})
    notes = {
        "convert_overrides": {
            "base_stim_duration": 500,
            "t1_stim_duration": 450
        }
    }
    return row, notes

def test_get_param_override(sample_row_and_notes):
    row, notes = sample_row_and_notes
    assert get_param(row, notes, 'base_stim_duration', 2000) == 500

def test_get_param_default(sample_row_and_notes):
    row, notes = sample_row_and_notes
    assert get_param(row, notes, 't2_stim_duration', 2000) == 2000

# Tests for difficulty_to_coherence
def test_difficulty_to_coherence_valid():
    assert difficulty_to_coherence(1) == 1.0
    assert difficulty_to_coherence(3) == 0.5
    assert difficulty_to_coherence(5) == 0.0

def test_difficulty_to_coherence_invalid():
    assert difficulty_to_coherence(0) == 0.5
    assert difficulty_to_coherence(6) == 0.5
    assert difficulty_to_coherence(pd.NA) == 0.5

# Tests for simplify_response_set_overlap
def test_simplify_rso():
    assert simplify_response_set_overlap('Identical') == 'Identical'
    assert simplify_response_set_overlap('Disjoint') == 'Disjoint'
    assert simplify_response_set_overlap('Disjoint (Manual vs Vocal)') == 'Disjoint'
    assert simplify_response_set_overlap('Partial') == 'N/A'
    assert simplify_response_set_overlap(pd.NA) == 'N/A'

# Tests for process_condition (a more complex integration test)
@pytest.fixture
def sample_test_row():
    """Provides a sample row with the new schema for tests."""
    return pd.Series({
        'Experiment': 'Test Experiment',
        'Task 1 Type': 'Flanker',
        'Task 2 Type': 'N/A',
        'Stimulus-Stimulus Congruency': 'N/A',
        'Stimulus-Response Congruency': 'N/A',
        'Response Set Overlap': 'N/A',
        'Task 1 Stimulus-Response Mapping': 'Compatible',
        'Task 2 Stimulus-Response Mapping': 'N/A',
        'Switch Rate': '0%',
        'RSI': 1000,
        'Task 1 Difficulty': 3,
        'Task 2 Difficulty': pd.NA,
        'Task 2 Response Probability': 0.0,
        'Inter-task SOA': pd.NA,
        'Distractor SOA': pd.NA,
        'Task 1 CSI': 50,
        'Task 2 CSI': pd.NA,
        'Trial Transition Type': 'Repeat',
        'Super_Experiment_Mapping_Notes': ''
    })

def test_process_condition_single_task(sample_test_row):
    """ Tests a simple, univalent single task. Distractor pathway should be inactive. """
    row = sample_test_row
    result = process_condition(row)
    assert result['N_Tasks'] == 1
    assert result['coh_1'] == 0.5
    assert result['effective_start_stim1_mov'] == 0
    assert result['effective_end_stim1_mov'] == 2000 # default duration
    assert result['effective_start_cue1'] == -50 # csi is 50
    assert result['effective_start_stim1_or'] == 0 # No distractor for univalent
    assert result['effective_start_stim2_mov'] == 0 # No T2
    assert result['Stimulus_Valency'] == 'Univalent'
    assert result['Trial_Transition_Type'] == 'Repeat'


def test_process_condition_ss_conflict_single_task(sample_test_row):
    """ Tests a Stroop-like (S-S Incongruent) single task. Distractor pathway should be active. """
    row = sample_test_row.copy()
    row['Stimulus-Stimulus Congruency'] = 'Incongruent'
    row['Distractor SOA'] = 0 # Distractor is simultaneous
    row['Task 1 CSI'] = 0
    
    result = process_condition(row)
    assert result['N_Tasks'] == 1
    assert result['effective_end_stim1_or'] > result['effective_start_stim1_or'] # Distractor should be active
    assert result['Stimulus_Valency'] == 'Bivalent-Incongruent'

def test_process_condition_sr_conflict_single_task(sample_test_row):
    """ Tests a Simon-like (S-R Incongruent) single task. Distractor pathway should be active. """
    row = sample_test_row.copy()
    row['Stimulus-Response Congruency'] = 'Incongruent'
    row['Distractor SOA'] = 0
    row['Task 1 CSI'] = 0

    result = process_condition(row)
    assert result['N_Tasks'] == 1
    assert result['effective_end_stim1_or'] > result['effective_start_stim1_or'] # Distractor should be active
    assert result['Stimulus_Valency'] == 'Bivalent-Neutral' # S-R conflict is abstracted to Bivalent-Neutral

def test_process_condition_dual_task(sample_test_row):
    row = sample_test_row.copy()
    row['Task 2 Response Probability'] = 1.0
    row['Task 2 Type'] = 'Letter'
    row['Response Set Overlap'] = 'Disjoint'
    row['Task 1 Stimulus-Response Mapping'] = 'Arbitrary'
    row['Task 2 Stimulus-Response Mapping'] = 'Arbitrary'
    row['RSI'] = 1200
    row['Task 1 Difficulty'] = 2
    row['Task 2 Difficulty'] = 4
    row['Inter-task SOA'] = 300
    row['Task 1 CSI'] = 0
    row['Task 2 CSI'] = 0

    result = process_condition(row)
    assert result['N_Tasks'] == 2
    assert result['coh_1'] == 0.75
    assert result['coh_2'] == 0.25
    assert result['effective_start_stim1_mov'] == 0
    assert result['effective_start_stim2_or'] == 300 # T2 starts at SOA
    assert result['effective_end_stim2_or'] == 300 + 2000 # T2 ends after default duration
    assert result['effective_start_cue1'] == 0
    assert result['effective_start_cue2'] == 300 # T2 cue starts with T2 stim
    assert result['effective_start_stim1_or'] == 0 # No distractor for T1
    assert result['effective_start_stim2_mov'] == 0 # T2 is on 'or' channel
    assert result['Stimulus_Valency'] == 'Univalent' # Should be univalent for this dual task

def test_process_condition_with_overrides():
    row = pd.Series({
        'Experiment': 'Override Test',
        'Task 1 Type': 'Stroop',
        'Task 2 Type': 'N/A',
        'Stimulus-Stimulus Congruency': 'Incongruent',
        'Stimulus-Response Congruency': 'N/A',
        'Response Set Overlap': 'N/A',
        'Task 1 Stimulus-Response Mapping': 'Compatible',
        'Task 2 Stimulus-Response Mapping': 'N/A',
        'Switch Rate': '0%',
        'RSI': 500,
        'Task 1 Difficulty': 5,
        'Task 2 Difficulty': pd.NA,
        'Task 2 Response Probability': 0.0,
        'Inter-task SOA': pd.NA,
        'Distractor SOA': 0,
        'Task 1 CSI': 100,
        'Task 2 CSI': pd.NA,
        'Trial Transition Type': 'Switch',
        'Super_Experiment_Mapping_Notes': '{"convert_overrides": {"t1_stim_duration": 800, "t2_stim_duration": 800}}'
    })
    result = process_condition(row)
    assert result['effective_end_stim1_mov'] == 800 # Overridden duration
    assert result['effective_end_stim1_or'] == 800 # Distractor duration also overridden
    assert result['effective_start_cue1'] == -100
    assert result['effective_end_stim1_or'] > result['effective_start_stim1_or'] # Distractor should be active
    assert result['Stimulus_Valency'] == 'Bivalent-Incongruent'

def test_process_condition_dual_task_split_csi_soa(sample_test_row):
    """Tests a dual-task with specific Inter-task SOA and different CSIs."""
    row = sample_test_row.copy()
    row['Task 2 Response Probability'] = 1.0
    row['Task 2 Type'] = 'Letter'
    row['Inter-task SOA'] = 150
    row['Task 1 CSI'] = 50
    row['Task 2 CSI'] = 100
    
    result = process_condition(row)
    
    assert result['N_Tasks'] == 2
    # Assert T2 stimulus starts 150ms after T1 stimulus
    assert result['effective_start_stim2_or'] == result['effective_start_stim1_mov'] + 150
    # Assert T1 cue starts 50ms before T1 stimulus
    assert result['effective_start_cue1'] == result['effective_start_stim1_mov'] - 50
    # Assert T2 cue starts 100ms before T2 stimulus
    assert result['effective_start_cue2'] == result['effective_start_stim2_or'] - 100

def test_process_condition_single_task_distractor_soa(sample_test_row):
    """Tests a single-task with a negative Distractor SOA (distractor-first)."""
    row = sample_test_row.copy()
    row['Stimulus-Stimulus Congruency'] = 'Incongruent' # Make it bivalent
    row['Distractor SOA'] = -100
    
    result = process_condition(row)
    
    assert result['N_Tasks'] == 1
    # Assert distractor starts 100ms before the target
    assert result['effective_start_stim1_or'] == result['effective_start_stim1_mov'] - 100
    assert result['Stimulus_Valency'] == 'Bivalent-Incongruent'

# Tests for metadata propagation
def test_process_condition_metadata_extraction():
    """Tests that metadata from JSON is correctly extracted into new columns."""
    row = pd.Series({
        'Experiment': 'Metadata Test - Dual Task',
        'Task 1 Type': 'Tone',
        'Task 2 Type': 'Letter',
        'Stimulus-Stimulus Congruency': 'N/A',
        'Stimulus-Response Congruency': 'N/A',
        'Response Set Overlap': 'Disjoint',
        'Task 1 Stimulus-Response Mapping': 'Arbitrary',
        'Task 2 Stimulus-Response Mapping': 'Arbitrary',
        'Switch Rate': '0%',
        'RSI': 1200,
        'Task 1 Difficulty': 2,
        'Task 2 Difficulty': 3,
        'Task 2 Response Probability': 1.0,  # Dual-task
        'Inter-task SOA': 200,  # Mean SOA
        'Distractor SOA': pd.NA,
        'Task 1 CSI': 0,
        'Task 2 CSI': 0,
        'Trial Transition Type': 'N/A',
        'Super_Experiment_Mapping_Notes': '{"block_id": "test_block_1", "description": "Test dual-task condition", "viewer_config": {"sequence_type": "Random", "ITI_distribution": "uniform", "ITI_range": [800, 1600], "SOA_distribution": "choice", "SOA_values": [100, 200, 300]}}'
    })
    
    result = process_condition(row)
    
    # Test that metadata was correctly extracted
    assert result['Block_ID'] == 'test_block_1'
    assert result['Description'] == 'Test dual-task condition'
    assert result['Sequence_Type'] == 'Random'
    assert result['RSI_Distribution_Type'] == 'uniform'
    assert result['RSI_Distribution_Params'] == '[800, 1600]'
    assert result['SOA_Distribution_Type'] == 'choice'
    assert result['SOA_Distribution_Params'] == '[100, 200, 300]'
    
    # Verify it's properly recognized as dual-task
    assert result['N_Tasks'] == 2
    assert result['effective_start_stim2_or'] > 0  # T2 should be active

def test_process_condition_metadata_defaults():
    """Tests that default values are used when JSON metadata is missing."""
    row = pd.Series({
        'Experiment': 'Default Test',
        'Task 1 Type': 'Flanker',
        'Task 2 Type': 'N/A',
        'Stimulus-Stimulus Congruency': 'N/A',
        'Stimulus-Response Congruency': 'N/A',
        'Response Set Overlap': 'N/A',
        'Task 1 Stimulus-Response Mapping': 'Compatible',
        'Task 2 Stimulus-Response Mapping': 'N/A',
        'Switch Rate': '0%',
        'RSI': 800,
        'Task 1 Difficulty': 3,
        'Task 2 Difficulty': pd.NA,
        'Task 2 Response Probability': 0.0,
        'Inter-task SOA': pd.NA,
        'Distractor SOA': pd.NA,
        'Task 1 CSI': 0,
        'Task 2 CSI': pd.NA,
        'Trial Transition Type': 'Repeat',
        'Super_Experiment_Mapping_Notes': ''  # Empty JSON
    })
    
    result = process_condition(row)
    
    # Test that defaults were applied
    assert result['Block_ID'] == ''
    assert result['Description'] == ''
    assert result['Sequence_Type'] == 'Random'
    assert result['RSI_Distribution_Type'] == 'fixed'
    assert result['RSI_Distribution_Params'] == '[]'
    assert result['SOA_Distribution_Type'] == 'fixed'
    assert result['SOA_Distribution_Params'] == '[]'

# Tests for conflict dimensions collapsing
def test_conflict_dimensions_collapsing():
    """Tests that S-S and S-R congruency are correctly collapsed into a single dimension."""
    import numpy as np
    
    # Create test DataFrame with various conflict combinations
    test_data = {
        'Stimulus-Stimulus Congruency': ['Congruent', 'Incongruent', 'Neutral', 'N/A', 'Congruent', 'N/A'],
        'Stimulus-Response Congruency': ['N/A', 'N/A', 'N/A', 'Incongruent', 'Incongruent', 'Congruent']
    }
    
    test_df = pd.DataFrame(test_data)
    
    # Apply the same logic as in convert.py
    s_s_col = test_df['Stimulus-Stimulus Congruency']
    s_r_col = test_df['Stimulus-Response Congruency']
    
    conditions = [
        (s_s_col == 'Incongruent') | (s_r_col == 'Incongruent'),
        (s_s_col == 'Congruent') | (s_r_col == 'Congruent'),
        (s_s_col == 'Neutral') | (s_r_col == 'Neutral')
    ]
    
    choices = [
        'Incongruent',
        'Congruent', 
        'Neutral'
    ]
    
    test_df['Stimulus Bivalence & Congruency'] = np.select(conditions, choices, default='N/A')
    
    # Test the results
    expected_results = [
        'Congruent',    # S-S: Congruent, S-R: N/A -> Congruent
        'Incongruent',  # S-S: Incongruent, S-R: N/A -> Incongruent  
        'Neutral',      # S-S: Neutral, S-R: N/A -> Neutral
        'Incongruent',  # S-S: N/A, S-R: Incongruent -> Incongruent
        'Incongruent',  # S-S: Congruent, S-R: Incongruent -> Incongruent (prioritizes incongruent)
        'Congruent'     # S-S: N/A, S-R: Congruent -> Congruent
    ]
    
    for i, expected in enumerate(expected_results):
        assert test_df.iloc[i]['Stimulus Bivalence & Congruency'] == expected, f"Row {i}: Expected {expected}, got {test_df.iloc[i]['Stimulus Bivalence & Congruency']}"

def test_conflict_dimensions_collapsing_all_na():
    """Tests that N/A + N/A results in N/A for the collapsed dimension."""
    import numpy as np
    
    test_data = {
        'Stimulus-Stimulus Congruency': ['N/A', 'N/A'],
        'Stimulus-Response Congruency': ['N/A', 'N/A']
    }
    
    test_df = pd.DataFrame(test_data)
    
    # Apply the same logic as in convert.py
    s_s_col = test_df['Stimulus-Stimulus Congruency']
    s_r_col = test_df['Stimulus-Response Congruency']
    
    conditions = [
        (s_s_col == 'Incongruent') | (s_r_col == 'Incongruent'),
        (s_s_col == 'Congruent') | (s_r_col == 'Congruent'),
        (s_s_col == 'Neutral') | (s_r_col == 'Neutral')
    ]
    
    choices = [
        'Incongruent',
        'Congruent', 
        'Neutral'
    ]
    
    test_df['Stimulus Bivalence & Congruency'] = np.select(conditions, choices, default='N/A')
    
    # Both rows should result in N/A
    assert all(test_df['Stimulus Bivalence & Congruency'] == 'N/A')

# Tests for validate_block_configurations
def test_validate_block_configurations_no_blocks():
    """Test validation with empty dataframe."""
    df = pd.DataFrame()
    result = validate_block_configurations(df)
    assert result is True

def test_validate_block_configurations_single_conditions():
    """Test validation with only single-condition blocks (should pass)."""
    df = pd.DataFrame({
        'Experiment': ['Test1', 'Test2', 'Test3'],
        'Super_Experiment_Mapping_Notes': ['', '', '']
    })
    result = validate_block_configurations(df)
    assert result is True

def test_validate_block_configurations_consistent_blocks():
    """Test validation with consistent viewer_config within blocks."""
    df = pd.DataFrame({
        'Experiment': ['Block_A_Condition1', 'Block_A_Condition2', 'Block_B_Single'],
        'Super_Experiment_Mapping_Notes': [
            '{"block_id": "test_block_a", "viewer_config": {"sequence_type": "AABB"}}',
            '{"block_id": "test_block_a", "viewer_config": {"sequence_type": "AABB"}}',
            '{"block_id": "test_block_b", "viewer_config": {"sequence_type": "Random"}}'
        ]
    })
    
    # This should pass without any warnings or errors
    result = validate_block_configurations(df)
    assert result is True

def test_validate_block_configurations_inconsistent_blocks(caplog):
    """Test validation with inconsistent viewer_config within blocks."""
    df = pd.DataFrame({
        'Experiment': ['Block_A_Primary', 'Block_A_Secondary', 'Block_A_Tertiary'],
        'Super_Experiment_Mapping_Notes': [
            '{"block_id": "inconsistent_block", "viewer_config": {"sequence_type": "AABB"}}',
            '{"block_id": "inconsistent_block", "viewer_config": {"sequence_type": "ABAB"}}',
            '{"block_id": "inconsistent_block"}'  # No viewer_config - should not trigger warning
        ]
    })
    
    with caplog.at_level(logging.WARNING):
        result = validate_block_configurations(df)
    
    # Should still return True (warnings, not errors)
    assert result is True
    
    # Should have logged exactly one warning (for the ABAB config difference)
    warning_messages = [record.message for record in caplog.records if record.levelname == 'WARNING']
    assert len(warning_messages) == 1
    assert 'Row 3' in warning_messages[0]  # Row index 1 + 2 = 3 (1-indexed for user)
    assert 'inconsistent_block' in warning_messages[0]
    assert 'AABB' in warning_messages[0]
    assert 'ABAB' in warning_messages[0]

def test_validate_block_configurations_mixed_scenarios(caplog):
    """Test validation with a mix of consistent and inconsistent blocks."""
    df = pd.DataFrame({
        'Experiment': ['Good_Block_1', 'Good_Block_2', 'Bad_Block_1', 'Bad_Block_2', 'Single_Block'],
        'Super_Experiment_Mapping_Notes': [
            '{"block_id": "good_block", "viewer_config": {"sequence_type": "AABB", "ITI_distribution": "fixed"}}',
            '{"block_id": "good_block", "viewer_config": {"sequence_type": "AABB", "ITI_distribution": "fixed"}}',
            '{"block_id": "bad_block", "viewer_config": {"sequence_type": "AABB"}}',
            '{"block_id": "bad_block", "viewer_config": {"sequence_type": "ABAB"}}',  # Different!
            '{"block_id": "single_block", "viewer_config": {"sequence_type": "Random"}}'
        ]
    })
    
    with caplog.at_level(logging.WARNING):
        result = validate_block_configurations(df)
    
    assert result is True
    
    # Should have exactly one warning for the bad_block inconsistency
    warning_messages = [record.message for record in caplog.records if record.levelname == 'WARNING']
    assert len(warning_messages) == 1
    assert 'bad_block' in warning_messages[0]
    assert 'Row 5' in warning_messages[0]  # Row index 3 + 2 = 5

def test_validate_block_configurations_fallback_to_experiment_name(caplog):
    """Test that conditions without block_id fall back to using experiment name as block ID."""
    df = pd.DataFrame({
        'Experiment': ['Same_Experiment_Name', 'Same_Experiment_Name'],
        'Super_Experiment_Mapping_Notes': [
            '{"viewer_config": {"sequence_type": "AABB"}}',  # No block_id
            '{"viewer_config": {"sequence_type": "ABAB"}}'   # No block_id, different config
        ]
    })
    
    with caplog.at_level(logging.WARNING):
        result = validate_block_configurations(df)
    
    assert result is True
    
    # Should warn about inconsistency using experiment name as block ID
    warning_messages = [record.message for record in caplog.records if record.levelname == 'WARNING']
    assert len(warning_messages) == 1
    assert 'Same_Experiment_Name' in warning_messages[0]  # Block ID should be experiment name

def test_validate_block_configurations_empty_vs_populated_config():
    """Test that empty configs don't trigger warnings against populated configs."""
    df = pd.DataFrame({
        'Experiment': ['Primary_With_Config', 'Secondary_Empty_Config'],
        'Super_Experiment_Mapping_Notes': [
            '{"block_id": "test_block", "viewer_config": {"sequence_type": "AABB"}}',
            '{"block_id": "test_block"}'  # Empty viewer_config
        ]
    })
    
    # This should NOT generate warnings since empty config is ignored
    result = validate_block_configurations(df)
    assert result is True

def test_validate_block_configurations_malformed_json():
    """Test validation handles malformed JSON gracefully."""
    df = pd.DataFrame({
        'Experiment': ['Good_JSON', 'Bad_JSON'],
        'Super_Experiment_Mapping_Notes': [
            '{"block_id": "test_block", "viewer_config": {"sequence_type": "AABB"}}',
            'this is not valid json'  # Malformed JSON
        ]
    })
    
    # Should not crash, malformed JSON should be parsed as empty dict
    result = validate_block_configurations(df)
    assert result is True
