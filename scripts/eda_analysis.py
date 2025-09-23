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


def create_output_directory():
    """Create output directory for plots if it doesn't exist."""
    output_dir = Path('eda_plots')
    output_dir.mkdir(exist_ok=True)
    return output_dir


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

    print(f"Preprocessing complete. Dataset shape: {df_processed.shape}")
    print(f"Paradigm distribution: {df_processed['Paradigm'].value_counts().to_dict()}")

    return df_processed, df_features


def print_summary_statistics(df_processed):
    """
    Print overall summary statistics for key continuous variables.

    Args:
        df_processed (pd.DataFrame): The processed dataset with paradigm labels
    """
    print("\n" + "="*60)
    print("OVERALL SUMMARY STATISTICS")
    print("="*60)

    # Define key continuous variables for summary
    continuous_vars = [
        'Task 2 Response Probability', 'RSI', 'Task 1 CSI', 'Task 2 CSI',
        'Inter-task SOA', 'Distractor SOA', 'Switch Rate',
        'Task 1 Difficulty', 'Task 2 Difficulty'
    ]

    # Calculate summary statistics
    for var in continuous_vars:
        if var in df_processed.columns:
            # Handle cleaning for specific variables
            if var == 'RSI':
                # Apply RSI cleaning function to get numeric values
                clean_values = df_processed[var].apply(au.clean_rsi)
            elif var == 'Switch Rate':
                # Apply switch rate cleaning function
                clean_values = df_processed[var].apply(au.clean_switch_rate)
            else:
                # Convert to numeric, coercing errors to NaN
                clean_values = pd.to_numeric(df_processed[var], errors='coerce')

            # Calculate statistics
            stats = clean_values.describe()
            print(f"\n{var}:")
            print(f"  Count (non-missing): {stats['count']:.0f}")
            print(f"  Mean: {stats['mean']:.3f}")
            print(f"  Std: {stats['std']:.3f}")
            print(f"  Min: {stats['min']:.3f}")
            print(f"  25th percentile: {stats['25%']:.3f}")
            print(f"  Median: {stats['50%']:.3f}")
            print(f"  75th percentile: {stats['75%']:.3f}")
            print(f"  Max: {stats['max']:.3f}")

    # Define categorical/discrete variables for summary
    print("\nCATEGORICAL FEATURES DISTRIBUTION:")
    print("-" * 40)

    categorical_vars = [
        'Number of Tasks', 'Trial Transition Type', 'Stimulus-Stimulus Congruency',
        'Stimulus-Response Congruency', 'Stimulus Bivalence & Congruency',
        'Response Set Overlap', 'Task 1 Stimulus-Response Mapping',
        'Task 2 Stimulus-Response Mapping', 'Task 1 Cue Type', 'Task 2 Cue Type',
        'RSI is Predictable', 'Inter-task SOA is Predictable',
        'Intra-Trial Task Relationship'
    ]

    for var in categorical_vars:
        if var in df_processed.columns:
            # Get value counts, including NaN
            value_counts = df_processed[var].value_counts(dropna=False)
            total_count = len(df_processed)

            print(f"\n{var}:")
            for value, count in value_counts.items():
                percentage = (count / total_count) * 100
                print(f"  {value}: {count} ({percentage:.1f}%)")

            # Show total non-missing
            non_missing = df_processed[var].notna().sum()
            missing = total_count - non_missing
            if missing > 0:
                print(f"  Non-missing: {non_missing}/{total_count} ({(non_missing/total_count)*100:.1f}%)")

    print("\n" + "="*60 + "\n")


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
    ax.set_title('Merged Conflict Distribution by Paradigm', fontsize=14, fontweight='bold')
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
    plt.savefig(output_dir / 'merged_conflict_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'merged_conflict_by_paradigm.png', format='png', dpi=100)
    plt.close()


def plot_task_structure_parameters(df_processed, output_dir):
    """
    Create visualizations for task structure parameters.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    # Switch Rate - focus on Task Switching paradigm
    plt.figure(figsize=(10, 6))

    # Filter to Task Switching paradigm
    task_switching_data = df_processed[df_processed['Paradigm'] == 'Task Switching'].copy()

    if len(task_switching_data) > 0:
        # Clean switch rate data
        task_switching_data['Switch Rate Clean'] = task_switching_data['Switch Rate'].apply(au.clean_switch_rate)

        # Create histogram
        plt.hist(
            task_switching_data['Switch Rate Clean'],
            bins=15,
            alpha=0.7,
            color=PARADIGM_COLOR_MAP['Task-Switching'],
            edgecolor='black'
        )
        plt.title('Distribution of Switch Rate in Task-Switching Paradigm', fontsize=14, fontweight='bold')
        plt.xlabel('Switch Rate (%)')
        plt.ylabel('Number of Conditions')

        # Set more granular x-axis ticks (by 10s)
        plt.xticks(range(0, 101, 10))
        plt.grid(True, alpha=0.3)

        # Add summary statistics as text
        mean_sr = task_switching_data['Switch Rate Clean'].mean()
        std_sr = task_switching_data['Switch Rate Clean'].std()
        plt.text(0.7, 0.8, f'Mean: {mean_sr:.1f}%\nStd: {std_sr:.1f}%\nN: {len(task_switching_data)}',
                transform=plt.gca().transAxes,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

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


def plot_paradigm_specific_soa_parameters(df_processed, output_dir):
    """
    Create visualizations for paradigm-specific SOA parameters.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    # Inter-task SOA for Dual-Task_PRP only
    plt.figure(figsize=(10, 6))

    # Filter to Dual-Task_PRP paradigm
    dual_task_data = df_processed[df_processed['Paradigm'] == 'Dual-Task_PRP'].copy()

    if len(dual_task_data) > 0:
        # Clean inter-task SOA data
        dual_task_data['Inter-task SOA Clean'] = pd.to_numeric(dual_task_data['Inter-task SOA'], errors='coerce')
        inter_task_soa_clean = dual_task_data['Inter-task SOA Clean'].dropna()

        if len(inter_task_soa_clean) > 0:
            # Create histogram with more bins for better granularity near the mean
            plt.hist(
                inter_task_soa_clean,
                bins=30,
                alpha=0.7,
                color=PARADIGM_COLOR_MAP['Dual-Task/PRP'],
                edgecolor='black'
            )
            plt.title('Distribution of Inter-task SOA in Dual-Task/PRP Paradigm', fontsize=14, fontweight='bold')
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
        plt.text(0.5, 0.5, 'No Dual-Task_PRP conditions found',
                horizontalalignment='center', verticalalignment='center',
                transform=plt.gca().transAxes, fontsize=14)

    plt.tight_layout()
    plt.savefig(output_dir / 'inter_task_soa_dual_task.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'inter_task_soa_dual_task.png', format='png', dpi=100)
    plt.close()

    # Distractor SOA for Interference paradigm only
    plt.figure(figsize=(10, 6))

    # Filter to Interference paradigm
    interference_data = df_processed[df_processed['Paradigm'] == 'Interference'].copy()

    if len(interference_data) > 0:
        # Clean distractor SOA data
        interference_data['Distractor SOA Clean'] = pd.to_numeric(interference_data['Distractor SOA'], errors='coerce')
        distractor_soa_clean = interference_data['Distractor SOA Clean'].dropna()

        if len(distractor_soa_clean) > 0:
            # Create histogram
            plt.hist(
                distractor_soa_clean,
                bins=15,
                alpha=0.7,
                color=PARADIGM_COLOR_MAP['Interference'],
                edgecolor='black'
            )
            plt.title('Distribution of Distractor SOA in Interference Paradigm', fontsize=14, fontweight='bold')
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
        plt.text(0.5, 0.5, 'No Interference conditions found',
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


def main():
    """Main function to run the complete EDA analysis."""
    print("="*60)
    print("EXPLORATORY DATA ANALYSIS FOR COGNITIVE SCIENCE EXPERIMENTS")
    print("="*60)

    # Task 1: Setup and Standard Preprocessing
    print("\nTask 1: Setup and Preprocessing")
    print("-" * 40)

    output_dir = create_output_directory()
    print(f"Output directory created: {output_dir}")

    df_processed, df_features = load_and_preprocess_data()

    # Task 2: Overall Distribution Analysis
    print("\nTask 2: Overall Distribution Analysis")
    print("-" * 40)

    print_summary_statistics(df_processed)

    # Create paradigm overview
    create_paradigm_overview_plot(df_processed, output_dir)
    print("✓ Created paradigm distribution overview plot")

    # Focus on Task 2 Response Probability (most important parameter)
    plot_task2_response_probability_distribution(df_processed, output_dir)
    print("✓ Created Task 2 Response Probability distribution plot")

    # Task 3: Stratified Distribution Analysis
    print("\nTask 3: Stratified Distribution Analysis by Paradigm")
    print("-" * 40)

    # Temporal Parameters
    plot_temporal_parameters_by_paradigm(df_processed, output_dir)
    print("✓ Created temporal parameter plots (Task 1 CSI, RSI)")

    # Merged Conflict Parameter
    plot_merged_conflict_by_paradigm(df_processed, output_dir)
    print("✓ Created merged conflict parameter plot")

    # Task Structure Parameters
    plot_task_structure_parameters(df_processed, output_dir)
    print("✓ Created task structure plots (Switch Rate, RSI Predictability)")

    # Paradigm-Specific SOA Parameters
    plot_paradigm_specific_soa_parameters(df_processed, output_dir)
    print("✓ Created paradigm-specific SOA plots")

    # Final summary
    print("\n" + "="*60)
    print("EDA ANALYSIS COMPLETE")
    print("="*60)
    print(f"All plots saved to: {output_dir.absolute()}")
    svg_count = len(list(output_dir.glob('*.svg')))
    png_count = len(list(output_dir.glob('*.png')))
    print(f"Total plots generated: {svg_count} SVG files, {png_count} PNG files")
    print("\nKey findings summary:")
    print(f"• Total experimental conditions analyzed: {len(df_processed)}")
    print(f"• Paradigm distribution: {df_processed['Paradigm'].value_counts().to_dict()}")
    print(f"• Task 2 Response Probability range: {df_processed['Task 2 Response Probability'].min():.1f} - {df_processed['Task 2 Response Probability'].max():.1f}")
    print("• All visualizations saved as high-quality SVG and PNG files")
    print("\nThe EDA reveals the parameter distributions across cognitive control paradigms,")
    print("showing clear distinctions between Interference, Task-Switching, and Dual-Task/PRP experiments.")


if __name__ == "__main__":
    main()
