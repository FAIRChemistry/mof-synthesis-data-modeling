# Data-Model–Based Processing and Analysis of MOF Synthesis Data
## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
---
## Overview
Preprint available at: https://chemrxiv.org/engage/chemrxiv/article-details/XXXX
This project formats, validates, serializes, and analyzes the given MOF synthesis data using data models. It was developed to demonstrate the usefulness of data models for realizing FAIR data and software management in chemical synthesis projects. The data models and codes can be reused by those who are interested in developing or using such a workflow.
---
## Features
- Two example datasets of MOF synthesis
- Formatting synthesis and characterization data into a well-defined and interoperable structure with the data models
- Rigorous data validation using JSON schema
- Data serialization into known formats, XDL and MPIF
- Phase mole fraction analysis of PXRD data using reference patterns
- Phase yield calculation based on mole fractions and yields using molar masses
- Modular scripts based on the data model APIs
---
## Installation
```bash
# Install uv
pip install uv
# Clone the repository
git clone https://github.com/FAIRChemistry/FAIRSynthesis_MOF.git
cd FAIRSynthesis_MOF
# Install dependencies in a virtual environment
uv pip install -e .
# Install Graphviz for decision tree visualization
brew install graphviz # macOS
sudo apt install graphviz # Debian/Ubuntu
# On Windows, install Graphviz from https://graphviz.org/download/
```
---
## Usage
### Formatting, validation, and serialization into XDL
```bash
uv run scripts/format_and_serialize_all.py
```
### Serialization into MPIF
```bash
cd scripts/mofsy2mpif
uv run npm install
uv run npm start
```
### Phase mole fraction analysis of PXRD patterns
```bash
uv run marimo edit
```
Workspace > scripts > pxrd_analysis.mo.py
Run all slate cells (right bottom)
### Decision tree modeling
```bash
uv run scripts/generate_decision_trees.py
```
### Convex hull plotting
```bash
uv run marimo edit
```
Workspace > scripts > convex-hull.mo.py
Run all slate cells (right bottom)

## Contributing
Use `uv run ...` as a substitution for `python ...`.
New packages can be added using `uv add ...` instead of `pip install ...`.
Best results using the VSCode debugger are achieved by running `uv sync --all-packages`. Then just run `Python Debugger: Clear Cache and Reload Window` in the command palette.