import os

from .generated.procedure_data_structure import SynthesisProcedure, Role, AmountUnit, TempUnit, XMLType, Solvent
from .generated.characterization_data_structure import Characterization
from .utils import load_json, save_json


def extract_interesting_params_for_mocof_1(procedure: SynthesisProcedure, characterization: Characterization):
    """Interesting are:
    Experimend ID: Metadata._description (just to keep track of data)
Aminoporphyrin monomer type: Search for the Reagent with _inchi containing "Co" (case sensitive) and extract sum formula from  _inchi
Aminoporphyrin monomer amount (µmol): Search for the Add Step with _reagent same as the _name above, and extract _amount.Value. Make sure Unit is "micromole".
Aldehyde monomer structure: Search for the Reagent with _role of "substrate" and _inchi does not contain "Co" and extract _inchi
Aldehyde monomer amount (µmol): Search for the Add Step with _reagent same as the _name of the Reagent above, and extract _amount.Value. Make sure Unit is "micromole".
Water amount (µmol): Search for the Reagent with _inchi matching "InChI=1S/H2O/h1H2". If not found return 0. Search for the Add Step with _reagent matching _name of the Reagent and extract _amount.Value. Make sure Unit is "micromole".
Acid structure: Search for the Reagent with _role of "acid". Match _inchi with the regex above and return $1.
Acid amount (µmol): Search for the Add Step with _reagent matching _name of the Reagent above. Extract _amount.Value. Make sure Unit is "micromole".
Other additives: Search for the Reagent with _role of "catalyst" and _inchi not matching "InChI=1S/H2O/h1H2". If not found, return None. Match _inchi with the regex above and return $1.
Solvent x (x=1,2,3) name: Search for all the Reagents with _role of "solvent". Give them number x and name in the following manner using _inchi.
InChI=1S/C4H8O2/c1-2-6-4-3-5-1/h1-4H2 → 1: 1,4-dioxane
InChI=1S/C6H5NO2/c8-7(9)6-4-2-1-3-5-6/h1-5H → 2: nitrobenzene
InChI=1S/C6H4Cl2/c7-5-3-1-2-4-6(5)8/h1-4H → 2: o-dichlorobenzene
InChI=1S/C9H12/c1-7-4-8(2)6-9(3)5-7/h4-6H,1-3H3 → 2: mesitylene
InChI=1S/C6H4N2O4/c9-7(10)5-2-1-3-6(4-5)8(11)12/h1-4H → 3: m-dinitrobenzene
If no matching, give the remaining smallest number and extract name with the regex above and $1.
Solvent x (x=1,2,3) volume (µL): Search for the Add Step with _reagent matching _name of the Reagent above. Extract _amount.Value. Make sure Unit is "microlitre".
Vessel: Hardware.Component._type
Degassing (boolean): EvacuateAndRefill exists or not
Temperature (°C): HeatChill _temp
Duration (h): HeatChill _time
Workup with NaCl (boolean): If there is WashSolid with _solvent = NaCl aq
Activation with scCO2 (boolean): If there is WashSolid with _solvent = scCO2 or MeOH+scCO2
MeOH in scCO2 activation (boolean): If the above condition is true and _solvent = MeOH+scCO2
Activation under vacuum (boolean): If there is Dry"""
    params_per_experiment = {}

    none_default = "none"

    for synthesis in procedure.synthesis:
        experiment_id = synthesis.metadata.description if synthesis.metadata.description else "unknown"
        params = {}

        # Aminoporphyrin monomer
        aminoporphyrin_reagent = next((r for r in synthesis.reagents.reagent if r.inchi and "Co" in r.inchi), none_default)
        if aminoporphyrin_reagent:
            params['aminoporphyrin_monomer_type'] = aminoporphyrin_reagent.inchi.split('/')[1] if aminoporphyrin_reagent.inchi.startswith("InChI=1S/") else aminoporphyrin_reagent.inchi
            add_step = next((step for step in synthesis.procedure.prep.step if step.reagent == aminoporphyrin_reagent.name), none_default)
            if add_step and add_step.amount and add_step.amount.unit == AmountUnit.MICROMOLE:
                params['aminoporphyrin_monomer_amount_umol'] = add_step.amount.value
            else:
                params['aminoporphyrin_monomer_amount_umol'] = -1.0
        else:
            params['aminoporphyrin_monomer_type'] = "unknown"
            params['aminoporphyrin_monomer_amount_umol'] = -1.0

        # Aldehyde monomer
        aldehyde_reagent = next((r for r in synthesis.reagents.reagent if r.role == Role.SUBSTRATE and (not r.inchi or "Co" not in r.inchi)), none_default)
        if aldehyde_reagent:
            params['aldehyde_monomer_structure'] = aldehyde_reagent.inchi.split('/')[1]
            add_step = next((step for step in synthesis.procedure.prep.step if step.reagent == aldehyde_reagent.name), none_default)
            if add_step and add_step.amount and add_step.amount.unit == AmountUnit.MICROMOLE:
                params['aldehyde_monomer_amount_umol'] = add_step.amount.value
            else:
                params['aldehyde_monomer_amount_umol'] = -1.0
        else:
            params['aldehyde_monomer_structure'] = "unknown"
            params['aldehyde_monomer_amount_umol'] = -1.0

        # Water amount
        water_reagent = next((r for r in synthesis.reagents.reagent if r.inchi == "InChI=1S/H2O/h1H2"), None)
        if water_reagent:
            add_step = next((step for step in synthesis.procedure.prep.step if step.reagent == water_reagent.name), none_default)
            if add_step and add_step.amount and add_step.amount.unit == AmountUnit.MICROMOLE:
                params['water_amount_umol'] = add_step.amount.value
            else:
                params['water_amount_umol'] = -1.0
        else:
            params['water_amount_umol'] = 0.0

        # Acid
        acid_structure_mapping = {
            "C6H4N2O5": ("2,4-Dinitrophenol", 5.1),
            "C7H6O2": ("Benzoic acid", 11.0),
            "C6H5BrO": ("m-Bromophenol", 15),
            "C7H5NO": ("p-Cyanophenol", 13.2),
            "C5H10O2": ("Pivalic acid", 13),
            "C6HF5O": ("Pentafluorophenol", 5.55),
            "unknown": ("unknown", 31.4),
            "C2HF3O2": ("Trifluoroacetic acid", 3.45),
            "C7H4N2O6": ("Dinitrobenzoic acid", 7),
            "C6H4ClNO3": ("4-Chloro-2-nitrophenol", 8),
            "C6H5NO3": ("p-Nitrophenol", 10.8),
            "C7H5NO4": ("p-Nitrobenzoic acid", 9.1),
            "C2H4O2": ("Acetic acid", 12.6),
            "3CHF3O3S.Sc": ("Scandium triflate", 20)
        }

        def get_acid_name_and_pKa(acid_structure):
            return acid_structure_mapping.get(acid_structure, ("unknown", -100.0))

        acid_reagent = next((r for r in synthesis.reagents.reagent if r.role == Role.ACID), none_default)
        if acid_reagent:
            acid_structure = acid_reagent.inchi.split('/')[1] if acid_reagent.inchi.startswith("InChI=1S/") else acid_reagent.inchi
            acid_name, acid_pKa = get_acid_name_and_pKa(acid_structure)
            params['acid_name'] = acid_name
            params['acid_pKa_DMSO'] = acid_pKa
            add_step = next((step for step in synthesis.procedure.prep.step if step.reagent == acid_reagent.name), none_default)
            if add_step and add_step.amount and add_step.amount.unit == AmountUnit.MICROMOLE:
                params['acid_amount_umol'] = add_step.amount.value
            else:
                params['acid_amount_umol'] = -1.0
        else:
            params['acid_name'] = "unknown"
            params['acid_pKa_DMSO'] = 31.4
            params['acid_amount_umol'] = -1.0

        # Other additives
        catalyst_reagent = next((r for r in synthesis.reagents.reagent if (r.role == Role.CATALYST or r.role == Role.REAGENT) and r.inchi != "InChI=1S/H2O/h1H2"), None)
        if catalyst_reagent:
            params['other_additives'] = catalyst_reagent.inchi.split('/')[1] if catalyst_reagent.inchi.startswith("InChI=1S/") else catalyst_reagent.inchi
        else:
            params['other_additives'] = none_default

        # Solvents
        solvent_inchi_map = {
              "InChI=1S/C4H8O2/c1-2-6-4-3-5-1/h1-4H2": (1, "1,4-dioxane"),
              "InChI=1S/C6H5NO2/c8-7(9)6-4-2-1-3-5-6/h1-5H": (2, "nitrobenzene"),
              "InChI=1S/C6H4Cl2/c7-5-3-1-2-4-6(5)8/h1-4H": (2, "o-dichlorobenzene"),
              "InChI=1S/C9H12/c1-7-4-8(2)6-9(3)5-7/h4-6H,1-3H3": (2, "mesitylene"),
              "InChI=1S/C6H4N2O4/c9-7(10)5-2-1-3-6(4-5)8(11)12/h1-4H": (3, "m-dinitrobenzene")
        }
        solvent_reagents = [r for r in synthesis.reagents.reagent if r.role == Role.SOLVENT]
        solvent_others = []
        for idx, solvent_reagent in enumerate(solvent_reagents):
            if solvent_reagent.inchi == "None" and solvent_reagent.name == "C4H8O2":
                      solvent_reagent.inchi = "InChI=1S/C4H8O2/c1-2-6-4-3-5-1/h1-4H2"
            if solvent_reagent.inchi in solvent_inchi_map:
                      solvent_number, solvent_name = solvent_inchi_map[solvent_reagent.inchi]
                      params[f'solvent_{solvent_number}_name'] = solvent_name
                      add_step = next((step for step in synthesis.procedure.prep.step if step.reagent == solvent_reagent.name), none_default)
                      if add_step and add_step.amount and add_step.amount.unit == AmountUnit.MICROLITRE:
                              params[f'solvent_{solvent_number}_volume_uL'] = add_step.amount.value
            else:
                      solvent_others.append(solvent_reagent.name)

        for solvent_other in solvent_others:
                for solvent_number in range(1, 3):
                        if f'solvent_{solvent_number}_name' not in params:
                                params[f'solvent_{solvent_number}_name'] = solvent_other
                                add_step = next((step for step in synthesis.procedure.prep.step if step.reagent == solvent_other), none_default)
                                if add_step and add_step.amount and add_step.amount.unit == AmountUnit.MICROLITRE:
                                        params[f'solvent_{solvent_number}_volume_uL'] = add_step.amount.value

        #if solvent slots 1-3 are missing, fill them with "None" and 0.0
        for solvent_number in range(1, 4):
           if f'solvent_{solvent_number}_name' not in params:
                params[f'solvent_{solvent_number}_name'] = none_default
                params[f'solvent_{solvent_number}_volume_uL'] = 0.0

        # Vessel
        if synthesis.hardware and synthesis.hardware.component:
            vessel_component = next((comp for comp in synthesis.hardware.component if comp.type), none_default)
            if vessel_component:
                params['vessel'] = vessel_component.type

        # Degassing
        params['degassing'] = any(step for step in synthesis.procedure.prep.step if step.xml_type == XMLType.EVACUATE_AND_REFILL)

        # Temperature and Duration
        heat_chill_step = next((step for step in synthesis.procedure.reaction.step if step.xml_type == XMLType.HEAT_CHILL), none_default)
        if heat_chill_step:
            if heat_chill_step.temp:
                params['temperature_C'] = heat_chill_step.temp.value
                assert heat_chill_step.temp.unit == TempUnit.CELSIUS
            if heat_chill_step.time:
                params['duration_h'] = heat_chill_step.time.value
                assert heat_chill_step.time.unit == AmountUnit.HOUR

        # Workup with NaCl
        params['workup_with_NaCl'] = any(step for step in synthesis.procedure.workup.step if step.xml_type == XMLType.WASH_SOLID and step.solvent == Solvent.NA_CL_AQ)

        # Activation with scCO2
        scCO2_activation = any(step for step in synthesis.procedure.workup.step if step.xml_type == XMLType.WASH_SOLID and (step.solvent == Solvent.SC_CO2 or step.solvent == Solvent.ME_OH_SC_CO2))
        params['activation_with_scCO2'] = scCO2_activation
        if scCO2_activation:
            params['MeOH_in_scCO2_activation'] = any(step for step in synthesis.procedure.workup.step if step.xml_type == XMLType.WASH_SOLID and step.solvent ==Solvent.ME_OH_SC_CO2)
        else:
            params['MeOH_in_scCO2_activation'] = False

        # Activation under vacuum
        params['activation_under_vacuum'] = any(step for step in synthesis.procedure.workup.step if step.xml_type == XMLType.DRY)

        params_per_experiment[experiment_id] = params

    return params_per_experiment



def extract_interesting_params():
    current_file_dir = __file__.rsplit('/', 1)[0]

    # sciformation case
    mofsy_procedure_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'converted', 'procedure_from_sciformation.json')
    mofsy_characterization_file_path = os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'converted', 'characterization_from_sciformation.json')
    procedure = SynthesisProcedure.from_dict(load_json(mofsy_procedure_file_path))
    characterization = Characterization.from_dict(load_json(mofsy_characterization_file_path))
    params = extract_interesting_params_for_mocof_1(procedure, characterization)
    save_json(params, os.path.join(current_file_dir, '../..', 'data', 'MOCOF-1', 'converted', 'params_from_sciformation.json'))

