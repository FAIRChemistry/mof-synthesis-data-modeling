import json
import os.path

import fairsynthesis_data_model.mofsy_api as api
from fairsynthesis_data_model.converted.procedure_data_structure import SynthesisProcedure
from fairsynthesis_data_model.converted.characterization_data_structure import ProductCharacterization
from fairsynthesis_data_model.converted.mocof_1_params import Mocof1Param

current_file_dir = __file__.rsplit('/', 1)[0]
procedure_file_path = os.path.join(current_file_dir, "../../data/MOCOF-1/converted/procedure_from_sciformation.json")
characterization_file_path = os.path.join(current_file_dir,
                                          "../../data/MOCOF-1/converted/characterization_from_sciformation.json")
params_file_path = os.path.join(current_file_dir, "../../data/MOCOF-1/converted/params_from_sciformation.json")

# Load Procedure file into our Procedure class structure
procedure: SynthesisProcedure = api.load_procedure(procedure_file_path)

# Load Characterization file into our CharacterizationEntry class structure
characterization: ProductCharacterization = api.load_characterization(characterization_file_path)

# Load Mocof 1 Params file into our Mocof1Param class structure
params: dict[str, Mocof1Param] = api.load_mocof_1_params(params_file_path)

# Access an individual experiment by id
example_experiment_id = "KE-232"
example_synthesis = api.get_synthesis_by_experiment_id(procedure, example_experiment_id)
example_characterization = api.get_characterization_by_experiment_id(characterization, example_experiment_id)
api.print_synthesis_data(example_synthesis, example_characterization)

# Access the product of an individual experiment
example_experiment_id_2 = "KE-010"
example_synthesis_2 = api.get_synthesis_by_experiment_id(procedure, example_experiment_id_2)
example_characterization_2 = api.get_characterization_by_experiment_id(characterization, example_experiment_id_2)
product_2 = api.find_product(example_synthesis_2, example_characterization_2)
print(f"Experiment ID: {example_experiment_id}")
api.print_product(product_2)

# Access and count all experiments
synthesis_list = api.get_synthesis_list(procedure)
print(f"Total number of experiments: {len(synthesis_list)}")

# Compute the average number of PXRD files per experiment
pxrd_files_per_experiment = []
for synthesis in synthesis_list:
    corresponding_characterization = api.get_characterization_by_experiment_id(characterization, synthesis.metadata.description)
    pxrd_files = api.find_corresponding_pxrd_files(corresponding_characterization)
    pxrd_files_per_experiment.append(len(pxrd_files))
average_pxrd_files = sum(pxrd_files_per_experiment) / len(pxrd_files_per_experiment)
print(f"Average number of PXRD files per experiment: {average_pxrd_files:.2f}")

# Print params of an experiment
example_experiment_id_3 = "KE-008"
example_synthesis_3 = api.get_params_by_experiment_id(params, example_experiment_id_3)
print(f"Parameters for Experiment ID {example_experiment_id_3}: {json.dumps(Mocof1Param.to_dict(example_synthesis_3))}")