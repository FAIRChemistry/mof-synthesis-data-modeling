# Data Model

This folder contains the JSON Schemas for this project.

Explore or edit a schema with [MetaConfigurator](https://metaconfigurator.org).
After clicking the link, open the corresponding schema files and navigate to the `Schema Editor` tab in the top left menu bar.


## Sciformation ELN Cleaned Schema

This is the schema of an intermediate step of our chain: the schema for a Sciformation ELN Export that has been cleaned up.
Data in this format is then used in a next step to export to MOFSY.



## MOFSY

MOFSY is based on a subset of [XDL](https://croningroup.gitlab.io/chemputer/xdl/standard/index.html) focused on MOF Synthesis and consists of a procedure schema, as well as a characterization schema.

## Fe–terephthalate

The Fe–terephthalate schema was inferred by MetaConfigurator when importing the `Fe–terephthalateRaw.csv` file.
It was used for code generation to parse the JSON files generated from the CSV file into MOFSY format.