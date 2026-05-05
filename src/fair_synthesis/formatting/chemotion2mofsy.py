import os
import re
from copy import deepcopy
from typing import List, Optional, Tuple
from jsonschema import validate

from fair_synthesis.generated_apis.procedure_data_structure import (
    SynthesisProcedure, SynthesisElement, ReagentElement, Metadata,
    ComponentElement, ProcedureSectionsClass, Reagents, XMLType,
    StepEntryClass, ProcedureSectionClass, Hardware,
    AmountUnit, Temperature, TemperatureUnit, TimeClass, Amount, TimeUnit, Role,
    Solvent,
)
from fair_synthesis.generated_apis.characterization_data_structure import (
    CharacterizationClass, Characterization,
    CharacterizationEntry, Weight, WeightUnit
)
from fair_synthesis.generated_apis.chemotion_cleaned_data_structure import (
    ChemotionCleanedSchema,
)
from fair_synthesis.generated_apis.chemotion_enriched_data_structure import (
    ChemotionEnrichedSchema,
)
from fair_synthesis.formatting.chemotion_cleaner import clean_chemotion, resolve_chemotion_input_path
from fair_synthesis.formatting.chemotion_text_extractor_mocof1 import (
    process_data_use_case_specific as enrich_cleaned_chemotion_for_mocof1,
)
from fair_synthesis.formatting.utils import load_json, save_json


def _parse_temperature(temperature: Optional[dict]) -> Temperature:
    if not temperature or not temperature.get("userText"):
        return Temperature(value=0.0, unit=TemperatureUnit.CELSIUS)

    user_text: str = temperature["userText"].strip()
    value_unit: str = temperature.get("valueUnit", "°C")

    if "->" in user_text:
        value = float(user_text.split("->")[-1].strip())
    else:
        value = float(user_text)

    if "K" in value_unit and "°C" not in value_unit:
        return Temperature(value=value, unit=TemperatureUnit.KELVIN)
    return Temperature(value=value, unit=TemperatureUnit.CELSIUS)


def _parse_duration(duration_str: str) -> TimeClass:
    if not duration_str:
        return TimeClass(value=0.0, unit=TimeUnit.HOUR)

    match = re.match(r"([\d.]+)\s*(Hour|Minute|Day|Week|Second)", duration_str, re.IGNORECASE)
    if not match:
        return TimeClass(value=0.0, unit=TimeUnit.HOUR)

    value = float(match.group(1))
    unit_str = match.group(2).lower()
    unit_map = {
        "hour": TimeUnit.HOUR,
        "minute": TimeUnit.MINUTE,
        "day": TimeUnit.DAY,
        "week": TimeUnit.WEEK,
        "second": TimeUnit.SECOND,
    }
    return TimeClass(value=value, unit=unit_map.get(unit_str, TimeUnit.HOUR))


def _parse_amount(sample: dict) -> Amount:
    value = sample.get("real_amount_value") or sample.get("target_amount_value") or 0.0
    unit_str = sample.get("real_amount_unit") or sample.get("target_amount_unit") or "g"

    if unit_str == "l":
        return Amount(value=round(float(value) * 1e6, 3), unit=AmountUnit.MICROLITRE)
    elif unit_str == "g":
        return Amount(value=round(float(value) * 1000, 3), unit=AmountUnit.MILLIGRAM)
    elif unit_str == "mg":
        return Amount(value=round(float(value), 3), unit=AmountUnit.MILLIGRAM)
    else:
        return Amount(value=round(float(value), 3), unit=AmountUnit.MILLIGRAM)


def _infer_role(entry: dict) -> Role:
    sample = entry["sample"]
    unit_str = sample.get("real_amount_unit") or sample.get("target_amount_unit") or "g"
    if entry.get("reference"):
        return Role.SUBSTRATE
    return Role.REAGENT


def _build_vessel_id(vessel_size: Optional[dict]) -> str:
    if not vessel_size:
        return "vial"
    amount = vessel_size.get("amount", "")
    unit = vessel_size.get("unit", "")
    return f"{amount}{unit}_vial"


def _get_vessel_id(rxn: dict) -> str:
    return rxn.get("vessel") or _build_vessel_id(rxn.get("vessel_size"))


def _parse_solvent(name: Optional[str]) -> Optional[Solvent]:
    if not name:
        return None

    normalized_name = name.strip().lower()
    solvent_map = {
        "acetone": Solvent.ACETONE,
        "acetonitrile": Solvent.ME_CN,
        "chcl3": Solvent.CH_CL3,
        "chloroform": Solvent.CH_CL3,
        "dmf": Solvent.DMF,
        "ethanol": Solvent.ET_OH,
        "etoh": Solvent.ET_OH,
        "et3n": Solvent.ET3_N,
        "meoh": Solvent.ME_OH,
        "methanol": Solvent.ME_OH,
        "mecn": Solvent.ME_CN,
        "nacl aq": Solvent.NA_CL_AQ,
        "scco2": Solvent.SC_CO2,
        "meoh+scco2": Solvent.ME_OH_SC_CO2,
        "triethylamine": Solvent.ET3_N,
        "dioxane-phno2": Solvent.DIOXANE_NITROBENZENE,
        "dioxane/nitrobenzene": Solvent.DIOXANE_NITROBENZENE,
        "dioxane/phno2": Solvent.DIOXANE_NITROBENZENE,
        "dioxane/phno₂": Solvent.DIOXANE_NITROBENZENE,
        "phno2/dioxane": Solvent.DIOXANE_NITROBENZENE,
        "phno₂/dioxane": Solvent.DIOXANE_NITROBENZENE,
    }
    return solvent_map.get(normalized_name)


def _append_wash_step(
        workup_steps: List[StepEntryClass],
        vessel_id: str,
        solvent: Solvent) -> None:
    if any(step.xml_type == XMLType.WASH_SOLID and step.solvent == solvent
           for step in workup_steps):
        return

    workup_steps.append(StepEntryClass(
        xml_type=XMLType.WASH_SOLID,
        vessel=vessel_id,
        amount=None,
        reagent=None,
        temp=None,
        time=None,
        gas=None,
        solvent=solvent,
        comment=None,
        pressure=None,
    ))


def _enrich_cleaned_chemotion(
        cleaned: ChemotionCleanedSchema) -> ChemotionEnrichedSchema:
    enriched_dict = deepcopy(cleaned.to_dict())
    reactions = enriched_dict.get("reactions", [])
    enrich_cleaned_chemotion_for_mocof1(reactions)
    return ChemotionEnrichedSchema.from_dict(enriched_dict)


def convert_cleaned_chemotion_to_mofsy(
        cleaned: ChemotionEnrichedSchema,
) -> Tuple[SynthesisProcedure, Characterization]:
    synthesis_list: List[SynthesisElement] = []
    characterization_list: List[CharacterizationEntry] = []

    for reaction in cleaned.reactions:
        rxn = reaction.to_dict()
        experiment_id: str = reaction.short_label or reaction.id
        vessel_id = _get_vessel_id(rxn)
        temperature = _parse_temperature(rxn.get("temperature"))
        duration = _parse_duration(reaction.duration)

        reagents: List[ReagentElement] = []
        prep_steps: List[StepEntryClass] = []

        all_input_entries = (
            [(e, "starting_material") for e in rxn["starting_materials"]]
            + [(e, "solvent") for e in rxn["solvents"]]
        )

        for entry, _section in all_input_entries:
            sample = entry["sample"]
            name = sample["name"] or sample.get("short_label", "unknown")
            role = Role.SOLVENT if _section == "solvent" else _infer_role(entry)
            inchi = sample.get("inchistring")
            amount = _parse_amount(sample)

            reagents.append(ReagentElement(
                inchi=inchi,
                name=name,
                role=role,
                purity=None,
                id=name,
                cas=None,
                comment=None,
            ))
            prep_steps.append(StepEntryClass(
                xml_type=XMLType.ADD,
                amount=amount,
                reagent=name,
                vessel=vessel_id,
                temp=None,
                time=None,
                gas=None,
                solvent=None,
                comment=None,
                pressure=None,
            ))

        reaction_steps = [StepEntryClass(
            xml_type=XMLType.HEAT_CHILL,
            temp=temperature,
            time=duration,
            vessel=vessel_id,
            amount=None,
            reagent=None,
            gas=None,
            solvent=None,
            comment=None,
            pressure=None,
        )]

        workup_steps: List[StepEntryClass] = []

        for solvent_name in rxn.get("rinse") or []:
            solvent = _parse_solvent(solvent_name)
            if solvent:
                _append_wash_step(workup_steps, vessel_id, solvent)

        wash_solid = _parse_solvent(rxn.get("wash_solid"))
        if wash_solid:
            _append_wash_step(workup_steps, vessel_id, wash_solid)

        if rxn.get("evaporate"):
            workup_steps.append(StepEntryClass(
                xml_type=XMLType.DRY,
                vessel=vessel_id,
                amount=None,
                reagent=None,
                temp=None,
                time=None,
                gas=None,
                solvent=None,
                comment=None,
                pressure=None,
            ))

        procedure = ProcedureSectionsClass(
            prep=ProcedureSectionClass(prep_steps),
            reaction=ProcedureSectionClass(reaction_steps),
            workup=ProcedureSectionClass(workup_steps),
        )
        hardware = Hardware([ComponentElement(id=vessel_id, type=vessel_id, chemical=None, comment=None)])

        synthesis_list.append(SynthesisElement(
            metadata=Metadata(description=experiment_id, product=None, product_inchi=None),
            hardware=hardware,
            procedure=procedure,
            reagents=Reagents(reagents),
        ))

        product_weight = Weight(value=0.0, unit=WeightUnit.MILLIGRAM)
        if rxn["products"]:
            product_sample = rxn["products"][0]["sample"]
            product_weight = _format_product_weight(product_sample)

        characterization_list.append(CharacterizationEntry(
            characterization=CharacterizationClass(pxrd=[], weight=[product_weight]),
            experiment_id=experiment_id,
        ))

    return (
        SynthesisProcedure(synthesis=synthesis_list),
        Characterization(characterization_list),
    )


def _format_product_weight(sample: dict) -> Weight:
    value = sample.get("real_amount_value") or sample.get("target_amount_value") or 0.0
    unit_str = sample.get("real_amount_unit") or sample.get("target_amount_unit") or "g"
    if unit_str == "g":
        return Weight(value=round(float(value) * 1000, 3), unit=WeightUnit.MILLIGRAM)
    elif unit_str == "mg":
        return Weight(value=round(float(value), 3), unit=WeightUnit.MILLIGRAM)
    return Weight(value=round(float(value), 3), unit=WeightUnit.MILLIGRAM)


def chemotion2mofsy():
    current_file_dir = __file__.rsplit("/", 1)[0]
    repo_root = os.path.join(current_file_dir, "../../..")

    try:
        input_path = resolve_chemotion_input_path(repo_root)
    except FileNotFoundError:
        print("Chemotion input data not found. Skipping Chemotion conversion.")
        return
    cleaned_output_path = os.path.join(repo_root, "data", "MOCOF-1_Chemotion", "converted", "chemotion_cleaned.json")
    enriched_output_filename = "chemotion_enriched.json"
    enriched_output_path = os.path.join(repo_root, "data", "MOCOF-1_Chemotion", "converted", enriched_output_filename)
    procedure_output_path = os.path.join(repo_root, "data", "MOCOF-1_Chemotion", "converted", "procedure_from_chemotion.json")
    characterization_output_path = os.path.join(repo_root, "data", "MOCOF-1_Chemotion", "converted", "characterization_from_chemotion.json")

    os.makedirs(os.path.dirname(cleaned_output_path), exist_ok=True)

    raw_data = load_json(input_path)
    cleaned = clean_chemotion(raw_data)
    save_json(cleaned.to_dict(), cleaned_output_path)
    print("Chemotion data cleaned.")
    validate(instance=cleaned.to_dict(), schema=load_json(
        os.path.join(repo_root, "data_model", "chemotion_cleaned.schema.json")))

    enriched_cleaned = _enrich_cleaned_chemotion(
        cleaned)
    save_json(enriched_cleaned.to_dict(), enriched_output_path)
    validate(instance=enriched_cleaned.to_dict(), schema=load_json(
        os.path.join(repo_root, "data_model", "chemotion_enriched.schema.json")))
    procedure, characterization = convert_cleaned_chemotion_to_mofsy(
        enriched_cleaned)

    result_procedure = procedure.to_dict()
    result_characterization = characterization.to_dict()

    save_json(result_procedure, procedure_output_path)
    save_json(result_characterization, characterization_output_path)

    validate(instance=result_procedure, schema=load_json(
        os.path.join(repo_root, "data_model", "procedure.schema.json")))
    print("Valid procedure JSON was generated.")

    validate(instance=result_characterization, schema=load_json(
        os.path.join(repo_root, "data_model", "characterization.schema.json")))
    print("Valid characterization JSON was generated.")


if __name__ == "__main__":
    chemotion2mofsy()
