from fair_synthesis.formatting.sciformation2mofsy import sciformation2mofsy
from fair_synthesis.formatting.mil2mofsy import mil2mofsy
from fair_synthesis.serialization.mofsy2xdl import mofsy2xdl
from fair_synthesis.serialization.extract_interesting_params import extract_interesting_params

sciformation2mofsy()
mil2mofsy()
mofsy2xdl()
# merge_mofsy()  Right now not executed because we do not work with a merged file.
extract_interesting_params()