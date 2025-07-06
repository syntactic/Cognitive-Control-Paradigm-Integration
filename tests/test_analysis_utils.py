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
    map_tct
)

# Fixtures for test data
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Number of Tasks': [1, 2, 1, 1],
        'Switch Rate': [0, 0, 50, 0],
        'Stimulus Valency': ['Univalent', 'Univalent', 'Bivalent', 'Bivalent Incongruent']
    })

# Tests for clean_rsi
def test_clean_rsi_numeric():
    assert clean_rsi(200) == 200.0
    assert clean_rsi('250') == 250.0

def test_clean_rsi_not_specified():
    assert np.isnan(clean_rsi('Not Specified'))

def test_clean_rsi_nan():
    assert np.isnan(clean_rsi(np.nan))

def test_clean_rsi_varied_choice():
    assert clean_rsi('Varied (choice: 100, 200, 300)') == 200.0

def test_clean_rsi_varied_uniform():
    assert clean_rsi('Varied (Uniform: 150-250)') == 200.0

# Tests for clean_switch_rate
def test_clean_switch_rate_string():
    assert clean_switch_rate('50%') == 50.0
    assert clean_switch_rate(' 25 % ') == 25.0

def test_clean_switch_rate_numeric():
    assert clean_switch_rate(75) == 75.0

def test_clean_switch_rate_nan():
    assert clean_switch_rate(np.nan) == 0.0

# Tests for classify_paradigm
def test_classify_paradigm(sample_data):
    paradigms = sample_data.apply(classify_paradigm, axis=1)
    assert paradigms.tolist() == ['Other', 'Dual-Task/PRP', 'Task Switching', 'Interference']

# Tests for mapping functions
def test_map_valency():
    assert map_valency('Univalent') == 'SBC_Univalent'
    assert map_valency('Bivalent Congruent') == 'SBC_Bivalent_Congruent'
    assert map_valency('Bivalent Incongruent') == 'SBC_Bivalent_Incongruent'
    assert map_valency('Bivalent Neutral') == 'SBC_Bivalent_Neutral'
    assert map_valency('N/A') == 'SBC_NA'

def test_map_rso():
    assert map_rso('Identical') == 'RSO_Identical'
    assert map_rso('Disjoint') == 'RSO_Disjoint'
    assert map_rso('Partial') == 'RSO_NA'

def test_map_srm():
    assert map_srm('Compatible') == 'SRM_Compatible'
    assert map_srm('Incompatible') == 'SRM_Incompatible'
    assert map_srm('Arbitrary') == 'SRM_Arbitrary'
    assert map_srm('Something else') == 'SRM_NA'

def test_map_tct():
    assert map_tct('Arbitrary (Symbolic)') == 'TCT_Arbitrary'
    assert map_tct('None/Implicit') == 'TCT_Implicit'
    assert map_tct(np.nan) == 'TCT_Implicit'