#!/usr/bin/env python3

import pandas as pd
import numpy as np
import pytest
from pathlib import Path

from analysis_utils import preprocess, create_pca_pipeline, reverse_map_categories


def test_pca_pipeline_with_real_dataset():
    """
    Tests the PCA pipeline with the full real dataset to ensure proper reconstruction
    and identify any issues that might be hidden by small test datasets.
    """
    # Load the real dataset
    data_path = Path(__file__).parent.parent / "data" / "super_experiment_design_space.csv"
    df_real = pd.read_csv(data_path)
    
    print(f"\n=== Real Dataset Test ===")
    print(f"Dataset shape: {df_real.shape}")
    print(f"Columns: {list(df_real.columns)}")
    
    # Preprocess the real data
    df_features, numerical_cols, categorical_cols, df_processed, preprocessor = preprocess(df_real)
    
    print(f"Features after preprocessing: {df_features.shape}")
    print(f"Numerical columns: {len(numerical_cols)}")
    print(f"Categorical columns: {len(categorical_cols)}")
    
    # Create and fit the PCA pipeline
    pipeline = create_pca_pipeline(numerical_cols, categorical_cols)
    pca_result = pipeline.fit_transform(df_features)
    
    # Get PCA diagnostics
    pca_step = pipeline.named_steps['pca']
    explained_variance_ratio = pca_step.explained_variance_ratio_
    cumulative_variance = explained_variance_ratio.cumsum()
    
    print(f"\n=== PCA Diagnostics ===")
    print(f"Original features: {df_features.shape[1]}")
    print(f"PCA components: {pca_result.shape[1]}")
    print(f"First 10 explained variance ratios: {explained_variance_ratio[:10]}")
    print(f"Total variance explained by first 5 components: {cumulative_variance[4]:.3f}")
    print(f"Total variance explained by all components: {cumulative_variance[-1]:.3f}")
    print(f"Dataset size: {df_features.shape[0]} samples")
    
    # Test reconstruction
    reconstructed_features_arr = pipeline.inverse_transform(pca_result)
    reconstructed_features_df = pd.DataFrame(
        reconstructed_features_arr, 
        columns=df_features.columns, 
        index=df_features.index
    )
    
    print(f"\n=== Reconstruction Analysis ===")
    
    # Test numerical reconstruction accuracy
    original_numeric = df_features[numerical_cols]
    reconstructed_numeric = reconstructed_features_df[numerical_cols].astype(float)
    
    # Calculate reconstruction errors for numerical columns
    numeric_errors = {}
    for col in numerical_cols:
        mse = np.mean((original_numeric[col] - reconstructed_numeric[col]) ** 2)
        max_abs_error = np.max(np.abs(original_numeric[col] - reconstructed_numeric[col]))
        numeric_errors[col] = {'mse': mse, 'max_abs_error': max_abs_error}
        print(f"Column '{col}': MSE={mse:.6f}, Max Abs Error={max_abs_error:.6f}")
    
    # Test categorical reconstruction
    original_categorical = df_features[categorical_cols]
    reconstructed_categorical = reconstructed_features_df[categorical_cols]
    
    categorical_accuracy = {}
    for col in categorical_cols:
        if col.endswith(' is NA') or col == 'RSI is Predictable':
            # Binary columns should now reconstruct perfectly with drop=None
            reconstructed_binary = reconstructed_categorical[col].astype(float).round().astype(int)
            accuracy = np.mean(original_categorical[col] == reconstructed_binary)
            categorical_accuracy[col] = accuracy
            print(f"Binary column '{col}': Accuracy={accuracy:.3f}")
            if accuracy < 0.99:  # Should be near perfect now
                print(f"  Unexpected low accuracy for binary column {col}")
        elif col.endswith(' Mapped'):
            # Categorical columns should also reconstruct very well
            original_vals = original_categorical[col].values
            reconstructed_vals = reconstructed_categorical[col].values
            accuracy = np.mean(original_vals == reconstructed_vals)
            categorical_accuracy[col] = accuracy
            print(f"Categorical column '{col}': Accuracy={accuracy:.3f}")
            if accuracy < 0.95:  # Should be near perfect now
                print(f"  Sample mismatches: Original={original_vals[:5]}, Reconstructed={reconstructed_vals[:5]}")
    
    # Assertions for the real dataset (should be much better than toy data)
    print(f"\n=== Test Assertions ===")
    
    # With real data, we should capture reasonable variance with first 5 components  
    # 60% is a more realistic threshold for real-world experimental data
    assert cumulative_variance[4] > 0.6, f"First 5 components should explain >60% variance, got {cumulative_variance[4]:.3f}"
    
    # Numerical reconstruction should be very accurate with sufficient data
    for col, errors in numeric_errors.items():
        assert errors['mse'] < 1e-10, f"Column {col} MSE too high: {errors['mse']}"
        assert errors['max_abs_error'] < 1e-8, f"Column {col} max error too high: {errors['max_abs_error']}"
    
    # With drop=None, reconstruction should be near perfect
    for col, accuracy in categorical_accuracy.items():
        if col.endswith(' is NA') or col == 'RSI is Predictable':
            assert accuracy > 0.95, f"Binary column {col} accuracy too low: {accuracy:.3f}"
        elif col.endswith(' Mapped'):
            assert accuracy > 0.90, f"Categorical column {col} accuracy too low: {accuracy:.3f}"


def test_pca_round_trip_is_near_perfect():
    """The full PCA round-trip should reproduce the original features."""
    data_path = Path(__file__).parent.parent / "data" / "super_experiment_design_space.csv"
    df_real = pd.read_csv(data_path)

    df_features, numerical_cols, categorical_cols, _, _ = preprocess(df_real)

    # Capture the canonical human-readable categories before any transformations.
    original_human_df = reverse_map_categories(df_features)
    human_readable_columns = [
        "Stimulus Bivalence & Congruency",
        "Stimulus-Stimulus Congruency",
        "Stimulus-Response Congruency",
        "Task 1 Stimulus-Response Mapping",
        "Task 2 Stimulus-Response Mapping",
        "Response Set Overlap",
        "Trial Transition Type",
        "Task 1 Cue Type",
        "Task 2 Cue Type",
        "Intra-Trial Task Relationship",
        "RSI is Predictable",
        "Inter-task SOA is Predictable",
    ]
    original_human_columns = [
        column for column in human_readable_columns if column in original_human_df.columns
    ]
    original_human_values = original_human_df[original_human_columns].copy()

    pipeline = create_pca_pipeline(numerical_cols, categorical_cols)
    pipeline.fit(df_features)

    preprocessor = pipeline.named_steps["preprocessor"]
    pca = pipeline.named_steps["pca"]

    # Transform to PCA space and reconstruct back to the original feature space
    transformed_features = preprocessor.transform(df_features)
    pc_scores = pca.transform(transformed_features)
    reconstructed_transformed = pca.inverse_transform(pc_scores)
    reconstructed_features = preprocessor.inverse_transform(reconstructed_transformed)

    reconstructed_df = pd.DataFrame(
        reconstructed_features,
        columns=df_features.columns,
        index=df_features.index,
    )

    original_numeric = df_features[numerical_cols].astype(float)
    reconstructed_numeric = reconstructed_df[numerical_cols].astype(float)
    numeric_diff = (original_numeric - reconstructed_numeric).abs()

    max_numeric_error = numeric_diff.to_numpy().max()
    mean_numeric_error = numeric_diff.to_numpy().mean()

    assert max_numeric_error < 1e-9, f"Max numeric error too high: {max_numeric_error}"
    assert mean_numeric_error < 1e-12, f"Mean numeric error too high: {mean_numeric_error}"

    original_categorical = df_features[categorical_cols]
    reconstructed_categorical = reconstructed_df[categorical_cols]

    for column in categorical_cols:
        mismatches = (~original_categorical[column].eq(reconstructed_categorical[column])).sum()
        assert mismatches == 0, f"Categorical column '{column}' failed to round-trip"

    reconstructed_human_df = reverse_map_categories(reconstructed_df)
    reconstructed_human_values = reconstructed_human_df[original_human_columns]

    for column in original_human_columns:
        pd.testing.assert_series_equal(
            original_human_values[column],
            reconstructed_human_values[column],
            check_dtype=False,
            obj=f"Human-readable column '{column}'",
        )
