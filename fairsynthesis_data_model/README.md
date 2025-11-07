# Data Model

## Setup
1. Install [uv](https://github.com/astral-sh/uv)
3. open cmd / terminal, and change directory to this folder `fairsynthesis_data_model`. There you can use `uv run ...` as a substitution for `python ...` and everything you need will be installed.
4. New packages can be added using `uv add ...` instead of `pip install ...`.

## Scripts

Run the following scripts from the `fairsynthesis_data_model` directory.

### MOCOF-1 and Sciformation ELN to MOFSY and XDL

Re-run all conversions:
```bash
uv run examples/convert_all.py
```

Output example data from the converted data:
```bash
uv run examples/mofsy_api_example.py
```

Clean the sciformation ELN export:
```bash
uv run -m fairsynthesis_data_model.sciformation_cleaner
```

Convert the sciformation ELN export to MOFSY:
```bash
uv run -m fairsynthesis_data_model.sciformation2mofsy
```

Export the data in MOFSY format to XDL:
```bash
uv run -m fairsynthesis_data_model.mofsy2xdl
```

Run the API example:
```bash
uv run -m examples.mofsy_api_example
```

## Contributing
- Best results using the vscode debugger are achieved by running `uv sync --all-packages`. Then just run `Python Debugger: Clear Cache and Reload Window` in the command palette.