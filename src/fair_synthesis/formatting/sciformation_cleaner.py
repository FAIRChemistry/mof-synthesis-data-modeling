import argparse
import os
from datetime import datetime

from fair_synthesis.conversion_config import get_repo_root
from .utils import format_to_camel_case, load_json, save_json
from fair_synthesis.generated_apis.sciformation_eln_cleaned_data_structure import (
    SciformationCleanedELNSchema,
    sciformation_cleaned_eln_schema_from_dict,
)

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

    elnReactionPropertyCollection = item.get(
        'elnReactionPropertyCollection', [])
    if elnReactionPropertyCollection:
        for reactionProperty in elnReactionPropertyCollection:
            if reactionProperty.get('name') in important_reaction_properties and reactionProperty.get(
                    'strValue') is not None:
                new_item[format_to_camel_case(reactionProperty.get(
                    'name'))] = reactionProperty.get('strValue')

    elnReactionComponentCollection = item.get(
        'elnReactionComponentCollection', [])
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
            component['rxnRole'] = rxnRoleMapping.get(
                component['rxnRole'], 'unknown')
            # sciformation always exports mass in g, even if different unit is
            # selected in the ELN
            component['massUnit'] = 'g'

        item['durationUnit'] = 'h'
        item['temperatureUnit'] = 'C'
        if 'reactionStartedWhen' in item:
            # for reaction start, convert original ms to formatted date
            start_date = datetime.fromtimestamp(
                item['reactionStartedWhen'] / 1000)
            item['reactionStartedWhen'] = start_date.strftime(
                '%Y-%m-%d %H:%M:%S.%f')[:-3]
    return data


def clean_sciformation_eln(
        data: dict,
        max_entry_length: int = -1) -> SciformationCleanedELNSchema:
    trimmed_data = clean_data(data)
    postprocessed_data = apply_conversions(trimmed_data)

    if max_entry_length > 0:
        postprocessed_data = postprocessed_data[:min(
            max_entry_length, len(postprocessed_data))]

    result = sciformation_cleaned_eln_schema_from_dict({
        "experiments": postprocessed_data
    })
    return result


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean a Sciformation export into the intermediate schema.")
    parser.add_argument("--input-path")
    parser.add_argument("--output-path")
    return parser


if __name__ == '__main__':
    args = _build_arg_parser().parse_args()
    repo_root = get_repo_root()
    file_path = args.input_path or os.path.join(
        repo_root,
        'data',
        'MOCOF-1',
        'Sciformation_KE-MOCOF_jsonRaw.json')
    result_file_path_normal = args.output_path or os.path.join(
        repo_root,
        'data',
        'MOCOF-1',
        'converted',
        'sciformation_eln_cleaned.json')
    os.makedirs(os.path.dirname(result_file_path_normal), exist_ok=True)
    data = load_json(file_path)
    result = clean_sciformation_eln(data)

    save_json(result.to_dict(), result_file_path_normal)
