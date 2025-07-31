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
from scipy.stats import skew


VIEW_MAPPING_UNIFIED = {
    'Temporal': ['Inter-task SOA', 'Distractor SOA', 'Task 1 CSI', 'Task 2 CSI', 'RSI'],
    'Context': ['Switch Rate', 'RSI is Predictable', 'Trial_Transition_Type'],
    'Task_Properties': ['Task 1 Difficulty', 'Task 2 Difficulty'],
    'Conflict': ['Stimulus-Stimulus Congruency', 'Stimulus-Response Congruency'],
    'Rules': ['Task 1 Stimulus-Response Mapping', 'Task 2 Stimulus-Response Mapping', 'Response Set Overlap'],
    'Structure': ['Task 2 Response Probability', 'Task_1_Cue_Type', 'Task_2_Cue_Type', 'Inter_task_SOA_is_NA', 'Distractor_SOA_is_NA', 'Task_2_CSI_is_NA', 'Task_2_Difficulty_is_NA']
}

VIEW_MAPPING = {
    'Temporal': ['num__Inter-task SOA', 'num__Distractor SOA', 'num__Task 1 CSI', 'num__Task 2 CSI', 'num__RSI'],
    'Context': ['num__Switch Rate', 'cat__RSI is Predictable_1', 'cat__Trial_Transition_Type_Mapped_TTT_NA', 'cat__Trial_Transition_Type_Mapped_TTT_Pure', 'cat__Trial_Transition_Type_Mapped_TTT_Repeat', 'cat__Trial_Transition_Type_Mapped_TTT_Switch'],
    'Task_Properties': ['num__Task 1 Difficulty', 'num__Task 2 Difficulty'],
    'Conflict': ['cat__Stimulus_Stimulus_Congruency_Mapped_SS_Congruent', 'cat__Stimulus_Stimulus_Congruency_Mapped_SS_Incongruent', 'cat__Stimulus_Stimulus_Congruency_Mapped_SS_Neutral', 'cat__Stimulus_Stimulus_Congruency_Mapped_SS_NA', 'cat__Stimulus_Response_Congruency_Mapped_SR_NA', 'cat__Stimulus_Response_Congruency_Mapped_SR_Neutral', 'cat__Stimulus_Response_Congruency_Mapped_SR_Congruent', 'cat__Stimulus_Response_Congruency_Mapped_SR_Incongruent'],
    'Rules': ['cat__Task_1_Stimulus-Response_Mapping_Mapped_SRM_Arbitrary', 'cat__Task_1_Stimulus-Response_Mapping_Mapped_SRM_Compatible', 'cat__Task_1_Stimulus-Response_Mapping_Mapped_SRM_Incompatible', 'cat__Task_2_Stimulus-Response_Mapping_Mapped_SRM2_Arbitrary', 'cat__Task_2_Stimulus-Response_Mapping_Mapped_SRM2_Compatible', 'cat__Task_2_Stimulus-Response_Mapping_Mapped_SRM2_Incompatible', 'cat__Task_2_Stimulus-Response_Mapping_Mapped_SRM2_NA', 'cat__Response_Set_Overlap_Mapped_RSO_Disjoint', 'cat__Response_Set_Overlap_Mapped_RSO_Identical', 'cat__Response_Set_Overlap_Mapped_RSO_NA'],
    'Structure': ['num__Task 2 Response Probability', 'cat__Task_1_Cue_Type_Mapped_TCT_Implicit', 'cat__Task_2_Cue_Type_Mapped_TCT2_Arbitrary', 'cat__Task_2_Cue_Type_Mapped_TCT2_Implicit', 'cat__Task_2_Cue_Type_Mapped_TCT2_NA', 'cat__Inter_task_SOA_is_NA_1', 'cat__Distractor_SOA_is_NA_1', 'cat__Task_2_CSI_is_NA_1', 'cat__Task_2_Difficulty_is_NA_1']
}

# Map original CSV columns to their designated view
FEATURE_TO_VIEW = {feature: view for view, features in VIEW_MAPPING.items() for feature in features}

NUMERICAL_COLS = ['Inter-task SOA', 'Distractor SOA', 'Task 1 CSI', 'Task 2 CSI', 'RSI',
'Switch Rate', 'Task 1 Difficulty', 'Task 2 Difficulty', 'Task 2 Response Probability']

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
    if row['Task 2 Response Probability'] == 1:
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

def reverse_map_categories(df):
    """
    Takes the interpolated dataframe and adds original human-readable columns
    based on the reconstructed mapped category columns from the PCA inversion.
    """
    df_out = df.copy()

    # Define the reverse mappings (the inverse of your 'map_*' functions)
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

    # Apply the reverse mappings
    if 'Stimulus_Stimulus_Congruency_Mapped' in df_out.columns:
        df_out['Stimulus-Stimulus Congruency'] = df_out['Stimulus_Stimulus_Congruency_Mapped'].map(ss_congruency_reverse_map)
    if 'Stimulus_Response_Congruency_Mapped' in df_out.columns:
        df_out['Stimulus-Response Congruency'] = df_out['Stimulus_Response_Congruency_Mapped'].map(sr_congruency_reverse_map)
    if 'Task_1_Stimulus-Response_Mapping_Mapped' in df_out.columns:
        df_out['Task 1 Stimulus-Response Mapping'] = df_out['Task_1_Stimulus-Response_Mapping_Mapped'].map(srm_reverse_map)
    if 'Task_2_Stimulus-Response_Mapping_Mapped' in df_out.columns:
        df_out['Task 2 Stimulus-Response Mapping'] = df_out['Task_2_Stimulus-Response_Mapping_Mapped'].map(srm2_reverse_map)
    if 'Response_Set_Overlap_Mapped' in df_out.columns:
        df_out['Response Set Overlap'] = df_out['Response_Set_Overlap_Mapped'].map(rso_reverse_map)
    if 'Trial_Transition_Type_Mapped' in df_out.columns:
        df_out['Trial Transition Type'] = df_out['Trial_Transition_Type_Mapped'].map(ttt_reverse_map)
    if 'Task_1_Cue_Type_Mapped' in df_out.columns:
        df_out['Task 1 Cue Type'] = df_out['Task_1_Cue_Type_Mapped'].map(tct_reverse_map)
    if 'Task_2_Cue_Type_Mapped' in df_out.columns:
        df_out['Task 2 Cue Type'] = df_out['Task_2_Cue_Type_Mapped'].map(tct2_reverse_map)

    # Handle the binary predictable RSI
    if 'RSI is Predictable' in df_out.columns:
         df_out['RSI is Predictable'] = df_out['RSI is Predictable'].apply(lambda x: 'Yes' if round(x) == 1 else 'No')

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
                          df_out['Task_2_Difficulty_is_NA'] > THRESHOLD,
                          df_out['Task_2_CSI_is_NA'] > THRESHOLD,
                          df_out['Task 2 Stimulus-Response Mapping'] == 'N/A',
                          df_out['Task 2 Cue Type'] == 'N/A']) > 4
    logger.warning(f"Is single task: {is_single_task}")

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

def preprocess(df_raw, target='pca'):
    """
    Performs all preprocessing for either PCA or MOFA+.

    Args:
        df_raw (pd.DataFrame): The raw data from the CSV.
        target (str): The target analysis pipeline ('pca' or 'mofa').

    Returns:
        For target='pca': (df_pca_features, numerical_cols, categorical_cols, df_processed)
        For target='mofa': (df_long, likelihoods)
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

    # Impute RSI with the median before it's used in calculations
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
    df['Inter_task_SOA_is_NA'] = df['Inter-task SOA'].isna().astype(int)
    df['Distractor_SOA_is_NA'] = df['Distractor SOA'].isna().astype(int)
    df['Task_2_CSI_is_NA'] = df['Task 2 CSI'].isna().astype(int)
    df['Task_2_Difficulty_is_NA'] = df['Task 2 Difficulty'].isna().astype(int)
    # Impute Main SOA Columns and other numeric columns.
    df['Inter-task SOA'] = df['Inter-task SOA'].fillna(df['Inter-task SOA'].median())
    df['Distractor SOA'] = df['Distractor SOA'].fillna(df['Distractor SOA'].median())
    df['Task 1 CSI'] = df['Task 1 CSI'].fillna(0) # this should never happen but in case it does
    df['Task 2 CSI'] = df['Task 2 CSI'].fillna(df['Task 2 CSI'].median())
    df['Task 1 Difficulty Norm'] = df['Task 1 Difficulty Norm'].fillna(df['Task 1 Difficulty Norm'].mean()) # This should never happen but in case it does
    df['Task 2 Difficulty Norm'] = df['Task 2 Difficulty Norm'].fillna(df['Task 2 Difficulty Norm'].mean())

    # Process new binary 'RSI is Predictable'
    df['RSI is Predictable'] = df['RSI is Predictable'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)

    # --- Step 5: Map Categorical Features ---
    df['Stimulus_Stimulus_Congruency_Mapped'] = df['Stimulus-Stimulus Congruency'].apply(map_ss_congruency)
    df['Stimulus_Response_Congruency_Mapped'] = df['Stimulus-Response Congruency'].apply(map_sr_congruency)
    df['Response_Set_Overlap_Mapped'] = df['Response Set Overlap'].apply(map_rso)
    df['Task_1_Stimulus-Response_Mapping_Mapped'] = df['Task 1 Stimulus-Response Mapping'].apply(map_srm)
    df['Task_1_Cue_Type_Mapped'] = df['Task 1 Cue Type'].apply(map_tct)
    # New categorical mappings
    df['Task_2_Stimulus-Response_Mapping_Mapped'] = df['Task 2 Stimulus-Response Mapping'].apply(map_srm2)
    df['Task_2_Cue_Type_Mapped'] = df['Task 2 Cue Type'].apply(map_tct2)
    df['Trial_Transition_Type_Mapped'] = df['Trial Transition Type'].apply(map_ttt)

    # --- Step 6: Select final columns for the PCA pipeline ---
    numerical_cols = [
        'Task 2 Response Probability', 'Inter-task SOA', 'Distractor SOA',
        'Task 1 CSI', 'Task 2 CSI',
        'RSI', 'Switch Rate', 'Task 1 Difficulty Norm', 'Task 2 Difficulty Norm', 
    ]
    categorical_cols = [ 'Inter_task_SOA_is_NA', 'Distractor_SOA_is_NA', 'Task_2_CSI_is_NA', 'Task_2_Difficulty_is_NA',
        'Stimulus_Stimulus_Congruency_Mapped', 'Stimulus_Response_Congruency_Mapped',
        'Response_Set_Overlap_Mapped', 'RSI is Predictable',
        'Task_1_Stimulus-Response_Mapping_Mapped', 'Task_1_Cue_Type_Mapped',
        'Task_2_Stimulus-Response_Mapping_Mapped', 'Task_2_Cue_Type_Mapped',
        'Trial_Transition_Type_Mapped'
    ]
    
    df_pca_features = df[numerical_cols + categorical_cols]
    
    # Rename columns for clarity in pipeline/loadings output
    df_pca_features = df_pca_features.rename(columns={
        'Task 1 Difficulty Norm': 'Task 1 Difficulty',
        'Task 2 Difficulty Norm': 'Task 2 Difficulty'
    })
    # Update the list of numerical columns to match the renamed columns
    numerical_cols = [name.replace(' Norm', '') if 'Norm' in name else name for name in numerical_cols]

    return df_pca_features, numerical_cols, categorical_cols, df

def preprocess_for_mofa(df_raw):
    df_pca_features, numerical_cols, categorical_cols, df = preprocess(df_raw, target="mofa")

    preprocessor = InvertibleColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', drop='if_binary'), categorical_cols)
        ],
        remainder='drop'
    )

    df_mofa = preprocessor.fit_transform(df_pca_features)
    column_names = preprocessor.get_feature_names_out()
    df_mofa = pd.DataFrame(df_mofa, columns=column_names)
    df_mofa['Experiment'] = df_raw['Experiment']

    value_vars = list(FEATURE_TO_VIEW.keys()) # All columns that are features
    
    df_long = pd.melt(df_mofa, id_vars=['Experiment'], value_vars=column_names,
                      var_name='feature', value_name='value')
    
    # --- Step 4: Add 'view' and 'group' columns ---
    df_long['view'] = df_long['feature'].map(FEATURE_TO_VIEW)
    # Commented out: use paradigm classification for the 'group' column
    # this is commented out because grouping them by paradigm yields no factors
    #df_temp_for_group = df_pca_features.set_index('Experiment')
    #df_long['group'] = df_long['Experiment'].apply(lambda x: classify_paradigm(df_temp_for_group.loc[x]))
    df_long['group'] = 'all_studies'
    df_pca_features['Experiment'] = df_raw['Experiment']
    df_long.rename(columns={'Experiment': 'sample'}, inplace=True)
    
    # --- Step 5: Final Cleanup ---
    df_long.dropna(subset=['value', 'view'], inplace=True)
    df_long['value'] = pd.to_numeric(df_long['value'])

    # --- Step 6: Define Likelihoods ---
    # For now, let's start with gaussian for all views
    # The order must be alphabetical by view name
    views_ordered = sorted(df_long['view'].unique())
    likelihoods = ['gaussian'] * len(views_ordered)

    return df_long, preprocessor, likelihoods

    return df_mofa, preprocessor



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
            ('cat', OneHotEncoder(handle_unknown='ignore', drop='if_binary'), categorical_cols)
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

def reconstruct_from_mofa_factors(factor_scores, model, preprocessor):
    """
    Reconstructs the original feature space from MOFA+ factor scores.

    Args:
        factor_scores (pd.DataFrame or pd.Series): A dataframe or series of factor scores for one or more samples.
        model (mfx.mofa_model): The trained mofax model.
        preprocessor (InvertibleColumnTransformer): The *fitted* preprocessor from the pipeline.

    Returns:
        pd.DataFrame: A DataFrame with the de-normalized and decoded original parameters.
    """
    # Ensure factor_scores is a 2D array for matrix multiplication
    if isinstance(factor_scores, pd.Series):
        factor_scores = factor_scores.to_frame().T
        
    Z = factor_scores.values
    W = model.get_weights(df=True) # Get weights as a DataFrame

    # --- THE CRITICAL FIX ---
    # 1. Get the exact feature order the preprocessor expects.
    expected_feature_order = preprocessor.get_feature_names_out()

    # 2. Re-index the weight matrix to match the preprocessor's order.
    #    This ensures the columns of W.T are aligned before multiplication.
    W_aligned = W.reindex(expected_feature_order)

    # 3. Perform the dot product. The resulting numpy array's columns
    #    are now implicitly in the correct order for the preprocessor.
    # 1. Reconstruct. The result is a DataFrame with the right columns but a default integer index.
    reconstructed_df = Z @ W_aligned.T

    # 2. CRITICAL: Assign the correct experiment name(s) as the index.
    reconstructed_df.index = factor_scores.index

    # 3. Now the DataFrame is perfect. Pass it to the inverse_transform method.
    reconstructed_original_data = preprocessor.inverse_transform(reconstructed_df)
    # --- END OF DEBUGGING BLOCK ---

    # Reconstruct the preprocessed data space

    # Use the preprocessor to inverse transform back to the original space
    #reconstructed_original_data = preprocessor.inverse_transform(reconstructed_data_array)

    # Return as a nice DataFrame
    return pd.DataFrame(reconstructed_original_data, 
                        columns=preprocessor.feature_names_in_, 
                        index=factor_scores.index)

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
