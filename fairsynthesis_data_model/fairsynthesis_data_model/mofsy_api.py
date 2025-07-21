import json
from typing import List

from .generated.mofsy_data_structure import Mofsy, ReagentElement, SynthesisElement, Role, Amount
from .pxrd_collector import PXRDFile

class Product:
    def __init__(self, name: str, mass: str|None, pxrd_files: List[PXRDFile]):
        self.name = name
        self.mass = mass
        self.pxrd_files = pxrd_files


def load_mofsy(file_path: str) -> Mofsy:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return Mofsy.from_dict(data)


def get_synthesis_list(mofsy: Mofsy) -> list[SynthesisElement]:
    return mofsy.synthesis


def get_synthesis_by_experiment_id(mofsy: Mofsy, experiment_id: str) -> SynthesisElement | None:
    for synthesis in mofsy.synthesis:
        if synthesis.metadata.description == experiment_id:
            return synthesis
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


def find_product(synthesis: SynthesisElement) -> Product | None:
    product_name = synthesis.metadata.product if synthesis.metadata.product else "unknown"
    product_mass = find_product_mass(synthesis)
    pxrd_files = find_corresponding_pxrd_files(synthesis)
    return Product(product_name, product_mass, pxrd_files)


def find_corresponding_pxrd_files(synthesis: SynthesisElement) -> List[PXRDFile]:
    result = []
    for characterization in synthesis.product_characterization:
        if characterization.relative_file_path and characterization.x_ray_source and characterization.sample_holder and synthesis.metadata.description:
                result.append(PXRDFile(
                    characterization.relative_file_path
                ))
    return result


def find_product_mass(synthesis: SynthesisElement) -> Amount | None:
    # Filter characterizations by whether they have the weight attribute
    mass_characterizations = [c for c in synthesis.product_characterization if c.weight]
    if mass_characterizations:
        # Return the weight of the first characterization that has it
        return mass_characterizations[0].weight
    return None


def print_synthesis_data(synthesis: SynthesisElement):
    print(f"Synthesis ID: {synthesis.metadata.description}")
    print_reagents(synthesis)
    print_procedure(synthesis)
    product = find_product(synthesis)
    if product:
        print_product(product)

def print_reagents(synthesis: SynthesisElement):
    print("Reagents:")
    for reagent in synthesis.reagents.reagent:
        print(f" - {reagent.name} (Role: {reagent.role.value})")

def print_procedure(synthesis: SynthesisElement):
    print("Procedure:")
    # The procedure either has all steps in the "step" array, or it is split into "prep", "reaction", and "workup"
    if synthesis.procedure.step:
        for step in synthesis.procedure.step:
            print(f" -(Type: {step.xml_type}, Amount: {step.amount}, Reagent: {step.reagent}, Stir: {step.stir}, Temp: {step.temp}, Time: {step.time})")
    else:
        if synthesis.procedure.prep:
            print("Prep Steps:")
            for step in synthesis.procedure.prep.step:
                print(f" -(Type: {step.xml_type}, Amount: {step.amount}, Reagent: {step.reagent}, Stir: {step.stir}, Temp: {step.temp}, Time: {step.time})")
        if synthesis.procedure.reaction:
            print("Reaction Steps:")
            for step in synthesis.procedure.reaction.step:
                print(f" -(Type: {step.xml_type}, Amount: {step.amount}, Reagent: {step.reagent}, Stir: {step.stir}, Temp: {step.temp}, Time: {step.time})")
        if synthesis.procedure.workup:
            print("Workup Steps:")
            for step in synthesis.procedure.workup.step:
                print(f" -(Type: {step.xml_type}, Amount: {step.amount}, Reagent: {step.reagent}, Stir: {step.stir}, Temp: {step.temp}, Time: {step.time})")

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
