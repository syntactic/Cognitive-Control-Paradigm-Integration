
import pytest
import pandas as pd
from convert import (
    parse_notes,
    get_param,
    difficulty_to_coherence,
    simplify_response_set_overlap,
    process_condition
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
        "param_overrides": {
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
        'Super_Experiment_Mapping_Notes': '{"param_overrides": {"t1_stim_duration": 800, "t2_stim_duration": 800}}'
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
