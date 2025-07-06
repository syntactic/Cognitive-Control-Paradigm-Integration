
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
def test_process_condition_single_task():
    row = pd.Series({
        'Experiment': 'Single Task Test',
        'Number of Tasks': 1,
        'Task 1 Type': 'Flanker',
        'Task 2 Type': 'N/A',
        'Stimulus Valency': 'Univalent',
        'Response Set Overlap': 'N/A',
        'Stimulus Response Mapping': 'Compatible',
        'Switch Rate': '0%',
        'RSI': 1000,
        'Task 1 Difficulty': 3,
        'Task 2 Difficulty': pd.NA,
        'SOA': pd.NA,
        'CSI': 50,
        'Super_Experiment_Mapping_Notes': ''
    })
    result = process_condition(row)
    assert result['N_Tasks'] == 1
    assert result['coh_1'] == 0.5
    assert result['effective_start_stim1_mov'] == 0
    assert result['effective_end_stim1_mov'] == 2000 # default duration
    assert result['effective_start_cue1'] == -50 # csi is 50
    assert result['effective_start_stim1_or'] == 0 # No distractor for univalent
    assert result['effective_start_stim2_mov'] == 0 # No T2
