# Data Model
## Scripts
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
