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

        # Heuristic 5: If Distractor SOA has a value, Stimulus Valency should be Bivalent.
        if pd.notna(row.get('Distractor SOA')) and row.get('Distractor SOA') != 'N/A' and 'Bivalent' not in str(row.get('Stimulus Valency')):
            logger.warning(f"Warning: Distractor SOA has a value but Stimulus Valency is not Bivalent in experiment {exp_name}.")


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
        return 'Dual-Task/PRP'

    # 2. For single-response paradigms, task-switching is the next major category.
    if row['Switch Rate'] > 0:
        return 'Task Switching'

    # At this point, we know T2RP == 0 and Switch Rate == 0.
    # The remaining paradigms are distinguished by stimulus valency.

    # 3. Interference tasks are non-switching, single-response tasks with a bivalent stimulus.
    if 'Bivalent' in str(row['Stimulus Valency']):
        return 'Interference'

    # 4. Pure single-task baselines are non-switching, single-response tasks with a univalent stimulus.
    if 'Univalent' in str(row['Stimulus Valency']):
        return 'Single-Task'

    # 5. 'Other' serves as a fallback for any combinations not explicitly defined.
    return 'Other'

def map_valency(val):
    val_str = str(val).lower()
    if 'univalent' in val_str: return 'SBC_Univalent'
    # CORRECTED BUG: 'incongruent' should map to Incongruent
    if 'incongruent' in val_str: return 'SBC_Bivalent_Incongruent'
    # CORRECTED BUG: 'congruent' should map to Congruent
    if 'congruent' in val_str: return 'SBC_Bivalent_Congruent'
    if 'neutral' in val_str: return 'SBC_Bivalent_Neutral'
    return 'SBC_NA'

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
    valency_reverse_map = {
        'SBC_Univalent': 'Univalent',
        'SBC_Bivalent_Congruent': 'Bivalent-Congruent',
        'SBC_Bivalent_Incongruent': 'Bivalent-Incongruent',
        'SBC_Bivalent_Neutral': 'Bivalent-Neutral',
        'SBC_NA': 'N/A'
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
    if 'Task_1_Stimulus-Response_Mapping_Mapped' in df_out.columns:
        df_out['Task 1 Stimulus-Response Mapping'] = df_out['Task_1_Stimulus-Response_Mapping_Mapped'].map(srm_reverse_map)
    if 'Task_2_Stimulus-Response_Mapping_Mapped' in df_out.columns:
        df_out['Task 2 Stimulus-Response Mapping'] = df_out['Task_2_Stimulus-Response_Mapping_Mapped'].map(srm2_reverse_map)
    if 'Stimulus_Valency_Mapped' in df_out.columns:
        df_out['Stimulus Valency'] = df_out['Stimulus_Valency_Mapped'].map(valency_reverse_map)
    if 'Response_Set_Overlap_Mapped' in df_out.columns:
        df_out['Response Set Overlap'] = df_out['Response_Set_Overlap_Mapped'].map(rso_reverse_map)
    if 'Trial_Transition_Type_Mapped' in df_out.columns:
        df_out['Trial Transition Type'] = df_out['Trial_Transition_Type_Mapped'].map(ttt_reverse_map)
    if 'Task_1_Cue_Type_Mapped' in df_out.columns:
        df_out['Task 1 Cue Type'] = df_out['Task_1_Cue_Type_Mapped'].map(tct_reverse_map)
    if 'Task_2_Cue_Type_Mapped' in df_out.columns:
        df_out['Task 2 Cue Type'] = df_out['Task_2_Cue_Type_Mapped'].map(tct2_reverse_map)

    # Handle the binary predictable RSI
    if 'RSI_Is_Predictable' in df_out.columns:
         df_out['RSI Is Predictable'] = df_out['RSI_Is_Predictable'].apply(lambda x: 'Yes' if round(x) == 1 else 'No')

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
    T2RP_THRESHOLD = 0.5

    # Identify rows that represent functionally single-task paradigms
    is_single_task = sum([df_out['Task 2 Response Probability'] < T2RP_THRESHOLD,
                          df_out['Trial Transition Type'] == 'Pure',
                          df_out['Response Set Overlap'] == 'N/A',
                          df_out['Task 2 Difficulty'] < 1,
                          df_out['Task 2 Cue Type'] == 'N/A']) > 3
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

def preprocess_for_pca(df_raw):
    """
    Performs all preprocessing steps to prepare the raw DataFrame for PCA.
    Returns:
        - df_pca_features: DataFrame ready to be fed into the PCA pipeline.
        - numerical_cols: List of numerical column names.
        - categorical_cols: List of mapped categorical column names.
        - df_processed: The fully cleaned and annotated DataFrame for visualization.
    """
    logger = logging.getLogger(__name__)
    df = df_raw.copy()

    # --- Step 0: Rename old columns for clarity BEFORE any processing ---
    df.rename(columns={
        'Stimulus Response Mapping': 'Task 1 Stimulus-Response Mapping',
        'Task Cue Type': 'Task 1 Cue Type',
        'CSI': 'Task 1 CSI'
    }, inplace=True)

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
    if 'RSI' in df.columns:
        rsi_median = df['RSI'].median()
        df['RSI'] = df['RSI'].fillna(rsi_median)

    # --- Step 2: Validate data and log warnings ---
    validate_and_log_warnings(df, logger)

    # --- Step 3: Add Paradigm Classification for Difficulty Placeholder and Plotting ---
    df['Paradigm'] = df.apply(classify_paradigm, axis=1)

    # --- Step 4: Create PCA-specific features ---
    # Generate Applicability Flags DIRECTLY from NaN status.
    # This is done BEFORE imputation.
    df['Inter_task_SOA_is_NA'] = df['Inter-task SOA'].isna().astype(int)
    df['Distractor_SOA_is_NA'] = df['Distractor SOA'].isna().astype(int)

    # Impute Main SOA Columns and other numeric columns. This is now safe.
    df['Inter-task SOA'] = df['Inter-task SOA'].fillna(0)
    df['Distractor SOA'] = df['Distractor SOA'].fillna(0)
    df['Task 1 CSI'] = df['Task 1 CSI'].fillna(0)
    df['Task 2 CSI'] = df['Task 2 CSI'].fillna(0) # New

    # Process new binary 'RSI Is Predictable'
    df['RSI_Is_Predictable'] = df['RSI Is Predictable'].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)

    # Normalize Task Difficulty (1-5 scale to 0-1)
    df['Task 1 Difficulty Norm'] = (df['Task 1 Difficulty'] - 1) / 4
    df['Task 2 Difficulty Norm'] = (df['Task 2 Difficulty'] - 1) / 4
    df['Task 1 Difficulty Norm'] = df['Task 1 Difficulty Norm'].fillna(0.5) # Impute missing T1 difficulty
    
    # Set to placeholder (-1) ONLY if it's NOT a Task-Switching or Dual-Task paradigm.
    is_true_single_task = ~df['Paradigm'].isin(['Task Switching', 'Dual-Task/PRP'])
    df.loc[is_true_single_task, 'Task 2 Difficulty Norm'] = -1.0
    # For any remaining NaNs (e.g., in TS or DT where it wasn't specified), impute with moderate difficulty.
    df['Task 2 Difficulty Norm'] = df['Task 2 Difficulty Norm'].fillna(0.5)

    # --- Step 5: Map Categorical Features ---
    df['Stimulus_Valency_Mapped'] = df['Stimulus Valency'].apply(map_valency)
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
        'Inter_task_SOA_is_NA', 'Distractor_SOA_is_NA', 'Task 1 CSI', 'Task 2 CSI',
        'RSI', 'Switch Rate', 'Task 1 Difficulty Norm', 'Task 2 Difficulty Norm',
        'RSI_Is_Predictable'
    ]
    categorical_cols = [
        'Stimulus_Valency_Mapped', 'Response_Set_Overlap_Mapped',
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
            transformed_slice = X[:, col_idx : col_idx + n_transformed_features]
            
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
