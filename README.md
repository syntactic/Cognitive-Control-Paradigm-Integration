# Cognitive Control Paradigm Integration

A Master's thesis project that integrates cognitive control paradigms (Interference, Task Switching, Dual-Task/PRP) into a unified, parametric design space with interactive visualization and analysis tools.

## Live Demos

- **[Interactive Experiment Viewer](https://syntactic.github.io/masters_thesis/)** - Explore and simulate coded experiments from the literature
- **[PCA Visualization](https://syntactic.github.io/masters_thesis/pca_plot.html)** - Interactive plot of experimental conditions in principal component space

## Project Overview

This project provides a systematic framework for understanding and comparing cognitive control experiments from the literature. It consists of three primary layers:

1. **Conceptual Layer** (`content/`): An Obsidian vault containing theoretical definitions, literature notes, and the conceptual framework
2. **Data Layer** (`data/`): Coded literature in CSV format representing the canonical design space
3. **Operational Layer**: Python data pipeline and JavaScript viewer for analysis and visualization

## Architecture

### Data Pipeline

The project follows a one-way data pipeline:

1. **Input**: `data/super_experiment_design_space.csv` - Master file with experiments coded using high-level derived dimensions
2. **Processing**: `convert.py` - Translates derived dimensions into absolute timing parameters
3. **Output**: `data/resolved_design_space.csv` - Resolved trial parameters with millisecond-level timings
4. **Visualization**: `index.html` + `viewer.js` - Web interface for exploring experiments and running simulations

### Key Components

#### Python Pipeline

- **`convert.py`**: Core translation engine that converts derived dimensions to low-level timing parameters
- **`analysis_utils.py`**: Utility functions for data analysis
- **`plot.py`**: Plotting utilities for visualizations
- **`tests/`**: Comprehensive test suite using pytest
  - `test_convert.py`: Tests for the conversion pipeline
  - `test_analysis_utils.py`: Tests for analysis utilities
  - `test_pca_with_real_data.py`: PCA validation tests

#### JavaScript Viewer

- **`index.html`**: Main user interface
- **`viewer.js`**: Client-side logic for experiment selection, timeline rendering, and simulation
- **`viewer.css`**: Styling for the web interface
- **`viewer.test.js`**: Jest unit tests for viewer logic
- **`viewer.test.data.js`**: Test data for viewer tests

#### Analysis Scripts

- **`scripts/eda_analysis.py`**: Exploratory data analysis
- **`scripts/study_stats.py`**: Statistical summaries
- **`scripts/convert_json_schema.py`**: JSON schema conversion utilities
- **Jupyter Notebooks**:
  - `pca_csv.ipynb`: PCA analysis with merged conflict dimensions
  - `pca_csv_distinct_conflict.ipynb`: PCA analysis with distinct conflict dimensions
  - `mofa_dense.ipynb`: MOFA+ analysis

## Requirements

- **Python**: 3.12+ (developed with Python 3.12.2)
- **Node.js**: For JavaScript dependencies and testing

## Installation

### Python Dependencies

```bash
pip install -r requirements.txt
```

Required packages (pinned versions in requirements.txt):
- pandas
- numpy
- scikit-learn
- pytest
- matplotlib
- seaborn
- mofapy2

### JavaScript Dependencies

```bash
npm install
```

Required packages:
- super-experiment (custom package)
- jest (for testing)

### Quartz (Documentation Site)

```bash
npm run quartz:install
```

## Usage

### Converting Data

Run the conversion pipeline to generate resolved timing parameters:

```bash
python convert.py
```

This reads `data/super_experiment_design_space.csv` and generates `data/resolved_design_space.csv`.

### Running Tests

Python tests:
```bash
pytest
```

JavaScript tests:
```bash
npm test
```

### Viewing Experiments

Open `index.html` in a web browser (preferably with a local server). The viewer provides:
- Dropdown selection of coded experiments
- SVG timeline visualization of trial structure
- Interactive simulation using the super-experiment package
- Experiment parameter display

### Building Documentation

Build the Quartz documentation site:
```bash
npm run quartz:build
```

Serve the documentation locally:
```bash
npm run quartz:serve
```

## Key Concepts

### Derived Dimensions

The project uses high-level derived dimensions to code experiments:
- **Task 1 CSI**: Cue-Stimulus Interval
- **Inter-task SOA**: Stimulus Onset Asynchrony between tasks
- **Distractor SOA**: Timing of distractor presentation
- **RSI**: Response-Stimulus Interval
- **Task 2 Response Probability**: Differentiates single-task (0.0) vs dual-task (1.0) paradigms
- **Switch Rate**: Proportion of task-switch trials
- **Stimulus Bivalence & Congruency**: Collapsed conflict dimension

### Conflict Dimensions

Two orthogonal conflict dimensions:
- **Stimulus-Stimulus (S-S) Congruency**: Semantic conflict (e.g., Stroop, Flanker)
- **Stimulus-Response (S-R) Congruency**: Spatial/structural conflict (e.g., Simon)

These are collapsed into a unified dimension for implementation.

### Parameter Overrides

The `Super_Experiment_Mapping_Notes` column in the CSV supports JSON parameter overrides for handling exceptions and special cases.

## Development Workflow

1. Verify experiment coding in `data/super_experiment_design_space.csv`
2. Run `python convert.py` to update resolved parameters
3. Open `index.html` to test visualization
4. Debug issues:
   - Timeline problems → Check `convert.py`
   - Simulation problems → Check `viewer.js`
5. Add tests for new logic in `viewer.test.js` or `tests/`

## Project Structure

```
.
├── content/                    # Obsidian vault with theoretical framework
│   ├── Canonical Tasks/       # Standard task definitions
│   ├── Dimensions/            # Dimension documentation
│   ├── Papers/                # Literature notes
│   └── ...
├── data/                       # Data files
│   ├── super_experiment_design_space.csv
│   └── resolved_design_space.csv
├── scripts/                    # Analysis scripts
│   ├── eda_analysis.py
│   ├── study_stats.py
│   └── eda_plots/             # Generated plots
├── tests/                      # Python test suite
├── report_data/                # PCA analysis outputs
├── convert.py                  # Main conversion pipeline
├── analysis_utils.py          # Analysis utilities
├── viewer.js                  # Web viewer logic
├── viewer.test.js             # Viewer tests
├── index.html                 # Web interface
└── *.ipynb                    # Analysis notebooks
```

## Analysis Outputs

- **PCA Results**: Principal component analysis with variance explained (see `report_data/`)
- **EDA Plots**: Exploratory visualizations (see `scripts/eda_plots/`)
- **Summary Statistics**: Dataset statistics (see `scripts/eda_stats/`)

## License

This project is part of a Master's thesis.