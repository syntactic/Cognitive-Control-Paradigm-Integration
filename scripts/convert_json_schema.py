#!/usr/bin/env python3
"""
One-off script to convert Super_Experiment_Mapping_Notes from old schema to new schema.

Old schema:
{
  "param_overrides": { ... },
  "sequence_type": "...",
  "RSI_distribution": "...",
  "RSI_range": [...],
  ...
}

New schema:
{
  "block_id": "...",
  "description": "...",
  "convert_overrides": { ... },
  "viewer_config": {
    "sequence_type": "...",
    "ITI_distribution": "...",
    "ITI_range": [...],
    ...
  }
}
"""

import pandas as pd
import json
import argparse
from pathlib import Path

def is_old_schema(notes_dict):
    """Check if a notes dictionary uses the old schema."""
    if not notes_dict:
        return False
    
    # Old schema indicators
    old_keys = ['param_overrides', 'sequence_type', 'RSI_distribution', 'RSI_range', 'RSI_values', 'SOA_distribution', 'SOA_range', 'SOA_values']
    
    # New schema indicators  
    new_keys = ['convert_overrides', 'viewer_config', 'block_id', 'description']
    
    has_old = any(key in notes_dict for key in old_keys)
    has_new = any(key in notes_dict for key in new_keys)
    
    # If it has old keys but not new structure, it's old schema
    return has_old and not has_new

def convert_to_new_schema(old_notes):
    """Convert old schema JSON to new schema."""
    if not old_notes:
        return {}
    
    new_notes = {}
    
    # Convert param_overrides to convert_overrides
    if 'param_overrides' in old_notes:
        new_notes['convert_overrides'] = old_notes['param_overrides']
    
    # Create viewer_config section
    viewer_config = {}
    
    # Map old top-level keys to viewer_config
    viewer_mappings = {
        'sequence_type': 'sequence_type',
        'RSI_distribution': 'ITI_distribution',  # RSI -> ITI mapping
        'RSI_range': 'ITI_range',
        'RSI_values': 'ITI_values', 
        'SOA_distribution': 'SOA_distribution',
        'SOA_range': 'SOA_range',
        'SOA_values': 'SOA_values'
    }
    
    for old_key, new_key in viewer_mappings.items():
        if old_key in old_notes:
            viewer_config[new_key] = old_notes[old_key]
    
    if viewer_config:
        new_notes['viewer_config'] = viewer_config
    
    # Add placeholders for new required fields (user can fill these in manually)
    # We don't add empty strings here since they would become the defaults
    
    return new_notes

def parse_notes_safely(notes_str):
    """Safely parse JSON from notes column."""
    if pd.isna(notes_str) or not isinstance(notes_str, str) or not notes_str.strip():
        return {}
    
    try:
        return json.loads(notes_str.strip('"'))
    except (json.JSONDecodeError, TypeError):
        return {}

def main():
    parser = argparse.ArgumentParser(description="Convert Super_Experiment_Mapping_Notes from old schema to new schema")
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output CSV file path (default: input_file with _converted suffix)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be converted without writing output')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist.")
        return 1
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(f"{input_path.stem}_converted{input_path.suffix}")
    
    print(f"Reading CSV from: {input_path}")
    
    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return 1
    
    if 'Super_Experiment_Mapping_Notes' not in df.columns:
        print("Error: 'Super_Experiment_Mapping_Notes' column not found in CSV.")
        return 1
    
    print(f"Found {len(df)} rows in CSV")
    
    # Track conversion statistics
    converted_count = 0
    skipped_count = 0
    error_count = 0
    
    # Process each row
    for idx, row in df.iterrows():
        notes_str = row['Super_Experiment_Mapping_Notes']
        
        # Parse the existing JSON
        old_notes = parse_notes_safely(notes_str)
        
        if not old_notes:
            # Empty or invalid JSON, skip
            skipped_count += 1
            continue
            
        # Check if it's old schema
        if not is_old_schema(old_notes):
            # Already new schema or unrecognized format, skip
            skipped_count += 1
            continue
        
        try:
            # Convert to new schema
            new_notes = convert_to_new_schema(old_notes)
            new_json_str = json.dumps(new_notes, separators=(',', ':'))
            
            if args.dry_run:
                print(f"\nRow {idx} - Experiment: {row.get('Experiment', 'N/A')}")
                print(f"  Old: {json.dumps(old_notes, separators=(',', ':'))}")
                print(f"  New: {new_json_str}")
            else:
                # Update the DataFrame
                df.at[idx, 'Super_Experiment_Mapping_Notes'] = new_json_str
            
            converted_count += 1
            
        except Exception as e:
            print(f"Error converting row {idx}: {e}")
            error_count += 1
    
    # Print summary
    print(f"\nConversion Summary:")
    print(f"  Rows converted: {converted_count}")
    print(f"  Rows skipped: {skipped_count}")
    print(f"  Errors: {error_count}")
    
    if args.dry_run:
        print(f"\nDry run complete. No files were modified.")
        return 0
    
    if converted_count == 0:
        print("No rows were converted. Output file not created.")
        return 0
    
    # Write the updated CSV
    try:
        df.to_csv(output_path, index=False)
        print(f"\nConverted CSV written to: {output_path}")
        print(f"You can now manually review and integrate this file back into your Excel sheet.")
    except Exception as e:
        print(f"Error writing output CSV: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())