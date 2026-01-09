import json
from typing import List, Dict

from fair_synthesis.generated_apis.procedure_data_structure import SynthesisProcedure, ReagentElement, SynthesisElement, Role, Quantity
from fair_synthesis.generated_apis.characterization_data_structure import CharacterizationEntry, Characterization
from fair_synthesis.generated_apis.mocof_1_params import Mocof1Param
from fair_synthesis.formatting.pxrd_collector import PXRDFile


class Product:
    def __init__(
            self,
            name: str,
            mass: str | None,
            pxrd_files: List[PXRDFile]):
        self.name = name
        self.mass = mass
        self.pxrd_files = pxrd_files


def load_procedure(file_path: str) -> SynthesisProcedure:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return SynthesisProcedure.from_dict(data)


def load_characterization(file_path: str) -> Characterization:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return Characterization.from_dict(data)


def load_mocof_1_params(file_path: str) -> Dict[str, Mocof1Param]:
    with open(file_path, 'r') as f:
        data: dict[str, dict] = json.load(f)
    # Convert each entry in the dictionary to Mocof1Param
    return {k: Mocof1Param.from_dict(v) for k, v in data.items()}


def get_synthesis_list(
        procedure: SynthesisProcedure) -> list[SynthesisElement]:
    return procedure.synthesis


def get_synthesis_by_experiment_id(
        procedure: SynthesisProcedure,
        experiment_id: str) -> SynthesisElement | None:
    for synthesis in procedure.synthesis:
        if synthesis.metadata.description == experiment_id:
            return synthesis
    return None


def get_characterization_by_experiment_id(
        characterization: Characterization,
        experiment_id: str) -> CharacterizationEntry | None:
    for entry in characterization.product_characterization:
        if entry.experiment_id == experiment_id:
            return entry
    return None


def get_params_by_experiment_id(
        params: Dict[str, Mocof1Param], experiment_id: str) -> Mocof1Param | None:
    return params.get(experiment_id, None)


def find_reagent_by_name(
        synthesis: SynthesisElement,
        reagent_name: str) -> ReagentElement | None:
    for reagent in synthesis.reagents.reagent:
        if reagent.name == reagent_name:
            return reagent
    return None


def find_reagents_by_role(
        synthesis: SynthesisElement,
        role: Role) -> list[ReagentElement]:
    results = []
    for reagent in synthesis.reagents.reagent:
        if reagent.role.value == role.value:
            results.append(reagent)
    return results


def find_product(
        synthesis: SynthesisElement,
        product_characterization: CharacterizationEntry) -> Product | None:
    product_name = synthesis.metadata.product if synthesis.metadata.product else "unknown"
    product_mass = find_product_mass(product_characterization)
    pxrd_files = find_corresponding_pxrd_files(product_characterization)
    return Product(product_name, product_mass, pxrd_files)


def find_corresponding_pxrd_files(
        characterization: CharacterizationEntry) -> List[PXRDFile]:
    result = []
    for ch in characterization.characterization.pxrd:
        if ch.relative_file_path and ch.x_ray_source and ch.sample_holder and characterization.experiment_id:
            result.append(PXRDFile(
                ch.relative_file_path
            ))
    return result


def find_product_mass(
        characterization: CharacterizationEntry) -> Quantity | None:
    # Filter characterizations by whether they have the weight attribute
    mass_characterizations = [
        c for c in characterization.characterization.weight if c.weight]
    if mass_characterizations:
        # Return the weight of the first characterization that has it
        return mass_characterizations[0].weight
    return None


def print_synthesis_data(
        synthesis: SynthesisElement,
        characterization: CharacterizationEntry):
    print(f"Synthesis ID: {synthesis.metadata.description}")
    print_reagents(synthesis)
    print_procedure(synthesis)
    product = find_product(synthesis, characterization)
    if product:
        print_product(product)


def print_reagents(synthesis: SynthesisElement):
    print("Reagents:")
    for reagent in synthesis.reagents.reagent:
        print(f" - {reagent.name} (Role: {reagent.role.value})")


def print_procedure(synthesis: SynthesisElement):
    print("Procedure:")
    if synthesis.procedure.prep:
        print("Prep Steps:")
        for step in synthesis.procedure.prep.step:
            print(
                f" -(Type: {
                    step.xml_type}, Amount: {
                    step.amount}, Reagent: {
                    step.reagent}, Temp: {
                    step.temp}, Time: {
                        step.time}, Vessel: {
                            step.vessel}, Solvent: {
                                step.solvent}, Gas: {
                                    step.gas}, Pressure: {
                                        step.pressure}, Comment: {
                                            step.comment})")
    if synthesis.procedure.reaction:
        print("Reaction Steps:")
        for step in synthesis.procedure.reaction.step:
            print(
                f" -(Type: {
                    step.xml_type}, Amount: {
                    step.amount}, Reagent: {
                    step.reagent}, Temp: {
                    step.temp}, Time: {
                        step.time}, Vessel: {
                            step.vessel}, Solvent: {
                                step.solvent}, Gas: {
                                    step.gas}, Pressure: {
                                        step.pressure}, Comment: {
                                            step.comment})")
    if synthesis.procedure.workup:
        print("Workup Steps:")
        for step in synthesis.procedure.workup.step:
            print(
                f" -(Type: {
                    step.xml_type}, Amount: {
                    step.amount}, Reagent: {
                    step.reagent}, Temp: {
                    step.temp}, Time: {
                        step.time}, Vessel: {
                            step.vessel}, Solvent: {
                                step.solvent}, Gas: {
                                    step.gas}, Pressure: {
                                        step.pressure}, Comment: {
                                            step.comment})")


def print_product(product: Product):
    if product:
        print(f"Product Name: {product.name}")
        print(f"Product Mass: {product.mass}")
        print("PXRD Files:")
        for pxrd_file in product.pxrd_files:
            print(f" - {pxrd_file.path}")
            print(f"   Experiment ID: {pxrd_file.experiment_id}")
            print(f"   X-ray Source: {pxrd_file.xray_source}")
            print(f"   Sample Holder Shape: {pxrd_file.sample_holder_shape}")
            print(
                f"   Sample Holder Diameter: {
                    pxrd_file.sample_holder_diameter}")
