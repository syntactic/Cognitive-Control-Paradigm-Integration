import pandas as pd
import re
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import analysis_utils as au

def find_paper(experiment_name):
    """
    Finds the author and year to identify the paper.
    """
    match = re.search(r'([A-Za-z\s.&]+)\s\(?(\d{4})\)?', experiment_name)
    if match:
        return f"{match.group(1).strip()} {match.group(2)}"
    return None

def get_block_id(row):
    """
    Extracts the block_id from the 'Super_Experiment_Mapping_Notes' column.
    If the column is empty or does not contain a 'block_id', it generates a unique ID
    based on the experiment and row index.
    """
    notes_str = row.get('Super_Experiment_Mapping_Notes')
    if pd.isna(notes_str) or not isinstance(notes_str, str):
        return f"{row['Experiment']}_row_{row.name}"
    try:
        notes = json.loads(notes_str.strip('"'))
        if 'block_id' in notes:
            return notes['block_id']
        else:
            return f"{row['Experiment']}_row_{row.name}"
    except (json.JSONDecodeError, TypeError):
        return f"{row['Experiment']}_row_{row.name}"

def get_most_frequent_paradigm(group):
    """
    Returns the most frequent paradigm in a DataFrame group.
    """
    return group['Paradigm'].mode()[0]

# --- Main Script ---

df_raw = pd.read_csv('../data/super_experiment_design_space.csv')

df_pca_features, numerical_cols, categorical_cols, df_processed, preprocessor = au.preprocess(df_raw, merge_conflict_dimensions=True)
df_processed['Paradigm'] = df_processed.apply(au.classify_paradigm, axis=1)

print("Distribution of paradigms across all conditions:")
print(df_processed['Paradigm'].value_counts())
print("-" * 50)

df_processed['Paper'] = df_processed['Experiment'].apply(find_paper)
unique_papers = df_processed['Paper'].dropna().unique()
number_of_papers = len(unique_papers)
print(f"Total number of unique papers: {number_of_papers}\n")

print("Distribution of paradigms by paper:")
print(df_processed[['Paper', 'Paradigm']].value_counts().sort_index())
print("-" * 50)

# ----------------- New Code for Block-level Analysis -----------------

# 1. Create a unique identifier for each experimental block
df_processed['Block_ID'] = df_processed.apply(get_block_id, axis=1)

# 2. Group the conditions by the newly created Block_ID
grouped_by_block = df_processed.groupby('Block_ID')

# 3. For each block, determine the most prevalent paradigm
block_paradigms = grouped_by_block.apply(get_most_frequent_paradigm).rename('Block Paradigm')

# 4. Count how many blocks there are for each paradigm type
block_paradigm_counts = block_paradigms.value_counts()
number_of_blocks = len(block_paradigms)

print(f"Total number of unique trial blocks: {number_of_blocks}")
print("Distribution of paradigms at the block level:")
print(block_paradigm_counts)
print("-" * 50)

# 5. Show which paradigms are represented by each block
block_to_paper = df_processed.groupby('Block_ID')['Paper'].first()
block_analysis = pd.DataFrame(block_paradigms)
block_analysis = block_analysis.join(block_to_paper)

print("Block-level analysis details:")
print(block_analysis.sort_values(by=['Block Paradigm', 'Paper']).to_markdown())

# Group the conditions by the Paper
grouped_by_paper = df_processed.groupby('Paper')

# For each paper, determine the most prevalent paradigm
paper_paradigms = grouped_by_paper.apply(get_most_frequent_paradigm).rename('Paper Paradigm')

# Count how many papers fall into each paradigm type
paper_paradigm_counts = paper_paradigms.value_counts()
number_of_papers_with_paradigms = len(paper_paradigms)

print(f"Total number of unique papers with a determined paradigm: {number_of_papers_with_paradigms}")
print("Distribution of paradigms at the paper level:")
print(paper_paradigm_counts)
print("-" * 50)

# Show which paradigms are represented by each paper
paper_analysis = pd.DataFrame(paper_paradigms)
print("Paper-level analysis details:")
print(paper_analysis.sort_values(by='Paper Paradigm').to_markdown())
