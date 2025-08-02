# mofa_utils.py

import pandas as pd
import numpy as np
# We can still import helpers if they are independent of the PCA pipeline
from analysis_utils import clean_rsi, clean_switch_rate, classify_paradigm
from sklearn.preprocessing import StandardScaler

# 1. Define Mappings
VIEW_MAPPING = {
    'Temporal': ['Inter-task SOA', 'Distractor SOA', 'Task 1 CSI', 'Task 2 CSI', 'RSI'],
    'Context': ['Switch Rate', 'RSI is Predictable'],
    'Task_Properties': ['Task 1 Difficulty', 'Task 2 Difficulty'],
    'Conflict': ['Stimulus-Stimulus Congruency', 'Stimulus-Response Congruency'],
    'Rules': ['Task 1 Stimulus-Response Mapping', 'Task 2 Stimulus-Response Mapping', 'Response Set Overlap', 'Trial Transition Type'],
    'Structure': ['Task 2 Response Probability', 'Task 1 Cue Type', 'Task 2 Cue Type']
}

# Map original CSV columns to their designated view
FEATURE_TO_VIEW = {feature: view for view, features in VIEW_MAPPING.items() for feature in features}

# Define how to convert categorical text to numbers
CATEGORICAL_ENCODING = {
    'Stimulus-Stimulus Congruency': {'Incongruent': -1, 'Neutral': 0, 'Congruent': 1, 'N/A': np.nan},
    'Stimulus-Response Congruency': {'Incongruent': -1, 'Neutral': 0, 'Congruent': 1, 'N/A': np.nan},
    'Response Set Overlap': {'Identical': 1, 'Disjoint': 0, 'N/A': np.nan, 'Disjoint - Category (Same Modality)': 0, 'Disjoint - Modality (Standard)': 0, 'Disjoint - Modality (Non-Standard)': 0, 'Disjoint - Effector': 0},
    'Task 1 Stimulus-Response Mapping': {'Incompatible':-1, 'Arbitrary': 0, 'Compatible': 1},
    'Task 1 Stimulus-Response Mapping': {'Compatible': 1.0, 'Incompatible': -1.0, 'Arbitrary': 0.0, 'N/A': np.nan},
    'Task 2 Stimulus-Response Mapping': {'Compatible': 1.0, 'Incompatible': -1.0, 'Arbitrary': 0.0, 'N/A': np.nan},
    'Trial Transition Type': {'Repeat': 1.0, 'Pure': 0.0, 'Switch': -1.0, 'N/A': np.nan},
    'Task 1 Cue Type': {'Arbitrary': 1.0, 'None/Implicit': 0.0, 'N/A': np.nan},
    'Task 2 Cue Type': {'Arbitrary': 1.0, 'None/Implicit': 0.0, 'N/A': np.nan},
    # ... add mappings for SRM, TCT, etc.
}

NUMERICAL_COLS = ['Inter-task SOA', 'Distractor SOA', 'Task 1 CSI', 'Task 2 CSI', 'RSI',
'Switch Rate', 'Task 1 Difficulty', 'Task 2 Difficulty', 'Task 2 Response Probability']

def preprocess_for_mofa(df_raw):
    """
    Transforms the raw, wide-format design space CSV into a long-format
    DataFrame suitable for mofapy2.
    """
    df = df_raw.copy()
    
    # --- Step 1: Initial Cleaning (can reuse some helpers) ---
    df['RSI'] = df['RSI'].apply(clean_rsi)
    df['Switch Rate'] = df['Switch Rate'].apply(clean_switch_rate)
    if 'RSI is Predictable' in df.columns:
            df['RSI is Predictable'] = df['RSI is Predictable'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0)

    # --- Step 2: Numerical Encoding of Categoricals, Normalization of Numerics ---
    for col, mapping in CATEGORICAL_ENCODING.items():
        if col in df.columns:
            df[col] = df[col].map(mapping)

    df_numeric = df[[col for col in NUMERICAL_COLS if col in df.columns]]

    scaler = StandardScaler()
    df_scaled_numeric = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns, index=df.index)

    # Update the main DataFrame with the scaled values
    df_before_scaling = df.copy()
    df.update(df_scaled_numeric)


    # --- Step 3: Melt DataFrame from Wide to Long ---
    id_vars = ['Experiment'] # The column that identifies a 'sample'
    value_vars = list(FEATURE_TO_VIEW.keys()) # All columns that are features
    
    df_long = pd.melt(df, id_vars=id_vars, value_vars=value_vars,
                      var_name='feature', value_name='value')
    
    # --- Step 4: Add 'view' and 'group' columns ---
    df_long['view'] = df_long['feature'].map(FEATURE_TO_VIEW)
    # Use paradigm classification for the 'group' column
    df_temp_for_group = df_before_scaling.set_index('Experiment')
    df_long['group'] = df_long['Experiment'].apply(lambda x: classify_paradigm(df_temp_for_group.loc[x]))
    df_long.rename(columns={'Experiment': 'sample'}, inplace=True)
    
    # --- Step 5: Final Cleanup ---
    df_long.dropna(subset=['value', 'view'], inplace=True)
    df_long['value'] = pd.to_numeric(df_long['value'])

    # --- Step 6: Define Likelihoods ---
    # For now, let's start with gaussian for all views
    # The order must be alphabetical by view name
    views_ordered = sorted(df_long['view'].unique())
    likelihoods = ['gaussian'] * len(views_ordered)

    return df_long, likelihoods
