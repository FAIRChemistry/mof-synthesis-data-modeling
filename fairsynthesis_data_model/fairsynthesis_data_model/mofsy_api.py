import json
from typing import List

from generated.procedure_data_structure import Procedure, ReagentElement, SynthesisElement, Role, Quantity
from generated.characterization_data_structure import CharacterizationEntry, ProductCharacterization
from pxrd_collector import PXRDFile

class Product:
    def __init__(self, name: str, mass: str|None, pxrd_files: List[PXRDFile]):
        self.name = name
        self.mass = mass
        self.pxrd_files = pxrd_files


def load_mofsy(file_path: str) -> Procedure:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return Procedure.from_dict(data)

def load_characterization(file_path: str) -> ProductCharacterization:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return ProductCharacterization.from_dict(data)


def get_synthesis_list(procedure: Procedure) -> list[SynthesisElement]:
    return procedure.synthesis


def get_synthesis_by_experiment_id(procedure: Procedure, experiment_id: str) -> SynthesisElement | None:
    for synthesis in procedure.synthesis:
        if synthesis.metadata.description == experiment_id:
            return synthesis
    return None

def get_characterization_by_experiment_id(characterization: ProductCharacterization, experiment_id: str) -> CharacterizationEntry | None:
    for entry in characterization.product_characterization:
        if entry.metadata.description == experiment_id:
            return entry
    return None

def find_reagent_by_name(synthesis: SynthesisElement, reagent_name: str) -> ReagentElement | None:
    for reagent in synthesis.reagents.reagent:
        if reagent.name == reagent_name:
            return reagent
    return None


def find_reagents_by_role(synthesis: SynthesisElement, role: Role) -> list[ReagentElement]:
    results = []
    for reagent in synthesis.reagents.reagent:
        if reagent.role.value == role.value:
            results.append(reagent)
    return results


def find_product(synthesis: SynthesisElement, product_characterization: CharacterizationEntry) -> Product | None:
    product_name = synthesis.metadata.product if synthesis.metadata.product else "unknown"
    product_mass = find_product_mass(product_characterization)
    pxrd_files = find_corresponding_pxrd_files(product_characterization)
    return Product(product_name, product_mass, pxrd_files)


def find_corresponding_pxrd_files(characterization: CharacterizationEntry) -> List[PXRDFile]:
    result = []
    for ch in characterization.characterization:
        if ch.relative_file_path and ch.x_ray_source and ch.sample_holder and characterization.metadata.description:
                result.append(PXRDFile(
                    ch.relative_file_path
                ))
    return result


def find_product_mass(characterization: CharacterizationEntry) -> Quantity | None:
    # Filter characterizations by whether they have the weight attribute
    mass_characterizations = [c for c in characterization.characterization if c.weight]
    if mass_characterizations:
        # Return the weight of the first characterization that has it
        return mass_characterizations[0].weight
    return None


def print_synthesis_data(synthesis: SynthesisElement, characterization: CharacterizationEntry):
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
            print(f" -(Type: {step.xml_type}, Amount: {step.amount}, Reagent: {step.reagent}, Temp: {step.temp}, Time: {step.time}, Vessel: {step.vessel}, Solvent: {step.solvent}, Gas: {step.gas}, Pressure: {step.pressure}, Comment: {step.comment})")
    if synthesis.procedure.reaction:
        print("Reaction Steps:")
        for step in synthesis.procedure.reaction.step:
            print(f" -(Type: {step.xml_type}, Amount: {step.amount}, Reagent: {step.reagent}, Temp: {step.temp}, Time: {step.time}, Vessel: {step.vessel}, Solvent: {step.solvent}, Gas: {step.gas}, Pressure: {step.pressure}, Comment: {step.comment})")
    if synthesis.procedure.workup:
        print("Workup Steps:")
        for step in synthesis.procedure.workup.step:
            print(f" -(Type: {step.xml_type}, Amount: {step.amount}, Reagent: {step.reagent}, Temp: {step.temp}, Time: {step.time}, Vessel: {step.vessel}, Solvent: {step.solvent}, Gas: {step.gas}, Pressure: {step.pressure}, Comment: {step.comment})")

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
            print(f"   Sample Holder Diameter: {pxrd_file.sample_holder_diameter}")
