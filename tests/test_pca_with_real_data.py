#!/usr/bin/env python3

import pandas as pd
import numpy as np
import pytest
from pathlib import Path

from analysis_utils import preprocess, create_pca_pipeline


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
    
    print("✓ All real dataset tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    test_pca_pipeline_with_real_dataset()