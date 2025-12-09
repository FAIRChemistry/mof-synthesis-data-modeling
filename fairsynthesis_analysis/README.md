# Data analysis tools
## Running
1. Install [uv](https://github.com/astral-sh/uv) by e.g., 'pip install uv'
2. Open cmd / Terminal, go to the `fairsynthesis_analysis` folder, and execute `uv run marimo edit` or `uv run examples/decision_tree.py`
In case of marimo:
3. Workspace > examples > pxrd_analysis.mo.py or statitstics.mo.py
4. Run all slate cells (right bottom)

## pxrd_analysis.mo.py
It imports PXRD patterns and metadata, and calculates the approximate molar fraction of each phase.

## statistics.mo.py
It imports molar fractions and synthesis data, calculates the approximate yield of each phase, and analyzes its statistics with respect to the synthesis procedure.

## decision_tree.py
It trains decision tree classifiers to model the outcome of the synthesis based on the synthesis parameters.
The decision tree it plotted.
Required the installation of graphviz (e.g., `brew install graphviz` on MacOS or `sudo apt install graphviz` on Linux).