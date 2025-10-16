import os
from typing import Tuple

from .generated.characterization_data_structure import \
    ProductCharacterization, CharacterizationEntry
from .utils import load_json, save_json
from .generated.procedure_data_structure import Procedure, SynthesisElement

def merge_mofsy_procecure_and_characterization(procedure: Procedure, characterization: ProductCharacterization) -> list[Tuple[SynthesisElement, CharacterizationEntry]]:
    """
    Merge Mofsy procedure and characterization into a single dictionary which is returned as a dict.
    Both inputs have a Metadata field which contains their unique id in the description field.
    Merging is done by finding the corresponding characterization for each procedure and adding it to the procedure.
    """
    result: list[Tuple[SynthesisElement, CharacterizationEntry]] = []

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
            result.append((proc, matching_char))

    return result



def merge_mofsy_procecure_and_characterization_to_dict(procedure: Procedure, characterization: ProductCharacterization) -> list[
    dict]:
    """
    Merge Mofsy procedure and characterization into a single dictionary which is returned as a dict.
    Both inputs have a Metadata field which contains their unique id in the description field.
    Merging is done by finding the corresponding characterization for each procedure and adding it to the procedure.
    """
    result = []

    matching_pairs = merge_mofsy_procecure_and_characterization(procedure, characterization)
    for proc, char in matching_pairs:
        proc_dict = proc.to_dict()
        proc_dict['Characterization'] = char.characterization.to_dict()

        for pxrd_entry in proc_dict['Characterization'].get('pxrd', []):
            if '_relative_file_path' in pxrd_entry:
                file_path = pxrd_entry['_relative_file_path']
                try:
                    with open(file_path, 'r') as f:
                        pxrd_content = f.read()
                    pxrd_entry['data'] = pxrd_content
                    proc_dict['Characterization']['pxrd'] = [pxrd_entry]
                except Exception as e:
                    print(f"Error processing PXRD file {file_path}: {e}")


        result.append(proc_dict)

    return result





def merge_mofsy():
    current_file_dir = __file__.rsplit('/', 1)[0]

    # sciformation case
    mofsy_procedure_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'procedure_from_sciformation.json')
    mofsy_characterization_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'characterization_from_sciformation.json')
    procedure = Procedure.from_dict(load_json(mofsy_procedure_file_path))
    characterization = ProductCharacterization.from_dict(load_json(mofsy_characterization_file_path))
    merged = merge_mofsy_procecure_and_characterization_to_dict(procedure, characterization)
    save_json(merged, os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'mofsy_from_sciformation.json'))

    # excel MIL_2 case
    mil_2_procedure_file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'procedure_from_MIL.json')
    mil_2_characterization_file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'characterization_from_MIL.json')
    procedure = Procedure.from_dict(load_json(mil_2_procedure_file_path))
    characterization = ProductCharacterization.from_dict(load_json(mil_2_characterization_file_path))
    merged = merge_mofsy_procecure_and_characterization_to_dict(procedure, characterization)
    save_json(merged, os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'mofsy_from_MIL.json'))





if __name__ == '__main__':
    merge_mofsy()