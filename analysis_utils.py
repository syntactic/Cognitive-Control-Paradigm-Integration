# analysis_utils.py

import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA

# =============================================================================
# 1. Helper Functions for Data Cleaning
# =============================================================================

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
    """Classifies each experimental condition into a broader paradigm class."""
    if row['Number of Tasks'] == 2:
        return 'Dual-Task/PRP'
    if row['Switch Rate'] > 0:
        return 'Task Switching'
    # Use a more robust check for 'Interference'
    if row['Number of Tasks'] == 1 and 'Bivalent' in str(row['Stimulus Valency']):
        return 'Interference'
    return 'Other'

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
    df = df_raw.copy()

    # --- Step 1: General Cleaning ---
    df['Number of Tasks'] = pd.to_numeric(df['Number of Tasks'], errors='coerce')
    df['SOA'] = pd.to_numeric(df['SOA'], errors='coerce')
    df['CSI'] = pd.to_numeric(df['CSI'], errors='coerce')
    df['Task 1 Difficulty'] = pd.to_numeric(df['Task 1 Difficulty'], errors='coerce')
    df['Task 2 Difficulty'] = pd.to_numeric(df['Task 2 Difficulty'], errors='coerce')
    df['RSI'] = df['RSI'].apply(clean_rsi)
    df['Switch Rate'] = df['Switch Rate'].apply(clean_switch_rate)

    rsi_median = df['RSI'].median()
    df['RSI'].fillna(rsi_median, inplace=True)


    # --- Step 2: Add Paradigm Classification for Difficulty Placeholder and Plotting ---
    df['Paradigm'] = df.apply(classify_paradigm, axis=1)

    # --- Step 3: Create PCA-specific features ---
    # Create a binary indicator for whether SOA was applicable
    df['SOA_is_NA'] = df['SOA'].isna().astype(int)
    # Impute N/A SOAs with 0, as this is the most neutral value
    df['SOA'].fillna(0, inplace=True)
    df['CSI'].fillna(0, inplace=True)

    # Normalize Task Difficulty (1-5 scale to 0-1)
    df['Task 1 Difficulty Norm'] = (df['Task 1 Difficulty'] - 1) / 4
    df['Task 2 Difficulty Norm'] = (df['Task 2 Difficulty'] - 1) / 4
    df['Task 1 Difficulty Norm'].fillna(0.5, inplace=True) # Impute missing T1 difficulty
    # Set to placeholder (-1) ONLY if it's NOT a Task-Switching or Dual-Task paradigm.
    # For Interference tasks, there is truly no 'Task 2'.
    is_true_single_task = ~df['Paradigm'].isin(['Task Switching', 'Dual-Task/PRP'])
    df.loc[is_true_single_task, 'Task 2 Difficulty Norm'] = -1.0
    # For any remaining NaNs (e.g., in TS or DT where it wasn't specified), impute with moderate difficulty.
    df['Task 2 Difficulty Norm'].fillna(0.5, inplace=True)

    # --- Step 4: Map Categorical Features ---
    def map_valency(val):
        val_str = str(val).lower()
        if 'univalent' in val_str: return 'SBC_Univalent'
        # CORRECTED BUG: 'incongruent' should map to Incongruent
        if 'incongruent' in val_str: return 'SBC_Bivalent_Incongruent'
        # CORRECTED BUG: 'congruent' should map to Congruent
        if 'congruent' in val_str: return 'SBC_Bivalent_Congruent'
        if 'neutral' in val_str: return 'SBC_Bivalent_Neutral'
        return 'SBC_NA'
    df['Stimulus_Valency_Mapped'] = df['Stimulus Valency'].apply(map_valency)

    def map_rso(val):
        val_str = str(val).lower()
        if 'identical' in val_str: return 'RSO_Identical'
        if 'disjoint' in val_str: return 'RSO_Disjoint'
        return 'RSO_NA'
    df['Response_Set_Overlap_Mapped'] = df['Response Set Overlap'].apply(map_rso)

    def map_srm(val):
        val_str = str(val).lower()
        if 'incompatible' in val_str: return 'SRM_Incompatible'
        if 'compatible' in val_str: return 'SRM_Compatible'
        if 'arbitrary' in val_str: return 'SRM_Arbitrary'
        return 'SRM_NA'
    df['Stimulus_Response_Mapping_Mapped'] = df['Stimulus Response Mapping'].apply(map_srm)

    def map_tct(val):
        """Maps the Task Cue Type column to simplified categories."""
        val_str = str(val).lower()
        if 'arbitrary' in val_str:
            return 'TCT_Arbitrary'
        if 'none/implicit' in val_str:
            return 'TCT_Implicit'
        # Default any other cases (like NaN or unexpected values) to Implicit
        return 'TCT_Implicit'
    
    df['Task_Cue_Type_Mapped'] = df['Task Cue Type'].apply(map_tct)

    # --- Step 5: Select final columns for the PCA pipeline ---
    numerical_cols = ['Number of Tasks', 'SOA_is_NA', 'SOA', 'CSI', 'RSI', 'Switch Rate', 'Task 1 Difficulty Norm', 'Task 2 Difficulty Norm']
    categorical_cols = ['Stimulus_Valency_Mapped', 'Response_Set_Overlap_Mapped', 'Stimulus_Response_Mapping_Mapped', 'Task_Cue_Type_Mapped']
    
    df_pca_features = df[numerical_cols + categorical_cols]
    
    # Rename columns for clarity in pipeline
    df_pca_features = df_pca_features.rename(columns={
        'Task 1 Difficulty Norm': 'Task 1 Difficulty',
        'Task 2 Difficulty Norm': 'Task 2 Difficulty'
    })
    numerical_cols = ['Number of Tasks', 'SOA_is_NA', 'SOA', 'CSI', 'RSI', 'Switch Rate', 'Task 1 Difficulty', 'Task 2 Difficulty']

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
    
    """# Get the feature names from the preprocessor step
    preprocessor = pipeline.named_steps['preprocessor']
    num_features = preprocessor.named_transformers_['num'].get_feature_names_out()
    cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out()
    
    # Create a DataFrame to hold the results
    result_df = pd.DataFrame(original_space_point, columns=list(num_features) + list(cat_features))
    
    # --- Decode the one-hot encoded columns ---
    decoded_params = {}
    
    # Decode each categorical variable by finding the argmax
    for original_col_name in preprocessor.named_transformers_['cat'].feature_names_in_:
        # Find all columns related to this original categorical variable
        related_cols = [c for c in cat_features if c.startswith(original_col_name)]
        
        # Get the values for these columns
        values = result_df[related_cols].iloc[0]
        
        # Find the column with the max value (this is our predicted category)
        if not values.empty:
            best_category_col = values.idxmax()
            # Extract the category name from the column name
            decoded_params[original_col_name] = best_category_col.split('_', 1)[1]
        else:
            # Handle binary 'drop=if_binary' case
            # If the column was dropped, we check if the remaining one is > 0.5
            # This logic is complex, simpler to just report the one column for now
            pass
            
    # Combine numerical and decoded categorical results
    final_params = result_df[list(num_features)].iloc[0].to_dict()
    final_params.update(decoded_params)
    
    return pd.Series(final_params)"""
