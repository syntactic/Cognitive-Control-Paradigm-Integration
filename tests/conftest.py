# tests/conftest.py

import pytest
import pandas as pd

@pytest.fixture
def raw_test_data_dict():
    """
    Provides a dictionary of raw test data, mimicking the CSV format.
    This serves as a single source of truth for test data structure.
    Expanded to include more comprehensive and realistic test scenarios.
    """
    return {
        'Experiment': [
            'Stroop_Incongruent', 'PRP_Short_SOA', 'TS_Switch_Incompatible', 
            'Flanker_Congruent', 'PRP_Long_SOA', 'TS_Repeat_Compatible',
            'Simon_Neutral', 'DualTask_Concurrent'
        ],
        'Task 2 Response Probability': [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
        'Inter-task SOA': ['N/A', 100, 'N/A', 'N/A', 500, 'N/A', 'N/A', 200],
        'Distractor SOA': [0, 'N/A', 0, -200, 'N/A', 0, -100, 'N/A'],
        'Task 1 CSI': [0, 0, 200, 100, 150, 300, 50, 0],
        'Task 2 CSI': ['N/A', 0, 200, 'N/A', 100, 250, 'N/A', 0],
        'Switch Rate': ['0%', '0%', '50%', '0%', '0%', '25%', '0%', '0%'],
        'Trial Transition Type': ['Pure', 'Pure', 'Switch', 'Pure', 'Pure', 'Repeat', 'Pure', 'Pure'],
        'Stimulus-Stimulus Congruency': ['Incongruent', 'N/A', 'Neutral', 'Congruent', 'N/A', 'Incongruent', 'Neutral', 'N/A'],
        'Stimulus-Response Congruency': ['N/A', 'N/A', 'Incongruent', 'Congruent', 'N/A', 'Compatible', 'Neutral', 'N/A'],
        'Response Set Overlap': ['N/A', 'Disjoint - Modality', 'Identical', 'N/A', 'Disjoint', 'Identical', 'N/A', 'Disjoint - Spatial'],
        'Task 1 Stimulus-Response Mapping': ['Compatible', 'Compatible', 'Incompatible', 'Compatible', 'Arbitrary', 'Incompatible', 'Compatible', 'Arbitrary'],
        'Task 2 Stimulus-Response Mapping': ['N/A', 'Compatible', 'Arbitrary', 'N/A', 'Compatible', 'Incompatible', 'N/A', 'Arbitrary'],
        'Task 1 Cue Type': ['None/Implicit', 'None/Implicit', 'Arbitrary', 'None/Implicit', 'Arbitrary', 'Arbitrary', 'None/Implicit', 'None/Implicit'],
        'Task 2 Cue Type': ['N/A', 'None/Implicit', 'Arbitrary', 'N/A', 'Arbitrary', 'Arbitrary', 'N/A', 'None/Implicit'],
        'Inter-task SOA is Predictable': ['N/A', 'Yes', 'N/A', 'N/A', 'Yes', 'N/A', 'N/A', 'No'],
        'RSI is Predictable': ['Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No'],
        'RSI': ['1000', '1500', 'Varied (choice: 600, 1600)', '800', '2000', '1200', '1000', '1800'],
        'Task 1 Difficulty': [3, 2, 3, 2, 4, 1, 3, 2],
        'Task 2 Difficulty': ['N/A', 2, 3, 'N/A', 3, 4, 'N/A', 1],
        'Task 1 Type': ['Color Naming', 'Auditory RT', 'Add 6', 'Arrow Direction', 'Visual RT', 'Subtract 3', 'Spatial Location', 'Memory Task'],
        'Task 2 Type': ['N/A', 'Auditory RT', 'Subtract 3', 'N/A', 'Auditory RT', 'Add 6', 'N/A', 'Memory Task'],
        'Intra-Trial Task Relationship': ['N/A', 'Same', 'Different', 'N/A', 'Different', 'Different', 'N/A', 'Same'],
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
        "Telford 1931 Auditory RT", # Classic PRP
        "Meiran 1996 Exp 1 (Short CSI) Switch Trials Incongruent" # Complex Task Switching
    ]
    
    subset_df = df[df['Experiment'].isin(experiments_to_test)].copy()
    return subset_df
