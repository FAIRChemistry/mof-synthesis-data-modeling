import os
from typing import List
from jsonschema import validate
from sympy import sympify

from .generated.mofsy_data_structure import Mofsy, SynthesisElement ,ReagentElement, Metadata, ComponentElement, \
    Procedure, Reagents, XMLType, Characterization, XRaySource, SampleHolder, StepEntryClass, FlatProcedureClass, \
    Hardware, Amount, Unit
from .generated.sciformation_eln_cleaned_data_structure import SciformationCleanedELNSchema, RxnRole, \
    Experiment, ReactionComponent, MassUnit
from .mofsy_utils import rxn_role_to_xdl_role
from .sciformation_cleaned_utils import find_reaction_components, get_inchi, mass_to_target_format, time_to_target_format, Unit as TimeUnit
from .sciformation_cleaner import clean_sciformation_eln
from .utils import load_json, save_json
from .pxrd_collector import collect_pxrd_files, filter_pxrd_files


def convert_cleaned_eln_to_mofsy(eln: SciformationCleanedELNSchema, default_code: str = "KE", split_procedure_in_sections: bool = True) -> Mofsy:
    synthesis_list: List[SynthesisElement] = []
    pxrd_files = collect_pxrd_files(os.path.join('../..', 'data', 'PXRD'))

    for experiment in eln.experiments:
        reaction_product = find_reaction_components(experiment, RxnRole.PRODUCT)[0]
        reaction_product_mass = format_mass(reaction_product.mass, reaction_product.mass_unit)
        reaction_product_inchi = get_inchi(reaction_product)
        reagents: List[ReagentElement] = construct_reagents(experiment.reaction_components)
        hardware: Hardware = construct_hardware(experiment)
        procedure: Procedure = construct_procedure(experiment, not split_procedure_in_sections)
        # pad the experiment nr in lab journal to a length of 3 digits, adding preceding zeros
        experiment_nr = str(experiment.nr_in_lab_journal).zfill(3)
        experiment_id = (experiment.code if experiment.code else default_code) + "-" + experiment_nr

        product_characterizations: List[Characterization] = [Characterization(
            weight=reaction_product_mass,
            relative_file_path=None,
            sample_holder=None,
            x_ray_source=None
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
                    x_ray_source=x_ray_source
                ))

        synthesis = SynthesisElement(
            metadata= Metadata(
                description= experiment_id,
                product= None,
                product_inchi= None
            ),
            hardware= hardware,
            procedure = procedure,
            reagents = Reagents(reagents),
            product_characterization = product_characterizations
        )
        synthesis_list.append(synthesis)

    return Mofsy(
        synthesis=synthesis_list,
    )

def construct_procedure(experiment: Experiment, merge_steps: bool = False) -> Procedure:
    vessel: str = str(experiment.vessel.value)
    steps = None
    prep = []
    reaction = []
    workup = []

    # First create steps with type Add for all components that are not products
    for component in experiment.reaction_components:
        amount = format_amount(component.amount)
        if component.rxn_role != RxnRole.PRODUCT:
            prep.append(
                StepEntryClass(XMLType.ADD, amount=amount, reagent=component.molecule_name, stir=None, temp=None, time=None, vessel=vessel, gas=None, solvent=None, comment=None)
            )

    if experiment.degassing:
        prep.append(
            StepEntryClass(XMLType.EVACUATE_AND_REFILL, temp=None, time=None, amount=None, reagent=None, stir=None, vessel=vessel, gas=experiment.degassing.value, solvent=None, comment=None)
        )

    time: Amount = format_time(experiment.duration, experiment.duration_unit)
    temp: Amount = format_temperature(experiment.temperature)
    reaction.append(
        StepEntryClass(XMLType.HEAT_CHILL, temp=temp, time=time, amount=None, reagent=None, stir=None, vessel=vessel, gas=None, solvent=None, comment=None)
    )

    if experiment.rinse:
        for rinseItem in experiment.rinse:
            workup.append(
                StepEntryClass(XMLType.WASH_SOLID, temp=None, time=None, amount=None, reagent=None, stir=None, vessel=vessel, gas=None, solvent=rinseItem, comment=None)
            )

    if experiment.wait_after_rinse:
        wait_time: Amount = format_time(str(experiment.wait_after_rinse), experiment.wait_after_rinse_unit)
        workup.append(
            StepEntryClass(XMLType.WAIT, temp=None, time=wait_time, amount=None, reagent=None, stir=None, vessel=vessel, gas=None, solvent=None, comment=None)
        )

    if experiment.wash_solid:
        workup.append(
            StepEntryClass(XMLType.WASH_SOLID, temp=None, time=None, amount=None, reagent=None, stir=None, vessel=vessel, gas=None, solvent=experiment.wash_solid, comment=None)
        )

    if experiment.evaporate:
        workup.append(
            StepEntryClass(XMLType.EVAPORATE, temp=None, time=None, amount=None, reagent=None, stir=None, vessel=vessel, gas=None, solvent=None, comment=None)
        )

    if merge_steps:
        # Merge the steps into one list
        steps = prep + reaction + workup
        prep = None
        reaction = None
        workup = None
    else:
        # Create a procedure with separate sections for prep, reaction, and workup
        steps = None
    prep = FlatProcedureClass(prep) if len(prep) > 0 else None
    reaction = FlatProcedureClass(reaction) if len(reaction) > 0 else None
    workup = FlatProcedureClass(workup) if len(workup) > 0 else None

    # Create the procedure
    procedure = Procedure(step=steps, prep=prep, reaction=reaction, workup=workup)
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
                id = component.molecule_name,
                cas=cas,
                comment=None
            )


            reagents.append(reagent)

    return reagents

def construct_hardware(experiment: Experiment):
    return Hardware(
        [ComponentElement(id=str(experiment.vessel.value), type=None, chemical=None, comment=None)]
    )


def format_temperature(temp: str) -> Amount:
    temperature_string: str = temp.replace("RT", "25")
    if "->" in temperature_string: # if temperature is a range
        start_temp: float = float(sympify(temperature_string.split("->")[0]))
        end_temp: float = float(sympify(temperature_string.split("->")[1]))
        return Amount(value=float(end_temp), unit=Unit.CELSIUS)
        # raise ValueError("Temperature ranges are not supported in MOFSY. Please provide a single temperature value.")
        # return str(start_temp) + " -> " + str(end_temp) + " C"
    else:
        temp: float = float(sympify(temperature_string))
        return Amount(value=round(temp, 2), unit=Unit.CELSIUS)

def format_mass(mass: float|None, mass_unit: MassUnit) -> Amount:
    if (mass is None) or (mass_unit is None):
        return Amount(value=None, unit=None)
    mass_in_mg = mass_to_target_format(mass, mass_unit, MassUnit.MG)
    return Amount(value=round(mass_in_mg, 2), unit=Unit.MILLIGRAM)

def format_amount(amount: float|None) -> Amount:
    if amount is None:
        return Amount(value=None, unit=None)
    return Amount(value=float(round(amount * 1000000,2)), unit=Unit.MICROMOLE)

def format_time(time: str, time_unit: TimeUnit) -> Amount:
    time_in_h = time_to_target_format(float(sympify(time)), time_unit, TimeUnit.H)
    return Amount(value=round(time_in_h, 2), unit=Unit.HOUR)

def format_length(length: str) -> Amount:
    if length.endswith("mm"):
        return Amount(value=float(length[:-2]), unit=Unit.MILLIMETER)
    elif length.endswith("cm"):
        return Amount(value=float(length[:-2]) * 10, unit=Unit.CENTIMETER)
    elif length.endswith("m"):
        return Amount(value=float(length[:-1]) * 1000, unit=Unit.METER)
    else:
        raise ValueError(f"Unknown length unit in {length}")


if __name__ == '__main__':
    current_file_dir = __file__.rsplit('/', 1)[0]
    file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'Sciformation_KE-MOCOF_jsonRaw.json')
    cleaned_eln = clean_sciformation_eln(load_json(file_path))
    print("Cleaned data: " + str(cleaned_eln))

    # Validate data according to schema
    validate(instance=cleaned_eln, schema=load_json(os.path.join(current_file_dir, 'schemas', 'sciformation_eln_cleaned.schema.json')))

    mofsy = convert_cleaned_eln_to_mofsy(SciformationCleanedELNSchema.from_dict(cleaned_eln))
    result_file_path = os.path.join(current_file_dir , '../..', 'data', 'MOCOF-1', 'generated', 'mofsy_from_sciformation.json')
    result_dict = mofsy.to_dict()
    print("MOFSY Result: " + str(result_dict))
    save_json(result_dict, result_file_path)



