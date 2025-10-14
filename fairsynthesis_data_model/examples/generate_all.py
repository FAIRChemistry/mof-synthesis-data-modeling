import os

from fairsynthesis_data_model.sciformation2mofsy import sciformation2mofsy
from fairsynthesis_data_model.mil2_2mofsy import mil2mofsy
from fairsynthesis_data_model.mofsy2xdl import mofsy2xdl
from fairsynthesis_data_model.merge_mofsy import merge_mofsy
from fairsynthesis_data_model.mofsy2mpif import mofsy2mpif

sciformation2mofsy()
mil2mofsy()
mofsy2xdl()
merge_mofsy()
mofsy2mpif()