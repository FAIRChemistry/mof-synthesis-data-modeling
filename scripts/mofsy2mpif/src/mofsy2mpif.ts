import {
    Characterization,
    Hardware,
    MPIFData,
    MPIFMetadata,
    ProcedureStep,
    ProductInfo,
    PXRDData,
    Solvent,
    Substrate,
    SynthesisDetails,
    SynthesisGeneral,
    Vessel
} from './mpif-gui/mpif'
import {stringifyMPIF} from './mpif-gui/mpifParser'
import {CharacterizationEntry, Convert as ConvertChar, XRaySource} from "./generated/characterization";
import {
    AmountUnit,
    ComponentElement,
    Convert as ConvertProc,
    FlatProcedureObject,
    ProcedureWithDifferentSectionsObject,
    Role,
    StepEntryObject,
    XMLType
} from "./generated/procedure";
import {Convert as ConvertToMpifParams, MPIFParameters, ReactionAtmosphere} from "./generated/mpif_params"
import * as fs from 'fs';
import path from "path";
import Ajv from 'ajv';


// __dirname gives the directory of the current script
const currentDir = __dirname;
const rootDirectory = path.join(currentDir, "..", "..", "..");
const dataDirectory = path.join(rootDirectory, "data");
const schemasDirectory = path.join(rootDirectory, "data_model");


function findStepByReagent(procedure: ProcedureWithDifferentSectionsObject, reagentId: string): StepEntryObject | undefined {
    for (const prepareStep of (procedure.Prep as FlatProcedureObject).Step as StepEntryObject[]) {
        if (prepareStep._reagent === reagentId) {
            return prepareStep;
        }
        if (prepareStep._solvent === reagentId) {
            return prepareStep;
        }
    }
    for (const reactionStep of (procedure.Reaction as FlatProcedureObject).Step as StepEntryObject[]) {
        if (reactionStep._reagent === reagentId) {
            return reactionStep;
        }
        if (reactionStep._solvent === reagentId) {
            return reactionStep;
        }
    }
    for (const workupStep of (procedure.Workup as FlatProcedureObject).Step as StepEntryObject[]) {
        if (workupStep._reagent === reagentId) {
            return workupStep;
        }
        if (workupStep._solvent === reagentId) {
            return workupStep;
        }
    }
}

function findStepByType(procedure: ProcedureWithDifferentSectionsObject, xmlType: XMLType): StepEntryObject | undefined {
    for (const reactionStep of (procedure.Reaction as FlatProcedureObject).Step as StepEntryObject[]) {
        if (reactionStep.$xml_type === xmlType) {
            return reactionStep;
        }
    }
    for (const prepareStep of (procedure.Prep as FlatProcedureObject).Step as StepEntryObject[]) {
        if (prepareStep.$xml_type === xmlType) {
            return prepareStep;
        }
    }
    for (const workupStep of (procedure.Workup as FlatProcedureObject).Step as StepEntryObject[]) {
        if (workupStep.$xml_type === xmlType) {
            return workupStep;
        }
    }
}

function stringifySteps(steps: StepEntryObject[]): string {
    let result = "";
    for (const step of steps) {
        switch (step.$xml_type) {
            case XMLType.Add:
                result += `Add ${step._amount ? step._amount.Value : ''} ${step._amount ? step._amount.Unit : ''} of ${step._reagent || step._solvent}. `;
                break;
            case XMLType.HeatChill:
                const verb = (step._temp && step._temp.Value && step._temp.Value > 25) ? "Heat" : "Chill";
                result += `${verb} to ${step._temp ? step._temp.Value : ''} ${step._temp ? step._temp.Unit : ''} for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}. `;
                break;
            case XMLType.Dry:
                if (step._time && step._time.Value) {
                    result += `Dry for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}. `;
                } else {
                    result += `Dry. `;
                }
                break;
            case XMLType.EvacuateAndRefill:
                result += `Degas the reaction mixture. `; // specific to MOCOF-1 case, otherwise: Evacuate and refill with ${step._gas || ''}
                break;
            case XMLType.Wait:
                result += `Wait for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}. `;
                break;
            case XMLType.Evaporate:
                result += `Evaporate solvent. `;
                break;
            case XMLType.Sonicate:
                result += `Sonicate for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}. `;
                break;
            case XMLType.WashSolid:
                result += `Wash solid with ${step._solvent || ''}${step._amount ? " " + step._amount.Value : ''}${step._amount ? " "+ step._amount.Unit : ''}. `;
                break;


        }
    }
    return result;
}

function mofsyToMpif(inputProcedurePath: string, inputCharacterizationPath: string, outputFolderPath: string, inputParamsPath: string, paramsSchemaPath: string) {

const procedureJsonFile = fs.readFileSync(inputProcedurePath, 'utf-8');
const characterizationJsonFile = fs.readFileSync(inputCharacterizationPath, 'utf-8');

const ajv = new Ajv();
const paramsSchema = JSON.parse(fs.readFileSync(paramsSchemaPath, 'utf-8'));
const paramsDataString = fs.readFileSync(inputParamsPath, 'utf-8');
const paramsData = JSON.parse(paramsDataString);
const validate = ajv.compile(paramsSchema);
if (!validate(paramsData)) {
  console.log(validate.errors);
    throw new Error("MPIF Parameters JSON file is not valid against the schema.");
}
const mpifParams: MPIFParameters = ConvertToMpifParams.toMPIFParameters(paramsDataString);

// reads in procedure and characterization JSON files and writes the corresponding data into the MPIFData structure, which is then converted to a string in MPIF format and written to a file
// the procedure and characterization values are actually objects of lists of procedure and characterization entries from many experiments.
// For each of them, a separate output file should be created.

const prodedure = ConvertProc.toProcedure(procedureJsonFile);
const productCharacterization = ConvertChar.toCharacterization(characterizationJsonFile);

prodedure.Synthesis.forEach((synthesisEntry, index) => {

    // prepare data
    const experimentId = synthesisEntry.Metadata._description;
    const correspondingCharacterization: CharacterizationEntry|undefined = productCharacterization.ProductCharacterization.find(charEntry => charEntry.ExperimentId === experimentId);
    if (!correspondingCharacterization) {
        console.warn(`No corresponding characterization found for experiment ID: ${experimentId}`);
        return;
    }
    const char = correspondingCharacterization.Characterization;

    const productWeight = char.Weight
    let productAmount = mpifParams.productInfo.productAmount;
    let productAmountUnit = mpifParams.productInfo.productAmountUnit;
    if (productWeight && productWeight.length>0) {
        const lastWeight = productWeight[productWeight.length -1];
        productAmount = lastWeight.Weight.Value;
        productAmountUnit = lastWeight.Weight.Unit;
        // shorten unit if needed
        if (productAmountUnit === "gram") {
            productAmountUnit = 'g';
        } else if (productAmountUnit === "milligram") {
            productAmountUnit = 'mg';
        } else if (productAmountUnit === "milliliter") {
            productAmountUnit = 'mL';
        }
    }

    let reactionTemp = -1;
    let reactionTime = -1;
    let reactionTimeUnit: '' | 's' | 'min' | 'h' | 'days' = '';
    let reactionNote = mpifParams.synthesisGeneral.reactionNote || '';

    const heatStep = findStepByType(synthesisEntry.Procedure as ProcedureWithDifferentSectionsObject, XMLType.HeatChill);
    if (heatStep) {
        if (heatStep._temp && heatStep._temp.Value !== undefined) {
            reactionTemp = heatStep._temp.Value;
        }
        if (heatStep._time && heatStep._time.Value !== undefined) {
            reactionTime = heatStep._time.Value;
            if (heatStep._time.Unit == AmountUnit.Hour) {
                reactionTimeUnit = 'h';
            } else if (heatStep._time.Unit == AmountUnit.Day) {
                reactionTimeUnit = 'days';
            }
        }

        if (heatStep._comment) {
            reactionNote += heatStep._comment;
        }
    }

    const substrates: Substrate[] = [];
    const solvents: Solvent[] = [];

    for (const reagent of synthesisEntry.Reagents.Reagent) {

            const step = findStepByReagent(synthesisEntry.Procedure as ProcedureWithDifferentSectionsObject, reagent._id!);
            if (!step) {
                continue;
            }
            const amountUnit = step._amount ? step._amount.Unit : undefined;

            if (reagent._role == Role.Substrate) {
            substrates.push({
                id: reagent._id || 'unknown_id',
                name: reagent._name || 'unknown_name',
                casNumber: reagent._cas,
                amount: step._amount ? step._amount.Value : undefined,
                amountUnit: amountUnit ? amountUnit.toString() : '',
            });
        } else if (reagent._role == Role.Solvent) {
            solvents.push({
                id: reagent._id || 'unknown_id',
                name: reagent._name || 'unknown_name',
                casNumber: reagent._cas,
                amount: step._amount ? step._amount.Value : undefined,
                amountUnit: amountUnit ? amountUnit.toString() : '',
            });
        }
    }

    const vessel: ComponentElement|undefined = synthesisEntry.Hardware!.Component![0]
    let vessel_material = "unknown"
    let vessel_type: '' | 'Vial' | 'Jar' | 'Autoclave' | 'Beaker' | 'Flask' | 'Centrifuge-tube' | 'Other' = ""
    let vessel_note = undefined
    if (vessel && vessel._type) {
        if (vessel._type!.toLowerCase().includes("glass")) {
            vessel_material = "Glass"
        }else if (vessel._type!.toLowerCase().includes("microwave")) {
            vessel_material = ''
            vessel_note = vessel._type;
        } else if (vessel._type!.toLowerCase().includes("teflon")) {
            vessel_material = "Teflon"
        } else if (vessel._type!.toLowerCase().includes("schlenk bomb")) {
            vessel_material = "Glass"
        } else {
            throw new Error("Vessel material not recognized: " + vessel._type)
        }
        if (vessel._type!.toLowerCase().includes("vial")) {
            vessel_type = "Vial"
        } else if (vessel._type!.toLowerCase().includes("autoclave")) {
            vessel_type = "Autoclave"
        } else if (vessel._type!.toLowerCase().includes("schlenk bomb")) {
            vessel_type = "Flask"
        } else {
            throw new Error("Vessel type not recognized: " + vessel._type)
        }
    }
    const vessels: Vessel[] = [
        {
            id: vessel._id,
            volume: undefined,
            volumeUnit: "mL",
            material: vessel_material,
            type: vessel_type,
            purpose: 'Reaction',
            note: vessel_note

        }
    ]

    let prep_details = stringifySteps(((synthesisEntry.Procedure as ProcedureWithDifferentSectionsObject).Prep as FlatProcedureObject).Step as StepEntryObject[])
    let reaction_details = stringifySteps(((synthesisEntry.Procedure as ProcedureWithDifferentSectionsObject).Reaction as FlatProcedureObject).Step as StepEntryObject[])
    let workup_details = stringifySteps(((synthesisEntry.Procedure as ProcedureWithDifferentSectionsObject).Workup as FlatProcedureObject).Step as StepEntryObject[])

    // write all the data into the MPIF structures
    const metadata: MPIFMetadata = {
        dataName: mpifParams.metadata.dataName,
        creationDate: new Date().toISOString().split('T')[0],
        generatorVersion: mpifParams.metadata.generatorVersion,
        publicationDOI: mpifParams.metadata.publicationDOI,
        procedureStatus: mpifParams.metadata.procedureStatus,
        name: mpifParams.metadata.name,
        email: mpifParams.metadata.email,
        orcid: mpifParams.metadata.orcid,
        address: mpifParams.metadata.address,
        phone: mpifParams.metadata.phone,
    }

    const productInfo: ProductInfo = {
        type: mpifParams.productInfo.type,
        casNumber: mpifParams.productInfo.casNumber,
        commonName: mpifParams.productInfo.commonName || '',
        systematicName: mpifParams.productInfo.systematicName,
        formula: mpifParams.productInfo.formula,
        formulaWeight: mpifParams.productInfo.formulaWeight,
        state: mpifParams.productInfo.state,
        color: mpifParams.productInfo.color,
        handlingAtmosphere: mpifParams.productInfo.handlingAtmosphere,
        handlingNote: mpifParams.productInfo.handlingNote,
        cif: mpifParams.productInfo.cif
    }

    // reaction atmosphere: if a step EvacuateAndRefill is present in the reaction steps, use vacuum, otherwise use air
    const evacuateStep = findStepByType(synthesisEntry.Procedure as ProcedureWithDifferentSectionsObject, XMLType.EvacuateAndRefill);
    const reactionAtmosphere = evacuateStep ? ReactionAtmosphere.Vacuum : ReactionAtmosphere.Air;

    const synthesisGeneral: SynthesisGeneral = {
        performedDate: synthesisEntry.Metadata._date as string || mpifParams.synthesisGeneral.performedDate.toString() || "undefined",
        labTemperature: mpifParams.synthesisGeneral.labTemperature,
        labHumidity: mpifParams.synthesisGeneral.labHumidity,
        reactionType: mpifParams.synthesisGeneral.reactionType,
        reactionTemperature: reactionTemp,
        temperatureController: mpifParams.synthesisGeneral.temperatureController,
        reactionTime: reactionTime,
        reactionTimeUnit: reactionTimeUnit,
        reactionAtmosphere: mpifParams.synthesisGeneral.reactionAtmosphere || reactionAtmosphere,
        reactionContainer: vessel._id || 'unknown_container',
        reactionNote: reactionNote,
        productAmount: productAmount,
        productAmountUnit: productAmountUnit,
        productYield: mpifParams.productInfo.productYield,
        scale: mpifParams.synthesisGeneral.scale,
    }

    const steps: ProcedureStep[] = [
        {
            id: 'preparation',
            type: 'Preparation',
            atmosphere: mpifParams.steps.preparationAtmosphere || 'Air',
            detail: prep_details
        },
        {
            id: 'reaction',
            type: 'Reaction',
            // use the reaction atmosphere determined above unless overridden in the mpifParams. Make first character upper case
            atmosphere: mpifParams.steps.reactionAtmosphere || (reactionAtmosphere.toString().charAt(0).toUpperCase() + reactionAtmosphere.toString().slice(1).toLowerCase()) as 'Air' | 'Vacuum',
            detail: reaction_details
        },
        {
            id: 'workup',
            type: 'Work-up',
            atmosphere: mpifParams.steps.workupAtmosphere || 'Air',
            detail: workup_details
        }

    ];

    const synthesisDetails: SynthesisDetails = {
        substrates: substrates,
        solvents: solvents,
        vessels: vessels,
        hardware: [] as Hardware[],
        steps
    }

    let pxrd: PXRDData|undefined = undefined;
    if (char.Pxrd.length > 0) {
        const firstPxrd = char.Pxrd[0];
        let pxrdSource: 'Cu' | 'Cr' | 'Fe' | 'Co' | 'Mo' | 'Ag' | 'synchrotron' | 'other'  = 'other'
        switch (firstPxrd.XRaySource) {
            case XRaySource.CoKα1:
                pxrdSource = 'Co';
                break;
            case XRaySource.CuKα1:
                pxrdSource = 'Cu';
                break;
        }


        const pxrdFilePath = path.join(rootDirectory, firstPxrd.RelativeFilePath);
        const pxrdContent = fs.readFileSync(pxrdFilePath, 'utf-8');
        const pxrdData: Array<{ twoTheta: number; intensity: number; }> = [];
        const lines = pxrdContent.split('\n');
        for (const line of lines) {
            const [twoThetaStr, intensityStr] = line.trim().split(/\s+/);
            const twoTheta = parseFloat(twoThetaStr);
            const intensity = parseFloat(intensityStr);
            if (!isNaN(twoTheta) && !isNaN(intensity)) {
                pxrdData.push({twoTheta, intensity});
            }
        }

        pxrd = {
            source: pxrdSource,
            data: pxrdData

        }
    }

    const characterization: Characterization = {
        pxrd: pxrd,
    }

    const mpifData: MPIFData = {
        metadata: metadata,
        productInfo: productInfo,
        synthesisGeneral: synthesisGeneral,
        synthesisDetails: synthesisDetails,
        characterization: characterization
    };


    const mpifString = stringifyMPIF(mpifData);
    const outputFilePath = outputFolder + "/" + `output_${experimentId}.mpif`; // replace with desired output path
    // first generate the folder if needed
    if (!fs.existsSync(outputFolder)) {
        fs.mkdirSync(outputFolder, { recursive: true });
    }
    fs.writeFileSync(outputFilePath, mpifString);

});
}

// Fe–terephthalate
let inputProcedure = path.join(dataDirectory, "Fe–terephthalate", "converted", "procedure_from_Fe–terephthalate.json");
let inputCharacterization = path.join(dataDirectory, "Fe–terephthalate", "converted", "characterization_from_Fe–terephthalate.json");
let outputFolder = path.join(dataDirectory, "Fe–terephthalate", "converted", "mpif_outputs");
let paramsFile = path.join(dataDirectory, "Fe–terephthalate", "mpif_params.json");
const paramsSchema = path.join(schemasDirectory, "mpif_params.schema.json");
mofsyToMpif(inputProcedure, inputCharacterization, outputFolder, paramsFile, paramsSchema);

// MOCOF-1
inputProcedure = path.join(dataDirectory, "MOCOF-1", "converted", "procedure_from_sciformation.json");
inputCharacterization = path.join(dataDirectory, "MOCOF-1", "converted", "characterization_from_sciformation.json");
outputFolder = path.join(dataDirectory, "MOCOF-1", "converted", "mpif_outputs");
paramsFile = path.join(dataDirectory, "MOCOF-1", "mpif_params.json");
mofsyToMpif(inputProcedure, inputCharacterization, outputFolder, paramsFile, paramsSchema);

