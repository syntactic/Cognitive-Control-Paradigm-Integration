#!/usr/bin/env python3
"""
Exploratory Data Analysis (EDA) for Cognitive Science Experiments Dataset

This script performs comprehensive exploratory data analysis on a dataset of cognitive
science experiments, creating visualizations and summary statistics to reveal the
distribution of key experimental parameters both overall and within specific paradigm
categories.

Author: Claude Code
Date: 2025-09-16
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import analysis_utils as au

PARADIGM_CANONICAL_MAP = {
    'Single-Task': 'Single-Task Baseline',
    'Interference': 'Interference',
    'Task Switching': 'Task-Switching',
    'Dual-Task_PRP': 'Dual-Task/PRP',
}

PARADIGM_ORDER_MAIN = ['Interference', 'Task-Switching', 'Dual-Task/PRP']
PARADIGM_ORDER_WITH_BASELINE = ['Single-Task Baseline', 'Interference', 'Task-Switching', 'Dual-Task/PRP']

PARADIGM_COLOR_MAP = {
    'Single-Task Baseline': '#8C8C8C',
    'Interference': '#35B779',
    'Task-Switching': '#31688E',
    'Dual-Task/PRP': '#7B3294',
}

POSITIVE_CSI_COLOR = '#2E8B57'


def add_paradigm_display_column(df, include_baseline=False):
    """Return a copy of df with a canonical paradigm display column."""
    order = PARADIGM_ORDER_WITH_BASELINE if include_baseline else PARADIGM_ORDER_MAIN
    df_copy = df.copy()
    df_copy['Paradigm Display'] = df_copy['Paradigm'].map(PARADIGM_CANONICAL_MAP).fillna(df_copy['Paradigm'])
    df_copy = df_copy[df_copy['Paradigm Display'].isin(order)]
    df_copy['Paradigm Display'] = pd.Categorical(df_copy['Paradigm Display'], categories=order, ordered=True)
    return df_copy, order

# Set up plotting style for professional-looking plots
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10


def create_output_directories():
    """Create output directories for plots and statistics if they don't exist."""
    base_dir = Path('eda_plots')
    global_dir = base_dir / 'global'
    stratified_dir = base_dir / 'stratified'
    stats_dir = Path('eda_stats')

    global_dir.mkdir(parents=True, exist_ok=True)
    stratified_dir.mkdir(parents=True, exist_ok=True)
    stats_dir.mkdir(parents=True, exist_ok=True)

    return global_dir, stratified_dir, stats_dir


def load_and_preprocess_data():
    """
    Load and preprocess the experimental data using analysis_utils.

    Returns:
        tuple: (df_processed, df_features) where df_processed contains the cleaned
               data with paradigm labels and df_features contains the feature matrix
    """
    print("Loading and preprocessing data...")

    # Load raw data
    df_raw = pd.read_csv('../data/super_experiment_design_space.csv')
    print(f"Loaded {len(df_raw)} experimental conditions from {len(df_raw.columns)} columns")

    # Preprocess data using analysis_utils
    df_features, numerical_cols, categorical_cols, df_processed, preprocessor = au.preprocess(
        df_raw, merge_conflict_dimensions=True, target='pca'
    )

    # Apply paradigm classification
    df_processed['Paradigm'] = df_processed.apply(au.classify_paradigm, axis=1)

    # Re-introduce NaNs for descriptive reporting where preprocess() used median fills.
    na_flag_map = {
        'Inter-task SOA': 'Inter-task SOA is NA',
        'Distractor SOA': 'Distractor SOA is NA',
        'Task 2 CSI': 'Task 2 CSI is NA',
        'Task 2 Difficulty': 'Task 2 Difficulty is NA',
    }
    for value_col, flag_col in na_flag_map.items():
        if value_col in df_processed.columns and flag_col in df_processed.columns:
            df_processed.loc[df_processed[flag_col] == 1, value_col] = np.nan

    print(f"Preprocessing complete. Dataset shape: {df_processed.shape}")
    print(f"Paradigm distribution: {df_processed['Paradigm'].value_counts().to_dict()}")

    return df_processed, df_features


def generate_summary_statistics(df_processed, stratify=True):
    """
    Generate summary statistics for key continuous variables.

    Args:
        df_processed (pd.DataFrame): The processed dataset with paradigm labels
        stratify (bool): If True, generate statistics by paradigm. If False, generate global statistics.

    Returns:
        str: Formatted statistics text
    """
    if stratify:
        title = "STRATIFIED SUMMARY STATISTICS BY PARADIGM"
        df_with_display, _ = add_paradigm_display_column(df_processed, include_baseline=False)
        paradigms_to_analyze = PARADIGM_ORDER_MAIN
    else:
        title = "GLOBAL SUMMARY STATISTICS"
        df_with_display = df_processed.copy()
        paradigms_to_analyze = ['All Data']

    output_text = "\n" + "=" * 60 + "\n"
    output_text += title + "\n"
    output_text += "=" * 60 + "\n"

    # Define key continuous variables for summary
    continuous_vars = [
        'Task 2 Response Probability', 'RSI', 'Task 1 CSI', 'Task 2 CSI',
        'Inter-task SOA', 'Distractor SOA', 'Switch Rate',
        'Task 1 Difficulty', 'Task 2 Difficulty'
    ]

    def format_stat(value):
        return f"{value:.3f}" if pd.notna(value) else "N/A"

    # Define categorical/discrete variables for summary
    categorical_vars = [
        'Number of Tasks', 'Trial Transition Type', 'Stimulus-Stimulus Congruency',
        'Stimulus-Response Congruency', 'Stimulus Bivalence & Congruency',
        'Response Set Overlap', 'Task 1 Stimulus-Response Mapping',
        'Task 2 Stimulus-Response Mapping', 'Task 1 Cue Type', 'Task 2 Cue Type',
        'RSI is Predictable', 'Inter-task SOA is Predictable',
        'Intra-Trial Task Relationship'
    ]

    for paradigm in paradigms_to_analyze:
        if stratify:
            output_text += f"\n===== SUMMARY STATISTICS FOR: {paradigm} =====\n"
            subset = df_with_display[df_with_display['Paradigm Display'] == paradigm]
        else:
            output_text += f"\n===== GLOBAL SUMMARY STATISTICS =====\n"
            subset = df_with_display

        for var in continuous_vars:
            if var in subset.columns:
                if var == 'RSI':
                    clean_values = subset[var].apply(au.clean_rsi)
                elif var == 'Switch Rate':
                    clean_values = subset[var].apply(au.clean_switch_rate)
                else:
                    clean_values = pd.to_numeric(subset[var], errors='coerce')

                stats = clean_values.describe()
                count_raw = stats.get('count', 0)
                count_value = int(count_raw) if pd.notna(count_raw) else 0

                output_text += f"\n{var}:\n"
                output_text += f"  Count (non-missing): {count_value}\n"
                if count_value > 0:
                    output_text += f"  Mean: {format_stat(stats.get('mean'))}\n"
                    output_text += f"  Std: {format_stat(stats.get('std'))}\n"
                    output_text += f"  Min: {format_stat(stats.get('min'))}\n"
                    output_text += f"  25th percentile: {format_stat(stats.get('25%'))}\n"
                    output_text += f"  Median: {format_stat(stats.get('50%'))}\n"
                    output_text += f"  75th percentile: {format_stat(stats.get('75%'))}\n"
                    output_text += f"  Max: {format_stat(stats.get('max'))}\n"
                else:
                    output_text += "  Mean: N/A\n"
                    output_text += "  Std: N/A\n"
                    output_text += "  Min: N/A\n"
                    output_text += "  25th percentile: N/A\n"
                    output_text += "  Median: N/A\n"
                    output_text += "  75th percentile: N/A\n"
                    output_text += "  Max: N/A\n"

        output_text += "\nCATEGORICAL FEATURES DISTRIBUTION:\n"
        output_text += "-" * 40 + "\n"

        total_count = len(subset)

        for var in categorical_vars:
            if var in subset.columns:
                output_text += f"\n{var}:\n"
                if total_count == 0:
                    output_text += "  No data available.\n"
                    continue

                value_counts = subset[var].value_counts(dropna=False)

                for value, count in value_counts.items():
                    percentage = (count / total_count) * 100 if total_count else 0
                    output_text += f"  {value}: {count} ({percentage:.1f}%)\n"

                non_missing = subset[var].notna().sum()
                missing = total_count - non_missing
                if missing > 0:
                    coverage = (non_missing / total_count) * 100 if total_count else 0
                    output_text += f"  Non-missing: {non_missing}/{total_count} ({coverage:.1f}%)\n"

    output_text += "\n" + "=" * 60 + "\n"
    return output_text


def plot_task2_response_probability_distribution(df_processed, output_dir):
    """
    Create histogram of Task 2 Response Probability distribution.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    plt.figure(figsize=(10, 6))

    # Convert to numeric and remove any NaN values
    t2rp_values = pd.to_numeric(df_processed['Task 2 Response Probability'], errors='coerce')
    t2rp_values = t2rp_values.dropna()

    # Create histogram with appropriate bins
    plt.hist(t2rp_values, bins=20, alpha=0.7, color='skyblue', edgecolor='black')

    plt.title('Distribution of Task 2 Response Probability', fontsize=14, fontweight='bold')
    plt.xlabel('Task 2 Response Probability')
    plt.ylabel('Number of Experimental Conditions')
    plt.grid(True, alpha=0.3)

    # Add text annotation about bimodal distribution
    plt.text(0.5, plt.ylim()[1]*0.8,
             f'N = {len(t2rp_values)} conditions',
             horizontalalignment='center',
             verticalalignment='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_dir / 'task2_response_probability_distribution.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'task2_response_probability_distribution.png', format='png', dpi=100)
    plt.close()


def plot_temporal_parameters_by_paradigm(df_processed, output_dir):
    """
    Create visualizations for temporal parameters stratified by paradigm.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    # Filter to main paradigms (exclude Single-Task for cleaner visualization)
    raw_main_paradigms = ['Interference', 'Task Switching', 'Dual-Task_PRP']
    df_main_raw = df_processed[df_processed['Paradigm'].isin(raw_main_paradigms)].copy()
    df_main, paradigm_order = add_paradigm_display_column(df_main_raw)
    paradigm_palette = {label: PARADIGM_COLOR_MAP[label] for label in paradigm_order}

    # Task 1 CSI by paradigm - two complementary views
    df_main['Task 1 CSI Clean'] = pd.to_numeric(df_main['Task 1 CSI'], errors='coerce')
    df_csi_clean = df_main.dropna(subset=['Task 1 CSI Clean'])

    # ------------------------------------------------------------------
    # Plot 1: proportion of zero CSI vs. positive CSI per paradigm
    # ------------------------------------------------------------------
    zero_summary = df_csi_clean.copy()
    zero_summary['CSI Category'] = np.where(
        zero_summary['Task 1 CSI Clean'] == 0, '0 ms', '> 0 ms'
    )

    zero_counts = (zero_summary
                   .groupby(['Paradigm Display', 'CSI Category'])
                   .size()
                   .unstack(fill_value=0)
                   .reindex(paradigm_order))
    zero_counts = zero_counts.reindex(columns=['0 ms', '> 0 ms'], fill_value=0).fillna(0)

    zero_proportions = zero_counts.div(zero_counts.sum(axis=1), axis=0).fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    indices = np.arange(len(paradigm_order))

    ax.bar(
        indices,
        zero_proportions['0 ms'],
        color='#A9A9A9', edgecolor='black', label='0 ms'
    )
    ax.bar(
        indices,
        zero_proportions['> 0 ms'],
        bottom=zero_proportions['0 ms'],
        color=POSITIVE_CSI_COLOR,
        edgecolor='black',
        label='> 0 ms'
    )

    ax.set_title('Task 1 CSI Presence by Paradigm', fontsize=14, fontweight='bold')
    ax.set_xlabel('Paradigm')
    ax.set_ylabel('Proportion of Conditions')
    ax.set_xticks(indices)
    ax.set_xticklabels(paradigm_order, rotation=45, ha='center', rotation_mode='anchor')
    ax.tick_params(axis='x', pad=10)
    for label in ax.get_xticklabels():
        label.set_ha('center')
        label.set_va('top')
        x, y = label.get_position()
        label.set_position((x, y - 0.05))
    ax.set_ylim(0, 1.15)
    ax.grid(True, alpha=0.3, axis='y', zorder=0)
    ax.legend(title='CSI Category', loc='upper right')

    # Annotate bars with counts
    for i, paradigm in enumerate(paradigm_order):
        total = zero_counts.loc[paradigm].sum()
        zero_count = zero_counts.loc[paradigm].get('0 ms', 0)
        positive_count = zero_counts.loc[paradigm].get('> 0 ms', 0)
        ax.text(i, zero_proportions.loc[paradigm, '0 ms'] / 2,
                f'n={zero_count}', ha='center', va='center', color='black', fontsize=9)
        ax.text(
            i,
            zero_proportions.loc[paradigm, '0 ms'] + zero_proportions.loc[paradigm, '> 0 ms'] / 2,
            f'n={positive_count}',
            ha='center', va='center', color='black', fontsize=9
        )
        ax.text(i, 1.07, f'total={total}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'task1_csi_zero_share_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'task1_csi_zero_share_by_paradigm.png', format='png', dpi=100)
    plt.close(fig)

    # ------------------------------------------------------------------
    # Plot 2: distribution of positive CSI only
    # ------------------------------------------------------------------
    df_positive_csi = df_csi_clean[df_csi_clean['Task 1 CSI Clean'] > 0].copy()

    if not df_positive_csi.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.swarmplot(
            data=df_positive_csi, x='Paradigm Display', y='Task 1 CSI Clean',
            order=paradigm_order, hue='Paradigm Display', palette=paradigm_palette,
            dodge=False, size=6, edgecolor='white', linewidth=0.5, ax=ax
        )
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()

        medians = df_positive_csi.groupby('Paradigm Display')['Task 1 CSI Clean'].median()
        for i, paradigm in enumerate(paradigm_order):
            if paradigm in medians:
                ax.scatter(i, medians[paradigm], color='black', s=70, marker='D', zorder=4,
                           label='Median' if i == 0 else None)

        ax.set_title('Task 1 CSI (Positive Values Only)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Paradigm')
        ax.set_ylabel('Task 1 CSI (ms)')
        ax.set_xticklabels(paradigm_order, rotation=45, ha='center', rotation_mode='anchor')
        ax.tick_params(axis='x', pad=10)
        for label in ax.get_xticklabels():
            label.set_ha('center')
            label.set_va('top')
            x, y = label.get_position()
            label.set_position((x, y - 0.05))
        ax.grid(True, alpha=0.3, axis='y', zorder=0)

        stats_text = []
        for paradigm in paradigm_order:
            paradigm_data = df_positive_csi[df_positive_csi['Paradigm Display'] == paradigm]['Task 1 CSI Clean']
            if not paradigm_data.empty:
                stats_text.append(
                    f"{paradigm}: median={paradigm_data.median():.0f}ms,"
                    f" mean={paradigm_data.mean():.0f}ms, n={len(paradigm_data)}"
                )

        ax.text(0.02, 0.98, '\n'.join(stats_text), transform=ax.transAxes,
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9))

        plt.tight_layout()
        plt.savefig(output_dir / 'task1_csi_positive_by_paradigm.svg', format='svg', dpi=300)
        plt.savefig(output_dir / 'task1_csi_positive_by_paradigm.png', format='png', dpi=100)
        plt.close(fig)
    else:
        print("No positive Task 1 CSI values found; skipping positive-only plot.")

    # RSI by paradigm
    plt.figure(figsize=(12, 6))

    # Clean the RSI data using the utility function
    df_main['RSI Clean'] = df_main['RSI'].apply(au.clean_rsi)

    # Create box plot for RSI (better for skewed data)
    ax = sns.boxplot(
        data=df_main,
        x='Paradigm Display',
        y='RSI Clean',
        order=paradigm_order,
        palette=[PARADIGM_COLOR_MAP[label] for label in paradigm_order]
    )
    ax.set_title('Distribution of RSI by Paradigm', fontsize=14, fontweight='bold')
    ax.set_xlabel('Paradigm')
    ax.set_ylabel('RSI (ms)')
    ax.set_xticklabels(paradigm_order, rotation=45, ha='center', rotation_mode='anchor')
    ax.tick_params(axis='x', pad=10)
    for label in ax.get_xticklabels():
        label.set_ha('center')
        label.set_va('top')
        x, y = label.get_position()
        label.set_position((x, y - 0.05))
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'rsi_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'rsi_by_paradigm.png', format='png', dpi=100)
    plt.close()


def plot_merged_conflict_by_paradigm(df_processed, output_dir):
    """
    Create bar plot for merged conflict dimension (Stimulus Bivalence & Congruency) by paradigm.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    main_paradigms = ['Interference', 'Task Switching', 'Dual-Task_PRP']
    df_main_raw = df_processed[df_processed['Paradigm'].isin(main_paradigms)].copy()
    df_main, paradigm_order = add_paradigm_display_column(df_main_raw)

    # Create merged conflict plot
    plt.figure(figsize=(12, 6))

    # Handle the merged conflict dimension and map N/A to Univalent
    df_main_merged = df_main.copy()
    df_main_merged['Stimulus Bivalence & Congruency Clean'] = df_main_merged['Stimulus Bivalence & Congruency'].apply(
        lambda x: 'Univalent' if pd.isna(x) or str(x) == 'N/A' or str(x) == 'nan' else x
    )

    # Create crosstab for counts
    merged_crosstab = pd.crosstab(df_main_merged['Paradigm Display'], df_main_merged['Stimulus Bivalence & Congruency Clean'])
    merged_crosstab = merged_crosstab.reindex(paradigm_order).fillna(0)

    # Normalize to proportions (each paradigm sums to 1.0)
    merged_crosstab_norm = merged_crosstab.div(merged_crosstab.sum(axis=1), axis=0)

    # Create bar plot with intuitive colors
    # Define intuitive color mapping for conflict types
    conflict_colors = {
        'Congruent': '#90EE90',      # Light green - positive/harmonious
        'Incongruent': '#FFB6C1',   # Light pink/red - conflict/tension
        'Neutral': '#87CEEB',       # Sky blue - neutral/balanced
        'Univalent': '#D3D3D3'      # Light gray - absence of conflict
    }

    # Get colors in the order they appear in the dataframe columns
    plot_colors = [conflict_colors.get(col, '#CCCCCC') for col in merged_crosstab_norm.columns]

    ax = merged_crosstab_norm.plot(kind='bar', stacked=False, figsize=(12, 6), color=plot_colors)
    ax.set_title('Conflict Distribution by Paradigm', fontsize=14, fontweight='bold')
    ax.set_xlabel('Paradigm')
    ax.set_ylabel('Proportion of Conditions')
    ax.set_xticklabels(paradigm_order, rotation=45, ha='center', rotation_mode='anchor')
    ax.tick_params(axis='x', pad=10)
    for label in ax.get_xticklabels():
        label.set_ha('center')
        label.set_va('top')
        x, y = label.get_position()
        label.set_position((x, y - 0.05))
    ax.legend(title='Conflict Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'conflict_distribution_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'conflict_distribution_by_paradigm.png', format='png', dpi=100)
    plt.close()


def plot_response_set_overlap_by_paradigm(df_processed, output_dir):
    """
    Create stacked bar chart for response set overlap categories by paradigm.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    relevant_paradigms = ['Task Switching', 'Dual-Task_PRP']
    df_main_raw = df_processed[df_processed['Paradigm'].isin(relevant_paradigms)].copy()

    if df_main_raw.empty:
        print("No paradigms found for response set overlap plot; skipping.")
        return

    df_main, _ = add_paradigm_display_column(df_main_raw)

    display_order = ['Task-Switching', 'Dual-Task/PRP']
    df_main = df_main[df_main['Paradigm Display'].isin(display_order)]

    if df_main.empty:
        print("No eligible paradigms remain for response set overlap plot; skipping.")
        return

    df_main['Paradigm Display'] = pd.Categorical(
        df_main['Paradigm Display'], categories=display_order, ordered=True
    )

    collapsed_map = {
        'RSO_Identical': 'Identical',
        'RSO_Disjoint': 'Disjoint',
        'RSO_NA': 'Not Specified'
    }
    overlap_collapsed = (
        df_main['Response Set Overlap']
        .apply(au.map_rso)
        .map(collapsed_map)
        .fillna('Not Specified')
    )

    df_main = df_main.assign(**{'Response Set Overlap Collapsed': overlap_collapsed})

    paradigm_order = display_order

    overlap_crosstab = pd.crosstab(
        df_main['Paradigm Display'],
        df_main['Response Set Overlap Collapsed']
    ).reindex(paradigm_order).fillna(0)

    if overlap_crosstab.values.sum() == 0:
        print("Response Set Overlap counts are all zero; skipping plot.")
        return

    category_order = (
        df_main['Response Set Overlap Collapsed']
        .value_counts()
        .reindex(overlap_crosstab.columns, fill_value=0)
        .sort_values(ascending=False)
        .index.tolist()
    )
    overlap_crosstab = overlap_crosstab.reindex(columns=category_order, fill_value=0)

    row_totals = overlap_crosstab.sum(axis=1)
    # Avoid division by zero while normalizing to proportions
    safe_totals = row_totals.replace(0, np.nan)
    overlap_crosstab_norm = overlap_crosstab.div(safe_totals, axis=0).fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    indices = np.arange(len(paradigm_order))
    widths = 0.6
    bottom = np.zeros(len(paradigm_order))
    base_palette = iter(sns.color_palette('Set2', len(category_order)))
    category_color_map = {
        'Identical': '#1B9E77',  # teal
        'Disjoint': '#D95F02',   # orange
        'Not Specified': '#B3B3B3'
    }

    colors = [category_color_map.get(category, next(base_palette)) for category in category_order]

    for color, category in zip(colors, category_order):
        proportions = overlap_crosstab_norm[category].to_numpy()
        ax.bar(
            indices,
            proportions,
            width=widths,
            bottom=bottom,
            color=color,
            edgecolor='black',
            label=category
        )

        for i, (prop, base) in enumerate(zip(proportions, bottom)):
            if prop <= 0:
                continue
            text_y = base + prop / 2
            va = 'center'
            if prop < 0.06:
                text_y = base + prop + 0.015
                va = 'bottom'
            ax.text(indices[i], text_y, f'{prop*100:.0f}%', ha='center', va=va, fontsize=9)

        bottom += proportions

    ax.set_title('Response Set Overlap by Paradigm', fontsize=14, fontweight='bold')
    ax.set_xlabel('Paradigm')
    ax.set_ylabel('Proportion of Conditions')
    ax.set_xticks(indices)
    ax.set_xticklabels(paradigm_order, rotation=45, ha='center', rotation_mode='anchor')
    ax.tick_params(axis='x', pad=10)
    for label in ax.get_xticklabels():
        label.set_ha('center')
        label.set_va('top')
        x, y = label.get_position()
        label.set_position((x, y - 0.05))
    ax.set_ylim(0, 1.15)
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(title='Response Set Overlap', bbox_to_anchor=(1.05, 1), loc='upper left')

    for i, paradigm in enumerate(paradigm_order):
        total = int(row_totals.get(paradigm, 0))
        ax.text(indices[i], 1.05, f'n={total}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / 'response_set_overlap_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'response_set_overlap_by_paradigm.png', format='png', dpi=100)
    plt.close(fig)


def plot_task_structure_parameters(df_processed, output_dir, stratify=True):
    """
    Create visualizations for task structure parameters.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
        stratify (bool): If True, filter to specific paradigms. If False, use all data.
    """
    # Switch Rate
    plt.figure(figsize=(10, 6))

    if stratify:
        # Filter to Task Switching paradigm
        switch_rate_data = df_processed[df_processed['Paradigm'] == 'Task Switching'].copy()
        title_suffix = " in Task-Switching Paradigm"
        color = PARADIGM_COLOR_MAP['Task-Switching']
    else:
        # Use all data (excluding NaNs)
        switch_rate_data = df_processed.copy()
        title_suffix = " (All Paradigms)"
        color = 'skyblue'

    if len(switch_rate_data) > 0:
        # Clean switch rate data
        switch_rate_data['Switch Rate Clean'] = switch_rate_data['Switch Rate'].apply(au.clean_switch_rate)
        switch_rate_clean = switch_rate_data['Switch Rate Clean'].dropna()

        if len(switch_rate_clean) > 0:
            # Create histogram
            plt.hist(
                switch_rate_clean,
                bins=15,
                alpha=0.7,
                color=color,
                edgecolor='black'
            )
            plt.title(f'Distribution of Switch Rate{title_suffix}', fontsize=14, fontweight='bold')
            plt.xlabel('Switch Rate (%)')
            plt.ylabel('Number of Conditions')

            # Set more granular x-axis ticks (by 10s)
            plt.xticks(range(0, 101, 10))
            plt.grid(True, alpha=0.3)

            # Add summary statistics as text
            mean_sr = switch_rate_clean.mean()
            std_sr = switch_rate_clean.std()
            plt.text(0.7, 0.8, f'Mean: {mean_sr:.1f}%\nStd: {std_sr:.1f}%\nN: {len(switch_rate_clean)}',
                    transform=plt.gca().transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        else:
            plt.text(0.5, 0.5, 'No valid Switch Rate data found',
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes, fontsize=14)

    plt.tight_layout()
    plt.savefig(output_dir / 'switch_rate_distribution.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'switch_rate_distribution.png', format='png', dpi=100)
    plt.close()

    # RSI Predictability by paradigm
    main_paradigms = ['Interference', 'Task Switching', 'Dual-Task_PRP']
    df_main_raw = df_processed[df_processed['Paradigm'].isin(main_paradigms)].copy()
    df_main, paradigm_order = add_paradigm_display_column(df_main_raw)

    # Create crosstab for RSI predictability
    rsi_pred_crosstab = pd.crosstab(df_main['Paradigm Display'], df_main['RSI is Predictable'])
    rsi_pred_crosstab = rsi_pred_crosstab.reindex(paradigm_order).fillna(0)

    # Normalize to proportions (each paradigm sums to 1.0)
    rsi_pred_crosstab_norm = rsi_pred_crosstab.div(rsi_pred_crosstab.sum(axis=1), axis=0)

    # Ensure consistent column ordering
    rsi_pred_crosstab_norm = rsi_pred_crosstab_norm.reindex(columns=[0, 1], fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    indices = np.arange(len(paradigm_order))
    widths = 0.6

    ax.bar(
        indices,
        rsi_pred_crosstab_norm[0],
        width=widths,
        color='lightcoral',
        edgecolor='black',
        label='No'
    )
    ax.bar(
        indices,
        rsi_pred_crosstab_norm[1],
        width=widths,
        bottom=rsi_pred_crosstab_norm[0],
        color='lightblue',
        edgecolor='black',
        label='Yes'
    )

    ax.set_title('RSI Predictability by Paradigm', fontsize=14, fontweight='bold')
    ax.set_xlabel('Paradigm')
    ax.set_ylabel('Proportion of Conditions')
    ax.set_xticks(indices)
    ax.set_xticklabels(paradigm_order, rotation=45, ha='center', rotation_mode='anchor')
    ax.tick_params(axis='x', pad=10)
    for label in ax.get_xticklabels():
        label.set_ha('center')
        label.set_va('top')
        x, y = label.get_position()
        label.set_position((x, y - 0.05))

    ax.set_ylim(0, 1.15)
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(title='RSI is Predictable', loc='upper right')

    # Annotate percentages; move outside if the segment is too small to read
    for i, paradigm in enumerate(paradigm_order):
        no_prop = rsi_pred_crosstab_norm.loc[paradigm, 0]
        yes_prop = rsi_pred_crosstab_norm.loc[paradigm, 1]
        no_y = no_prop / 2
        no_va = 'center'
        if no_prop < 0.06:
            no_y = no_prop + 0.015
            no_va = 'bottom'
        ax.text(
            i,
            no_y,
            f'{no_prop*100:.0f}%',
            ha='center', va=no_va, color='black', fontsize=9
        )
        ax.text(
            i,
            no_prop + yes_prop / 2,
            f'{yes_prop*100:.0f}%',
            ha='center', va='center', color='black', fontsize=9
        )
    plt.tight_layout()
    plt.savefig(output_dir / 'rsi_predictable_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'rsi_predictable_by_paradigm.png', format='png', dpi=100)
    plt.close()


def plot_paradigm_specific_soa_parameters(df_processed, output_dir, stratify=True):
    """
    Create visualizations for paradigm-specific SOA parameters.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
        stratify (bool): If True, filter to specific paradigms. If False, use all data.
    """
    # Inter-task SOA
    plt.figure(figsize=(10, 6))

    if stratify:
        # Filter to Dual-Task_PRP paradigm
        inter_task_data = df_processed[df_processed['Paradigm'] == 'Dual-Task_PRP'].copy()
        title_suffix = " in Dual-Task/PRP Paradigm"
        color = PARADIGM_COLOR_MAP['Dual-Task/PRP']
    else:
        # Use all data
        inter_task_data = df_processed.copy()
        title_suffix = " (All Paradigms)"
        color = 'purple'

    if len(inter_task_data) > 0:
        # Clean inter-task SOA data
        inter_task_data['Inter-task SOA Clean'] = pd.to_numeric(inter_task_data['Inter-task SOA'], errors='coerce')
        inter_task_soa_clean = inter_task_data['Inter-task SOA Clean'].dropna()

        if len(inter_task_soa_clean) > 0:
            # Create histogram with more bins for better granularity near the mean
            plt.hist(
                inter_task_soa_clean,
                bins=30,
                alpha=0.7,
                color=color,
                edgecolor='black'
            )
            plt.title(f'Distribution of Inter-task SOA{title_suffix}', fontsize=14, fontweight='bold')
            plt.xlabel('Inter-task SOA (ms)')
            plt.ylabel('Number of Conditions')
            plt.grid(True, alpha=0.3)

            # Add summary statistics
            mean_soa = inter_task_soa_clean.mean()
            std_soa = inter_task_soa_clean.std()
            plt.text(0.7, 0.8, f'Mean: {mean_soa:.0f} ms\nStd: {std_soa:.0f} ms\nN: {len(inter_task_soa_clean)}',
                    transform=plt.gca().transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        else:
            plt.text(0.5, 0.5, 'No valid Inter-task SOA data found',
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes, fontsize=14)
    else:
        plt.text(0.5, 0.5, f'No {"Dual-Task_PRP" if stratify else "Inter-task SOA"} conditions found',
                horizontalalignment='center', verticalalignment='center',
                transform=plt.gca().transAxes, fontsize=14)

    plt.tight_layout()
    plt.savefig(output_dir / 'inter_task_soa_dual_task.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'inter_task_soa_dual_task.png', format='png', dpi=100)
    plt.close()

    # Distractor SOA
    plt.figure(figsize=(10, 6))

    if stratify:
        # Filter to Interference paradigm
        distractor_data = df_processed[df_processed['Paradigm'] == 'Interference'].copy()
        title_suffix = " in Interference Paradigm"
        color = PARADIGM_COLOR_MAP['Interference']
    else:
        # Use all data
        distractor_data = df_processed.copy()
        title_suffix = " (All Paradigms)"
        color = 'green'

    if len(distractor_data) > 0:
        # Clean distractor SOA data
        distractor_data['Distractor SOA Clean'] = pd.to_numeric(distractor_data['Distractor SOA'], errors='coerce')
        distractor_soa_clean = distractor_data['Distractor SOA Clean'].dropna()

        if len(distractor_soa_clean) > 0:
            # Create histogram
            plt.hist(
                distractor_soa_clean,
                bins=15,
                alpha=0.7,
                color=color,
                edgecolor='black'
            )
            plt.title(f'Distribution of Distractor SOA{title_suffix}', fontsize=14, fontweight='bold')
            plt.xlabel('Distractor SOA (ms)')
            plt.ylabel('Number of Conditions')
            plt.grid(True, alpha=0.3)

            # Add summary statistics
            mean_dsoa = distractor_soa_clean.mean()
            std_dsoa = distractor_soa_clean.std()
            plt.text(0.7, 0.8, f'Mean: {mean_dsoa:.0f} ms\nStd: {std_dsoa:.0f} ms\nN: {len(distractor_soa_clean)}',
                    transform=plt.gca().transAxes,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        else:
            plt.text(0.5, 0.5, 'No valid Distractor SOA data found',
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes, fontsize=14)
    else:
        plt.text(0.5, 0.5, f'No {"Interference" if stratify else "Distractor SOA"} conditions found',
                horizontalalignment='center', verticalalignment='center',
                transform=plt.gca().transAxes, fontsize=14)

    plt.tight_layout()
    plt.savefig(output_dir / 'distractor_soa_interference.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'distractor_soa_interference.png', format='png', dpi=100)
    plt.close()


def create_paradigm_overview_plot(df_processed, output_dir):
    """
    Create an overview plot showing the distribution of paradigms.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    plt.figure(figsize=(10, 6))

    # Count paradigms
    paradigm_counts = df_processed['Paradigm'].value_counts()

    # Create bar plot
    bars = plt.bar(paradigm_counts.index, paradigm_counts.values,
                   color=['skyblue', 'lightgreen', 'lightcoral', 'gold'])

    plt.title('Distribution of Experimental Conditions by Paradigm', fontsize=14, fontweight='bold')
    plt.xlabel('Paradigm')
    plt.ylabel('Number of Experimental Conditions')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_dir / 'paradigm_distribution_overview.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'paradigm_distribution_overview.png', format='png', dpi=100)
    plt.close()


def run_analysis(df_processed, output_dir, stats_dir, stratify=True):
    """
    Run either global or stratified analysis.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
        stats_dir (Path): Directory to save statistics
        stratify (bool): If True, run stratified analysis. If False, run global analysis.
    """
    analysis_type = "stratified" if stratify else "global"
    print(f"\n{'='*60}")
    print(f"RUNNING {analysis_type.upper()} ANALYSIS")
    print(f"{'='*60}")

    # Generate and save summary statistics
    stats_text = generate_summary_statistics(df_processed, stratify=stratify)
    stats_file = stats_dir / f"{analysis_type}_summary_statistics.txt"
    with open(stats_file, 'w') as f:
        f.write(stats_text)
    print(f"✓ Saved {analysis_type} summary statistics to: {stats_file}")

    # Create plots
    create_paradigm_overview_plot(df_processed, output_dir)
    print(f"✓ Created paradigm distribution overview plot ({analysis_type})")

    plot_task2_response_probability_distribution(df_processed, output_dir)
    print(f"✓ Created Task 2 Response Probability distribution plot ({analysis_type})")

    plot_temporal_parameters_by_paradigm(df_processed, output_dir)
    print(f"✓ Created temporal parameter plots ({analysis_type})")

    plot_merged_conflict_by_paradigm(df_processed, output_dir)
    print(f"✓ Created merged conflict parameter plot ({analysis_type})")

    plot_response_set_overlap_by_paradigm(df_processed, output_dir)
    print(f"✓ Created response set overlap plot ({analysis_type})")

    plot_task_structure_parameters(df_processed, output_dir, stratify=stratify)
    print(f"✓ Created task structure plots ({analysis_type})")

    plot_paradigm_specific_soa_parameters(df_processed, output_dir, stratify=stratify)
    print(f"✓ Created SOA parameter plots ({analysis_type})")


def main():
    """Main function to run both global and stratified EDA analysis."""
    print("="*60)
    print("EXPLORATORY DATA ANALYSIS FOR COGNITIVE SCIENCE EXPERIMENTS")
    print("="*60)

    # Setup and Standard Preprocessing
    print("\nTask 1: Setup and Preprocessing")
    print("-" * 40)

    global_dir, stratified_dir, stats_dir = create_output_directories()
    print(f"Output directories created:")
    print(f"  Global plots: {global_dir}")
    print(f"  Stratified plots: {stratified_dir}")
    print(f"  Statistics: {stats_dir}")

    df_processed, df_features = load_and_preprocess_data()

    # Run both analyses
    run_analysis(df_processed, global_dir, stats_dir, stratify=False)
    run_analysis(df_processed, stratified_dir, stats_dir, stratify=True)

    # Final summary
    print("\n" + "="*60)
    print("EDA ANALYSIS COMPLETE")
    print("="*60)

    # Count generated files
    global_svg = len(list(global_dir.glob('*.svg')))
    global_png = len(list(global_dir.glob('*.png')))
    stratified_svg = len(list(stratified_dir.glob('*.svg')))
    stratified_png = len(list(stratified_dir.glob('*.png')))
    stats_files = len(list(stats_dir.glob('*.txt')))

    print(f"Global analysis: {global_svg} SVG files, {global_png} PNG files")
    print(f"Stratified analysis: {stratified_svg} SVG files, {stratified_png} PNG files")
    print(f"Statistics files: {stats_files} text files")

    print("\nKey findings summary:")
    print(f"• Total experimental conditions analyzed: {len(df_processed)}")
    print(f"• Paradigm distribution: {df_processed['Paradigm'].value_counts().to_dict()}")
    print(f"• Task 2 Response Probability range: {df_processed['Task 2 Response Probability'].min():.1f} - {df_processed['Task 2 Response Probability'].max():.1f}")
    print("• All visualizations saved as high-quality SVG and PNG files")
    print("• Summary statistics saved to separate text files for global and stratified analyses")
    print("\nThe EDA reveals parameter distributions both globally and stratified by paradigm,")
    print("enabling comparison of overall patterns vs. paradigm-specific characteristics.")


if __name__ == "__main__":
    main()
