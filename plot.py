import mofax as mfx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_factor_weights_by_view(model, factor, n_features_per_view=5, figsize=(10, 15)):
    """
    Creates a clear, faceted horizontal bar plot of feature weights for a single factor,
    grouped by the conceptual views defined in the project.

    Args:
        model (mfx.mofa_model): The trained mofax model.
        factor (str): The name of the factor to plot (e.g., "Factor1").
        n_features_per_view (int): The number of top features to show for each view.
        figsize (tuple): The figure size.
    """
    # 1. Get all weights for the specified factor
    weights_df = model.get_weights(factors=factor, df=True)
    weights_df = weights_df.join(model.features_metadata[['view']])
    weights_df.rename(columns={factor: 'weight'}, inplace=True)
    weights_df['abs_weight'] = weights_df['weight'].abs()

    # 2. Get the top N features for each view
    top_features = []
    for view_name in model.views:
        top_view_features = weights_df[weights_df['view'] == view_name].nlargest(n_features_per_view, 'abs_weight')
        top_features.append(top_view_features)
    
    plot_data = pd.concat(top_features).sort_values(['view', 'abs_weight'], ascending=[True, False])
    plot_data.reset_index(names='feature', inplace=True) # feature names are in 'feature' column

    # 3. Create the faceted plot
    views = plot_data['view'].unique()
    n_views = len(views)
    fig, axes = plt.subplots(n_views, 1, figsize=figsize, sharex=True)
    if n_views == 1:
        axes = [axes] # Make it iterable if there's only one view

    # Define colors for positive and negative weights
    colors = ['#d6604d' if x < 0 else '#4393c3' for x in plot_data['weight']]
    plot_data['color'] = colors

    for i, view_name in enumerate(views):
        ax = axes[i]
        view_data = plot_data[plot_data['view'] == view_name]
        
        # Plot horizontal bars
        ax.barh(view_data['feature'], view_data['weight'], color=view_data['color'])

        ax.set_title(f'View: {view_name}', loc='left', fontweight='bold')
        ax.axvline(0, color='grey', linestyle='--', linewidth=0.8)
        ax.tick_params(axis='y', labelsize=9)
        ax.invert_yaxis()  # Puts the most important feature on top
        ax.grid(axis='x', linestyle=':', color='lightgrey')
        
        # Remove spines for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

    fig.suptitle(f'Top Feature Weights for {factor}', fontsize=16, y=1.0)
    axes[-1].set_xlabel("Feature Weight")
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    return fig

def add_na_mask_from_flag(final_plot_df):
    columns_to_mask = {'Inter-task SOA' : 'Inter-task SOA is NA', 'Distractor SOA': 'Distractor SOA is NA',
                       'Task 2 CSI': 'Task 2 CSI is NA', 'Task 2 Difficulty': 'Task 2 Difficulty is NA'}
    for column, flag_column in columns_to_mask.items():
        final_plot_df[column] = np.where(
                final_plot_df[flag_column] == 1,
                'N/A',
                final_plot_df[column].astype(str)
                )
    return final_plot_df
