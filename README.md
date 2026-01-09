# Data-Model–Based Processing and Analysis of MOF Synthesis Data
## Preparation
1. `pip install uv`
2. `cd [FAIRSynthesis_MOF folder path]`
3. `uv pip install -e .` (Do not forget the last dot)
4. `brew install graphviz` on macOS or `sudo apt install graphviz` on Linux

## Formatting, validation, and serialization into XDL
`uv run scripts/format_and_serialize_all.py`
## Serialization into MPIF
1. `cd scripts/mofsy2mpif`
2. `uv run npm install`
3. `uv run npm start`
## Phase mole fraction analysis of PXRD patterns
1. `uv run marimo edit`
2. Workspace > scripts > pxrd_analysis.mo.py
3. Run all slate cells (right bottom)
## Decision tree modeling
1. `uv run scripts/generate_decision_trees.py`
## Convex hull plotting
1. `uv run marimo edit`
2. Workspace > scripts > convex-hull.mo.py
3. Run all slate cells (right bottom)

## Contributing
Use `uv run ...` as a substitution for `python ...`.
New packages can be added using `uv add ...` instead of `pip install ...`.
Best results using the VSCode debugger are achieved by running `uv sync --all-packages`. Then just run `Python Debugger: Clear Cache and Reload Window` in the command palette.