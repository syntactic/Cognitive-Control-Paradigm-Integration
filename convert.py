import pandas as pd
import json
import numpy as np
import argparse
import logging

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
    if 'param_overrides' in notes and param_name in notes['param_overrides']:
        override_value = notes['param_overrides'][param_name]
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

def process_condition(row):
    """
    Takes a row from the conceptual CSV and returns a dictionary of
    resolved, absolute parameters for the new CSV.
    """
    notes = parse_notes(row.get('Super_Experiment_Mapping_Notes'))

    # --- 1. Determine base durations and offsets, allowing for overrides ---
    # Default values can be overridden by the JSON in the notes column.
    TRIAL_START_OFFSET = 1000  # Default start time for the first event
    BASE_STIM_DURATION = get_param(row, notes, 'base_stim_duration', 2000)
    BASE_CUE_GO_DURATION = get_param(row, notes, 'base_cue_go_duration', BASE_STIM_DURATION)

    # Allow separate duration overrides for T1 and T2
    t1_stim_duration = get_param(row, notes, 't1_stim_duration', BASE_STIM_DURATION)
    t2_stim_duration = get_param(row, notes, 't2_stim_duration', BASE_STIM_DURATION)
    t1_cue_go_duration = get_param(row, notes, 't1_cue_go_duration', BASE_CUE_GO_DURATION)
    t2_cue_go_duration = get_param(row, notes, 't2_cue_go_duration', BASE_CUE_GO_DURATION)

    # --- 2. Pre-process conceptual info to be passed to the client ---
    resolved_params = {
        'Experiment': row['Experiment'],
        'Task_1_Type': row['Task 1 Type'],
        'Task_2_Type': row['Task 2 Type'],
        'Stimulus_Valency': row['Stimulus Valency'],
        'Simplified_RSO': simplify_response_set_overlap(row['Response Set Overlap']),
        'SRM': row['Stimulus Response Mapping'],
        'Switch_Rate_Percent': row['Switch Rate'].replace('%', '') if isinstance(row['Switch Rate'], str) else row['Switch Rate'],
        'Sequence_Type': notes.get('sequence_type', 'Random'),
        'ITI_ms': row.get('RSI'),
        'ITI_Distribution_Type': notes.get('RSI_distribution', 'fixed'),
        'ITI_Distribution_Params': str(notes.get('RSI_range', notes.get('RSI_values', []))),
        'coh_1': difficulty_to_coherence(row['Task 1 Difficulty']),
        'coh_2': difficulty_to_coherence(row['Task 2 Difficulty']),
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
        
    # --- 3. Calculate Absolute Timings based on N_Tasks ---
    n_tasks = int(row['Number of Tasks'])
    soa = 0 if pd.isna(row['SOA']) else int(row['SOA'])
    csi = 0 if pd.isna(row['CSI']) else int(row['CSI'])

    if n_tasks == 2:
        # Standard Dual-Task / PRP paradigm
        # T1 -> mov pathway, T2 -> or pathway
        
        # T1 Events
        t1_stim_start = TRIAL_START_OFFSET
        resolved_params['effective_start_stim1_mov'] = t1_stim_start
        resolved_params['effective_end_stim1_mov'] = t1_stim_start + t1_stim_duration
        
        resolved_params['effective_start_cue1'] = t1_stim_start - csi
        resolved_params['effective_end_cue1'] = resolved_params['effective_start_cue1'] + t1_cue_go_duration
        resolved_params['effective_start_go1'] = resolved_params['effective_start_cue1']
        resolved_params['effective_end_go1'] = resolved_params['effective_end_cue1']

        # T2 Events
        t2_stim_start = t1_stim_start + soa
        resolved_params['effective_start_stim1_or'] = t2_stim_start
        resolved_params['effective_end_stim1_or'] = t2_stim_start + t2_stim_duration
        
        resolved_params['effective_start_cue2'] = t2_stim_start - csi
        resolved_params['effective_end_cue2'] = resolved_params['effective_start_cue2'] + t2_cue_go_duration
        resolved_params['effective_start_go2'] = resolved_params['effective_start_cue2']
        resolved_params['effective_end_go2'] = resolved_params['effective_end_cue2']
        
    elif n_tasks == 1:
        # Single-Task / Task-Switching / Interference paradigm
        # Target -> mov pathway, Distractor -> or pathway
        
        # Target Events
        target_stim_start = TRIAL_START_OFFSET
        resolved_params['effective_start_stim1_mov'] = target_stim_start
        resolved_params['effective_end_stim1_mov'] = target_stim_start + t1_stim_duration
        
        resolved_params['effective_start_cue1'] = target_stim_start - csi
        resolved_params['effective_end_cue1'] = resolved_params['effective_start_cue1'] + t1_cue_go_duration
        resolved_params['effective_start_go1'] = resolved_params['effective_start_cue1']
        resolved_params['effective_end_go1'] = resolved_params['effective_end_cue1']
        
        # Distractor Events (if stimulus is bivalent)
        if 'Bivalent' in str(row['Stimulus Valency']):
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
    if args.verbose:
        logger = setup_logger()
        logger.info("Verbose logging enabled.")
    try:
        # Load the source CSV file
        source_df = pd.read_csv('data/super_experiment_design_space.csv')
        print(f"Loaded {len(source_df)} conditions from the source CSV.")
        
        # List to hold all the processed condition dictionaries
        resolved_conditions = []
        
        # Loop and process each row
        for index, row in source_df.iterrows():
            resolved_row = process_condition(row)
            resolved_conditions.append(resolved_row)
            
        # Create the final DataFrame
        resolved_df = pd.DataFrame(resolved_conditions)
        
        # Define the final column order for the output CSV
        final_column_order = [
            'Experiment', 'Task_1_Type', 'Task_2_Type',
            'Stimulus_Valency', 'Simplified_RSO', 'SRM',
            'Switch_Rate_Percent', 'Sequence_Type', 'ITI_Distribution_Type',
            'ITI_Distribution_Params', 'ITI_ms',
            'coh_1', 'coh_2',
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
