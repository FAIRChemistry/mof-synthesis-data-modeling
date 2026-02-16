import os
from copy import deepcopy

import jsonschema


from utils import load_json, save_json
from fair_synthesis.generated_apis.chemotion_fixed_data_structure import ChemotionFixed, Collection, CollectionsReaction, Reaction, Sample, \
    MoleculeName, Molecule, ReactionsStartingMaterialSample, ReactionsSolventSample, \
    ReactionsReactantSample, ReactionsProductSample


def clean_data(data: ChemotionFixed) -> dict:
    # chemotion data comes as a number of table-like arrays of dictionaries, which we have to match and combine to a more intuitive format
    collections = {}
    reactions = {}
    samples = {}
    molecule_names = {}
    molecules = {}

    # go over collections, which is a dictionary of key (collection id) and value (collection data)
    for collection_id, collection_data in data.collection.items():
        collection_data: Collection = collection_data  # type hint for better IDE support
        # create a new dictionary for the cleaned collection
        # relevant attributes: id, created_at, user_id
        cleaned_collection = {
            'id': collection_id,
            'created_at': collection_data.created_at.isoformat() if collection_data.created_at else '',
            'user_id': str(collection_data.user_id),
        }
        collections[collection_id] = cleaned_collection

    # go over reactions
    for reaction_id, reaction_data in data.reaction.items():
        reaction_data: Reaction = reaction_data
        # create a new dictionary for the cleaned reaction
        # relevant attributes: id, created_at, name, description, solvent, temperature, status, observation, purification, rf_value, timestamp_start, timestamp_stop, tlc_description, tlc_solvents
        cleaned_reaction = {
            'id': reaction_id,
            'created_at': reaction_data.created_at.isoformat() if reaction_data.created_at else '',
            'name': reaction_data.name,
            'description': reaction_data.description.to_dict(),
            'solvent': reaction_data.solvent,
            'temperature': reaction_data.temperature.to_dict(),
            'status': reaction_data.status,
            'observation': reaction_data.observation.to_dict(),
            'purification': reaction_data.purification,
            'rf_value': reaction_data.rf_value,
            'timestamp_start': reaction_data.timestamp_start if reaction_data.timestamp_start else '',
            'timestamp_stop': reaction_data.timestamp_stop if reaction_data.timestamp_stop else '',
            'tlc_description': reaction_data.tlc_description,
            'tlc_solvents': reaction_data.tlc_solvents,
        }
        reactions[reaction_id] = cleaned_reaction

    # go over molecule names
    for moleculename_id, molecule_name in data.molecule_name.items():
        # we will create a new dictionary for the cleaned molecule name
        # relevant attributes: id, name
        molecule_name: MoleculeName = molecule_name
        cleaned_molecule_name = {
            'molecule_id': str(molecule_name.molecule_id),
            'name': molecule_name.name,
            'description': molecule_name.description,
            'created_at': molecule_name.created_at.isoformat() if molecule_name.created_at else '',
            'updated_at': molecule_name.updated_at.isoformat() if molecule_name.updated_at else '',
        }
        molecule_names[str(molecule_name.molecule_id)] = cleaned_molecule_name

    # go over molecules
    for molecule_id, molecule_data in data.molecule.items():
        # we will create a new dictionary for the cleaned molecule
        # relevant attributes: id, created_at, inchikey, inchistring, density, molecular_weight, molfile, melting_point, boiling_point, names, created_at, updated_at
        molecule_data: Molecule = molecule_data
        cleaned_molecule = {
            'id': str(molecule_id),
            'created_at': molecule_data.created_at.isoformat() if molecule_data.created_at else '',
            'inchikey': molecule_data.inchikey,
            'inchistring': molecule_data.inchistring,
            'density': molecule_data.density,
            'molecular_weight': molecule_data.molecular_weight,
            'molfile': molecule_data.molfile,
            'melting_point': molecule_data.melting_point,
            'boiling_point': molecule_data.boiling_point,
            'names': molecule_data.names,
            "additionalName": molecule_names.get(str(molecule_id), None),
            'updated_at': molecule_data.updated_at.isoformat() if molecule_data.updated_at else '',
        }
        molecules[str(molecule_id)] = cleaned_molecule

    # go over samples
    for sample_id, sample_data in data.sample.items():

        # we will create a new dictionary for the cleaned sample
        sample_data: Sample = sample_data  # type hint for better IDE support
        cleaned_sample = {
            'id': str(sample_id),
            'name': sample_data.name,
            'description': sample_data.description,
            'created_at': sample_data.created_at.isoformat() if sample_data.created_at else '',
            'created_by': str(sample_data.created_by),
            'impurities': sample_data.impurities,
            # 'molecule_id': str(sample_data.molecule_id),
            'molecule': molecules.get(str(sample_data.molecule_id), None),
            'molfile': sample_data.molfile,
            'purity': sample_data.purity,
            'target_amount_unit': sample_data.target_amount_unit,
            'target_amount_value': sample_data.target_amount_value,
        }
        samples[sample_id] = cleaned_sample


    # go over reactions_starting_material_sample and link them
    for row_id, reaction_starting_material in data.reactions_starting_material_sample.items():
        reaction_starting_material: ReactionsStartingMaterialSample = reaction_starting_material  # type hint for better IDE support
        reaction_id = str(reaction_starting_material.reaction_id)
        sample_id = str(reaction_starting_material.sample_id)

        if not reaction_id in reactions:
            print(f"Skipping row {row_id} due to missing reaction {reaction_id}")
            continue
        if not sample_id in samples:
            print(f"Skipping row {row_id} due to missing sample {sample_id}")
            continue
        reaction: dict = reactions[reaction_id]
        sample: dict = samples[sample_id]
        if 'starting_materials' not in reactions[reaction_id]:
            reaction['starting_materials'] = []
        reaction['starting_materials'].append(
            {
            "sample": sample,
            "coefficient": reaction_starting_material.coefficient,
            "position": reaction_starting_material.position,
            "waste": reaction_starting_material.waste,
            "reference": reaction_starting_material.reference,
        })

    # go over reactions_solvent_sample and link them
    for row_id, reaction_solvent_sample in data.reactions_solvent_sample.items():
        reaction_solvent_sample: ReactionsSolventSample = reaction_solvent_sample  # type hint for better IDE support
        reaction_id = str(reaction_solvent_sample.reaction_id)
        sample_id = str(reaction_solvent_sample.sample_id)

        if not reaction_id in reactions:
            print(f"Skipping row {row_id} due to missing reaction {reaction_id}")
            continue
        if not sample_id in samples:
            print(f"Skipping row {row_id} due to missing sample {sample_id}")
            continue
        reaction: dict = reactions[reaction_id]
        sample: dict = samples[sample_id]

        if 'solvents' not in reactions[reaction_id]:
            reaction['solvents'] = []
        reaction['solvents'].append(
            {
                "sample": sample,
                "coefficient": reaction_solvent_sample.coefficient,
                "position": reaction_solvent_sample.position,
                "waste": reaction_solvent_sample.waste,
                "reference": reaction_solvent_sample.reference,
            }
        )

    # go over reactions_reactant_sample
    for row_id, reaction_reactant_sample in data.reactions_reactant_sample.items():
        reaction_reactant_sample: ReactionsReactantSample = reaction_reactant_sample  # type hint for better IDE support
        reaction_id = str(reaction_reactant_sample.reaction_id)
        sample_id = str(reaction_reactant_sample.sample_id)

        if not reaction_id in reactions:
            print(f"Skipping row {row_id} due to missing reaction {reaction_id}")
            continue
        if not sample_id in samples:
            print(f"Skipping row {row_id} due to missing sample {sample_id}")
            continue
        reaction: dict = reactions[reaction_id]
        sample: dict = samples[sample_id]

        if 'reactants' not in reactions[reaction_id]:
            reaction['reactants'] = []
        reaction['reactants'].append(
            {
                "sample": sample,
                "coefficient": reaction_reactant_sample.coefficient,
                "position": reaction_reactant_sample.position,
                "waste": reaction_reactant_sample.waste,
                "reference": reaction_reactant_sample.reference,
            }
        )

    # go over reactions_product_sample
    for row_id, reaction_product_sample in data.reactions_product_sample.items():
        reaction_product_sample: ReactionsProductSample = reaction_product_sample  # type hint for better IDE support
        reaction_id = str(reaction_product_sample.reaction_id)
        sample_id = str(reaction_product_sample.sample_id)

        if not reaction_id in reactions:
            print(f"Skipping row {row_id} due to missing reaction {reaction_id}")
            continue
        if not sample_id in samples:
            print(f"Skipping row {row_id} due to missing sample {sample_id}")
            continue
        reaction: dict = reactions[reaction_id]
        sample: dict = samples[sample_id]

        if 'products' not in reactions[reaction_id]:
            reaction['products'] = []
        reaction['products'].append(
            {
                "sample": sample,
                "coefficient": reaction_product_sample.coefficient,
                "position": reaction_product_sample.position,
                "waste": reaction_product_sample.waste,
                "reference": reaction_product_sample.reference,
            }
        )

    # go over collections_reaction table and link them
    for row_id, collection_reaction in data.collections_reaction.items():
        collection_reaction: CollectionsReaction = collection_reaction # type hint for better IDE support
        collection_id = str(collection_reaction.collection_id)
        reaction_id = str(collection_reaction.reaction_id)

        if not collection_id in collections:
            print(f"Skipping row {row_id} due to missing collection {collection_id}")
            continue
        if not reaction_id in reactions:
            print(f"Skipping row {row_id} due to missing reaction {reaction_id}")
            continue
        collection = collections[collection_id]
        reaction = reactions[reaction_id]

        if 'reactions' not in collections[collection_id]:
            collection['reactions'] = []
        collection['reactions'].append(reaction)

    # now we have cleaned all data and linked them together
    result = {
        "collections" : collections
    }

    return result

def clean_chemotion(
        data: ChemotionFixed,
        use_llm_for_extraction: bool = False) -> dict:
    trimmed_data = clean_data(data)
    # postprocessed_data = apply_conversions(trimmed_data)

    # Process the data according to the current use-case
    # if use_llm_for_extraction:
    #     process_data_with_llm(postprocessed_data)
    # else:
    #     process_data(postprocessed_data)

    # if max_entry_length > 0:
    #    postprocessed_data = postprocessed_data[:min(
    #        max_entry_length, len(postprocessed_data))]

    result = {
        "experiments": trimmed_data
    }

    return result


if __name__ == '__main__':
    # Can be run independently to test the function
    current_file_dir = __file__.rsplit('/', 1)[0]
    file_path = os.path.join(
        current_file_dir,
        '../../..',
        'data',
        'MOCOF-1-Chemotion',
        'Sciformation_KE-MOCOF_jsonRaw.json')
    result_file_path_normal = os.path.join(
        current_file_dir,
        '../../..',
        'data',
        'MOCOF-1-Chemotion',
        'converted',
        'chemotion_cleaned.json')
    result_file_path_with_llm = os.path.join(
        current_file_dir,
        '../../..',
        'data',
        'MOCOF-1',
        'converted',
        'chemotion_cleaned_with_llm.json')
    input_file_schema = os.path.join(
        current_file_dir,
        '../../..',
        'data_model',
        'chemotion.schema.json')
    data = load_json(file_path)
    result_file_schema = os.path.join(
        current_file_dir,
        '../../..',
        'data_model',
        'chemotion_cleaned.schema.json')

    data = load_json(file_path)
    input_schema = load_json(input_file_schema)
    result_schema = load_json(result_file_schema)

    # validate input file by schema
    jsonschema.validate(instance=data, schema=input_schema)
    chemotion: ChemotionFixed = ChemotionFixed.from_dict(data)

    result = clean_chemotion(deepcopy(chemotion))
    # result_llm = clean_sciformation_eln(
    #     deepcopy(data), use_llm_for_extraction=True)

    save_json(result, result_file_path_normal)
    # save_json(result_llm, result_file_path_with_llm)
