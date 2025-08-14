import pandas as pd
import json
import numpy as np
import argparse
import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def setup_logger(level=logging.INFO):
    """
    Configures a basic logger to print to the console.
    """
    # Get the same logger instance used throughout the script
    log = logging.getLogger(__name__)
    log.setLevel(level)
    
    # Avoid adding handlers multiple times
    if not log.handlers or isinstance(log.handlers[0], logging.NullHandler):
        # Clear existing NullHandler if it exists
        log.handlers = []
        
        # Create a handler to write to the console (stderr by default)
        handler = logging.StreamHandler()
        
        # Create a simple formatter
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add the handler to the logger
        log.addHandler(handler)
    return log

def parse_notes(notes_str):
    """
    Safely parses a JSON string from the notes column.
    Returns an empty dictionary if the string is not valid JSON, empty, or NaN.
    """
    if pd.isna(notes_str) or not isinstance(notes_str, str):
        return {}
    try:
        # The notes might be enclosed in extra quotes, so we strip them
        return json.loads(notes_str.strip('"'))
    except (json.JSONDecodeError, TypeError):
        # If it fails, it's likely a plain text note, which we ignore for overrides.
        return {}

def get_param(row, notes, param_name, default_value):
    """
    Gets a parameter for the current condition, prioritizing JSON overrides.
    """
    if 'convert_overrides' in notes and param_name in notes['convert_overrides']:
        override_value = notes['convert_overrides'][param_name]
        logger.info(
            f"Experiment '{row.get('Experiment', 'N/A')}': Overriding '{param_name}'. "
            f"Default: {default_value}, New: {override_value}"
        )
        return override_value
    return default_value

def difficulty_to_coherence(difficulty):
    """
    Converts a 1-5 difficulty rating to a 0-1 coherence value for SE.
    1 (Very Low Difficulty) -> 1.0 coh
    5 (Very High Difficulty) -> 0.0 coh
    """
    if pd.isna(difficulty) or not (1 <= difficulty <= 5):
        # Default to moderate difficulty if not specified
        return 0.5 
    
    # Linear mapping: (5 - difficulty) / 4
    return (5 - float(difficulty)) / 4.0

def simplify_response_set_overlap(rso_string):
    """
    Simplifies the detailed RSO from literature into categories SE can handle.
    SE cannot distinguish different modalities (vocal vs manual) or effectors.
    The key distinction it can model is whether the response keys are the same
    or different for the two conceptual tasks.
    """
    if pd.isna(rso_string):
        return 'N/A'
    
    rso_lower = rso_string.lower()
    
    if 'identical' in rso_lower:
        return 'Identical'
    elif 'disjoint' in rso_lower:
        return 'Disjoint'
    else:
        return 'N/A'

def validate_block_configurations(df):
    """
    Validates that conditions within the same Block_ID have consistent viewer_config.
    Logs detailed warnings for any inconsistencies found.
    
    Args:
        df: pandas DataFrame with condition data
        
    Returns:
        bool: True if validation passes (no critical errors), False if processing should halt
    """
    if df.empty:
        return True
        
    # Group by Block_ID, extracting it from the JSON notes
    blocks = {}
    
    for index, row in df.iterrows():
        notes = parse_notes(row.get('Super_Experiment_Mapping_Notes', ''))
        block_id = notes.get('block_id', '')
        
        # Skip empty block IDs or use experiment name as fallback
        if not block_id:
            block_id = row['Experiment']
            
        if block_id not in blocks:
            blocks[block_id] = []
            
        blocks[block_id].append({
            'index': index,
            'experiment': row['Experiment'],
            'viewer_config': notes.get('viewer_config', {}),
            'viewer_config_str': str(notes.get('viewer_config', {}))
        })
    
    # Validate each block with multiple conditions
    validation_passed = True
    warnings_found = False
    
    for block_id, conditions in blocks.items():
        if len(conditions) <= 1:
            continue  # Single-condition blocks don't need validation
            
        primary_condition = conditions[0]
        primary_config_str = primary_condition['viewer_config_str']
        
        # Check each subsequent condition for inconsistencies
        for i, condition in enumerate(conditions[1:], start=1):
            current_config_str = condition['viewer_config_str']
            
            # Only warn if current condition has a config AND it's different from primary
            if (current_config_str != '{}' and 
                current_config_str != primary_config_str):
                
                logger.warning(
                    f"Row {condition['index'] + 2}: Inconsistent viewer_config found for Block_ID '{block_id}'. "
                    f"Primary condition '{primary_condition['experiment']}' (row {primary_condition['index'] + 2}) "
                    f"has config: {primary_config_str}, but condition '{condition['experiment']}' "
                    f"has different config: {current_config_str}. "
                    f"Using configuration from primary condition."
                )
                warnings_found = True
    
    if warnings_found:
        logger.info("Block validation completed with warnings. Primary condition rule will be enforced in viewer.")
    else:
        logger.info("Block validation passed - no configuration inconsistencies found.")
        
    return validation_passed

def process_condition(row):
    """
    Takes a row from the conceptual CSV and returns a dictionary of
    resolved, absolute parameters for the new CSV.
    """
    notes = parse_notes(row.get('Super_Experiment_Mapping_Notes'))

    # --- 1. Determine base durations and offsets, allowing for overrides ---
    # Default values can be overridden by the JSON in the notes column.
    TRIAL_START_OFFSET = 0  # Default start time for the first event
    BASE_STIM_DURATION = get_param(row, notes, 'base_stim_duration', 2000)
    BASE_CUE_GO_DURATION = get_param(row, notes, 'base_cue_go_duration', BASE_STIM_DURATION)

    # Allow separate duration overrides for T1 and T2
    t1_stim_duration = get_param(row, notes, 't1_stim_duration', BASE_STIM_DURATION)
    t2_stim_duration = get_param(row, notes, 't2_stim_duration', BASE_STIM_DURATION)
    t1_cue_go_duration = get_param(row, notes, 't1_cue_go_duration', BASE_CUE_GO_DURATION)
    t2_cue_go_duration = get_param(row, notes, 't2_cue_go_duration', BASE_CUE_GO_DURATION)

    # --- 2. Derive backwards-compatible Stimulus_Valency ---
    ss_congruency = row['Stimulus-Stimulus Congruency']
    sr_congruency = row['Stimulus-Response Congruency']
    derived_stimulus_valency = 'Univalent' # Default

    if ss_congruency == 'Congruent':
        derived_stimulus_valency = 'Bivalent-Congruent'
    elif ss_congruency == 'Incongruent':
        derived_stimulus_valency = 'Bivalent-Incongruent'
    elif ss_congruency == 'Neutral':
        derived_stimulus_valency = 'Bivalent-Neutral'
    elif ss_congruency == 'N/A':
        if sr_congruency in ['Congruent', 'Incongruent', 'Neutral']:
            # Abstracting pure S-R conflict as Bivalent-Neutral for the viewer
            derived_stimulus_valency = 'Bivalent-Neutral'

    # --- 3. Extract metadata from JSON notes ---
    viewer_config = notes.get('viewer_config', {})
    
    # Extract metadata with defaults
    block_id = notes.get('block_id', '')
    description = notes.get('description', '')
    sequence_type = viewer_config.get('sequence_type', 'Random')
    iti_distribution_type = viewer_config.get('ITI_distribution', 'fixed')
    iti_distribution_params = str(viewer_config.get('ITI_range', viewer_config.get('ITI_values', [])))
    soa_distribution_type = viewer_config.get('SOA_distribution', 'fixed')
    soa_distribution_params = str(viewer_config.get('SOA_range', viewer_config.get('SOA_values', [])))
    
    # --- 4. Pre-process conceptual info to be passed to the client ---
    task_2_prob = float(row['Task 2 Response Probability'])
    n_tasks = 2 if task_2_prob == 1.0 else 1
    
    resolved_params = {
        'Experiment': row['Experiment'],
        'N_Tasks': n_tasks,
        'Task_1_Type': row['Task 1 Type'],
        'Task_2_Type': row['Task 2 Type'],
        'Stimulus_Valency': derived_stimulus_valency, # Use the derived value
        'Simplified_RSO': simplify_response_set_overlap(row['Response Set Overlap']),
        'SRM_1': row['Task 1 Stimulus-Response Mapping'],
        'SRM_2': row['Task 2 Stimulus-Response Mapping'],
        'Switch_Rate_Percent': row['Switch Rate'].replace('%', '') if isinstance(row['Switch Rate'], str) else row['Switch Rate'],
        'Block_ID': block_id,
        'Description': description,
        'Sequence_Type': sequence_type,
        'RSI_Distribution_Type': iti_distribution_type,
        'RSI_Distribution_Params': iti_distribution_params,
        'SOA_Distribution_Type': soa_distribution_type,
        'SOA_Distribution_Params': soa_distribution_params,
        'ITI_ms': row.get('RSI'),
        'coh_1': difficulty_to_coherence(row['Task 1 Difficulty']),
        'coh_2': difficulty_to_coherence(row['Task 2 Difficulty']),
        'Trial_Transition_Type': row['Trial Transition Type'],
    }
    
    # Initialize all timing parameters to 0
    timing_keys = [
        'effective_start_cue1', 'effective_end_cue1', 'effective_start_go1', 'effective_end_go1',
        'effective_start_stim1_mov', 'effective_end_stim1_mov', 'effective_start_stim2_mov', 'effective_end_stim2_mov',
        'effective_start_cue2', 'effective_end_cue2', 'effective_start_go2', 'effective_end_go2',
        'effective_start_stim1_or', 'effective_end_stim1_or', 'effective_start_stim2_or', 'effective_end_stim2_or',
    ]
    for key in timing_keys:
        resolved_params[key] = 0
        
    # --- 4. Calculate Absolute Timings based on N_Tasks ---
    soa_str = row['Inter-task SOA'] if n_tasks == 2 else row['Distractor SOA']
    soa = 0 if pd.isna(soa_str) or soa_str == 'N/A' else int(soa_str)
    
    csi1_str = row['Task 1 CSI']
    csi2_str = row['Task 2 CSI']
    csi1 = 0 if pd.isna(csi1_str) or csi1_str == 'N/A' else int(csi1_str)
    csi2 = 0 if pd.isna(csi2_str) or csi2_str == 'N/A' else int(csi2_str)
    
    # Calculate timeline offset to ensure all timestamps are non-negative
    # When CSI is positive, cue start becomes negative, so we need to shift everything forward
    timeline_offset = max(0, csi1, csi2)  # Ensure offset handles both tasks

    if n_tasks == 2:
        # Standard Dual-Task / PRP paradigm
        # T1 -> Channel 1 mov pathway, T2 -> Channel 2 or pathway
        
        # T1 Events (Channel 1) - Apply timeline offset
        t1_stim_start = TRIAL_START_OFFSET + timeline_offset
        resolved_params['effective_start_stim1_mov'] = t1_stim_start
        resolved_params['effective_end_stim1_mov'] = t1_stim_start + t1_stim_duration
        
        resolved_params['effective_start_cue1'] = t1_stim_start - csi1
        resolved_params['effective_end_cue1'] = resolved_params['effective_start_cue1'] + t1_cue_go_duration
        resolved_params['effective_start_go1'] = resolved_params['effective_start_cue1']
        resolved_params['effective_end_go1'] = resolved_params['effective_end_cue1']

        # T2 Events (Channel 2) - FIXED: Use stim2_or instead of stim1_or
        t2_stim_start = t1_stim_start + soa
        resolved_params['effective_start_stim2_or'] = t2_stim_start
        resolved_params['effective_end_stim2_or'] = t2_stim_start + t2_stim_duration
        
        resolved_params['effective_start_cue2'] = t2_stim_start - csi2
        resolved_params['effective_end_cue2'] = resolved_params['effective_start_cue2'] + t2_cue_go_duration
        resolved_params['effective_start_go2'] = resolved_params['effective_start_cue2']
        resolved_params['effective_end_go2'] = resolved_params['effective_end_cue2']
        
    elif n_tasks == 1:
        # Single-Task / Task-Switching / Interference paradigm
        # Target -> mov pathway, Distractor -> or pathway
        
        # Target Events - Apply timeline offset
        target_stim_start = TRIAL_START_OFFSET + timeline_offset
        resolved_params['effective_start_stim1_mov'] = target_stim_start
        resolved_params['effective_end_stim1_mov'] = target_stim_start + t1_stim_duration
        
        resolved_params['effective_start_cue1'] = target_stim_start - csi1
        resolved_params['effective_end_cue1'] = resolved_params['effective_start_cue1'] + t1_cue_go_duration
        resolved_params['effective_start_go1'] = resolved_params['effective_start_cue1']
        resolved_params['effective_end_go1'] = resolved_params['effective_end_cue1']
        
        # Distractor Events (if stimulus is bivalent based on new columns)
        if row['Stimulus-Stimulus Congruency'] != 'N/A' or row['Stimulus-Response Congruency'] != 'N/A':
            distractor_stim_start = target_stim_start + soa
            resolved_params['effective_start_stim1_or'] = distractor_stim_start
            resolved_params['effective_end_stim1_or'] = distractor_stim_start + t2_stim_duration # Use T2 duration for distractor

    return resolved_params

# --- Main Execution Block ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process the Super Experiment design space into absolute parameters.")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose logging to see parameter overrides."
    )
    args = parser.parse_args()
    
    # Always set up logger for validation, use INFO level for validation messages
    logger = setup_logger(logging.INFO)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled.")
    
    try:
        # Load the source CSV file
        source_df = pd.read_csv('data/super_experiment_design_space.csv')
        print(f"Loaded {len(source_df)} conditions from the source CSV.")
        
        # Validate block configurations before processing
        logger.info("Validating block configurations...")
        if not validate_block_configurations(source_df):
            logger.error("Block validation failed. Aborting processing.")
            sys.exit(1)
        
        # List to hold all the processed condition dictionaries
        resolved_conditions = []
        
        # Loop and process each row
        for index, row in source_df.iterrows():
            resolved_row = process_condition(row)
            resolved_conditions.append(resolved_row)
            
        # Create the final DataFrame
        resolved_df = pd.DataFrame(resolved_conditions)
        
        # --- Collapse Conflict Dimensions ---
        # Add the source columns from the original dataset for conflict collapsing
        resolved_df['Stimulus-Stimulus Congruency'] = source_df['Stimulus-Stimulus Congruency']
        resolved_df['Stimulus-Response Congruency'] = source_df['Stimulus-Response Congruency']
        
        # Apply the conflict collapsing logic
        s_s_col = resolved_df['Stimulus-Stimulus Congruency']
        s_r_col = resolved_df['Stimulus-Response Congruency']
        
        conditions = [
            (s_s_col == 'Incongruent') | (s_r_col == 'Incongruent'),
            (s_s_col == 'Congruent') | (s_r_col == 'Congruent'),
            (s_s_col == 'Neutral') | (s_r_col == 'Neutral')
        ]
        
        choices = [
            'Incongruent',
            'Congruent',
            'Neutral'
        ]
        
        resolved_df['Stimulus Bivalence & Congruency'] = np.select(conditions, choices, default='N/A')
        
        # Remove the temporary source columns
        resolved_df = resolved_df.drop(columns=['Stimulus-Stimulus Congruency', 'Stimulus-Response Congruency'])
        
        # Define the final column order for the output CSV
        final_column_order = [
            'Experiment', 'N_Tasks', 'Task_1_Type', 'Task_2_Type',
            'Stimulus_Valency', 'Stimulus Bivalence & Congruency', 'Simplified_RSO', 'SRM_1', 'SRM_2',
            'Switch_Rate_Percent', 'Block_ID', 'Description', 'Sequence_Type', 
            'RSI_Distribution_Type', 'RSI_Distribution_Params', 
            'SOA_Distribution_Type', 'SOA_Distribution_Params', 'ITI_ms',
            'coh_1', 'coh_2', 'Trial_Transition_Type',
            'effective_start_cue1', 'effective_end_cue1', 'effective_start_go1', 'effective_end_go1',
            'effective_start_stim1_mov', 'effective_end_stim1_mov', 'effective_start_stim2_mov', 'effective_end_stim2_mov',
            'effective_start_cue2', 'effective_end_cue2', 'effective_start_go2', 'effective_end_go2',
            'effective_start_stim1_or', 'effective_end_stim1_or', 'effective_start_stim2_or', 'effective_end_stim2_or',
        ]
        
        # Ensure all columns exist, fill missing with 0 or a suitable default
        for col in final_column_order:
            if col not in resolved_df.columns:
                resolved_df[col] = 0
        
        resolved_df = resolved_df[final_column_order]
        
        # Save the new CSV
        output_path = 'data/resolved_design_space.csv'
        resolved_df.to_csv(output_path, index=False)
        
        print(f"\nSuccessfully processed {len(resolved_df)} conditions.")
        print(f"Saved the resolved absolute parameter space to '{output_path}'")
        
        # Display the head of the output for verification
        print("\n--- Head of the Resolved Output CSV ---")
        print(resolved_df.head().to_markdown(index=False))
        
    except FileNotFoundError:
        print("Error: 'data/super_experiment_design_space.csv' not found. Please make sure the file is in the correct directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
