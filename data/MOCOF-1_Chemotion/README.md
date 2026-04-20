# MOCOF-1_Chemotion

This folder will contain the dataset for the synthesis of MOCOF-1-(OH)2 (unpublished). Currently, the data is not published.

## chemotion_export.json

Synthetic procedures and product masses exported from [Chemotion electronic lab notebook](https://chemotion.net/#eln) v3.0.0.
Export procedure:
1. Create a new collection.
2. Assign reactions to the new collection.
3. Import and export > Export Collections > Choose the new collection, Export ZIP
4. Wait for a while
5. Notifications > click the link to download
6. Unzip the folder
7. Copy export.json to this folder and rename it to chemotion_export.json

## [converted](converted/)

Contains
- [the cleaned data](converted/chemotion_cleaned.json)
- the reformatted and validated data (converted/procedure_from_chemotion.json, characterization_from_chemotion.json)
