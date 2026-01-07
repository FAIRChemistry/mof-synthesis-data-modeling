import os
from datetime import datetime
from copy import deepcopy

from .utils import format_to_camel_case, load_json, save_json
from fair_synthesis.formatting.sciformation_text_extractor_llm_mocof1 import process_data_use_case_specific as process_data_with_llm
from fair_synthesis.formatting.sciformation_text_extractor_mocof1 import process_data_use_case_specific as process_data

important_item_attributes = [
    '@id',
    'nrInLabJournal',
    'creator',
    'code',
    'modifier'
    'reactionTitle',
    'reactionStartedWhen',
    'realizationText',
    'observationText',
]

important_reaction_properties = [
    'duration',
    'reaction_mass_unit',
    'reaction_volume_unit',
    'solventAmount'
    'solvent_volume_unit',
    'temperature'
]

important_reaction_component_attributes = [
    'moleculeName',
    'casNr',
    'mw',
    'empFormula',
    'concentration',
    'concentrationUnit',
    'smiles',
    'smilesStereo',
    'inchi',
    'inchiKey',
    'density20',
    'rxnRole',
    'mass',
    'massUnit',
    'volume',
    'volumeUnit',
    'amount',
    'amountUnit',
    'measured'
    'elnReaction'
    'cdbMolecule'
    'rxnRole',
    'labNotebookEntryAndRole'
]

rxnRoleMapping = {
    1: 'reactant',
    2: 'reagent',
    3: 'solvent',
    6: 'product'
}

def clean_data(data):
    trimmed_data = []
    for item in data:
        result = clean_item(item)
        if result:
            trimmed_data.append(result)
    return trimmed_data

def clean_item(item):
    new_item = {}
    for key, value in item.items():
        if key in important_item_attributes and value is not None:
            new_item[format_to_camel_case(key)] = value

    elnReactionPropertyCollection = item.get('elnReactionPropertyCollection', [])
    if elnReactionPropertyCollection:
        for reactionProperty in elnReactionPropertyCollection:
            if reactionProperty.get('name') in important_reaction_properties and reactionProperty.get('strValue') is not None:
                new_item[format_to_camel_case(reactionProperty.get('name'))] = reactionProperty.get('strValue')

    elnReactionComponentCollection = item.get('elnReactionComponentCollection', [])
    if elnReactionComponentCollection:
        reaction_components = []
        for reactionComponent in elnReactionComponentCollection:
            new_component = {}
            for key, value in reactionComponent.items():
                if key in important_reaction_component_attributes and value is not None:
                    new_component[key] = value
            reaction_components.append(new_component)
        new_item['reactionComponents'] = reaction_components

    return new_item


def apply_conversions(data):
    # convert rxnRole int to string
    for item in data:
        for component in item['reactionComponents']:
            component['rxnRole'] = rxnRoleMapping.get(component['rxnRole'], 'unknown')
            # sciformation always exports mass in g, even if different unit is selected in the ELN
            component['massUnit'] = 'g'

        item['durationUnit'] = 'h'
        item['temperatureUnit'] = 'C'
        if 'reactionStartedWhen' in item:
            # for reaction start, convert original ms to formatted date
            start_date = datetime.fromtimestamp(item['reactionStartedWhen'] / 1000)
            item['reactionStartedWhen'] = start_date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return data


def clean_sciformation_eln(data: dict, max_entry_length: int = -1, use_llm_for_extraction: bool = False) -> dict:
    trimmed_data = clean_data(data)
    postprocessed_data = apply_conversions(trimmed_data)

    # Process the data according to the current use-case
    if use_llm_for_extraction:
        process_data_with_llm(postprocessed_data)
    else:
        process_data(postprocessed_data)

    if max_entry_length > 0:
        postprocessed_data = postprocessed_data[:min(max_entry_length, len(postprocessed_data))]

    result = {
        "experiments": postprocessed_data
    }

    return result


if __name__ == '__main__':
    # Can be run independently to test the function
    current_file_dir = __file__.rsplit('/', 1)[0]
    file_path = os.path.join(current_file_dir, '../../..', 'data', 'MOCOF-1', 'Sciformation_KE-MOCOF_jsonRaw.json')
    result_file_path_normal = os.path.join(current_file_dir, '../../..', 'data', 'MOCOF-1', 'converted', 'sciformation_eln_cleaned.json')
    result_file_path_with_llm =  os.path.join(current_file_dir, '../../..', 'data', 'MOCOF-1', 'converted', 'sciformation_eln_cleaned_with_llm.json')
    data = load_json(file_path)
    result = clean_sciformation_eln(deepcopy(data))
    result_llm = clean_sciformation_eln(deepcopy(data), use_llm_for_extraction=True)

    save_json(result, result_file_path_normal)
    save_json(result_llm, result_file_path_with_llm)