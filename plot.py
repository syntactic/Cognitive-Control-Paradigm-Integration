import mofax as mfx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt

PARADIGM_COLORS = alt.Scale(domain=['Dual-Task_PRP', 'Interference', 'Task Switching', 'Single-Task'], 
                            range=['#440154', '#34CBAF', '#CB3450', '#FFA500'])

def hex_to_rgb(h):
    """Converts a hex color string to an RGB tuple."""
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_latent_space_plot(
    plot_df: pd.DataFrame,
    x_col: str,
    y_col: str,
    x_title: str,
    y_title: str,
    chart_title: str,
    tooltip_cols: list,
    width: int = 800,
    height: int = 750,
    has_interpolation: bool = False,
    output_filename: str = None
):
    """
    Creates a layered Altair scatter plot for a latent space (PCA or MOFA).

    Args:
        plot_df (pd.DataFrame): DataFrame containing the data to plot.
                                Must include x_col, y_col, 'Paradigm', and 'Point Type'.
                                If has_interpolation is True, must also include 'Parent1' and 'Parent2'.
        x_col (str): The name of the column for the x-axis (e.g., 'PC1', 'Factor1').
        y_col (str): The name of the column for the y-axis (e.g., 'PC2', 'Factor2').
        x_title (str): The title for the x-axis.
        y_title (str): The title for the y-axis.
        chart_title (str): The main title for the chart.
        tooltip_cols (list): A list of alt.Tooltip objects for the interactive tooltip.
        width (int): The width of the chart.
        height (int): The height of the chart.
        has_interpolation (bool): If True, adds a layer for interpolated points.
        output_filename (str): If provided, saves the chart to this file.

    Returns:
        alt.Chart: The final layered Altair chart object.
    """
    chart_layers = []

    # Layer 1: Centroids with radial gradient
    for category, hex_color in zip(PARADIGM_COLORS.domain, PARADIGM_COLORS.range):
        r, g, b = hex_to_rgb(hex_color)
        transparent_rgba = f'rgba({r}, {g}, {b}, 0)'
        layer = alt.Chart(plot_df).mark_circle(size=20000).encode(
            x=f'{x_col}:Q',
            y=f'{y_col}:Q',
            color=alt.value({
                "gradient": "radial",
                "stops": [{"offset": 0, "color": hex_color}, {"offset": 1, "color": transparent_rgba}]
            })
        ).transform_filter(
            (alt.datum.Paradigm == category) & (alt.datum['Point Type'] == 'Centroid')
        )
        chart_layers.append(layer)

    # Layer 2: Empirical Data Points
    empirical_chart = alt.Chart(plot_df).mark_circle(
        size=100,
        opacity=0.8,
        stroke='black',
        strokeWidth=0.2
    ).encode(
        x=alt.X(f'{x_col}:Q', title=x_title),
        y=alt.Y(f'{y_col}:Q', title=y_title),
        #color=alt.Color('Paradigm:N', title='Paradigm Class', scale=PARADIGM_COLORS),
        color=alt.Color(
            'Paradigm:N', 
            title='Paradigm Class', 
            scale=PARADIGM_COLORS,
            legend=alt.Legend(
                direction='horizontal',
                orient='bottom',
                titleOrient='left',
                titleAnchor='middle',
            )
        ),
        tooltip=tooltip_cols
    ).transform_filter(
        alt.datum['Point Type'] == 'Empirical Data'
    )
    chart_layers.append(empirical_chart)

    # Layer 3 (Conditional): Interpolated Points
    if has_interpolation:
        interpolated_chart = alt.Chart(plot_df).mark_point(
            size=400,
            shape='M0,.5L.6,.8L.5,.1L1,-.3L.3,-.4L0,-1L-.3,-.4L-1,-.3L-.5,.1L-.6,.8L0,.5Z', # Star shape
            filled=True,
            strokeWidth=4
        ).encode(
            x=alt.X(f'{x_col}:Q'),
            y=alt.Y(f'{y_col}:Q'),
            color=alt.Color('Parent1:N', title='Paradigm Class', scale=PARADIGM_COLORS, legend=None),
            stroke=alt.Color('Parent2:N', title='Paradigm Class', scale=PARADIGM_COLORS, legend=None),
            tooltip=tooltip_cols
        ).transform_filter(
            alt.datum['Point Type'] == 'Interpolated'
        )
        chart_layers.append(interpolated_chart)

    # Layer 4: Zero Lines
    zero_line_h = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5,5], color='grey').encode(y='y')
    zero_line_v = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(strokeDash=[5,5], color='grey').encode(x='x')
    chart_layers.append(zero_line_h)
    chart_layers.append(zero_line_v)

    # Combine layers
    final_chart = alt.layer(*chart_layers).properties(
        title=chart_title,
        width=width,
        height=height
    ).interactive()

    # Resolve scales if interpolation is used
    if has_interpolation:
        final_chart = final_chart.resolve_scale(
            color='independent',
            stroke='independent'
        ).resolve_legend(
            color='shared'
        )

    # Save the chart if a filename is provided
    if output_filename:
        final_chart.save(output_filename)

    return final_chart

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
