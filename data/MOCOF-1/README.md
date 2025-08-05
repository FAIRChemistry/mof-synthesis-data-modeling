# MOCOF-1

This folder contains the dataset for [the synthesis of MOCOF-1](https://www.nature.com/articles/s44160-024-00719-x).

## Sciformation_KE-MOCOF_jsonRaw.json

Synthetic procedures and product masses exported from [Sciformation electronic lab notebook](https://sciformation.com/sciformation_eln.html).

TODO

## [generated](./generated/)

Converting to the MOFSY format
For the conversion to the MOFSY format, see the [data model folder README](../../fairsynthesis_data_model/).

## [PXRD](./PXRD/)

PXRD patterns recorded on a Stoe Stadi P diffractometer (primary Ge(111)-Johann-type monochromator, single Mythen detector (Dectris), Debye-Scherrer geometry) and WinXPow software (v3.12.3).  
The measurements were conducted with sample spinning at room temperature.  
The measured data were converted into the XYD format (ASCII text. first column, 2theta; second column, counts per seconds) using the Raw Data Handling function of WinXPow.  
As this format does not support metadata export, all the metadata have been written in the filename according to the following rules, which are recognized by the Sciformation-MOFSY importer.

Filename template: PXRD\_(Experiment code)\_(X-ray source)\_(sample holder)\_\[conditions\]\_\[component\].xyd  
*The last two fields are optional and ignored by the Sciformation-MOFSY importer.  
X-ray source: Cu-Ka1 or Co-Ka1  
sample holder: capillary (Hilgenberg glass No. 14) or film (Kapton tape), with diameter
