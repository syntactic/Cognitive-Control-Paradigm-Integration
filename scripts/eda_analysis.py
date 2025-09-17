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
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import analysis_utils as au

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
        'Task 2 Response Probability', 'RSI', 'Task 1 CSI',
        'Inter-task SOA', 'Distractor SOA', 'Switch Rate'
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
    main_paradigms = ['Interference', 'Task Switching', 'Dual-Task_PRP']
    df_main = df_processed[df_processed['Paradigm'].isin(main_paradigms)].copy()

    # Task 1 CSI by paradigm
    plt.figure(figsize=(12, 6))

    # Clean the CSI data
    df_main['Task 1 CSI Clean'] = pd.to_numeric(df_main['Task 1 CSI'], errors='coerce')

    # Create violin plot
    sns.violinplot(data=df_main, x='Paradigm', y='Task 1 CSI Clean', inner='box')
    plt.title('Distribution of Task 1 CSI by Paradigm', fontsize=14, fontweight='bold')
    plt.xlabel('Paradigm')
    plt.ylabel('Task 1 CSI (ms)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'task1_csi_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'task1_csi_by_paradigm.png', format='png', dpi=100)
    plt.close()

    # RSI by paradigm
    plt.figure(figsize=(12, 6))

    # Clean the RSI data using the utility function
    df_main['RSI Clean'] = df_main['RSI'].apply(au.clean_rsi)

    # Create box plot for RSI (better for skewed data)
    sns.boxplot(data=df_main, x='Paradigm', y='RSI Clean')
    plt.title('Distribution of RSI by Paradigm', fontsize=14, fontweight='bold')
    plt.xlabel('Paradigm')
    plt.ylabel('RSI (ms)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'rsi_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'rsi_by_paradigm.png', format='png', dpi=100)
    plt.close()


def plot_conflict_parameters_by_paradigm(df_processed, output_dir):
    """
    Create bar plots for conflict/congruency parameters by paradigm.

    Args:
        df_processed (pd.DataFrame): The processed dataset
        output_dir (Path): Directory to save plots
    """
    main_paradigms = ['Interference', 'Task Switching', 'Dual-Task_PRP']
    df_main = df_processed[df_processed['Paradigm'].isin(main_paradigms)].copy()

    # Stimulus-Stimulus Congruency by paradigm
    plt.figure(figsize=(14, 8))

    # Collapse neutral subtypes into just "Neutral" and handle N/A values
    df_main_ss = df_main.copy()
    df_main_ss['Stimulus-Stimulus Congruency Collapsed'] = df_main_ss['Stimulus-Stimulus Congruency'].apply(
        lambda x: 'Neutral' if pd.notna(x) and 'Neutral' in str(x)
        else 'N/A' if pd.isna(x) or str(x) == 'nan'
        else x
    )

    # Create crosstab for counts
    ss_crosstab = pd.crosstab(df_main_ss['Paradigm'], df_main_ss['Stimulus-Stimulus Congruency Collapsed'])

    # Normalize to proportions (each paradigm sums to 1.0)
    ss_crosstab_norm = ss_crosstab.div(ss_crosstab.sum(axis=1), axis=0)

    # Create stacked bar plot
    ss_crosstab_norm.plot(kind='bar', stacked=False, figsize=(12, 6))
    plt.title('Stimulus-Stimulus Congruency Distribution by Paradigm', fontsize=14, fontweight='bold')
    plt.xlabel('Paradigm')
    plt.ylabel('Proportion of Conditions')
    plt.xticks(rotation=45)
    plt.legend(title='Stimulus-Stimulus Congruency', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'stimulus_stimulus_congruency_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'stimulus_stimulus_congruency_by_paradigm.png', format='png', dpi=100)
    plt.close()

    # Stimulus-Response Congruency by paradigm
    plt.figure(figsize=(14, 8))

    # Handle N/A values for Stimulus-Response Congruency
    df_main_sr = df_main.copy()
    df_main_sr['Stimulus-Response Congruency Clean'] = df_main_sr['Stimulus-Response Congruency'].apply(
        lambda x: 'N/A' if pd.isna(x) or str(x) == 'nan' else x
    )

    # Create crosstab for counts
    sr_crosstab = pd.crosstab(df_main_sr['Paradigm'], df_main_sr['Stimulus-Response Congruency Clean'])

    # Normalize to proportions (each paradigm sums to 1.0)
    sr_crosstab_norm = sr_crosstab.div(sr_crosstab.sum(axis=1), axis=0)

    # Create stacked bar plot
    sr_crosstab_norm.plot(kind='bar', stacked=False, figsize=(12, 6))
    plt.title('Stimulus-Response Congruency Distribution by Paradigm', fontsize=14, fontweight='bold')
    plt.xlabel('Paradigm')
    plt.ylabel('Proportion of Conditions')
    plt.xticks(rotation=45)
    plt.legend(title='Stimulus-Response Congruency', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'stimulus_response_congruency_by_paradigm.svg', format='svg', dpi=300)
    plt.savefig(output_dir / 'stimulus_response_congruency_by_paradigm.png', format='png', dpi=100)
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
        plt.hist(task_switching_data['Switch Rate Clean'], bins=15, alpha=0.7, color='orange', edgecolor='black')
        plt.title('Distribution of Switch Rate in Task Switching Paradigm', fontsize=14, fontweight='bold')
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
    plt.figure(figsize=(12, 6))

    main_paradigms = ['Interference', 'Task Switching', 'Dual-Task_PRP']
    df_main = df_processed[df_processed['Paradigm'].isin(main_paradigms)].copy()

    # Create crosstab for RSI predictability
    rsi_pred_crosstab = pd.crosstab(df_main['Paradigm'], df_main['RSI is Predictable'])

    # Normalize to proportions (each paradigm sums to 1.0)
    rsi_pred_crosstab_norm = rsi_pred_crosstab.div(rsi_pred_crosstab.sum(axis=1), axis=0)

    # Create stacked bar plot
    ax = rsi_pred_crosstab_norm.plot(kind='bar', stacked=False, color=['lightcoral', 'lightblue'])

    # Update legend labels from 0/1 to No/Yes
    handles, labels = ax.get_legend_handles_labels()
    new_labels = ['No' if label == '0' else 'Yes' if label == '1' else label for label in labels]
    ax.legend(handles, new_labels, title='RSI is Predictable')
    plt.title('RSI Predictability by Paradigm', fontsize=14, fontweight='bold')
    plt.xlabel('Paradigm')
    plt.ylabel('Proportion of Conditions')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
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
            plt.hist(inter_task_soa_clean, bins=30, alpha=0.7, color='green', edgecolor='black')
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
            plt.hist(distractor_soa_clean, bins=15, alpha=0.7, color='red', edgecolor='black')
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

    # Conflict & Congruency Parameters
    plot_conflict_parameters_by_paradigm(df_processed, output_dir)
    print("✓ Created conflict parameter plots (S-S and S-R congruency)")

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
    print("showing clear distinctions between Interference, Task Switching, and Dual-Task/PRP experiments.")


if __name__ == "__main__":
    main()
