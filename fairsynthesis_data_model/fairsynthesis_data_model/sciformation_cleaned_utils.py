from typing import List


from generated.sciformation_eln_cleaned_data_structure import RxnRole, Unit, Experiment, \
    ReactionComponent, MassUnit
from utils import query_compound_from_pub_chem


cached_inchis = {}

def get_inchi(reaction_component: ReactionComponent) -> str | None:
    if reaction_component.inchi:
        return reaction_component.inchi

    if reaction_component.smiles in cached_inchis:
        inchi = cached_inchis[reaction_component.smiles]
        if inchi == "None":
            return None
        return inchi

    result = "None"

    if reaction_component.smiles:
        pub_chem_compound = query_compound_from_pub_chem(reaction_component.smiles)
        if pub_chem_compound:
            result = pub_chem_compound.inchi

    cached_inchis[reaction_component.smiles] = result
    return result

def time_to_seconds(time: float, time_unit: Unit) -> float:
    if time_unit == Unit.S:
        return time
    elif time_unit == Unit.M:
        return time * 60
    elif time_unit == Unit.H:
        return time * 3600
    elif time_unit == Unit.D:
        return time * 86400
    else:
        return time

def time_to_target_format(time: float, time_unit_source: Unit, time_unit_target: Unit) -> float:
    time_in_seconds = time_to_seconds(time, time_unit_source)
    if time_unit_target == Unit.S:
        return time_in_seconds
    elif time_unit_target == Unit.M:
        return time_in_seconds / 60
    elif time_unit_target == Unit.H:
        return time_in_seconds / 3600
    elif time_unit_target == Unit.D:
        return time_in_seconds / 86400
    else:
        raise ValueError(f"Unknown target time unit: {time_unit_target}")

def mass_to_gram(mass: float, mass_unit: MassUnit) -> float:
    if mass_unit == MassUnit.UG:
        return mass / 1000000
    elif mass_unit == MassUnit.MG:
        return mass / 1000
    elif mass_unit == MassUnit.G:
        return mass
    elif mass_unit == MassUnit.KG:
        return mass * 1000
    else:
        raise ValueError("Unknown mass unit")

def mass_to_target_format(mass: float, mass_unit_source: MassUnit, mass_unit_target: MassUnit) -> float:
    mass_in_gram = mass_to_gram(mass, mass_unit_source)
    if mass_unit_target == MassUnit.MG:
        return mass_in_gram * 1000
    elif mass_unit_target == MassUnit.G:
        return mass_in_gram
    elif mass_unit_target == MassUnit.KG:
        return mass_in_gram / 1000
    elif mass_unit_target == MassUnit.UG:
        return mass_in_gram * 1000000
    else:
        raise ValueError(f"Unknown target mass unit: {mass_unit_target}")

def find_reaction_components(experiment: Experiment, rxn_type: RxnRole) -> List[ReactionComponent]:
    results = []
    for component in experiment.reaction_components:
        if component.rxn_role.value == rxn_type.value:
            results.append(component)
    return results
