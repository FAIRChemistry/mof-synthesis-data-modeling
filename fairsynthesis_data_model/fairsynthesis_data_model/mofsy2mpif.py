import math
import os
from datetime import date
from typing import Tuple

from .generated.characterization_data_structure import \
    ProductCharacterization, CharacterizationEntry
from .merge_mofsy import merge_mofsy_procecure_and_characterization
from .utils import load_json, save_string_as_file, save_starfile
from .generated.procedure_data_structure import Procedure, SynthesisElement, XMLType, AmountUnit, Role, ReagentElement
import starfile
import pandas as pd

def convert_mofsy_to_mpif(procedure: Procedure, characterization: ProductCharacterization) -> dict[str, dict]:
    """
    Convert Mofsy procedure to MPIF from EU4MOFs, which is in STARFile format.
    Result is a dictionary of filenames and their content.
    """
    results: dict[str, dict] = {}

    merged_pairs: list[Tuple[SynthesisElement, CharacterizationEntry]]  = merge_mofsy_procecure_and_characterization(procedure, characterization)
    for proc, char in merged_pairs:
        star_content = experiment_to_mpif(proc, char)
        experiment_id = proc.metadata.description if proc.metadata and proc.metadata.description else "unknown_id"
        filename = f"{experiment_id}.mpif"
        results[filename] = star_content
    return results

def experiment_to_mpif(proc, char) -> dict:
    """Generate an MPIF-compliant STARFILE data structure from synthesis and characterization data."""

    product_name = getattr(proc.metadata, "product", "unknown")

    # Extract reaction conditions
    react_temperature = -1
    react_time = -1
    react_time_unit = "unknown"
    react_vessel = "unknown"
    for reaction_step in proc.procedure.reaction.step:
        if reaction_step.xml_type == XMLType.HEAT_CHILL:
            react_temperature = reaction_step.temp.value
            react_time = reaction_step.time.value
            if reaction_step.time.unit == AmountUnit.HOUR:
                react_time_unit = "hours"
            elif reaction_step.time.unit == AmountUnit.MINUTE:
                react_time_unit = "minutes"
            elif reaction_step.time.unit == AmountUnit.DAY:
                react_time_unit = "days"
            react_vessel = reaction_step.vessel
            if react_vessel:
                for hardware in proc.hardware.component:
                    if hardware.id == react_vessel and hardware.type:
                        react_vessel = hardware.type
                        break
            break

    # Collect solvents
    solvents = [
        reagent for reagent in getattr(proc.reagents, "reagent", [])
        if reagent.role == Role.SOLVENT
    ]

    solvent_rows = []
    for reagent in solvents:
        solvent_rows.append({
            "mpif_solvent_id": getattr(reagent, "id", ""),
            "mpif_solvent_name": getattr(reagent, "name", ""),
            "mpif_solvent_molarity": "",
            "mpif_solvent_molarity_unit": "",
            "mpif_solvent_amount": getattr(reagent, "amount", ""),
            "mpif_solvent_amount_unit": getattr(reagent, "amount_unit", ""),
            "mpif_solvent_supplier": getattr(reagent, "supplier", ""),
            "mpif_solvent_purity_percent": "",
            "mpif_solvent_cas": "?",
            "mpif_solvent_smiles": ""
        })

    solvent_df = pd.DataFrame(solvent_rows)

    # Example placeholders for other loops (vessels, hardware, procedures)
    vessel_df = pd.DataFrame([{
        "mpif_vessel_id": "V1",
        "mpif_vessel_volume": "10",
        "mpif_vessel_volume_unit": "mL",
        "mpif_vessel_material": "glass",
        "mpif_vessel_type": "Vial",
        "mpif_vessel_supplier": "-",
        "mpif_vessel_purpose": "Reaction",
        "mpif_vessel_note": "S-1"
    }])

    procedure_df = pd.DataFrame([
        {
            "mpif_procedure_id": "1760366103586",
            "mpif_procedure_type": "Preparation",
            "mpif_procedure_atmosphere": "Air",
            "mpif_procedure_detail": (
                "Add 16mg FeCl3 to vessel S-1.\n"
                "Add 16mg Benzene-1,4-dicarboxylic acid to vessel S-1.\n"
                "Add 4ml DMF to vessel S-1."
            )
        },
        {
            "mpif_procedure_id": "1760366256793",
            "mpif_procedure_type": "Reaction",
            "mpif_procedure_atmosphere": "Air",
            "mpif_procedure_detail": (
                "Sonicate 30 minute.\n"
                f"HeatChill for {react_time} {react_time_unit} at {react_temperature} Celsius. In: oven."
            )
        },
        {
            "mpif_procedure_id": "1760366347169",
            "mpif_procedure_type": "Work-up",
            "mpif_procedure_atmosphere": "Air",
            "mpif_procedure_detail": (
                "Wash with Ethanol.\n"
                "Dry at 120 Celsius."
            )
        }
    ])

    # Build the flat data block
    data_block = {
        # Header info
        "mpif_audit_creation_date": str(date.today()),
        "mpif_audit_generator_version": "1.0",
        "mpif_audit_publication_doi": "''",
        "mpif_audit_procedure_status": "'success'",

        # Section 1: Author details
        "mpif_audit_contact_author_name": "'Kenichi Endo'",
        "mpif_audit_contact_author_email": "ken@uni-stuttgart.de",
        "mpif_audit_contact_author_id_orcid": "https://orcid.org/0000-0002-4128-6514",
        "mpif_audit_contact_author_address": "''",
        "mpif_audit_contact_author_phone": "?",

        # Section 2: Product General Information
        "mpif_product_type": "'composite'",
        "mpif_product_cas": "?",
        "mpif_product_ccdc": "''",
        "mpif_product_name_common": f"'{product_name}'",
        "mpif_product_name_systematic": "''",
        "mpif_product_formula": "''",
        "mpif_product_formula_weight": "",
        "mpif_product_state": "'solid'",
        "mpif_product_color": "'gray'",
        "mpif_product_handling_atmosphere": "'air'",
        "mpif_product_handling_note": ";\n\n;",

        # Section 3: Synthesis General Information
        "mpif_synthesis_performed_date": "",
        "mpif_synthesis_lab_temperature_C": 24,
        "mpif_synthesis_lab_humidity_percent": 35,
        "mpif_synthesis_type": "'mix'",
        "mpif_synthesis_react_temperature_C": react_temperature,
        "mpif_synthesis_react_temperature_controller": "'oven'",
        "mpif_synthesis_react_time": react_time,
        "mpif_synthesis_react_time_unit": f"'{react_time_unit}'",
        "mpif_synthesis_react_atmosphere": "'air'",
        "mpif_synthesis_react_container": f"'{react_vessel}'",
        "mpif_synthesis_react_note": ";\n\n;",
        "mpif_synthesis_product_amount": math.nan,
        "mpif_synthesis_product_amount_unit": "''",
        "mpif_synthesis_scale": "''",
        "mpif_synthesis_safety_note": ";\n\n;",

        # Section 4: Synthesis Procedure Details
        "mpif_solvent_number": len(solvent_df),
        "loop_": solvent_df,

        "mpif_vessel_number": len(vessel_df),
        "loop__vessels": vessel_df,

        "mpif_procedure_number": len(procedure_df),
        "loop__procedure": procedure_df
    }

    return {product_name: data_block}



def mofsy2mpif():
    current_file_dir = __file__.rsplit('/', 1)[0]

    # sciformation case
    procedure_mocof_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'procedure_from_sciformation.json')
    characterization_mocof_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'characterization_from_sciformation.json')

    results = convert_mofsy_to_mpif(Procedure.from_dict(load_json(procedure_mocof_file_path)), ProductCharacterization.from_dict(load_json(characterization_mocof_file_path)))
    for filename, content in results.items():
        print(f"Filename: {filename}\nContent:\n{content}\n")
        save_starfile(content, os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'generated', 'mpif_from_sciformation', filename))

    # excel MIL_2 case
    procedure_mil_file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'procedure_from_MIL_2.json')
    characterization_mil_file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'characterization_from_MIL_2.json')
    results = convert_mofsy_to_mpif(Procedure.from_dict(load_json(procedure_mil_file_path)), ProductCharacterization.from_dict(load_json(characterization_mil_file_path)))
    for filename, content in results.items():
        print(f"Filename: {filename}\nContent:\n{content}\n")
        save_starfile(content, os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'mpif_from_MIL_2', filename))



if __name__ == '__main__':
    mofsy2mpif()