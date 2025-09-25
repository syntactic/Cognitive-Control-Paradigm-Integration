# analysis_utils.py

import pandas as pd
import numpy as np
import re
import logging
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from scipy.stats import skew


VIEW_MAPPING_UNIFIED = {
    'Temporal': ['Inter-task SOA', 'Distractor SOA', 'Task 1 CSI', 'Task 2 CSI', 'RSI'],
    'Context': ['Switch Rate', 'RSI is Predictable', 'Trial Transition Type'],
    'Task_Properties': ['Task 1 Difficulty', 'Task 2 Difficulty', 'Intra-Trial Task Relationship'],
    'Conflict': ['Stimulus-Stimulus Congruency', 'Stimulus-Response Congruency', 'Stimulus Bivalence & Congruency'],
    'Rules': ['Task 1 Stimulus-Response Mapping', 'Task 2 Stimulus-Response Mapping', 'Response Set Overlap'],
    'Structure': ['Task 2 Response Probability', 'Task 1 Cue Type', 'Task 2 Cue Type']
}

def get_view_mapping_unified(binary_flags=False):
    view_mapping_unified = VIEW_MAPPING_UNIFIED
    if binary_flags:
        view_mapping_unified["Structure"].extend(['Inter task SOA is NA', 'Distractor SOA is NA', 'Task 2 CSI is NA', 'Task 2 Difficulty is NA'])
    return view_mapping_unified

# =============================================================================
# 1. Helper Functions for Data Cleaning
# =============================================================================

def validate_and_log_warnings(df, logger):
    """
    Validates the DataFrame for common logical inconsistencies and logs warnings.
    """
    for index, row in df.iterrows():
        # Use a more descriptive name for logging, if available
        exp_name = row.get('Experiment', f"index {index}")

        # Heuristic 1: If T2RP is 0, T2-related columns should be N/A.
        if row['Task 2 Response Probability'] == 0 and row['Switch Rate'] == 0:
            if pd.notna(row.get('Task 2 Difficulty')) and row.get('Task 2 Difficulty') != 'N/A':
                logger.warning(f"Warning: Task 2 Difficulty is present for a single-task condition in experiment {exp_name}.")
            if pd.notna(row.get('Task 2 CSI')) and row.get('Task 2 CSI') != 'N/A':
                logger.warning(f"Warning: Task 2 CSI is present for a single-task condition in experiment {exp_name}.")
            if pd.notna(row.get('Task 2 Stimulus-Response Mapping')) and row.get('Task 2 Stimulus-Response Mapping') != 'N/A':
                logger.warning(f"Warning: Task 2 Stimulus-Response Mapping is present for a single-task condition in experiment {exp_name}.")
            if pd.notna(row.get('Task 2 Cue Type')) and row.get('Task 2 Cue Type') != 'N/A':
                logger.warning(f"Warning: Task 2 Cue Type is present for a single-task condition in experiment {exp_name}.")

        # Heuristic 2 & 3: Check for logical consistency between Trial Transition Type and Switch Rate.
        if row.get('Trial Transition Type') == 'Pure' and row.get('Switch Rate', 0) != 0:
            logger.warning(f"Warning: Trial Transition is 'Pure' but Switch Rate is not 0% in experiment {exp_name}.")
        if row.get('Trial Transition Type') in ['Switch', 'Repeat'] and row.get('Switch Rate', 0) == 0:
            logger.warning(f"Warning: Trial Transition is 'Switch' or 'Repeat' but Switch Rate is 0% in experiment {exp_name}.")

        # Heuristic 4: If Inter-task SOA has a value, T2RP should be 1.
        if pd.notna(row.get('Inter-task SOA')) and row.get('Inter-task SOA') != 'N/A' and row.get('Task 2 Response Probability') != 1:
            logger.warning(f"Warning: Inter-task SOA has a value but T2RP is not 1 in experiment {exp_name}.")

        # Heuristic 5: If Distractor SOA has a value, there must be some form of S-S or S-R conflict defined.
        if pd.notna(row.get('Distractor SOA')) and row.get('Distractor SOA') != 'N/A':
            ss_is_na = pd.isna(row.get('Stimulus-Stimulus Congruency')) or row.get('Stimulus-Stimulus Congruency') == 'N/A'
            sr_is_na = pd.isna(row.get('Stimulus-Response Congruency')) or row.get('Stimulus-Response Congruency') == 'N/A'
            if ss_is_na and sr_is_na:
                logger.warning(f"Warning: Distractor SOA has a value but neither S-S nor S-R congruency is defined in experiment {exp_name}.")

        # Heuristic 6: Check Intra-Trial Task Relationship consistency with Task 1 and Task 2 Types
        ittr_value = row.get('Intra-Trial Task Relationship')
        task1_type = row.get('Task 1 Type')
        task2_type = row.get('Task 2 Type')
        
        if pd.notna(ittr_value) and ittr_value != 'N/A':
            # Check if single-task condition should be N/A
            # For dual-task conditions, validate the relationship
            if pd.notna(task1_type) and pd.notna(task2_type) and task1_type != 'N/A' and task2_type != 'N/A':
                expected_relationship = 'Same' if task1_type == task2_type else 'Different'
                if ittr_value != expected_relationship:
                    logger.warning(f"Warning: Intra-Trial Task Relationship is '{ittr_value}' but Task 1 Type ('{task1_type}') and Task 2 Type ('{task2_type}') suggest it should be '{expected_relationship}' in experiment {exp_name}.")


def clean_rsi(value):
    """Converts various RSI string formats to a single float, or NaN."""
    if pd.isna(value) or value == 'Not Specified':
        return np.nan
    value_str = str(value)
    # Handle specific "Varied" formats from your notes
    if "Varied (choice:" in value_str:
        numbers = [float(x) for x in re.findall(r'\d+', value_str)]
        return np.mean(numbers) if numbers else np.nan
    elif "Varied (Uniform:" in value_str:
        numbers = [float(x) for x in re.findall(r'\d+', value_str)]
        return np.mean(numbers) if len(numbers) == 2 else np.nan
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return np.nan

def clean_switch_rate(value):
    """Converts switch rate percentages (as strings) to floats."""
    if pd.isna(value):
        return 0.0  # Assume 0 if not specified
    value_str = str(value).replace('%', '').strip()
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return 0.0

def classify_paradigm(row):
    """
    Classifies each experimental condition into a broader paradigm class based on key dimensions.
    The order of checks is hierarchical to ensure correct classification.
    """
    # 1. Dual-Task/PRP paradigms are defined by requiring a response to a second task.
    if row['Task 2 Response Probability'] > 0:
        return 'Dual-Task_PRP'

    # 2. For single-response paradigms, task-switching is the next major category.
    if row['Switch Rate'] > 0:
        return 'Task Switching'

    # 3. Interference tasks are non-switching, single-response tasks with either S-S or S-R conflict.
    if (row.get('Stimulus-Stimulus Congruency') != 'N/A' and pd.notna(row.get('Stimulus-Stimulus Congruency'))) or \
       (row.get('Stimulus-Response Congruency') != 'N/A' and pd.notna(row.get('Stimulus-Response Congruency'))):
        return 'Interference'

    # 4. Pure single-task baselines are what remains.
    return 'Single-Task' # Simplified remaining logic

def map_ss_congruency(val):
    """Maps Stimulus-Stimulus Congruency to standardized codes."""
    val_str = str(val)
    if val_str == 'Congruent':
        return 'SS_Congruent'
    if val_str == 'Incongruent':
        return 'SS_Incongruent'
    if val_str == 'Neutral':
        return 'SS_Neutral'
    return 'SS_NA'

def map_sr_congruency(val):
    """Maps Stimulus-Response Congruency to standardized codes."""
    val_str = str(val)
    if val_str == 'Congruent':
        return 'SR_Congruent'
    if val_str == 'Incongruent':
        return 'SR_Incongruent'
    if val_str == 'Neutral':
        return 'SR_Neutral'
    return 'SR_NA'

def map_sbc(val):
    """Maps the merged Stimulus Bivalence & Congruency column."""
    val_str = str(val)
    if val_str == 'Congruent':
        return 'Congruent'
    if val_str == 'Incongruent':
        return 'Incongruent'
    if val_str == 'Neutral':
        return 'Neutral'
    return 'N/A'


def map_rso(val):
    val_str = str(val).lower()
    if 'identical' in val_str: return 'RSO_Identical'
    if 'disjoint' in val_str: return 'RSO_Disjoint'
    return 'RSO_NA'

def map_srm(val): # For Task 1
    val_str = str(val).lower()
    if 'incompatible' in val_str: return 'SRM_Incompatible'
    if 'compatible' in val_str: return 'SRM_Compatible'
    if 'arbitrary' in val_str: return 'SRM_Arbitrary'
    return 'SRM_NA'

def map_tct(val): # For Task 1
    """Maps the Task Cue Type column to simplified categories."""
    val_str = str(val).lower()
    if 'arbitrary' in val_str:
        return 'TCT_Arbitrary'
    if 'none/implicit' in val_str:
        return 'TCT_Implicit'
    # Default any other cases (like NaN or unexpected values) to Implicit
    return 'TCT_Implicit'

# --- NEW MAPPING FUNCTIONS ---
def map_srm2(val): # For Task 2
    val_str = str(val).lower()
    if 'incompatible' in val_str: return 'SRM2_Incompatible'
    if 'compatible' in val_str: return 'SRM2_Compatible'
    if 'arbitrary' in val_str: return 'SRM2_Arbitrary'
    return 'SRM2_NA'

def map_tct2(val): # For Task 2
    val_str = str(val).lower()
    if 'arbitrary' in val_str: return 'TCT2_Arbitrary'
    if 'none/implicit' in val_str: return 'TCT2_Implicit'
    return 'TCT2_NA'

def map_ttt(val): # For Trial Transition Type
    val_str = str(val).lower()
    if 'pure' in val_str: return 'TTT_Pure'
    if 'switch' in val_str: return 'TTT_Switch'
    if 'repeat' in val_str: return 'TTT_Repeat'
    return 'TTT_NA'

def map_ittr(val): # For Intra-Trial Task Relationship
    val_str = str(val).lower()
    if val_str == 'same': return 'ITTR_Same'
    if val_str == 'different': return 'ITTR_Different'
    if val_str == 'n/a' or pd.isna(val): return 'ITTR_NA'
    return 'ITTR_NA'

def reverse_map_categories(df):
    """
    Takes the interpolated dataframe and adds original human-readable columns
    based on the reconstructed mapped category columns from the PCA inversion.
    """
    df_out = df.copy()
    print(df_out)

    # Define the reverse mappings (the inverse of your 'map_*' functions)
    sbc_reverse_map = {
        'Congruent': 'Congruent',
        'Incongruent': 'Incongruent',
        'Neutral': 'Neutral',
        'N/A': 'N/A'
    }
    ss_congruency_reverse_map = {
        'SS_Congruent': 'Congruent',
        'SS_Incongruent': 'Incongruent',
        'SS_Neutral': 'Neutral',
        'SS_NA': 'N/A'
    }
    sr_congruency_reverse_map = {
        'SR_Congruent': 'Congruent',
        'SR_Incongruent': 'Incongruent',
        'SR_Neutral': 'Neutral',
        'SR_NA': 'N/A'
    }
    srm_reverse_map = {
        'SRM_Compatible': 'Compatible',
        'SRM_Incompatible': 'Incompatible',
        'SRM_Arbitrary': 'Arbitrary',
        'SRM_NA': 'N/A'
    }
    srm2_reverse_map = {
        'SRM2_Compatible': 'Compatible',
        'SRM2_Incompatible': 'Incompatible',
        'SRM2_Arbitrary': 'Arbitrary',
        'SRM2_NA': 'N/A'
    }
    rso_reverse_map = {
        'RSO_Identical': 'Identical',
        'RSO_Disjoint': 'Disjoint',
        'RSO_NA': 'N/A'
    }
    ttt_reverse_map = {
        'TTT_Pure': 'Pure',
        'TTT_Switch': 'Switch',
        'TTT_Repeat': 'Repeat',
        'TTT_NA': 'N/A'
    }
    tct_reverse_map = {
        'TCT_Implicit': 'None/Implicit',
        'TCT_Arbitrary': 'Arbitrary (Symbolic)',
        'TCT_NA': 'N/A'
    }
    tct2_reverse_map = {
        'TCT2_Implicit': 'None/Implicit',
        'TCT2_Arbitrary': 'Arbitrary (Symbolic)',
        'TCT2_NA': 'N/A'
    }
    ittr_reverse_map = {
        'ITTR_Same': 'Same',
        'ITTR_Different': 'Different',
        'ITTR_NA': 'N/A'
    }

    # Apply the reverse mappings
    if 'SBC_Mapped' in df_out.columns:
        df_out['Stimulus Bivalence & Congruency'] = df_out['SBC_Mapped'].map(sbc_reverse_map)
    if 'Stimulus-Stimulus Congruency Mapped' in df_out.columns:
        df_out['Stimulus-Stimulus Congruency'] = df_out['Stimulus-Stimulus Congruency Mapped'].map(ss_congruency_reverse_map)
    if 'Stimulus-Response Congruency Mapped' in df_out.columns:
        df_out['Stimulus-Response Congruency'] = df_out['Stimulus-Response Congruency Mapped'].map(sr_congruency_reverse_map)
    if 'Task 1 Stimulus-Response Mapping Mapped' in df_out.columns:
        df_out['Task 1 Stimulus-Response Mapping'] = df_out['Task 1 Stimulus-Response Mapping Mapped'].map(srm_reverse_map)
    if 'Task 2 Stimulus-Response Mapping Mapped' in df_out.columns:
        df_out['Task 2 Stimulus-Response Mapping'] = df_out['Task 2 Stimulus-Response Mapping Mapped'].map(srm2_reverse_map)
    if 'Response Set Overlap Mapped' in df_out.columns:
        df_out['Response Set Overlap'] = df_out['Response Set Overlap Mapped'].map(rso_reverse_map)
    if 'Trial Transition Type Mapped' in df_out.columns:
        df_out['Trial Transition Type'] = df_out['Trial Transition Type Mapped'].map(ttt_reverse_map)
    if 'Task 1 Cue Type Mapped' in df_out.columns:
        df_out['Task 1 Cue Type'] = df_out['Task 1 Cue Type Mapped'].map(tct_reverse_map)
    if 'Task 2 Cue Type Mapped' in df_out.columns:
        df_out['Task 2 Cue Type'] = df_out['Task 2 Cue Type Mapped'].map(tct2_reverse_map)
    if 'Intra-Trial Task Relationship Mapped' in df_out.columns:
        df_out['Intra-Trial Task Relationship'] = df_out['Intra-Trial Task Relationship Mapped'].map(ittr_reverse_map)

    # Handle the binary predictable RSI
    if 'RSI is Predictable' in df_out.columns:
        print(df_out['RSI is Predictable'].value_counts())
        df_out['RSI is Predictable'] = df_out['RSI is Predictable'].apply(lambda x: 1 if round(x) == 1 else 'No')

    return df_out

def apply_conceptual_constraints(df):
    """
    Cleans up an interpolated dataframe by applying conceptual rules.
    For example, if a point is single-task, all T2-related
    parameters should be set to 'N/A'.
    """
    df_out = df.copy()
    logger = logging.getLogger(__name__)

    # Define a threshold for what we consider a 'single-task' paradigm
    THRESHOLD = 0.5

    # Identify rows that represent functionally single-task paradigms
    is_single_task = sum([df_out['Task 2 Response Probability'] < THRESHOLD,
                          df_out['Trial Transition Type'] == 'Pure',
                          df_out['Response Set Overlap'] == 'N/A',
                          'Task 2 Difficulty is NA' not in df_out.columns or df_out['Task 2 Difficulty is NA'] > THRESHOLD,
                          'Task 2 CSI is NA' not in df_out.columns or df_out['Task 2 CSI is NA'] > THRESHOLD,
                          df_out['Task 2 Stimulus-Response Mapping'] == 'N/A',
                          df_out['Task 2 Cue Type'] == 'N/A']) > 4

    # For these rows, nullify all Task 2-specific parameters
    t2_columns_to_nullify = [
        'Task 2 CSI',
        'Task 2 Difficulty',
        'Task 2 Stimulus-Response Mapping',
        'Task 2 Cue Type',
        'Response Set Overlap'
    ]

    for col in t2_columns_to_nullify:
        if col in df_out.columns:
            df_out.loc[is_single_task, col] = 'N/A'

    return df_out

# =============================================================================
# 2. Main Preprocessing Pipeline Function
# =============================================================================

def preprocess(df_raw, merge_conflict_dimensions=False, target='pca'):
    """
    Performs all preprocessing for either PCA or MOFA+.

    Args:
        df_raw (pd.DataFrame): The raw data from the CSV.
        merge_conflict_dimensions (bool): If True, merge conflict columns.
        target (str): The target analysis pipeline ('pca' or 'mofa').

    Returns:
        (df_features, numerical_cols, categorical_cols, df_processed, preprocessor)
    """
    logger = logging.getLogger(__name__)
    df = df_raw.copy()

    # --- Step 1: General Cleaning & Type Conversion ---
    # Convert all potentially numeric columns to numeric, coercing errors
    numeric_cols_to_clean = [
        'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA',
        'Task 1 CSI', 'Task 2 CSI', 'Task 1 Difficulty', 'Task 2 Difficulty'
    ]
    for col in numeric_cols_to_clean:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Apply special cleaning functions
    if 'RSI' in df.columns:
        df['RSI'] = df['RSI'].apply(clean_rsi)
    if 'Switch Rate' in df.columns:
        df['Switch Rate'] = df['Switch Rate'].apply(clean_switch_rate)

    # Impute RSI with the median for PCA, but not for MOFA
    if target == 'pca':
        if 'RSI' in df.columns:
            rsi_median = df['RSI'].median()
            df['RSI'] = df['RSI'].fillna(rsi_median)

    # Normalize Task Difficulty (1-5 scale to 0-1)
    df['Task 1 Difficulty Norm'] = (df['Task 1 Difficulty'] - 1) / 4
    df['Task 2 Difficulty Norm'] = (df['Task 2 Difficulty'] - 1) / 4

    # --- Step 2: Validate data and log warnings ---
    validate_and_log_warnings(df, logger)

    # --- Step 3: Add Paradigm Classification for Difficulty Placeholder and Plotting ---
    df['Paradigm'] = df.apply(classify_paradigm, axis=1)

    # --- Step 4: Create binary presence features ---
    # Generate Applicability Flags DIRECTLY from NaN status.
    # This is done BEFORE imputation.
    df['Inter-task SOA is NA'] = df['Inter-task SOA'].isna().astype(int)
    df['Distractor SOA is NA'] = df['Distractor SOA'].isna().astype(int)
    df['Task 2 CSI is NA'] = df['Task 2 CSI'].isna().astype(int)
    df['Task 2 Difficulty is NA'] = df['Task 2 Difficulty'].isna().astype(int)
    
    # --- Step 5: Manual Imputation ---
    df['Inter-task SOA'] = df['Inter-task SOA'].fillna(df['Inter-task SOA'].median())
    df['Distractor SOA'] = df['Distractor SOA'].fillna(df['Distractor SOA'].median())
    df['Task 1 CSI'] = df['Task 1 CSI'].fillna(0)
    df['Task 2 CSI'] = df['Task 2 CSI'].fillna(df['Task 2 CSI'].median())
    df['Task 1 Difficulty Norm'] = df['Task 1 Difficulty Norm'].fillna(df['Task 1 Difficulty Norm'].mean())
    df['Task 2 Difficulty Norm'] = df['Task 2 Difficulty Norm'].fillna(df['Task 2 Difficulty Norm'].mean())

    # Process new binary 'RSI is Predictable'
    df['RSI is Predictable'] = df['RSI is Predictable'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)

    # --- Step 6: Map Categorical Features ---
    if merge_conflict_dimensions:
        s_s_col = df['Stimulus-Stimulus Congruency']
        s_r_col = df['Stimulus-Response Congruency']

        conditions = [
            (s_s_col == 'Incongruent') | (s_r_col == 'Incongruent'),  # Priority 1: If either is Incongruent
            (s_s_col == 'Congruent') | (s_r_col == 'Congruent'),      # Priority 2: If either is Congruent
            (s_s_col == 'Neutral') | (s_r_col == 'Neutral')          # Priority 3: If either is Neutral
        ]

        choices = [
            'Incongruent',
            'Congruent',
            'Neutral'
        ]

        df['Stimulus Bivalence & Congruency'] = np.select(conditions, choices, default='N/A')
        """# Create the merged column
        df['Stimulus Bivalence & Congruency'] = np.where(
            df['Stimulus-Stimulus Congruency'].notna() & (df['Stimulus-Stimulus Congruency'] != 'N/A'),
            df['Stimulus-Stimulus Congruency'],
            df['Stimulus-Response Congruency']
        )"""
        df['SBC_Mapped'] = df['Stimulus Bivalence & Congruency'].apply(map_sbc)
    else:
        df['Stimulus-Stimulus Congruency Mapped'] = df['Stimulus-Stimulus Congruency'].apply(map_ss_congruency)
        df['Stimulus-Response Congruency Mapped'] = df['Stimulus-Response Congruency'].apply(map_sr_congruency)

    df['Response Set Overlap Mapped'] = df['Response Set Overlap'].apply(map_rso)
    df['Task 1 Stimulus-Response Mapping Mapped'] = df['Task 1 Stimulus-Response Mapping'].apply(map_srm)
    df['Task 1 Cue Type Mapped'] = df['Task 1 Cue Type'].apply(map_tct)
    # New categorical mappings
    df['Task 2 Stimulus-Response Mapping Mapped'] = df['Task 2 Stimulus-Response Mapping'].apply(map_srm2)
    df['Task 2 Cue Type Mapped'] = df['Task 2 Cue Type'].apply(map_tct2)
    df['Trial Transition Type Mapped'] = df['Trial Transition Type'].apply(map_ttt)
    df['Intra-Trial Task Relationship Mapped'] = df['Intra-Trial Task Relationship'].apply(map_ittr)

    # --- Step 7: Select final columns for the pipeline ---
    numerical_cols = [
        'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA',
        'Task 1 CSI', 'Task 2 CSI',
        'RSI', 'Switch Rate', 'Task 1 Difficulty Norm', 'Task 2 Difficulty Norm', 
    ]
    categorical_cols = [ 'Inter-task SOA is NA', 'Distractor SOA is NA', 'Task 2 CSI is NA', 'Task 2 Difficulty is NA',
        'Response Set Overlap Mapped', 'RSI is Predictable',
        'Task 1 Stimulus-Response Mapping Mapped', 'Task 1 Cue Type Mapped',
        'Task 2 Stimulus-Response Mapping Mapped', 'Task 2 Cue Type Mapped',
        'Trial Transition Type Mapped', 'Intra-Trial Task Relationship Mapped'
    ]
    
    if merge_conflict_dimensions:
        categorical_cols.append('SBC_Mapped')
    else:
        categorical_cols.extend(['Stimulus-Stimulus Congruency Mapped', 'Stimulus-Response Congruency Mapped'])

    df_features = df[numerical_cols + categorical_cols]
    
    # Rename columns for clarity in pipeline/loadings output
    df_features = df_features.rename(columns={
        'Task 1 Difficulty Norm': 'Task 1 Difficulty',
        'Task 2 Difficulty Norm': 'Task 2 Difficulty'
    })
    # Update the list of numerical columns to match the renamed columns
    numerical_cols = [name.replace(' Norm', '') if 'Norm' in name else name for name in numerical_cols]


    preprocessor = InvertibleColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', drop=None), categorical_cols)
        ],
        remainder='drop'
    )

    return df_features, numerical_cols, categorical_cols, df, preprocessor

def generate_dynamic_view_mapping(preprocessor, view_mapping_unified):
    """
    Generates a dynamic mapping from transformed feature names to views,
    ensuring no overgeneration by inspecting the fitted preprocessor.

    Args:
        preprocessor: A fitted InvertibleColumnTransformer.
        view_mapping_unified (dict): The single source of truth for conceptual mappings.

    Returns:
        dict: A dictionary mapping transformed feature names to their corresponding view.
    """
    # 1. Create a lookup from original conceptual feature name to its view.
    conceptual_name_to_view = {
        feature: view
        for view, features in view_mapping_unified.items()
        for feature in features
    }

    # 2. Get the exact list of columns that were fed into the preprocessor.
    input_features = preprocessor.feature_names_in_
    # 3. Get the exact list of columns that came out of the preprocessor.
    output_features = preprocessor.get_feature_names_out()

    final_mapping = {}
    # 4. Iterate through each output feature and work backwards to find its origin.
    for t_name in output_features:
        # e.g., t_name = 'cat__Stimulus_Stimulus_Congruency_Mapped_SS_Congruent'
        # or 'num__Inter-task SOA'
        original_name_from_transformer = t_name.split('__')[1]

        # Find which of the input columns is the source of this transformed column.
        # This works because OHE appends to the name, so startswith is a reliable check.
        source_input_col = None
        for input_name in input_features:
            if original_name_from_transformer.startswith(input_name):
                source_input_col = input_name
                break
        
        if source_input_col:
            # Now, map this source column (e.g., 'Stimulus-Stimulus Congruency Mapped')
            # back to its conceptual name (e.g., 'Stimulus-Stimulus Congruency').
            conceptual_name = None
            if source_input_col.endswith(' Mapped') or source_input_col == 'SBC_Mapped':
                if source_input_col == 'SBC_Mapped':
                    conceptual_name = 'Stimulus Bivalence & Congruency'
                else:
                    # e.g., 'Stimulus-Stimulus Congruency Mapped' -> 'Stimulus-Stimulus Congruency'
                    conceptual_name = source_input_col.replace(' Mapped', '')
            else:
                # It's a numerical or binary column that didn't get mapped.
                conceptual_name = source_input_col

            # Finally, find the view for that conceptual name.
            view = conceptual_name_to_view.get(conceptual_name)
            if view:
                final_mapping[t_name] = view
            else:
                logging.warning(f"Could not find view for conceptual name: '{conceptual_name}' (from transformed: {t_name})")
        else:
            logging.warning(f"Could not find source input column for transformed feature: {t_name}")
            
    return final_mapping

def prepare_mofa_data(df_raw: pd.DataFrame, strategy: str = 'sparse', 
                     merge_conflict_dimensions: bool = False) -> tuple:
    """
    Prepares data for MOFA+ analysis with support for different preprocessing strategies.
    
    This function serves as the unified entry point for MOFA+ data preparation, supporting
    both sparse (ordinal encoding) and dense (one-hot encoding) preprocessing strategies.
    Both strategies now use the same underlying preprocessing pipeline for data cleaning
    and feature engineering.
    
    Args:
        df_raw (pd.DataFrame): The raw experimental data from CSV.
        strategy (str): Preprocessing strategy - either 'sparse' or 'dense'.
                       Default is 'sparse'.
        merge_conflict_dimensions (bool): Whether to merge conflict dimensions (S-S and S-R congruency)
                                        into a single 'Stimulus Bivalence & Congruency' dimension.
                                        Default is False.
    
    Returns:
        tuple: (df_long, likelihoods, preprocessor_obj, view_map)
            - df_long: Long-format DataFrame for MOFA+ with columns 
                      ['sample', 'feature', 'value', 'view', 'group']
            - likelihoods: List of likelihoods ('gaussian' for all views)
            - preprocessor_obj: Fitted preprocessor object for inverse transformation
                               (StandardScaler for sparse, InvertibleColumnTransformer for dense)
            - view_map: Dictionary mapping feature names to their conceptual view
    """
    # Always use preprocess() for data cleaning and feature engineering
    df_features, numerical_cols, categorical_cols, df_processed, preprocessor = preprocess(
        df_raw, merge_conflict_dimensions=merge_conflict_dimensions, target='mofa'
    )
    
    if strategy == 'dense':
        # Dense strategy: Use the preprocessor as-is (one-hot encoding)
        df_features_transformed = preprocessor.fit_transform(df_features)
        
        # Convert to DataFrame for easier handling
        feature_names = preprocessor.get_feature_names_out()
        df_features_wide = pd.DataFrame(
            df_features_transformed, 
            columns=feature_names,
            index=df_features.index
        )
        
        # Add experiment names back
        df_features_wide['Experiment'] = df_processed['Experiment'].values
        
        # Melt to long format
        df_long = pd.melt(
            df_features_wide, 
            id_vars=['Experiment'], 
            value_vars=[col for col in df_features_wide.columns if col != 'Experiment'],
            var_name='feature', 
            value_name='value'
        )
        
        # Rename Experiment to sample
        df_long.rename(columns={'Experiment': 'sample'}, inplace=True)
        
        # Generate dynamic view mapping using the fitted preprocessor
        view_map = generate_dynamic_view_mapping(preprocessor, VIEW_MAPPING_UNIFIED)
        
        # Add view mapping to df_long
        df_long['view'] = df_long['feature'].map(view_map)
        
        # Filter out rows where view couldn't be assigned
        df_long = df_long.dropna(subset=['view'])
        
        # Add group column
        df_long['group'] = 'all_studies'
        
        # Create likelihoods list
        views_ordered = sorted(df_long['view'].unique())
        likelihoods = ['gaussian'] * len(views_ordered)
        
        return df_long, likelihoods, preprocessor, view_map
        
    elif strategy == 'sparse':
        # Sparse strategy: Post-process the cleaned features with ordinal encoding
        df_sparse = df_features.copy()
        
        # For sparse strategy, we need to re-introduce NaN values where the original data was 'N/A'
        # The preprocess() function imputes these, but we want them to be missing for sparsity
        for col in numerical_cols:
            if col in df_sparse.columns:
                # Check the corresponding "is NA" indicator column
                na_indicator_col = f'{col} is NA'
                if na_indicator_col in df_sparse.columns:
                    # Where the indicator is 1, set the value back to NaN
                    df_sparse.loc[df_sparse[na_indicator_col] == 1, col] = np.nan
        
        # Apply ordinal encoding to categorical features (ignoring the one-hot preprocessor)
        for col in categorical_cols:
            if col in df_sparse.columns:
                if col == 'SBC_Mapped':
                    # Handle merged conflict dimension (Stimulus Bivalence & Congruency)
                    # Only map actual values, leave N/A as NaN so they get dropped later
                    sbc_mapping = {
                        'Congruent': 1.0, 'Neutral': 0.0, 'Incongruent': -1.0
                        # Note: 'N/A' is intentionally not mapped - it stays as NaN and gets dropped
                    }
                    df_sparse[col] = df_sparse[col].map(sbc_mapping)
                    
                elif 'Congruency' in col:
                    # Map congruency columns to ordinal scale: Congruent=1.0, Neutral=0.0, Incongruent=-1.0
                    congruency_mapping = {
                        'SS_Congruent': 1.0, 'SS_Neutral': 0.0, 'SS_Incongruent': -1.0,
                        'SR_Congruent': 1.0, 'SR_Neutral': 0.0, 'SR_Incongruent': -1.0,
                        'Congruent': 1.0, 'Neutral': 0.0, 'Incongruent': -1.0
                        # Note: mapped N/A values stay as NaN and get dropped
                    }
                    df_sparse[col] = df_sparse[col].map(congruency_mapping)
                    
                elif 'Response Set Overlap' in col:
                    # Map RSO to ordinal scale: Identical=1.0, Disjoint variants=-1.0
                    # RSO_NA values stay as NaN and get dropped
                    rso_mapping = {
                        'RSO_Identical': 1.0,
                        'RSO_Disjoint': -1.0
                    }
                    df_sparse[col] = df_sparse[col].map(rso_mapping)
                    
                elif 'Stimulus-Response Mapping' in col:
                    # Map SRM to ordinal scale: Compatible=1.0, Arbitrary=0.0, Incompatible=-1.0
                    # SRM_NA/SRM2_NA values stay as NaN and get dropped
                    srm_mapping = {
                        'SRM_Compatible': 1.0, 'SRM_Arbitrary': 0.0, 'SRM_Incompatible': -1.0,
                        'SRM2_Compatible': 1.0, 'SRM2_Arbitrary': 0.0, 'SRM2_Incompatible': -1.0
                    }
                    df_sparse[col] = df_sparse[col].map(srm_mapping)
                    
                elif 'Trial Transition Type' in col:
                    # Map TTT to ordinal scale: Pure=0.0, Repeat=0.5, Switch=-0.5
                    # TTT_NA values stay as NaN and get dropped
                    ttt_mapping = {
                        'TTT_Pure': 0.0, 'TTT_Repeat': 0.5, 'TTT_Switch': -0.5
                    }
                    df_sparse[col] = df_sparse[col].map(ttt_mapping)
                    
                elif 'Cue Type' in col:
                    # Map cue type to ordinal scale: None/Implicit=0.0, Arbitrary=1.0
                    # TCT_NA/TCT2_NA values stay as NaN and get dropped
                    cue_mapping = {
                        'TCT_Implicit': 0.0, 'TCT_Arbitrary': 1.0,
                        'TCT2_Implicit': 0.0, 'TCT2_Arbitrary': 1.0
                    }
                    df_sparse[col] = df_sparse[col].map(cue_mapping)
                    
                elif 'Intra-Trial Task Relationship' in col:
                    # Map ITTR to ordinal scale: Same=1.0, Different=-1.0
                    # ITTR_NA values stay as NaN and get dropped
                    ittr_mapping = {
                        'ITTR_Same': 1.0, 'ITTR_Different': -1.0
                    }
                    df_sparse[col] = df_sparse[col].map(ittr_mapping)
                    
                elif col == 'RSI is Predictable':
                    # Already binary (0/1), keep as-is
                    pass
                    
                else:
                    # For other binary/indicator columns, keep as-is (0/1)
                    pass
        
        # Standardize continuous features
        scaler = StandardScaler()
        if numerical_cols:
            # Only fit/transform if we have continuous columns
            continuous_data = df_sparse[numerical_cols]
            if not continuous_data.isna().all().all():
                df_sparse[numerical_cols] = scaler.fit_transform(continuous_data)
            else:
                # Edge case: if all continuous data is NaN, create a dummy scaler
                scaler.fit([[0.0] * len(numerical_cols)])
        else:
            # Edge case: if no continuous columns, create a dummy scaler
            scaler.fit([[0.0]])
        
        # Melt to long format
        feature_columns = [col for col in df_sparse.columns]
        df_sparse['Experiment'] = df_processed['Experiment'].values
        
        df_long = pd.melt(df_sparse, id_vars=['Experiment'], value_vars=feature_columns,
                          var_name='feature', value_name='value')
        
        # Rename Experiment to sample
        df_long.rename(columns={'Experiment': 'sample'}, inplace=True)
        
        # Drop missing values (MOFA+ native approach)
        df_long.dropna(subset=['value'], inplace=True)
        
        # Convert values to numeric (handle any remaining object types)
        df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')
        df_long.dropna(subset=['value'], inplace=True)
        
        # Generate view mapping for cleaned features
        # Map the processed feature names back to their conceptual names for view assignment
        feature_to_view = {}
        for view, features in VIEW_MAPPING_UNIFIED.items():
            for feature in features:
                # Handle mapped column names
                for col in df_sparse.columns:
                    if (col.replace(' Mapped', '').replace('SBC_Mapped', 'Stimulus Bivalence & Congruency') == feature or
                        col == feature):
                        feature_to_view[col] = view
        
        # Add view mapping to df_long
        df_long['view'] = df_long['feature'].map(feature_to_view)
        
        # Filter out rows where view couldn't be assigned
        df_long = df_long.dropna(subset=['view'])
        
        # Add group column
        df_long['group'] = 'all_studies'
        
        # Create likelihoods list
        views_ordered = sorted(df_long['view'].unique())
        likelihoods = ['gaussian'] * len(views_ordered)
        
        return df_long, likelihoods, scaler, feature_to_view
        
    else:
        raise ValueError(f"Unknown strategy: {strategy}. Must be either 'sparse' or 'dense'.")

def _prepare_mofa_data_sparse(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, list, StandardScaler]:
    """
    Prepares data for MOFA+ by numerically encoding features, standardizing continuous variables,
    and handling missing values by omission.
    
    This function transforms raw experimental data into the precise long-format DataFrame that 
    mofapy2 expects, with categorical features mapped to meaningful numerical scales, continuous
    features standardized for proper MOFA+ analysis, and missing values handled by dropping 
    the corresponding rows (MOFA+ native approach).
    
    Args:
        df_raw (pd.DataFrame): The raw experimental data from CSV.
        
    Returns:
        tuple[pd.DataFrame, list, StandardScaler]: 
            - Long-format DataFrame with columns ['sample', 'feature', 'value', 'view', 'group']
            - List of likelihoods ('gaussian' for all views)
            - Fitted StandardScaler for inverse transformation of continuous features
    """
    logger = logging.getLogger(__name__)
    df = df_raw.copy()
    
    # --- Step 1: Initial Data Cleaning ---
    # Replace string 'N/A' and 'Not Specified' with np.nan
    with pd.option_context('future.no_silent_downcasting', True):
        df = df.replace(['N/A', 'Not Specified'], np.nan)
    
    # Apply special cleaning functions
    if 'RSI' in df.columns:
        df['RSI'] = df['RSI'].apply(clean_rsi)
    if 'Switch Rate' in df.columns:
        df['Switch Rate'] = df['Switch Rate'].apply(clean_switch_rate)
    
    # Convert numeric columns to proper types
    numeric_cols_to_clean = [
        'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA',
        'Task 1 CSI', 'Task 2 CSI', 'Task 1 Difficulty', 'Task 2 Difficulty'
    ]
    for col in numeric_cols_to_clean:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # --- Step 2: Numerical and Ordinal Encoding ---
    # Congruency features: Congruent=1.0, Neutral=0.0, Incongruent=-1.0
    congruency_mapping = {'Congruent': 1.0, 'Neutral': 0.0, 'Incongruent': -1.0}
    
    if 'Stimulus-Stimulus Congruency' in df.columns:
        df['Stimulus-Stimulus Congruency'] = df['Stimulus-Stimulus Congruency'].map(congruency_mapping)
    if 'Stimulus-Response Congruency' in df.columns:
        df['Stimulus-Response Congruency'] = df['Stimulus-Response Congruency'].map(congruency_mapping)
    
    # Response Set Overlap: Identical=1.0, Disjoint variants=-1.0
    def map_response_set_overlap(val):
        if pd.isna(val):
            return np.nan
        val_str = str(val).lower()
        if 'identical' in val_str:
            return 1.0
        elif 'disjoint' in val_str:
            return -1.0
        else:
            return np.nan
    
    if 'Response Set Overlap' in df.columns:
        df['Response Set Overlap'] = df['Response Set Overlap'].apply(map_response_set_overlap)
    
    # Stimulus-Response Mapping: Compatible=1.0, Arbitrary=0.0, Incompatible=-1.0
    srm_mapping = {'Compatible': 1.0, 'Arbitrary': 0.0, 'Incompatible': -1.0}
    
    if 'Task 1 Stimulus-Response Mapping' in df.columns:
        df['Task 1 Stimulus-Response Mapping'] = df['Task 1 Stimulus-Response Mapping'].map(srm_mapping)
    if 'Task 2 Stimulus-Response Mapping' in df.columns:
        df['Task 2 Stimulus-Response Mapping'] = df['Task 2 Stimulus-Response Mapping'].map(srm_mapping)
    
    # Trial Transition Type: Pure=0.0, Repeat=0.5, Switch=-0.5
    ttt_mapping = {'Pure': 0.0, 'Repeat': 0.5, 'Switch': -0.5}
    
    if 'Trial Transition Type' in df.columns:
        df['Trial Transition Type'] = df['Trial Transition Type'].map(ttt_mapping)
    
    # Task Cue Type: None/Implicit=0.0, Arbitrary=1.0
    cue_mapping = {'None/Implicit': 0.0, 'Arbitrary': 1.0}
    
    if 'Task 1 Cue Type' in df.columns:
        df['Task 1 Cue Type'] = df['Task 1 Cue Type'].map(cue_mapping)
    if 'Task 2 Cue Type' in df.columns:
        df['Task 2 Cue Type'] = df['Task 2 Cue Type'].map(cue_mapping)
    
    # RSI is Predictable: Yes=1.0, No=0.0
    if 'RSI is Predictable' in df.columns:
        df['RSI is Predictable'] = df['RSI is Predictable'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0)
    
    # --- Step 2.5: Standardize Continuous Numerical Features ---
    # Identify continuous numerical columns (those that were NOT created from categorical mappings)
    continuous_columns = [
        'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA', 
        'Task 1 CSI', 'Task 2 CSI', 'RSI', 'Switch Rate', 
        'Task 1 Difficulty', 'Task 2 Difficulty'
    ]
    # Filter to only include columns that actually exist in the DataFrame
    continuous_columns = [col for col in continuous_columns if col in df.columns]
    
    # Initialize and fit StandardScaler on continuous columns only
    scaler = StandardScaler()
    if continuous_columns:
        # Fit scaler on non-NaN values and transform
        continuous_data = df[continuous_columns]
        # Only fit/transform if we have some non-NaN data
        if not continuous_data.isna().all().all():
            df[continuous_columns] = scaler.fit_transform(continuous_data)
        else:
            # Edge case: if all continuous data is NaN, create a dummy scaler
            scaler.fit([[0.0] * len(continuous_columns)])
    else:
        # Edge case: if no continuous columns, create a dummy scaler
        scaler.fit([[0.0]])
    
    # --- Step 3: Melt to Long Format ---
    # Select all columns except 'Experiment' for melting
    feature_columns = [col for col in df.columns if col != 'Experiment']
    
    df_long = pd.melt(df, id_vars=['Experiment'], value_vars=feature_columns,
                      var_name='feature', value_name='value')
    
    # Rename Experiment to sample
    df_long.rename(columns={'Experiment': 'sample'}, inplace=True)
    
    # --- Step 4: Drop Missing Values (MOFA+ native approach) ---
    df_long.dropna(subset=['value'], inplace=True)
    
    # Convert values to numeric (handle any remaining object types)
    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')
    df_long.dropna(subset=['value'], inplace=True)  # Drop any values that couldn't be converted
    
    # --- Step 5: Add View Mapping ---
    # Map features to views using VIEW_MAPPING_UNIFIED
    feature_to_view = {}
    for view, features in VIEW_MAPPING_UNIFIED.items():
        for feature in features:
            feature_to_view[feature] = view
    
    df_long['view'] = df_long['feature'].map(feature_to_view)
    
    # Filter out rows where view couldn't be assigned
    df_long = df_long.dropna(subset=['view'])
    
    # --- Step 6: Add Group Column ---
    df_long['group'] = 'all_studies'
    
    # --- Step 7: Create Likelihoods List ---
    views_ordered = sorted(df_long['view'].unique())
    likelihoods = ['gaussian'] * len(views_ordered)
    
    return df_long, likelihoods, scaler


# =============================================================================
# 3. PCA Pipeline and Model Analysis
# =============================================================================

class InvertibleColumnTransformer(ColumnTransformer):
    """
    A custom ColumnTransformer that supports inverse_transform, assuming all its
    component transformers also support it.
    """
    def inverse_transform(self, X):
        """
        Applies inverse_transform to each transformer and concatenates the results.
        """
        original_cols = []
        col_idx = 0
        
        # Iterate through the fitted transformers
        for name, trans, original_feature_names, _ in self._iter(
                fitted=True,
                column_as_labels=True,
                skip_drop=False,
                skip_empty_columns=True
            ):
            if trans == 'drop' or not hasattr(trans, 'inverse_transform'):
                continue

            n_transformed_features = len(self._transformer_to_input_indices[name])
            if name == 'cat': # OneHotEncoder has its own way of telling us
                 n_transformed_features = len(trans.get_feature_names_out(original_feature_names))

            # Slice the correct part of the transformed data
            if hasattr(X, 'iloc'):
                transformed_slice = X.iloc[:, col_idx : col_idx + n_transformed_features]
            else:
                transformed_slice = X[:, col_idx : col_idx + n_transformed_features]

            # --- START OF DEBUGGING BLOCK ---
            try:
                # This is the line that is expected to fail
                original_slice = trans.inverse_transform(transformed_slice)
            except ValueError as e:
                print(f"--- DEBUG: Error in transformer '{name}' ---")
                print(f"Problematic Data Slice (shape: {transformed_slice.shape}):")
                # Print the slice that's causing the error
                print(transformed_slice)
                print("-----------------------------------------")
                # Re-raise the original error to stop execution
                raise e
            # --- END OF DEBUGGING BLOCK ---
            
            # Apply inverse_transform
            original_slice = trans.inverse_transform(transformed_slice)
            
            # Store the result as a DataFrame to preserve column names
            original_cols.append(pd.DataFrame(original_slice, columns=original_feature_names))
            
            col_idx += n_transformed_features
            
        # Concatenate all the inverted columns
        df_original = pd.concat(original_cols, axis=1)
        
        # Ensure the final column order matches the original input order
        # Get the original column order from the fitted preprocessor
        original_feature_order = self.feature_names_in_
        
        return df_original[original_feature_order].values

def create_pca_pipeline(numerical_cols, categorical_cols):
    """Creates and returns an sklearn pipeline for preprocessing and PCA."""
    preprocessor = InvertibleColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', drop=None), categorical_cols)
        ],
        remainder='drop'
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('pca', PCA())
    ])
    return pipeline

def get_component_loadings(pipeline, numerical_cols, categorical_cols):
    """Extracts and formats the PCA component loadings into a DataFrame."""
    preprocessor = pipeline.named_steps['preprocessor']
    pca = pipeline.named_steps['pca']
    
    # Get feature names after one-hot encoding
    ohe_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
    all_feature_names = numerical_cols + list(ohe_feature_names)
    
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(pca.n_components_)],
        index=all_feature_names
    )
    return loadings

"""def export_component_loadings(loadings_df, component_name, feature_map, output_path, top_n=10):"""
"""
    Selects, sorts, renames, and formats the top N component loadings,
    then writes them to a file as LaTeX table rows.
    
    Args:
        loadings_df (pd.DataFrame): DataFrame containing all component loadings.
        component_name (str): The column name of the component to process (e.g., 'PC1').
        feature_map (dict): A dictionary mapping raw feature names to display names.
        output_path (str): The file path for the output file (e.g., 'pc1_loadings.tex').
        top_n (int): The number of top features to export.
    """# 1. Select, sort, and round the data
"""
    component_series = loadings_df[component_name].sort_values(key=abs, ascending=False).head(top_n)
    df_for_latex = component_series.round(3).reset_index()
    df_for_latex.columns = ['Feature', 'Loading']

    # 2. Prepare feature names for LaTeX
    def clean_feature_name(name):
        name = feature_map.get(name, name)
        # Replace characters that would break LaTeX
        name = name.replace('_', ' ').replace('=', ': ')
        # Escape any remaining special LaTeX characters
        name = name.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
        return name

    df_for_latex['Feature'] = df_for_latex['Feature'].apply(clean_feature_name)

    # 3. Build the string of LaTeX table rows
    table_rows = []
    for index, row in df_for_latex.iterrows():
        # Format each row as "Feature & Loading \\" with proper indentation
        table_rows.append(f"    {row['Feature']} & {row['Loading']} \\\\")
    
    output_string = "\n".join(table_rows)

    # 4. Write the generated string directly to the output file
    try:
        with open(output_path, 'w') as f:
            f.write(output_string)
        print(f"Successfully wrote LaTeX content for {component_name} to {output_path}")
    except IOError as e:
        print(f"Error writing to file {output_path}: {e}")"""

def _filter_redundant_binary_features(component_series):
    """
    Filters a series of loadings to remove redundant, anti-correlated binary features.
    
    For pairs like 'Feature_1' and 'Feature_0' that are perfectly anti-correlated,
    this function keeps only the one with the higher absolute loading.
    
    Args:
        component_series (pd.Series): A series of feature loadings, sorted by
                                      absolute value in descending order.
                                      
    Returns:
        pd.Series: A filtered series with redundant binary features removed.
    """
    features_to_keep = []
    processed_bases = set() # Keep track of feature bases we've already handled

    for feature, loading in component_series.items():
        # Use regex to find binary features ending in _0 or _1
        match = re.match(r'^(.*?)_([01])$', feature)
        
        if match:
            base_name = match.group(1) # The part of the name before _0 or _1
            
            if base_name in processed_bases:
                continue # Skip if we've already processed this pair
            
            # Find the opposite feature
            current_suffix = match.group(2)
            opposite_suffix = '1' if current_suffix == '0' else '0'
            opposite_feature = f"{base_name}_{opposite_suffix}"
            
            # Check if the opposite feature exists in the original series
            if opposite_feature in component_series:
                # Compare absolute loadings and decide which to keep
                opposite_loading = component_series[opposite_feature]
                if abs(loading) >= abs(opposite_loading):
                    features_to_keep.append(feature)
                else:
                    features_to_keep.append(opposite_feature)
                processed_bases.add(base_name)
            else:
                # It's a binary feature without a pair in the top list, so keep it
                features_to_keep.append(feature)
        else:
            # Not a binary feature of the form name_0/1, so keep it
            features_to_keep.append(feature)
            
    # Return the filtered series, preserving the original order as much as possible
    # We use .loc to select the features in our desired order and filter duplicates
    return component_series.loc[features_to_keep].drop_duplicates()


def export_component_loadings(loadings_df, component_name, feature_map, output_path, top_n=10):
    """
    Selects, sorts, renames, filters redundant binary features, and formats the
    top N component loadings, then writes them to a file as LaTeX table rows.
    """
    # 1. Select and sort a larger pool of features to ensure we find pairs
    # We fetch more than top_n initially to have a better chance of finding the anti-correlated pairs.
    initial_fetch_count = top_n * 2
    component_series = loadings_df[component_name].sort_values(key=abs, ascending=False).head(initial_fetch_count)

    # 2. Filter out the redundant binary features
    filtered_series = _filter_redundant_binary_features(component_series)
    
    # 3. Select the final top N from the filtered list and prepare for LaTeX
    df_for_latex = filtered_series.head(top_n).round(3).reset_index()
    df_for_latex.columns = ['Feature', 'Loading']

    # 4. Prepare feature names for LaTeX (cleaning)
    def clean_feature_name(name):
        name = feature_map.get(name, name)
        name = name.replace('_', ' ').replace('=', ': ')
        # Special handling for the binary features to make them more readable
        name = re.sub(r' (\d+)$', r' = \1', name) 
        # Escape any remaining special LaTeX characters
        name = name.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#')
        return name

    df_for_latex['Feature'] = df_for_latex['Feature'].apply(clean_feature_name)

    # 5. Build the string of LaTeX table rows
    table_rows = []
    for index, row in df_for_latex.iterrows():
        table_rows.append(f"    {row['Feature']} & {row['Loading']} \\\\")
    
    output_string = "\n".join(table_rows)

    # 6. Write the generated string directly to the output file
    try:
        with open(output_path, 'w') as f:
            f.write(output_string)
        print(f"Successfully wrote LaTeX content for {component_name} to {output_path}")
    except IOError as e:
        print(f"Error writing to file {output_path}: {e}")

# =============================================================================
# 4. Interpolation Functions (NEW)
# =============================================================================

def find_centroids(pca_df, paradigm_col='Paradigm'):
    """
    Calculates the centroid (mean position) for each paradigm class in the PC space.
    
    Args:
        pca_df (pd.DataFrame): DataFrame containing the PCA results and paradigm labels.
        paradigm_col (str): The name of the column with paradigm labels.
        
    Returns:
        dict: A dictionary where keys are paradigm names and values are centroid vectors.
    """
    return pca_df.groupby(paradigm_col).mean().to_dict('index')

def interpolate_centroids(centroid1, centroid2, alpha=0.5):
    """
    Performs linear interpolation between two points in PC space.
    
    Args:
        centroid1 (dict or pd.Series): The first point.
        centroid2 (dict or pd.Series): The second point.
        alpha (float): Interpolation factor. 0.0 is pure centroid1, 1.0 is pure centroid2.
        
    Returns:
        np.array: The interpolated point.
    """
    p1 = np.array(list(centroid1.values()))
    p2 = np.array(list(centroid2.values()))
    return p1 + alpha * (p2 - p1)

def inverse_transform_point(point_pc, pipeline):
    """
    Takes a point from the PC space and transforms it back to the original,
    human-readable feature space.
    
    Args:
        point_pc (np.array): A 1D array representing the point in PC space.
        pipeline (sklearn.Pipeline): The *fitted* PCA pipeline.
        
    Returns:
        pd.DataFrame: A DataFrame with the de-normalized and decoded parameters.
    """
    # Reshape for the pipeline's expected input
    point_pc_reshaped = point_pc.reshape(1, -1)
    
    # The pipeline's inverse_transform handles both PCA and preprocessor inversion
    original_space_point = pipeline.inverse_transform(point_pc_reshaped)

    # Get the original feature names from the pipeline
    feature_names = pipeline.named_steps['preprocessor'].feature_names_in_

    # Create a Series for the final output
    final_params = pd.Series(original_space_point[0], index=feature_names)

    # Re-normalize difficulty scores back to 1-5 scale for easier interpretation
    final_params['Task 1 Difficulty'] = (final_params['Task 1 Difficulty'] * 4) + 1
    final_params['Task 2 Difficulty'] = (final_params['Task 2 Difficulty'] * 4) + 1

    return final_params

def reconstruct_from_mofa_factors(factor_scores, model, preprocessor_obj):
    """
    Reconstructs the original feature space from MOFA+ factor scores using different
    types of preprocessor objects.

    Args:
        factor_scores (pd.DataFrame or pd.Series): A dataframe or series of factor scores for one or more samples.
        model (mfx.mofa_model): The trained mofax model.
        preprocessor_obj: The fitted preprocessor object - can be either StandardScaler 
                         (for sparse strategy) or InvertibleColumnTransformer (for dense strategy).

    Returns:
        pd.DataFrame: A DataFrame with the de-normalized and decoded original parameters.
    """
    # Ensure factor_scores is a 2D array for matrix multiplication
    if isinstance(factor_scores, pd.Series):
        factor_scores = factor_scores.to_frame().T
        
    Z = factor_scores.values
    W = model.get_weights(df=True)  # Get weights as DataFrame

    # Reconstruct the scaled/encoded data space
    reconstructed_data_scaled = pd.DataFrame(
        Z @ W.T, 
        columns=W.index, 
        index=factor_scores.index
    )
    
    # Handle different preprocessor types
    if isinstance(preprocessor_obj, ColumnTransformer):
        # Dense case: Use InvertibleColumnTransformer
        # The pipeline already knows how to reverse both scaling and one-hot encoding
        
        # Get the exact feature order the preprocessor expects
        expected_feature_order = preprocessor_obj.get_feature_names_out()

        # Re-index the weight matrix to match the preprocessor's order
        W_aligned = W.reindex(expected_feature_order)
        
        # Reconstruct with properly aligned features
        reconstructed_df = pd.DataFrame(
            Z @ W_aligned.T,
            columns=expected_feature_order,
            index=factor_scores.index
        )
        
        # Apply inverse transformation
        reconstructed_original_data = preprocessor_obj.inverse_transform(reconstructed_df)
        print("RECON", reconstructed_original_data)
        
        # Return as DataFrame with proper column names
        return pd.DataFrame(
            reconstructed_original_data, 
            columns=preprocessor_obj.feature_names_in_, 
            index=factor_scores.index
        )
        
    elif isinstance(preprocessor_obj, StandardScaler):
        # Sparse case: Manual inverse transformation for StandardScaler
        
        # Get the list of continuous features that were standardized
        continuous_columns = [
            'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA', 
            'Task 1 CSI', 'Task 2 CSI', 'RSI', 'Switch Rate', 
            'Task 1 Difficulty', 'Task 2 Difficulty'
        ]
        continuous_columns_present = [col for col in continuous_columns if col in reconstructed_data_scaled.columns]
        
        # Apply inverse standardization to continuous features only
        if continuous_columns_present and hasattr(preprocessor_obj, 'scale_'):
            reconstructed_data_scaled[continuous_columns_present] = preprocessor_obj.inverse_transform(
                reconstructed_data_scaled[continuous_columns_present]
            )
        
        # For ordinal features, map reconstructed float values back to nearest categories
        ordinal_mappings = {
            'Stimulus-Stimulus Congruency': {-1: -1.0, 0: 0.0, 1: 1.0},
            'Stimulus-Response Congruency': {-1: -1.0, 0: 0.0, 1: 1.0},
            'Response Set Overlap': {-1: -1.0, 1: 1.0},
            'Task 1 Stimulus-Response Mapping': {-1: -1.0, 0: 0.0, 1: 1.0},
            'Task 2 Stimulus-Response Mapping': {-1: -1.0, 0: 0.0, 1: 1.0},
            'Trial Transition Type': {-0.5: -0.5, 0: 0.0, 0.5: 0.5},
            'Task 1 Cue Type': {0: 0.0, 1: 1.0},
            'Task 2 Cue Type': {0: 0.0, 1: 1.0},
            'RSI is Predictable': {0: 0.0, 1: 1.0},
            'Intra-Trial Task Relationship': {-1: -1.0, 1: 1.0}
        }
        
        for col, mapping in ordinal_mappings.items():
            if col in reconstructed_data_scaled.columns:
                # Map each reconstructed value to its nearest ordinal value
                possible_values = list(mapping.values())
                def map_to_nearest(value):
                    return min(possible_values, key=lambda x: abs(x - value))
                
                reconstructed_data_scaled[col] = reconstructed_data_scaled[col].apply(map_to_nearest)
        
        return reconstructed_data_scaled
        
    else:
        raise ValueError(f"Unsupported preprocessor type: {type(preprocessor_obj)}. "
                        f"Expected StandardScaler or ColumnTransformer.")

def sparseness_hoyer(x):
    """
    The sparseness of array x is a real number in [0, 1], where sparser array
    has value closer to 1. Sparseness is 1 iff the vector contains a single
    nonzero component and is equal to 0 iff all components of the vector are 
    the same
        
    modified from Hoyer 2004: [sqrt(n)-L1/L2]/[sqrt(n)-1]
    
    adapted from nimfa package: https://nimfa.biolab.si/
    """
    from math import sqrt # faster than numpy sqrt 
    eps = np.finfo(x.dtype).eps if 'int' not in str(x.dtype) else 1e-9
    
    n = x.size

    # patch for array of zeros
    if np.allclose(x, np.zeros(x.shape), atol=1e-6):
        return 0.0
    
    L1 = abs(x).sum()
    L2 = sqrt(np.multiply(x, x).sum())
    sparseness_num = sqrt(n) - (L1 + eps) / (L2 + eps)
    sparseness_den = sqrt(n) - 1
    
    return sparseness_num / sparseness_den

def get_loadings_sparseness(loadings):
    """
    Args:
        loadings (numpy.array): a loadings matrix in the shape of (factors/components, features)

    Returns:
        factor_sparsities (list): a list of with as many elements as factors/components
    """
    
    transposed_loadings = loadings.T  # Shape will get turned into (features, factors/components)
    factor_sparsities = [sparseness_hoyer(factor) for factor in transposed_loadings]
    return factor_sparsities

def check_skewness(data_column: np.ndarray, threshold: float = 0.5) -> str:
    """
    Checks if a 1D NumPy array is symmetric or skewed based on its skewness coefficient.

    Args:
        data_column: A 1D NumPy array of numerical data.
        threshold: The skewness value |s| above which data is considered skewed.
                   A common threshold is 0.5.

    Returns:
        A string indicating if the data is "Symmetric", "Moderately Skewed",
        or "Highly Skewed".
    """
    # Calculate the skewness coefficient
    skewness = skew(data_column, nan_policy='omit')
    
    # Interpret the result
    if abs(skewness) < threshold:
        return f"Symmetric (Skewness: {skewness:.4f})"
    elif abs(skewness) < 1.0:
        return f"Moderately Skewed (Skewness: {skewness:.4f})"
    else:
        return f"Highly Skewed (Skewness: {skewness:.4f})"

def generate_interpolated_points(
    latent_space_df: pd.DataFrame,
    model_artifacts: dict,
    interpolation_pairs: list
) -> pd.DataFrame:
    """
    Generates interpolated points between paradigm centroids in a latent space,
    and reconstructs them back to the original feature space.

    This function is agnostic to the model (PCA or MOFA) and handles the
    appropriate inverse transformation.

    Args:
        latent_space_df (pd.DataFrame): DataFrame containing latent space coordinates
                                      and a 'Paradigm' column for labeling.
        model_artifacts (dict): A dictionary containing the necessary objects for reconstruction.
                                For PCA: {'type': 'pca', 'pipeline': sklearn.Pipeline}
                                For MOFA: {'type': 'mofa', 'model': mfx.mofa_model, 'preprocessor': object}
        interpolation_pairs (list): A list of tuples, where each tuple contains two
                                    paradigm names to interpolate between.

    Returns:
        pd.DataFrame: A DataFrame of the newly generated interpolated points, with
                      reconstructed features and metadata for plotting.
    """
    factors = [c for c in latent_space_df.columns if c.startswith("Factor")]
    pcs = [c for c in latent_space_df.columns if c.startswith("PC")]
    assert (bool(factors) and not bool(pcs)) or (not bool(factors) and bool(pcs)), "Either there are no factors or PCs, or both have been found"
    latent_cols = factors if factors else pcs
    latent_col_prefix = longest_common_prefix(latent_cols)
    
    # 1. Find the centroids in the latent space
    if not (latent_space_df["Point Type"] == "Centroid").any():
        paradigm_centroids = find_centroids(latent_space_df[latent_cols + ["Paradigm"]], paradigm_col='Paradigm')

    interpolated_points_list = []

    for p1_name, p2_name in interpolation_pairs:
        centroid1 = paradigm_centroids.get(p1_name)
        centroid2 = paradigm_centroids.get(p2_name)
        
        if not centroid1 or not centroid2:
            logging.warning(f"Could not find centroids for pair ({p1_name}, {p2_name}). Skipping interpolation.")
            continue

        # 2. Interpolate to find the midpoint in the latent space
        interpolated_coords = interpolate_centroids(
            {k: v for k, v in centroid1.items() if k in latent_cols},
            {k: v for k, v in centroid2.items() if k in latent_cols},
            alpha=0.5
        )

        # 3. Reconstruct the point back to the original feature space
        if model_artifacts['type'] == 'pca':
            original_space_params = inverse_transform_point(interpolated_coords, model_artifacts['pipeline'])
        elif model_artifacts['type'] == 'mofa':
            # Create a Series for reconstruction
            factor_scores = pd.Series(interpolated_coords, index=latent_cols)
            # The reconstruction returns a DataFrame, so we take the first row
            original_space_params = reconstruct_from_mofa_factors(
                factor_scores, 
                model_artifacts['model'], 
                model_artifacts['preprocessor']
            ).iloc[0]
        else:
            raise ValueError("model_artifacts['type'] must be 'pca' or 'mofa'")

        # 4. Create a dictionary for the new point, including metadata
        new_point = original_space_params.to_dict()
        for i, coord in enumerate(interpolated_coords):
            new_point[f'{latent_col_prefix}{i+1}'] = coord
        
        new_point.update({
            'Point Type': 'Interpolated',
            'Experiment': f"Interpolation: {p1_name} <-> {p2_name}",
            'Paradigm': 'Interpolated Point',
            'Parent1': p1_name,
            'Parent2': p2_name
        })
        
        interpolated_points_list.append(new_point)

    # 5. Finalize the DataFrame
    if not interpolated_points_list:
        return pd.DataFrame() # Return empty if no points were generated

    interpolated_df = pd.DataFrame(interpolated_points_list)
    # Perform post-reconstruction cleanup
    interpolated_df = reverse_map_categories(interpolated_df)
    interpolated_df = apply_conceptual_constraints(interpolated_df)
    
    return interpolated_df

def longest_common_prefix(strs: list[str]) -> str:
    """
    Finds the longest common prefix string amongst an array of strings.

    If there is no common prefix, it returns an empty string.

    Args:
        strs: A list of strings.

    Returns:
        The longest common prefix of all strings in the list.
    """
    # Handle edge cases: an empty list or a list with only one string
    if not strs:
        return ""
    if len(strs) == 1:
        return strs[0]

    # Use the first string as the initial prefix
    prefix = strs[0]

    # Iterate through the rest of the strings in the list
    for s in strs[1:]:
        # While the current string does not start with the prefix,
        # shorten the prefix by one character from the end
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            
            # If the prefix becomes empty, there is no common prefix
            if not prefix:
                return ""

    return prefix

def validate_paradigm_separation(
    pca_df,
    pc_cols,
    target_col='Paradigm',
    repeats=1,
    base_seed=42,
    test_size=0.2,
    n_neighbors=None
):
    """
    Validate how separable paradigms are in PCA space with a lightweight classifier.

    A k-Nearest Neighbors classifier is trained on repeated stratified splits of the
    requested principal components. Re-running the validation with multiple random seeds
    provides a more stable estimate of separability while keeping the original function
    signature compatible (defaults match the previous single-run behaviour).

    Args:
        pca_df (pd.DataFrame): Principal component coordinates and paradigm labels.
        pc_cols (Sequence[str]): Columns to use as features, e.g., ('PC1', 'PC2').
        target_col (str): Name of the paradigm label column. Default ``'Paradigm'``.
        repeats (int): Number of random train/test splits to evaluate. Default ``1``.
        base_seed (int): Seed offset used when generating repeated splits. Default ``42``.
        test_size (float): Maximum fraction of observations reserved for evaluation.
            A smaller value may be used automatically to maintain class support. Default ``0.2``.
        n_neighbors (int | None): Optional override for the KNN neighborhood size.

    Returns:
        dict: Aggregated validation metrics containing:
            - ``accuracy`` / ``accuracy_sd``: Mean accuracy and sample SD across repeats.
            - ``macro_f1`` / ``macro_f1_sd``: Mean macro F1-score and sample SD.
            - ``classification_report``: Detailed metrics for the first split (backwards compatible).
            - ``classification_report_mean``: Averaged precision/recall/F1 across repeats.
            - ``classification_report_runs``: Per-repeat classification report dictionaries.
            - ``confusion_matrix``: Confusion matrix for the first split.
            - ``confusion_matrix_sum``: Sum of confusion matrices across repeats.
            - ``per_run``: List of per-repeat summary metrics.
            - ``model_name``: String representation of the classifier used.
            - ``feature_names``: List of PC feature columns.
            - ``class_names``: Sorted list of detected paradigm labels.
            - ``train_size`` / ``test_size``: Sizes from the first evaluated split.
            - ``repeats`` and ``random_seeds``: Metadata for reproducibility.
    """
    if repeats < 1:
        raise ValueError("'repeats' must be at least 1.")

    pc_cols = list(pc_cols)
    X = pca_df[pc_cols].copy()
    y = pca_df[target_col].copy()

    valid_indices = ~y.isna()
    X = X.loc[valid_indices]
    y = y.loc[valid_indices]

    if len(X) == 0:
        raise ValueError(f"No valid data found. Check that '{target_col}' column has non-null values.")

    class_counts = y.value_counts()
    min_samples_per_class = class_counts.min()

    if min_samples_per_class < 2:
        raise ValueError(
            "At least one class has fewer than 2 samples. Cannot perform train/test split. "
            f"Class counts: {class_counts.to_dict()}"
        )

    if not 0 < test_size < 1:
        raise ValueError("'test_size' must be between 0 and 1 (exclusive).")

    # Cap the evaluation set so each class keeps representation while avoiding empty folds.
    effective_test_size = min(test_size, 1.0 / max(min_samples_per_class, 1))
    effective_test_size = max(effective_test_size, 1.0 / len(X))

    class_names = sorted(y.unique())

    accs = []
    macro_f1s = []
    reports = []
    conf_matrices = []
    per_run = []
    used_seeds = []

    for repeat_idx in range(repeats):
        base_state = base_seed + repeat_idx
        split_seed = base_state
        current_test_size = effective_test_size

        for attempt in range(5):
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=current_test_size,
                random_state=split_seed,
                stratify=y
            )

            if len(np.unique(y_test)) == len(class_names):
                break

            # Expand the evaluation split slightly and try again with nudged seed.
            current_test_size = min(0.5, current_test_size + max(0.05, 1.0 / len(X)))
            split_seed += 1
        else:
            raise ValueError(
                "Unable to create a stratified split that retains every class in the test set. "
                "Consider increasing 'test_size' or reviewing class imbalances."
            )

        if n_neighbors is None:
            dynamic_k = len(X_train) // len(class_names)
            k = max(1, min(3, dynamic_k))
        else:
            k = max(1, int(n_neighbors))

        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        report = classification_report(
            y_test,
            y_pred,
            target_names=class_names,
            output_dict=True,
            zero_division=0
        )
        macro_f1 = report['macro avg']['f1-score']
        conf_matrix = confusion_matrix(y_test, y_pred, labels=class_names)

        accs.append(accuracy)
        macro_f1s.append(macro_f1)
        reports.append(report)
        conf_matrices.append(conf_matrix)
        used_seeds.append(split_seed)

        per_run.append({
            'repeat': repeat_idx,
            'random_state': split_seed,
            'test_size': len(y_test),
            'train_size': len(y_train),
            'accuracy': float(accuracy),
            'macro_f1': float(macro_f1),
            'k': k,
            'classification_report': report,
            'confusion_matrix': conf_matrix
        })

    accuracy_mean = float(np.mean(accs))
    accuracy_sd = float(np.std(accs, ddof=1)) if repeats > 1 else 0.0
    macro_f1_mean = float(np.mean(macro_f1s))
    macro_f1_sd = float(np.std(macro_f1s, ddof=1)) if repeats > 1 else 0.0

    confusion_matrix_sum = np.sum(conf_matrices, axis=0)

    def _average_reports(run_reports):
        averaged = {}
        for key, value in run_reports[0].items():
            if isinstance(value, dict):
                averaged[key] = {}
                for metric in value:
                    metric_values = [rep[key][metric] for rep in run_reports if metric in rep[key]]
                    averaged[key][metric] = float(np.mean(metric_values))
            else:
                averaged[key] = float(np.mean([rep[key] for rep in run_reports]))
        return averaged

    report_mean = _average_reports(reports)

    first_run = per_run[0]

    results = {
        'repeats': repeats,
        'random_seeds': used_seeds,
        'accuracy': accuracy_mean,
        'accuracy_sd': accuracy_sd,
        'macro_f1': macro_f1_mean,
        'macro_f1_sd': macro_f1_sd,
        'classification_report': first_run['classification_report'],
        'classification_report_mean': report_mean,
        'classification_report_runs': reports,
        'confusion_matrix': first_run['confusion_matrix'],
        'confusion_matrix_sum': confusion_matrix_sum,
        'model_name': f'KNeighborsClassifier(n_neighbors={first_run["k"]})',
        'feature_names': pc_cols,
        'class_names': class_names,
        'train_size': first_run['train_size'],
        'test_size': first_run['test_size'],
        'per_run': per_run
    }

    return results
