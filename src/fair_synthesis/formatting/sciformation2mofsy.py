import os
from typing import List, Tuple
from jsonschema import validate
from sympy import sympify

from fair_synthesis.generated_apis.procedure_data_structure import SynthesisProcedure, SynthesisElement ,ReagentElement, Metadata, ComponentElement, \
    ProcedureSectionsClass, Reagents, XMLType, StepEntryClass, ProcedureSectionClass, \
    Hardware, Quantity, AmountUnit, Temperature , TempUnit, Time, Solvent, Gas
from fair_synthesis.generated_apis.characterization_data_structure import CharacterizationClass, Characterization, XRaySource, \
    SampleHolder, Quantity as AmountCharacterization, CharacterizationEntry, \
    Unit as UnitCharacterization, Weighing, Pxrd, SampleHolderType
from fair_synthesis.generated_apis.sciformation_eln_cleaned_data_structure import SciformationCleanedELNSchema, RxnRole, \
    Experiment, ReactionComponent, MassUnit
from .mofsy_utils import rxn_role_to_xdl_role
from .sciformation_cleaned_utils import find_reaction_components, get_inchi, mass_to_target_format, time_to_target_format, Unit as TimeUnit
from .sciformation_cleaner import clean_sciformation_eln
from .utils import load_json, save_json
from .pxrd_collector import collect_pxrd_files, filter_pxrd_files


def convert_cleaned_eln_to_mofsy(eln: SciformationCleanedELNSchema, pxrd_folder_path: str, repo_root_path: str, default_code: str = "KE") -> Tuple[SynthesisProcedure, Characterization]:
    synthesis_list: List[SynthesisElement] = []
    characterization_list: List[CharacterizationEntry] = []
    pxrd_files = collect_pxrd_files(pxrd_folder_path, repo_root_path)

    for experiment in eln.experiments:
        reaction_product = find_reaction_components(experiment, RxnRole.PRODUCT)[0]
        reaction_product_mass = format_mass(reaction_product.mass, reaction_product.mass_unit)
        reagents: List[ReagentElement] = construct_reagents(experiment.reaction_components)
        hardware: Hardware = construct_hardware(experiment)
        procedure: ProcedureSectionsClass = construct_procedure(experiment)
        # pad the experiment nr in lab journal to a length of 3 digits, adding preceding zeros
        experiment_nr = str(experiment.nr_in_lab_journal).zfill(3)
        experiment_id = (experiment.code if experiment.code else default_code) + "-" + experiment_nr

        pxrd_list: List[Pxrd] = []
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
                    other_metadata=None,
                ))

        characterization_list.append(CharacterizationEntry(characterization=CharacterizationClass(
            pxrd = pxrd_list,
            weight=[ Weighing(reaction_product_mass) ]

        ), experiment_id=experiment_id))

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
        SynthesisProcedure(
            synthesis=synthesis_list,
        ),
        Characterization(characterization_list)
    )

def construct_procedure(experiment: Experiment) -> ProcedureSectionsClass:
    vessel: str = str(experiment.vessel.value)
    prep = []
    reaction = []
    workup = []

    # First create steps with type Add for all components that are not products
    for component in experiment.reaction_components:
        amount = format_amount_mole(component.amount)
        # for solvents, use volume instead of mole as unit for amount
        if component.rxn_role == RxnRole.SOLVENT:
            amount = format_amount_volume(component.volume)

        if component.rxn_role != RxnRole.PRODUCT and amount.value > 0:
            prep.append(
                StepEntryClass(xml_type=XMLType.ADD, amount=amount, reagent=component.molecule_name, temp=None, time=None, vessel=vessel, gas=None, solvent=None, comment=None, pressure=None)
            )

    if experiment.degassing:
        gas: Gas = Gas(experiment.degassing.value)
        prep.append(
            StepEntryClass(xml_type=XMLType.EVACUATE_AND_REFILL, temp=None, time=None, amount=None, reagent=None, vessel=vessel, gas=gas, solvent=None, comment=None, pressure=None)
        )

    time: Time = format_time(experiment.duration, experiment.duration_unit)
    temp: Temperature = format_temperature(experiment.temperature)
    reaction.append(
        StepEntryClass(xml_type=XMLType.HEAT_CHILL, temp=temp, time=time, amount=None, reagent=None, vessel=vessel, gas=None, solvent=None, comment=None, pressure=None)
    )

    if experiment.rinse:
        for rinseItem in experiment.rinse:
            solvent: Solvent = Solvent(rinseItem)
            workup.append(
                StepEntryClass(xml_type=XMLType.WASH_SOLID, temp=None, time=None, amount=None, reagent=None, vessel=vessel, gas=None, solvent=solvent, comment=None, pressure=None)
            )

    if experiment.wait_after_rinse:
        wait_time: Time = format_time(str(experiment.wait_after_rinse), experiment.wait_after_rinse_unit)
        workup.append(
            StepEntryClass(xml_type=XMLType.WAIT, temp=None, time=wait_time, amount=None, reagent=None, vessel=vessel, gas=None, solvent=None, comment=None, pressure=None)
        )

    if experiment.wash_solid:
        solvent = Solvent(experiment.wash_solid)
        workup.append(
            StepEntryClass(xml_type=XMLType.WASH_SOLID, temp=None, time=None, amount=None, reagent=None, vessel=vessel, gas=None, solvent=solvent, comment=None, pressure=None)
        )

    if experiment.evaporate:
        workup.append(
            StepEntryClass(xml_type=XMLType.DRY, temp=None, time=None, amount=None, reagent=None, vessel=vessel, gas=None, solvent=None, comment=None, pressure=None)
        )

    prep = ProcedureSectionClass(prep)
    reaction = ProcedureSectionClass(reaction)
    workup = ProcedureSectionClass(workup)

    # Create the procedure
    procedure = ProcedureSectionsClass(prep=prep, reaction=reaction, workup=workup)
    return procedure


def construct_reagents(reaction_components: List[ReactionComponent]) -> List[ReagentElement]:
    reagents = []
    for component in reaction_components:

        role = rxn_role_to_xdl_role(component.rxn_role)
        inchi = get_inchi(component)
        cas = component.cas_nr

        if component.rxn_role != RxnRole.PRODUCT:
            reagent = ReagentElement(
                inchi=inchi,
                name=component.molecule_name,
                role=role,
                purity=None,
                id=component.molecule_name,
                cas=cas,
                comment=None
            )


            reagents.append(reagent)

    return reagents

def construct_hardware(experiment: Experiment):
    return Hardware(
        [ComponentElement(id=str(experiment.vessel.value), type=str(experiment.vessel.value), chemical=None, comment=None)]
    )


def format_temperature(temp: str) -> Temperature:
    temperature_string: str = temp.replace("RT", "25")
    if "->" in temperature_string: # if temperature is a range
        start_temp: float = float(sympify(temperature_string.split("->")[0]))
        end_temp: float = float(sympify(temperature_string.split("->")[1]))
        return Temperature(value=float(end_temp), unit=TempUnit.CELSIUS)
        # raise ValueError("Temperature ranges are not supported in MOFSY. Please provide a single temperature value.")
        # return str(start_temp) + " -> " + str(end_temp) + " C"
    else:
        temp: float = float(sympify(temperature_string))
        return Temperature(value=round(temp, 2), unit=TempUnit.CELSIUS)

def format_mass(mass: float|None, mass_unit: MassUnit) -> AmountCharacterization:
    if (mass is None) or (mass_unit is None):
        return AmountCharacterization(value=-1, unit=UnitCharacterization.MILLIGRAM)
    mass_in_mg = mass_to_target_format(mass, mass_unit, MassUnit.MG)
    return AmountCharacterization(value=round(mass_in_mg, 2), unit=UnitCharacterization.MILLIGRAM)

def format_amount_mole(amount: float | None) -> Quantity:
    if amount is None:
        return Quantity(value=-1, unit=AmountUnit.MICROMOLE)
    return Quantity(value=float(round(amount * 1000000,2)), unit=AmountUnit.MICROMOLE)

def format_amount_volume(amount: float | None) -> Quantity:
    if amount is None:
        return Quantity(value=-1, unit=AmountUnit.MICROLITRE)
    # original value from sciformation is in mL but we want to export to microLitre
    amount_in_ul = round(float(amount) * 1000, 3)
    return Quantity(value=amount_in_ul, unit=AmountUnit.MICROLITRE)

def format_time(time: str, time_unit: TimeUnit) -> Time:
    time_in_h = time_to_target_format(float(sympify(time)), time_unit, TimeUnit.H)
    return Time(value=round(time_in_h, 2), unit=AmountUnit.HOUR)

def format_length(length: str) -> AmountCharacterization:
    if length.endswith("mm"):
        return AmountCharacterization(value=float(length[:-2]), unit=UnitCharacterization.MILLIMETER)
    elif length.endswith("cm"):
        return AmountCharacterization(value=float(length[:-2]) * 10, unit=UnitCharacterization.CENTIMETER)
    elif length.endswith("m"):
        return AmountCharacterization(value=float(length[:-1]) * 1000, unit=UnitCharacterization.METER)
    else:
        raise ValueError(f"Unknown length unit in {length}")


def sciformation2mofsy():
    current_file_dir = __file__.rsplit('/', 1)[0]
    repo_root_path = os.path.join(current_file_dir, '../../..')
    file_path = os.path.join(repo_root_path, 'data', 'MOCOF-1', 'Sciformation_KE-MOCOF_jsonRaw.json')
    pxrd_folder = os.path.join(repo_root_path, 'data', 'MOCOF-1', 'PXRD')
    cleaned_eln = clean_sciformation_eln(load_json(file_path))
    # print("Cleaned data: " + str(cleaned_eln))
    print("The Sciformation ELN data has been cleaned.")


    # Validate data according to schema
    validate(instance=cleaned_eln, schema=load_json(os.path.join(repo_root_path, 'data_model', 'sciformation_eln_cleaned.schema.json')))

    procedure, characterization = convert_cleaned_eln_to_mofsy(SciformationCleanedELNSchema.from_dict(cleaned_eln), pxrd_folder, repo_root_path)
    result_file_path_procedure = os.path.join(repo_root_path, 'data', 'MOCOF-1', 'converted', 'procedure_from_sciformation.json')
    result_file_path_characterization = os.path.join(repo_root_path, 'data', 'MOCOF-1', 'converted', 'characterization_from_sciformation.json')
    result_dict_procedure = procedure.to_dict()
    result_dict_characterization = characterization.to_dict()
    # print("Procedure Result: " + str(result_dict_procedure))
    # print("Characterization Result: " + str(result_dict_characterization))

    # Validate results according to schemas
    validate(instance=result_dict_procedure, schema=load_json(os.path.join(repo_root_path, 'data_model', 'procedure.schema.json')))
    print("Valid procedure JSON was generated.")
    validate(instance=result_dict_characterization, schema=load_json(os.path.join(repo_root_path, 'data_model', 'characterization.schema.json')))
    print("Valid characterization JSON was generated.")

    # Additionally validate based on more strict use case specific schema
    validate(instance=result_dict_procedure, schema=load_json(os.path.join(repo_root_path, 'data_model', 'procedure_MOCOF-1.schema.json')))
    print("The procedure JSON is valid according to the MOCOF-1 specific schema.")

    save_json(result_dict_procedure, result_file_path_procedure)
    save_json(result_dict_characterization, result_file_path_characterization)



if __name__ == '__main__':
    sciformation2mofsy()