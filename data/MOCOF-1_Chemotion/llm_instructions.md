# LLM Instructions

This repository is about using data models in chemistry to model the synthesis procedure and characterization of Metal Organic Framework (MOF) compounds.

We have data from different sources (in `/data` folder):
- Fe-terephthalate: from Excel sheet
- MOCOF-1: from Sciformation ELN (electronic laboratory notebook)

And now newly added should be MOCOF-1 data from Chemotion ELN, which is a different format than the Sciformation ELN data.

For the Excel data, we have used MetaConfigurator to convert it to JSON, the Sciformation data already came as JSON and the Chemotion data also already is in JSON.
Our approach is, that for each of these input formats we create a JSON Schema using MetaConfigurator, my software which we want to showcase in our scientific paper, for which we do all this work.
Then we also built a JSON schema for our standardized format, which in this repository we call "MOFSY". 
Find the schemas in the `/data_model` folder.

We then generate data structure source code from the schemas using MetaConfigurator and the integrated quicktype library.
Find these data structures in `src/fair_synthesis/generated_apis`.

We then have python scripts to load the JSON data via the generated data structure code into Python dictionaries/structures. 
Then we have python scripts to read these dictionaries and write them into the standardized MOFSY format, which is then serialized as JSON and stored in the `/data/x/converted` folder.
These scripts are in `src/fair_synthesis/formatting`.

For the newly added Chemotion ELN, the provided schema is not matching the data. So first a second schema must be created (copy of the first one) and then adapted to the data.
The data file is huge. One way to avoid spending too many tokens could be iteratively using the jsonschema python library to check whether the schema is valid for the data, and if not, to check the error messages and adapt the schema accordingly.

Once the schema is proper, let me know and I will use MetaConfigurator with quicktype to generate the data structure source code. I will ping you once that is done.
Then we can write the python script to load the data using the generated data structures and then write the conversion script to convert it to MOFSY format.