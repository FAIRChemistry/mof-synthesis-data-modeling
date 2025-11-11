# Data analysis tools
## Running
1. Install [uv](https://github.com/astral-sh/uv) by e.g., 'pip install uv'
2. open cmd / Terminal, go to the `fairsynthesis_analysis` folder, and type `uv run marimo edit`
3. Workspace > examples > pxrd_analysis.mo.py or statitstics.mo.py
4. run all slate cells (right bottom)

## pxrd_analysis.mo.py
It imports PXRD patterns and metadata, and calculates the approximate molar fraction of each phase.

## statistics.mo.py
It imports molar fractions and synthesis data, calculates the approximate yield of each phase, and analyzes its statistics with respect to the synthesis procedure.