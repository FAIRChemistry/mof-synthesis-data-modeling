import os

from fairsynthesis_data_model.sciformation2mofsy import sciformation2mofsy
from fairsynthesis_data_model.mil2mofsy import mil2mofsy
from fairsynthesis_data_model.mofsy2xdl import mofsy2xdl
from fairsynthesis_data_model.merge_mofsy import merge_mofsy
from fairsynthesis_data_model.extract_interesting_params import extract_interesting_params

sciformation2mofsy()
mil2mofsy()
mofsy2xdl()
# merge_mofsy()  Right now not executed because we do not work with a merged file.
extract_interesting_params()