import os

from .generated.characterization_data_structure import \
    ProductCharacterization
from .utils import load_json, save_string_as_file, save_json
from .generated.procedure_data_structure import Procedure
import json

def merge_mofsy_procecure_and_characterization(procedure: Procedure, characterization: ProductCharacterization) -> dict:
    """
    Merge Mofsy procedure and characterization into a single dictionary which is returned as a dict.
    Both inputs have a Metadata field which contains their unique id in the description field.
    Merging is done by finding the corresponding characterization for each procedure and adding it to the procedure.
    """
    result = []

    for proc in procedure.synthesis:
        metadata = proc.metadata
        proc_id = metadata.description if metadata and metadata.description else None

        if not proc_id:
            print("Warning: Procedure entry without metadata description (id). Skipping.")
            continue

        # Find the corresponding characterization
        matching_char = None
        for char in characterization.product_characterization:
            char_metadata = char.metadata
            char_id = char_metadata.description if char_metadata and char_metadata.description else None

            if char_id == proc_id:
                matching_char = char
                break

        if matching_char:
            proc_dict = proc.to_dict()
            proc_dict['Characterization'] = matching_char.characterization.to_dict()
            result.append(proc_dict)

    return result




def merge_mofsy():
    current_file_dir = __file__.rsplit('/', 1)[0]

    # sciformation case
    mofsy_procedure_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'procedure_from_sciformation.json')
    mofsy_characterization_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'characterization_from_sciformation.json')
    procedure = Procedure.from_dict(load_json(mofsy_procedure_file_path))
    characterization = ProductCharacterization.from_dict(load_json(mofsy_characterization_file_path))
    merged = merge_mofsy_procecure_and_characterization(procedure, characterization)
    save_json(merged, os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'merged_procedure_characterization.json'))

    # excel MIL_2 case
    mil_2_procedure_file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'procedure_from_MIL_2.json')
    mil_2_characterization_file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'characterization_from_MIL_2.json')
    procedure = Procedure.from_dict(load_json(mil_2_procedure_file_path))
    characterization = ProductCharacterization.from_dict(load_json(mil_2_characterization_file_path))
    merged = merge_mofsy_procecure_and_characterization(procedure, characterization)
    save_json(merged, os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'merged_procedure_characterization.json'))





if __name__ == '__main__':
    merge_mofsy()