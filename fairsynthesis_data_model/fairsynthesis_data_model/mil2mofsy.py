import os
from typing import List, Tuple
from jsonschema import validate
from sympy import sympify

from .generated.procedure_data_structure import Procedure, SynthesisElement, ReagentElement, Metadata, ComponentElement, \
    ProcedureClass, Reagents, XMLType, StepEntryClass, FlatProcedureClass, \
    Hardware, Amount, Unit, Role
from .generated.characterization_data_structure import ProductCharacterization, Characterization, XRaySource, SampleHolder, Quantity as AmountCharacterization, CharacterizationEntry, Metadata as MetadataCharacterization, Unit as UnitCharacterization
from .generated.mil_json_from_excel_data_structure import Mil
from .utils import load_json, save_json
from .pxrd_collector import collect_pxrd_files, filter_pxrd_files


def convert_mil_json_from_excel_to_mofsy(mil: Mil, pxrd_folder_path: str) -> Tuple[Procedure, ProductCharacterization]:
    synthesis_list: List[SynthesisElement] = []
    characterization_list: List[CharacterizationEntry] = []
    pxrd_files = collect_pxrd_files(pxrd_folder_path)

    # hardcoded values
    solvent_volume = 4.0


    for experiment in mil.esenmofsynthesis:
        vial_no = experiment.vial_no
        metal_salt = experiment.metal_salt_name
        metal_salt_mass = experiment.metal_salt_mass
        metal_salt_mass_unit = experiment.metal_salt_mass_unit
        linker = experiment.linker_name
        linker_mass = experiment.linker_mass
        linker_mass_unit = experiment.linker_mass_unit
        solvent = experiment.solvent
        temperature = experiment.temperature
        temperature_unit = experiment.temperature_unit
        time = experiment.time
        time_unit = experiment.time_unit
        place = experiment.place
        phase_purity = experiment.phase_purity

        experiment_id = "Esen_" + vial_no

        reagents: List[ReagentElement] = [
            ReagentElement(
                cas=None,
                comment=None,
                id=metal_salt,
                inchi=None,
                name = metal_salt,
                purity=None,
                role=Role.SUBSTRATE),
            ReagentElement(
                cas=None,
                comment=None,
                id=linker,
                inchi=None,
                name = linker,
                purity=None,
                role=Role.LIGAND),
            ReagentElement(
                cas=None,
                comment=None,
                id=solvent,
                inchi=None,
                name = solvent,
                purity=None,
                role=Role.SOLVENT),
            ReagentElement(
                cas=None,
                comment=None,
                id="ethanol",
                inchi=None,
                name = "ethanol",
                purity=None,
                role=Role.SOLVENT),
            ReagentElement(
                cas=None,
                comment=None,
                id="chcl3",
                inchi=None,
                name = "chcl3",
                purity=None,
                role=Role.SOLVENT),
            ReagentElement(
                cas=None,
                comment=None,
                id="meoh",
                inchi=None,
                name = "meoh",
                purity=None,
                role=Role.SOLVENT),
            ReagentElement(
                cas=None,
                comment=None,
                id="scCO2",
                inchi=None,
                name = "scCO2",
                purity=None,
                role=Role.SOLVENT)


        ]

        hardware: Hardware = Hardware([
            ComponentElement(chemical=None, comment=None, id=vial_no, type="vial")
        ])

        procedure: ProcedureClass = ProcedureClass(
            step=None,
            prep=FlatProcedureClass(step=[
                StepEntryClass(
                    XMLType.ADD,
                    amount=format_mass(metal_salt_mass, metal_salt_mass_unit),
                    reagent=metal_salt,
                    stir=None,
                    temp=None,
                    time=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure=None
                ),
                StepEntryClass(
                    XMLType.ADD,
                    amount=format_mass(linker_mass, linker_mass_unit),
                    reagent=linker,
                    stir=None,
                    temp=None,
                    time=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure=None
                ),
                StepEntryClass(
                    XMLType.ADD,
                    amount=format_amount_volume(float(sympify(solvent_volume))),
                    reagent=solvent,
                    stir=None,
                    temp=None,
                    time=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure=None
                )
            ]),
            reaction=FlatProcedureClass(step=[
                StepEntryClass(
                    XMLType.HEAT_CHILL,
                    temp=format_temperature(str(temperature)),
                    time=format_time(time, time_unit),
                    amount=None,
                    reagent=None,
                    stir=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure=None
                )
            ]),
            workup=construct_workup(vial_no))


        product_characterizations: List[Characterization] = [Characterization(
            weight=None,
            relative_file_path=None,
            sample_holder=None,
            x_ray_source=None,
            purity=phase_purity
        )]

        experiment_pxrd_files = filter_pxrd_files(experiment_id, pxrd_files)
        if experiment_pxrd_files:
            for pxrd_file in experiment_pxrd_files:
                x_ray_source = XRaySource[pxrd_file.xray_source.replace(" ", "_").replace("-", "_").upper()]
                diameter = format_length(pxrd_file.sample_holder_diameter)
                sample_holder: SampleHolder = SampleHolder(
                    diameter=diameter,
                    type=pxrd_file.sample_holder_shape
                )
                product_characterizations.append(Characterization(
                    weight=None,
                    relative_file_path=pxrd_file.path,
                    sample_holder=sample_holder,
                    x_ray_source=x_ray_source,
                    purity=None
                ))

        characterization_list.append(CharacterizationEntry(product_characterizations, MetadataCharacterization(description=experiment_id)))

        synthesis = SynthesisElement(
            metadata= Metadata(
                description= experiment_id,
                product= None,
                product_inchi= None
            ),
            hardware= hardware,
            procedure = procedure,
            reagents = Reagents(reagents),
        )
        synthesis_list.append(synthesis)


    return (
        Procedure(
            synthesis=synthesis_list,
        ),
        ProductCharacterization(characterization_list)
    )


def construct_workup(vial_no):
    workup = FlatProcedureClass(step=[
        StepEntryClass(
            XMLType.WASH_SOLID,
            temp=None,
            time=None,
            amount=None,
            reagent=None,
            stir=None,
            vessel=vial_no,
            gas=None,
            solvent="ethanol",
            comment=None,
            pressure=None
        ),
        StepEntryClass(
            XMLType.WASH_SOLID,
            temp=None,
            time=None,
            amount=None,
            reagent=None,
            stir=None,
            vessel=vial_no,
            gas=None,
            solvent="DMF",
            comment=None,
            pressure=None
        ),
        StepEntryClass(
            XMLType.WASH_SOLID,
            temp=None,
            time=None,
            amount=None,
            reagent=None,
            stir=None,
            vessel=vial_no,
            gas=None,
            solvent="chcl3",
            comment=None,
            pressure=None
        ),
        StepEntryClass(
            XMLType.WASH_SOLID,
            temp=None,
            time=None,
            amount=None,
            reagent=None,
            stir=None,
            vessel=vial_no,
            gas=None,
            solvent="meoh",
            comment=None,
            pressure=None
        ),
        StepEntryClass(
            XMLType.WAIT,
            temp=None,
            time=format_time(24, "h"),
            amount=None,
            reagent=None,
            stir=None,
            vessel=vial_no,
            gas=None,
            solvent=None,
            comment=None,
            pressure=None
        ),
        StepEntryClass(
            XMLType.WASH_SOLID,
            temp=None,
            time=None,
            amount=None,
            reagent=None,
            stir=None,
            vessel=vial_no,
            gas=None,
            solvent="scCO2",
            comment=None,
            pressure=None
        )
    ])
    return workup


def format_temperature(temp: str) -> Amount:
    temperature_string: str = temp.replace("RT", "25")
    temp: float = float(sympify(temperature_string))
    return Amount(value=round(temp, 2), unit=Unit.CELSIUS)

def format_mass(mass: float|None, mass_unit: str) -> Amount:
    if (mass is None) or (mass_unit is None):
        return Amount(value=None, unit=None)
    if not mass_unit == "mg":
        raise ValueError(f"Only mg is supported as mass unit in converter, but got {mass_unit}")
    return Amount(value=round(mass, 2), unit=Unit.MILLIGRAM)


def format_amount_volume(amount: float | None) -> Amount:
    if amount is None:
        return Amount(value=None, unit=None)
    # original value is in Ml and we keep it that way
    return Amount(value=amount, unit=Unit.MILLILITRE)

def format_time(time: float | None, time_unit: str) -> Amount:
    if time is None or time_unit is None:
        return Amount(value=None, unit=None)
    if time_unit in ["h", "hour", "hours"]:
        return Amount(value=round(time, 2), unit=Unit.HOUR)
    elif time_unit in ["min", "mins", "minute", "minutes"]:
        return Amount(value=round(time, 2), unit=Unit.MINUTE)
    elif time_unit in ["s", "sec", "secs", "second", "seconds"]:
        return Amount(value=round(time, 2), unit=Unit.SECOND)
    elif time_unit in ["d", "day", "days"]:
        return Amount(value=round(time, 2), unit=Unit.DAY)
    else:
        raise ValueError(f"Unknown time unit in {time_unit}")

def format_length(length: str) -> AmountCharacterization:
    if length.endswith("mm"):
        return AmountCharacterization(value=float(length[:-2]), unit=UnitCharacterization.MILLIMETER)
    elif length.endswith("cm"):
        return AmountCharacterization(value=float(length[:-2]) * 10, unit=UnitCharacterization.CENTIMETER)
    elif length.endswith("m"):
        return AmountCharacterization(value=float(length[:-1]) * 1000, unit=UnitCharacterization.METER)
    else:
        raise ValueError(f"Unknown length unit in {length}")


if __name__ == '__main__':
    current_file_dir = __file__.rsplit('/', 1)[0]
    file_path = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'generated', 'MIL.json')
    pxrd_folder = os.path.join(current_file_dir, '../..', 'data', 'MIL-88B_101', 'pxrd')
    pxrd_folder_relative = rel_path = os.path.relpath(pxrd_folder, os.getcwd())
    mil = load_json(file_path)

    # Validate data according to schema
    validate(instance=mil, schema=load_json(os.path.join(current_file_dir, 'schemas', 'MIL.schema.json')))

    mofsy, characterization = convert_mil_json_from_excel_to_mofsy(Mil.from_dict(mil), pxrd_folder_relative)
    result_file_path_mofsy = os.path.join(current_file_dir , '../..', 'data', 'MIL-88B_101', 'generated', 'procedure_from_MIL.json')
    result_file_path_characterization = os.path.join(current_file_dir , '../..', 'data', 'MIL-88B_101', 'generated', 'characterization_from_MIL.json')
    result_dict_mofsy = mofsy.to_dict()
    result_dict_characterization = characterization.to_dict()
    print("Procedure Result: " + str(result_dict_mofsy))
    print("Characterization Result: " + str(result_dict_characterization))
    save_json(result_dict_mofsy, result_file_path_mofsy)
    save_json(result_dict_characterization, result_file_path_characterization)



