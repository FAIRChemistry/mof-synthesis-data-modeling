# Data

This folder contains example datasets as subfolders.
In each subfolder, the "converted" folder contains
- cleaned ELN export
- reformatted and validated data (synthesis procedure and characterization)
- XDL and MPIF serializations

## PXRD data
In each subfolder, the "PXRD" folder contains PXRD patterns recorded on a Stoe Stadi P diffractometer (primary Ge(111)-Johann-type monochromator, single Mythen detector (Dectris), Debye-Scherrer geometry) and WinXPOW software (v3.12.3).
The measurements were conducted with sample spinning at room temperature.
The measured data were converted into the XYD format (ASCII text. first column, 2theta; second column, counts per seconds) using the Raw Data Handling function of WinXPOW.
As this format does not support metadata export, all the metadata have been written in the filename according to the following rules, which are recognized by the Sciformation-MOFSY importer.

Filename template: PXRD\_(Experiment code)\_(X-ray source)\_(sample holder)\_\[conditions\]\_\[component\].xyd
*The last two fields are optional and ignored by the Sciformation-MOFSY importer.
X-ray source: Cu-Ka1 or Co-Ka1
sample holder: capillary (Hilgenberg glass No. 14) or film (Kapton tape), with a diameter

## [Synthesis of Fe–terephthalate recorded on CSV](./Fe-terephthalate)

This folder contains the dataset for the synthesis of Fe–terephthalate.
The synthetic procedures and product masses were recorded in the CSV format, which has been converted to MOFSY format.

## [Synthesis of MOCOF-1 recorded on Sciformation electronic lab notebook](./MOCOF-1)

This folder contains the dataset for [the synthesis of MOCOF-1](https://www.nature.com/articles/s44160-024-00719-x), consisting of 183 entries.

## [Synthesis of MOCOF-1-(OH)2 recorded on Chemotion electronic lab notebook](./MOCOF-1_Chemotion)

This folder will contain the dataset for the synthesis of MOCOF-1-(OH)2 (unpublished). Currently, the data is not published.

## [Synthesis of Zr-NU-1000 recorded on Chemotion electronic lab notebook](./Zr-NU-1000)

This folder will contain the dataset for [the synthesis of Zr-NU-1000](https://chemrxiv.org/doi/full/10.26434/chemrxiv.15000703/v1), consisting of 4 entries.

## Data export procedure on [Chemotion electronic lab notebook](https://chemotion.net/#eln) v3.0.0
1. Create a new collection.
2. Assign reactions to the new collection.
3. Import and export > Export Collections > Choose the new collection, Export ZIP
4. Wait for a while (it can take several hours)
5. Notifications > click the link to download
6. Unzip the folder
7. Use export.json

## Data export procedure on [Sciformation electronic lab notebook](https://sciformation.com/sciformation_eln.html)
1. Lab journal > Search experiments
2. Search with certain parameters
3. ">>" → Copy Query URL
4. Paste it into the address bar. Change the "startUseCase?useCase=performSearch&" in the beginning to "performSearch?". Add "format=jsonRaw" at the end. Open the URL. (It takes time for large data)
5. Save the JSON data