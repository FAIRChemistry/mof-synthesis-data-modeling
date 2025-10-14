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
import * as fs from 'fs';
import path from "path";


// __dirname gives the directory of the current script
const currentDir = __dirname;
const rootDirectory = path.join(currentDir, "..", "..", "..");
const dataDirectory = path.join(rootDirectory, "data");


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
                result += `Add ${step._amount ? step._amount.Value : ''} ${step._amount ? step._amount.Unit : ''} of ${step._reagent || step._solvent}\n`;
                break;
            case XMLType.HeatChill:
                result += `Heat/Chill to ${step._temp ? step._temp.Value : ''} ${step._temp ? step._temp.Unit : ''} for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}\n`;
                break;
            case XMLType.Dry:
                result += `Dry for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}\n`;
                break;
            case XMLType.EvacuateAndRefill:
                result += `Evacuate and refill with ${step._gas || ''}\n`;
                break;
            case XMLType.Wait:
                result += `Wait for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}\n`;
                break;
            case XMLType.Evaporate:
                result += `Evaporate solvent\n`;
                break;
            case XMLType.Sonicate:
                result += `Sonicate for ${step._time ? step._time.Value : ''} ${step._time ? step._time.Unit : ''}\n`;
                break;
            case XMLType.WashSolid:
                result += `Wash solid with ${step._solvent || ''} ${step._amount ? step._amount.Value : ''} ${step._amount ? step._amount.Unit : ''}\n`;
                break;


        }
    }
    return result;
}

function mofsyToMpif(inputProcedure: string, inputCharacterization: string, outputFolder: string) {

const procedureJsonFile = fs.readFileSync(inputProcedure, 'utf-8');
const characterizationJsonFile = fs.readFileSync(inputCharacterization, 'utf-8');

// reads in procedure and characterization JSON files and writes the corresponding data into the MPIFData structure, which is then converted to a string in MPIF format and written to a file
// the procedure and characterization values are actually objects of lists of procedure and characterization entries from many experiments.
// For each of them, a separate output file should be created.

const prodedure = ConvertProc.toProcedure(procedureJsonFile);
const productCharacterization = ConvertChar.toProductCharacterization(characterizationJsonFile);

prodedure.Synthesis.forEach((synthesisEntry, index) => {

    // prepare data
    const experimentId = synthesisEntry.Metadata._description;
    const correspondingCharacterization: CharacterizationEntry|undefined = productCharacterization.ProductCharacterization.find(charEntry => charEntry.Metadata._description === experimentId);
    if (!correspondingCharacterization) {
        console.warn(`No corresponding characterization found for experiment ID: ${experimentId}`);
        return;
    }
    const char = correspondingCharacterization.Characterization;

    const productName = synthesisEntry.Metadata._product || 'unknown_product';

    let reactionTemp = -1;
    let reactionTime = -1;
    let reactionTimeUnit: '' | 's' | 'min' | 'h' | 'days' = '';
    let reactionNote = undefined;

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
            reactionNote = heatStep._comment;
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
        } else {
            throw new Error("Vessel material not recognized: " + vessel._type)
        }
        if (vessel._type!.toLowerCase().includes("vial")) {
            vessel_type = "Vial"
        } else if (vessel._type!.toLowerCase().includes("autoclave")) {
            vessel_type = "Autoclave"
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
        dataName: productName,
        creationDate: new Date().toISOString().split('T')[0],
        generatorVersion: '1.0',
        publicationDOI: 'TODO',
        procedureStatus: 'success',
        name: 'Todo',
        email: 'Todo',
        orcid: 'Todo',
        address: 'Todo',
        phone: undefined
    }

    const productInfo: ProductInfo = {
        type: 'composite',
        casNumber: undefined,
        commonName: productName,
        systematicName: 'Todo',
        formula: undefined,
        formulaWeight: undefined,
        state: 'solid',
        color: 'white',
        handlingAtmosphere: 'air',
        handlingNote: undefined,
        cif: undefined
    }

    const synthesisGeneral: SynthesisGeneral = {
        performedDate: synthesisEntry.Metadata._date as string || new Date().toISOString().split('T')[0].toString(),
        labTemperature: 35,
        labHumidity: 45,
        reactionType: 'mix',
        reactionTemperature: reactionTemp,
        temperatureController: 'oven',
        reactionTime: reactionTime,
        reactionTimeUnit: reactionTimeUnit,
        reactionAtmosphere: 'air',
        reactionContainer: vessel._name || 'unknown_container',
        reactionNote: reactionNote,
        productAmount: undefined,
        productAmountUnit: "",
        productYield: undefined,
        scale: 'gram',
    }

    const steps: ProcedureStep[] = [
        {
            id: 'preparation',
            type: 'Preparation',
            atmosphere: 'Air',
            detail: prep_details
        },
        {
            id: 'reaction',
            type: 'Reaction',
            atmosphere: 'Air',
            detail: reaction_details
        },
        {
            id: 'workup',
            type: 'Work-up',
            atmosphere: 'Air',
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

    if (char.pxrd.length > 0) {
        const firstPxrd = char.pxrd[0];
        let pxrdSource: 'Cu' | 'Cr' | 'Fe' | 'Co' | 'Mo' | 'Ag' | 'synchrotron' | 'other'  = 'other'
        switch (firstPxrd["_x-ray_source"]) {
            case XRaySource.CoKα1:
                pxrdSource = 'Co';
                break;
            case XRaySource.CuKα1:
                pxrdSource = 'Cu';
                break;
        }


        const pxrdFilePath = path.join(dataDirectory, firstPxrd._relative_file_path);
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

// MIL-88B_101
let inputProcedure = path.join(dataDirectory, "MIL-88B_101", "generated", "procedure_from_MIL_2.json");
let inputCharacterization = path.join(dataDirectory, "MIL-88B_101", "generated", "characterization_from_MIL_2.json");
let outputFolder = path.join(dataDirectory, "MIL-88B_101", "generated", "mpif_outputs");
mofsyToMpif(inputProcedure, inputCharacterization, outputFolder);

// MOCOF-1
inputProcedure = path.join(dataDirectory, "MOCOF-1", "generated", "procedure_from_sciformation.json");
inputCharacterization = path.join(dataDirectory, "MOCOF-1", "generated", "characterization_from_sciformation.json");
outputFolder = path.join(dataDirectory, "MOCOF-1", "generated", "mpif_outputs");
mofsyToMpif(inputProcedure, inputCharacterization, outputFolder);

