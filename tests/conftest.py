# tests/conftest.py

import pytest
import pandas as pd

@pytest.fixture
def raw_test_data_dict():
    """
    Provides a dictionary of raw test data, mimicking the CSV format.
    This serves as a single source of truth for test data structure.
    """
    return {
        'Experiment': ['Stroop_Incongruent', 'PRP_Short_SOA', 'TS_Switch_Incompatible'],
        'Task 2 Response Probability': [0.0, 1.0, 0.0],
        'Inter-task SOA': ['N/A', 100, 'N/A'],
        'Distractor SOA': [0, 'N/A', 0],
        'Task 1 CSI': [0, 0, 200],
        'Task 2 CSI': ['N/A', 0, 200],
        'Switch Rate': ['0%', '0%', '50%'],
        'Trial Transition Type': ['Pure', 'Pure', 'Switch'],
        'Stimulus-Stimulus Congruency': ['Incongruent', 'N/A', 'Neutral'],
        'Stimulus-Response Congruency': ['N/A', 'N/A', 'Incongruent'],
        'Response Set Overlap': ['N/A', 'Disjoint - Modality', 'Identical'],
        'Task 1 Stimulus-Response Mapping': ['Compatible', 'Compatible', 'Incompatible'],
        'Task 2 Stimulus-Response Mapping': ['N/A', 'Compatible', 'Arbitrary'],
        'Task 1 Cue Type': ['None/Implicit', 'None/Implicit', 'Arbitrary'],
        'Task 2 Cue Type': ['N/A', 'None/Implicit', 'Arbitrary'],
        'RSI is Predictable': ['Yes', 'Yes', 'No'],
        'RSI': ['1000', '1500', '1100'],
        'Task 1 Difficulty': [3, 2, 3],
        'Task 2 Difficulty': ['N/A', 2, 3],
    }

@pytest.fixture(scope="module")
def real_raw_data():
    """
    Reads a small, representative subset of rows from the actual design space CSV.
    This fixture is shared across test modules.
    'scope="module"' means it only reads the file once per test module, not for every test.
    """
    df = pd.read_csv("data/super_experiment_design_space.csv", keep_default_na=False)
    
    # Select a few representative rows by their 'Experiment' name
    experiments_to_test = [
        "Stroop 1935 Color Naming", # Classic Interference
        "Telford 1931 Auditory RT (500ms SOA)", # Classic PRP
        "Meiran 1996 Exp 1 (Short CSI) Switch Trials Incongruent" # Complex Task Switching
    ]
    
    subset_df = df[df['Experiment'].isin(experiments_to_test)].copy()
    return subset_df
