import argparse
import os

from fair_synthesis.formatting.utils import load_json, save_json
from fair_synthesis.conversion_config import get_repo_root
from fair_synthesis.generated_apis.chemotion_cleaned_data_structure import (
    ChemotionCleanedSchema,
    chemotion_cleaned_schema_from_dict,
)
from fair_synthesis.generated_apis.chemotion_data_structure import schema_from_dict


def resolve_chemotion_input_path(repo_root: str) -> str:
    candidate_paths = [
        os.path.join(repo_root, "data", "MOCOF-1_Chemotion", "chemotion_export.json"),
        os.path.join(repo_root, "data", "chemotion_export.json", "export.json"),
    ]
    for candidate_path in candidate_paths:
        if os.path.exists(candidate_path):
            return candidate_path
    raise FileNotFoundError(
        "No Chemotion export found. Looked in: "
        + ", ".join(candidate_paths)
    )


def _resolve_sample(sample_id: str, samples: dict, molecules: dict, molecule_names: dict) -> dict:
    sample = samples.get(sample_id, {})
    molecule_id = sample.get("molecule_id")
    molecule_name_id = sample.get("molecule_name_id")
    molecule = molecules.get(molecule_id, {}) if molecule_id else {}
    mol_name_entry = molecule_names.get(molecule_name_id, {}) if molecule_name_id else {}

    name = mol_name_entry.get("name") or sample.get("name") or molecule.get("iupac_name") or sample.get("short_label", "")

    return {
        "id": sample_id,
        "name": name,
        "short_label": sample.get("short_label"),
        "inchikey": molecule.get("inchikey"),
        "inchistring": molecule.get("inchistring"),
        "molecular_weight": molecule.get("molecular_weight"),
        "real_amount_value": sample.get("real_amount_value"),
        "real_amount_unit": sample.get("real_amount_unit"),
        "target_amount_value": sample.get("target_amount_value"),
        "target_amount_unit": sample.get("target_amount_unit"),
    }


def _build_sample_entry(row: dict, sample_id: str, samples: dict, molecules: dict, molecule_names: dict) -> dict:
    return {
        "sample": _resolve_sample(sample_id, samples, molecules, molecule_names),
        "reference": row.get("reference", False),
        "equivalent": row.get("equivalent"),
        "position": row.get("position"),
    }


def _normalize_vessel_size(vessel_size: dict | None) -> dict | None:
    if not vessel_size:
        return None

    amount = vessel_size.get("amount")
    unit = vessel_size.get("unit")
    if amount is None or unit is None:
        return None

    return {
        "amount": amount,
        "unit": unit,
    }


def clean_chemotion(data: dict) -> ChemotionCleanedSchema:
    schema = schema_from_dict(data)

    samples: dict = data.get("Sample", {})
    molecules: dict = data.get("Molecule", {})
    molecule_names: dict = data.get("MoleculeName", {})
    reactions_raw: dict = data.get("Reaction", {})

    reactions = {}
    for reaction_id, rxn in reactions_raw.items():
        reactions[reaction_id] = {
            "id": reaction_id,
            "short_label": rxn.get("short_label", ""),
            "name": rxn.get("name", ""),
            "temperature": rxn.get("temperature"),
            "duration": rxn.get("duration", ""),
            "vessel_size": _normalize_vessel_size(rxn.get("vessel_size")),
            "plain_text_description": rxn.get("plain_text_description"),
            "plain_text_observation": rxn.get("plain_text_observation"),
            "starting_materials": [],
            "solvents": [],
            "purification_solvents": [],
            "products": [],
        }

    for row_id, row in data.get("ReactionsStartingMaterialSample", {}).items():
        rid = row.get("reaction_id")
        sid = row.get("sample_id")
        if rid not in reactions or sid not in samples:
            continue
        reactions[rid]["starting_materials"].append(
            _build_sample_entry(row, sid, samples, molecules, molecule_names)
        )

    for row_id, row in data.get("ReactionsSolventSample", {}).items():
        rid = row.get("reaction_id")
        sid = row.get("sample_id")
        if rid not in reactions or sid not in samples:
            continue
        reactions[rid]["solvents"].append(
            _build_sample_entry(row, sid, samples, molecules, molecule_names)
        )

    for row_id, row in data.get("ReactionsPurificationSolventSample", {}).items():
        rid = row.get("reaction_id")
        sid = row.get("sample_id")
        if rid not in reactions or sid not in samples:
            continue
        reactions[rid]["purification_solvents"].append(
            _build_sample_entry(row, sid, samples, molecules, molecule_names)
        )

    for row_id, row in data.get("ReactionsProductSample", {}).items():
        rid = row.get("reaction_id")
        sid = row.get("sample_id")
        if rid not in reactions or sid not in samples:
            continue
        reactions[rid]["products"].append(
            _build_sample_entry(row, sid, samples, molecules, molecule_names)
        )

    # Sort each section by position
    for rxn in reactions.values():
        for section in ("starting_materials", "solvents", "purification_solvents", "products"):
            rxn[section].sort(key=lambda e: e.get("position") or 0)

    cleaned = {"reactions": list(reactions.values())}
    return chemotion_cleaned_schema_from_dict(cleaned)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean a Chemotion export into the intermediate schema.")
    parser.add_argument("--input-path")
    parser.add_argument("--output-path")
    return parser


if __name__ == "__main__":
    args = _build_arg_parser().parse_args()
    repo_root = get_repo_root()
    input_path = args.input_path or resolve_chemotion_input_path(repo_root)
    output_path = args.output_path or os.path.join(
        repo_root, "data", "MOCOF-1_Chemotion", "converted", "chemotion_cleaned.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    result = clean_chemotion(load_json(input_path))
    save_json(result.to_dict(), output_path)
    print("Chemotion data cleaned and saved.")
