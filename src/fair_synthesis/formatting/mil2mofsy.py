import os
from typing import List, Tuple
from jsonschema import validate
from sympy import sympify

from fair_synthesis.generated_apis.procedure_data_structure import SynthesisProcedure, SynthesisElement, ReagentElement, Metadata, ComponentElement, \
    ProcedureSectionClass, ProcedureSectionsClass, Reagents, XMLType, StepEntryClass, \
    Hardware, Quantity, AmountUnit, Role, Temperature, TempUnit, Pressure, PressureUnit, Time, Solvent
from fair_synthesis.generated_apis.characterization_data_structure import CharacterizationClass, Characterization, XRaySource, \
    SampleHolder, Quantity as AmountCharacterization, CharacterizationEntry, \
    Unit as UnitCharacterization, Pxrd, SampleHolderType
from fair_synthesis.generated_apis.mil_json_from_excel_data_structure import Mil
from .utils import load_json, save_json
from .pxrd_collector import collect_pxrd_files, filter_pxrd_files


def convert_mil_2_json_from_excel_to_mofsy(mil: Mil, pxrd_folder_path: str, repo_root_path: str) -> Tuple[SynthesisProcedure, Characterization]:
    synthesis_list: List[SynthesisElement] = []
    characterization_list: List[CharacterizationEntry] = []
    pxrd_files = collect_pxrd_files(pxrd_folder_path, repo_root_path)

    for experiment in mil.esenmof:
        vial_no = experiment.the_0__vial_no
        date = experiment.the_0__date
        metal_salt = experiment.the_1__metal_salt_name
        metal_salt_mass = experiment.the_1__metal_salt_mass
        metal_salt_mass_unit = experiment.the_1__metal_salt_mass_unit
        linker = experiment.the_2__linker_name
        linker_mass = experiment.the_2__linker_mass
        linker_mass_unit = experiment.the_2__linker_mass_unit
        solvent = experiment.the_3__solvent
        solvent_unit = experiment.the_3__solvent_unit
        solvent_amount = experiment.the_3__solvent_amount
        modulator = experiment.the_4__modulator
        modulator_amount = experiment.the_4__modulator_amount
        modulator_unit = experiment.the_4__modulator_unit
        sonicator_time = experiment.the_5__sonicator_time
        sonicator_time_unit = experiment.the_5__sonicator_time_unit
        temperature = experiment.the_6__temperature
        temperature_unit = experiment.the_6__temperature_unit
        reaction_time = experiment.the_6__reaction_time
        reaction_time_unit = experiment.the_6__reaction_time_unit
        reaction_vessel = experiment.the_6__reaction_vessel
        reaction_place = experiment.the_6__place
        washing_solids = experiment.the_7__washing_solids
        activation_temperature = experiment.the_8__activation_temperature
        activation_temperature_unit = experiment.the_8__activation_temperature_unit
        drying_solids = experiment.the_8__drying_solids
        drying_solids_time = experiment.the_8__drying_solids_time
        drying_time_unit = experiment.the_8__drying_time_unit
        mof = experiment.the_9__mof
        phase_purity = experiment.the_9__phase_purity

        experiment_id = vial_no

        # Build up a list of all reagents
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
                id=washing_solids,
                inchi=None,
                name = washing_solids,
                purity=None,
                role=Role.SOLVENT)
        ]

        # The hardware is simply the one vial
        hardware: Hardware = Hardware([
            ComponentElement(chemical=None, comment=None, id=vial_no, type=reaction_vessel)
        ])

        prep_steps = [
                StepEntryClass(
                    xml_type=XMLType.ADD,
                    amount=format_mass(metal_salt_mass, metal_salt_mass_unit),
                    reagent=metal_salt,
                    temp=None,
                    time=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure = None
                ),
                StepEntryClass(
                    xml_type=XMLType.ADD,
                    amount=format_mass(linker_mass, linker_mass_unit),
                    reagent=linker,
                    temp=None,
                    time=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure = None
                ),
                StepEntryClass(
                    xml_type=XMLType.ADD,
                    amount=format_amount_volume(solvent_amount, solvent_unit),
                    reagent=solvent,
                    temp=None,
                    time=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure = None
                )
            ]

        # if modulator is given, add it to the reagents and the prep steps
        if modulator:
            reagents.append(ReagentElement(
                cas=None,
                comment=None,
                id=modulator,
                inchi=None,
                name = modulator,
                purity=None,
                role=Role.REAGENT)
            )
            prep_steps.append(
                StepEntryClass(
                    xml_type=XMLType.ADD,
                    amount=format_amount_volume(float(modulator_amount), modulator_unit),
                    reagent=modulator,
                    temp=None,
                    time=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure = None
                )
            )

        reaction_steps = [

                StepEntryClass(
                    xml_type=XMLType.SONICATE,
                    temp=None,
                    time=format_time(sonicator_time, sonicator_time_unit),
                    amount=None,
                    reagent=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment=None,
                    pressure = None
                ),
                StepEntryClass(
                    xml_type=XMLType.HEAT_CHILL,
                    temp=format_temperature(str(temperature), temperature_unit),
                    time=format_time(reaction_time, reaction_time_unit),
                    amount=None,
                    reagent=None,
                    vessel=vial_no,
                    gas=None,
                    solvent=None,
                    comment="In: " + reaction_place,
                    pressure = None
                )
            ]

        workup_steps = [
            StepEntryClass(
                xml_type=XMLType.WASH_SOLID,
                amount=None,
                reagent=None,
                temp=None,
                time=None,
                vessel=vial_no,
                gas=None,
                solvent=Solvent(washing_solids),
                comment=None,
                pressure = None
            ),
            StepEntryClass(
                xml_type=XMLType.DRY,
                temp=format_temperature(str(activation_temperature), activation_temperature_unit),
                time=format_time(drying_solids_time, drying_time_unit),
                amount=None,
                reagent=None,
                vessel=vial_no,
                gas=None,
                solvent=None,
                comment=None,
                pressure = Pressure(value=0, unit=PressureUnit.PASCAL) # hardcode, because it always is vacuum in every experiment
            ),
        ]

        # Build up the full procedure
        procedure: ProcedureSectionsClass = ProcedureSectionsClass(
            prep=ProcedureSectionClass(step=prep_steps),
            reaction=ProcedureSectionClass(step=reaction_steps),
            workup=ProcedureSectionClass(step=workup_steps))

        # Collect all PXRD files for this experiment
        pxrd_list = []
        experiment_pxrd_files = filter_pxrd_files(experiment_id, pxrd_files)
        if experiment_pxrd_files:
            for pxrd_file in experiment_pxrd_files:
                x_ray_source = XRaySource[pxrd_file.xray_source.replace(" ", "_").replace("-", "_").upper()]
                diameter = format_length(pxrd_file.sample_holder_diameter)
                sample_holder: SampleHolder = SampleHolder(
                    diameter=diameter,
                    type=SampleHolderType(pxrd_file.sample_holder_shape)
                )
                pxrd_list.append(Pxrd(
                    relative_file_path=pxrd_file.path,
                    sample_holder=sample_holder,
                    x_ray_source=x_ray_source,
                    other_metadata=pxrd_file.other_metadata
                ))

        characterization_list.append(CharacterizationEntry(characterization=CharacterizationClass(
            pxrd=pxrd_list,
            weight=[]
        ), experiment_id=experiment_id))

        synthesis = SynthesisElement(
            metadata= Metadata(
                description= experiment_id,
                product= mof,
                product_inchi= None
            ),
            hardware= hardware,
            procedure = procedure,
            reagents = Reagents(reagents),
        )
        synthesis_list.append(synthesis)


    return (
        SynthesisProcedure(
            synthesis=synthesis_list,
        ),
        Characterization(characterization_list)
    )




def format_temperature(temp: str, temp_unit: str) -> Temperature:
    if not temp_unit in ["C", "°C", "deg C"]:
        raise ValueError(f"Only Celsius is supported as temperature unit in converter, but got {temp_unit}")
    temperature_string: str = temp.replace("RT", "25")
    temp: float = float(sympify(temperature_string))
    return Temperature(value=round(temp, 2), unit=TempUnit.CELSIUS)

def format_mass(mass: float|None, mass_unit: str) -> Quantity:
    if (mass is None) or (mass_unit is None):
        return Quantity(value=-1, unit=None)
    if mass_unit == "mg":
        return Quantity(value=round(mass, 2), unit=AmountUnit.MILLIGRAM)
    elif mass_unit == "mmol":
        return Quantity(value=round(mass, 2), unit=AmountUnit.MILLIMOLE)
    else:
        raise ValueError(f"Only mg is supported as mass unit in converter, but got {mass_unit}")


def format_amount_volume(amount: float | None, volume_unit: str) -> Quantity:
    if amount is None:
        return Quantity(value=-1, unit=None)
    if volume_unit.lower() == "ml":
        return Quantity(value=amount, unit=AmountUnit.MILLILITRE)
    elif volume_unit.lower() in ["l", "lt", "liter", "litre"]:
        return Quantity(value=round(amount, 2), unit=AmountUnit.LITRE)
    elif volume_unit.lower() in ["µl", "ul", "microliter", "microlitre", "μl"]:
        return Quantity(value=round(amount, 2), unit=AmountUnit.MICROLITRE)

    raise ValueError(f"{volume_unit} is not supported as volume unit in converter")

def format_time(time: float | None, time_unit: str) -> Time:
    if time is None or time_unit is None:
        return Time(value=-1, unit=None)
    if time_unit in ["h", "hour", "hours"]:
        return Time(value=round(time, 2), unit=AmountUnit.HOUR)
    elif time_unit in ["min", "mins", "minute", "minutes"]:
        return Time(value=round(time, 2), unit=AmountUnit.MINUTE)
    elif time_unit in ["s", "sec", "secs", "second", "seconds"]:
        return Time(value=round(time, 2), unit=AmountUnit.SECOND)
    elif time_unit in ["d", "day", "days"]:
        return Time(value=round(time, 2), unit=AmountUnit.DAY)
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


def mil2mofsy():
    current_file_dir = __file__.rsplit('/', 1)[0]
    repo_root_path = os.path.join(current_file_dir, '../../..')
    file_path = os.path.join(repo_root_path, 'data', 'Fe–terephthalate', 'converted', 'MIL.json')
    pxrd_folder = os.path.join(repo_root_path, 'data', 'Fe–terephthalate', 'PXRD')
    mil = load_json(file_path)

    # Validate data according to schema
    validate(instance=mil, schema=load_json(os.path.join(repo_root_path, 'data_model', 'MIL.schema.json')))

    procedure, characterization = convert_mil_2_json_from_excel_to_mofsy(Mil.from_dict(mil), pxrd_folder, repo_root_path)
    result_file_path_procedure = os.path.join(repo_root_path, 'data', 'Fe–terephthalate', 'converted', 'procedure_from_MIL.json')
    result_file_path_characterization = os.path.join(repo_root_path, 'data', 'Fe–terephthalate', 'converted', 'characterization_from_MIL.json')
    result_dict_procedure = procedure.to_dict()
    result_dict_characterization = characterization.to_dict()
    # print("Procedure Result: " + str(result_dict_mofsy))
    # print("Characterization Result: " + str(result_dict_characterization))

    # Validate results according to schemas
    validate(instance=result_dict_procedure, schema=load_json(os.path.join(repo_root_path, 'data_model', 'procedure.schema.json')))
    print("Valid procedure JSON was generated.")
    validate(instance=result_dict_characterization, schema=load_json(os.path.join(repo_root_path, 'data_model', 'characterization.schema.json')))
    print("Valid characterization JSON was generated.")


    save_json(result_dict_procedure, result_file_path_procedure)
    save_json(result_dict_characterization, result_file_path_characterization)


if __name__ == '__main__':
    mil2mofsy()

