# Scripts
## Running
1. Install [uv](https://github.com/astral-sh/uv) by e.g., 'pip install uv'
2. Open cmd / Terminal, go to the `scripts` folder, and execute `uv run format_and_serialize_all.py`, `uv run generate_decision_trees.py` or `uv run marimo edit`.

In case of marimo:
3. Workspace > examples > pxrd_analysis.mo.py or statitstics.mo.py
4. Run all slate cells (right bottom)

## format_and_serialize_all.py
Runs all formatting and serialization scripts to convert raw data into the MOFSY format and serialize it into XDL and MPIF.

## generate_decision_trees.py
It trains decision tree classifiers to model the outcome of the synthesis based on the synthesis parameters.
The decision tree it plotted.
Required the installation of graphviz (e.g., `brew install graphviz` on MacOS or `sudo apt install graphviz` on Linux).

## pxrd_analysis.mo.py
It imports PXRD patterns and metadata, and calculates the approximate molar fraction of each phase.

## convex-hull.mo.py
It imports molar fractions and synthesis data, calculates the approximate yield of each phase, and plots convex hulls with respect to the synthesis procedure.