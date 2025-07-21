from . import mofsy_api as api
from .generated.mofsy_data_structure import Mofsy

mofsy_file_path = "../../data/generated/mofsy_from_sciformation.json"
# Load MOFSY file into our MOFSYSchema class structure
mofsy: Mofsy = api.load_mofsy(mofsy_file_path)

# Access an individual experiment by id
example_experiment_id = "KE-232"
example_synthesis = api.get_synthesis_by_experiment_id(mofsy, example_experiment_id)
api.print_synthesis_data(example_synthesis)

# Access the product of an individual experiment
example_experiment_id_2 = "KE-010"
example_synthesis_2 = api.get_synthesis_by_experiment_id(mofsy, example_experiment_id_2)
product_2 = api.find_product(example_synthesis_2)
print(f"Experiment ID: {example_experiment_id}")
api.print_product(product_2)

# Access and count all experiments
synthesis_list = api.get_synthesis_list(mofsy)
print(f"Total number of experiments: {len(synthesis_list)}")

# Compute the average number of PXRD files per experiment
pxrd_files_per_experiment = []
for synthesis in synthesis_list:
    pxrd_files = api.find_corresponding_pxrd_files(synthesis)
    pxrd_files_per_experiment.append(len(pxrd_files))
average_pxrd_files = sum(pxrd_files_per_experiment) / len(pxrd_files_per_experiment)
print(f"Average number of PXRD files per experiment: {average_pxrd_files:.2f}")
