import type {
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
} from './mpif-gui/mpif.ts'
import {stringifyMPIF} from './mpif-gui/mpifParser.ts'
import {Convert as ConvertChar, XRaySource} from "./generated/characterization.ts";
import type {CharacterizationEntry} from "./generated/characterization.ts";
import {
    Convert as ConvertProc,
    Role,
    TimeUnit,
    XMLType
} from "./generated/procedure.ts";
import type {
    ComponentElement,
    ProcedureSectionObject,
    ProcedureSectionsObject,
    StepEntryObject
} from "./generated/procedure.ts";
import {Convert as ConvertToMpifParams} from "./generated/mpif_params.ts"
import type {MPIFParameters} from "./generated/mpif_params.ts"
import * as fs from 'fs';
import path from "path";
import Ajv from 'ajv';
import {fileURLToPath} from "url";


// __dirname gives the directory of the current script
const currentDir = path.dirname(fileURLToPath(import.meta.url));
const rootDirectory = path.join(currentDir, "..", "..", "..");
const dataDirectory = path.join(rootDirectory, "data");
const schemasDirectory = path.join(rootDirectory, "data_model");

type Mofsy2MpifSource = {
    id: string;
    procedure: string;
    characterization: string;
    mpifOutputFolder: string;
    mpifParams: string;
}

type ConversionSources = {
    mofsy2mpif?: Mofsy2MpifSource[];
}

function resolveRepoPath(relativePath: string): string {
    return path.join(rootDirectory, relativePath);
}

function findStepByReagent(procedure: ProcedureSectionsObject, reagentId: string): StepEntryObject | undefined {
    for (const prepareStep of (procedure.Prep as ProcedureSectionObject).Step as StepEntryObject[]) {
        if (prepareStep._reagent === reagentId) {
            return prepareStep;
        }
        if (prepareStep._solvent === reagentId) {
            return prepareStep;
        }
    }
    for (const reactionStep of (procedure.Reaction as ProcedureSectionObject).Step as StepEntryObject[]) {
        if (reactionStep._reagent === reagentId) {
            return reactionStep;
        }
        if (reactionStep._solvent === reagentId) {
            return reactionStep;
        }
    }
    for (const workupStep of (procedure.Workup as ProcedureSectionObject).Step as StepEntryObject[]) {
        if (workupStep._reagent === reagentId) {
            return workupStep;
        }
        if (workupStep._solvent === reagentId) {
            return workupStep;
        }
    }
}

function findStepByType(procedure: ProcedureSectionsObject, xmlType: XMLType): StepEntryObject | undefined {
    for (const reactionStep of (procedure.Reaction as ProcedureSectionObject).Step as StepEntryObject[]) {
        if (reactionStep.$xml_type === xmlType) {
            return reactionStep;
        }
    }
    for (const prepareStep of (procedure.Prep as ProcedureSectionObject).Step as StepEntryObject[]) {
        if (prepareStep.$xml_type === xmlType) {
            return prepareStep;
        }
    }
    for (const workupStep of (procedure.Workup as ProcedureSectionObject).Step as StepEntryObject[]) {
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
                if (step._time && step._time.Value !== undefined) {
                    result += `Dry for ${step._time.Value} ${step._time.Unit}. `;
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

const prodedure = ConvertProc.toSynthesisProcedure(procedureJsonFile);
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
        productAmount = lastWeight.Value;
        productAmountUnit = lastWeight.Unit;
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

    const heatStep = findStepByType(synthesisEntry.Procedure as ProcedureSectionsObject, XMLType.HeatChill);
    if (heatStep) {
        if (heatStep._temp && heatStep._temp.Value !== undefined) {
            reactionTemp = heatStep._temp.Value;
        }
        if (heatStep._time && heatStep._time.Value !== undefined) {
            reactionTime = heatStep._time.Value;
            if (heatStep._time.Unit == TimeUnit.Hour) {
                reactionTimeUnit = 'h';
            } else if (heatStep._time.Unit == TimeUnit.Day) {
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

            const step = findStepByReagent(synthesisEntry.Procedure as ProcedureSectionsObject, reagent._id!);
            if (!step) {
                continue;
            }
            const amountUnit = step._amount ? step._amount.Unit : undefined;

            if (reagent._role !== Role.Solvent) {
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
    const vesselId = vessel?._id || 'unknown_container';
    let vessel_material = "unknown"
    let vessel_type: '' | 'Vial' | 'Jar' | 'Autoclave' | 'Beaker' | 'Flask' | 'Centrifuge-tube' | 'Other' = ""
    let vessel_note = undefined
    if (vessel && vessel._type) {
        const normalizedVesselType = vessel._type!.toLowerCase();
        if (normalizedVesselType.includes("glass")) {
            vessel_material = "Glass"
        }else if (normalizedVesselType.includes("microwave")) {
            vessel_material = ''
            vessel_note = vessel._type;
        } else if (normalizedVesselType.includes("teflon")) {
            vessel_material = "Teflon"
        } else if (normalizedVesselType.includes("schlenk bomb")) {
            vessel_material = "Glass"
        }
        if (normalizedVesselType.includes("vial")) {
            vessel_type = "Vial"
        } else if (normalizedVesselType.includes("autoclave")) {
            vessel_type = "Autoclave"
        } else if (normalizedVesselType.includes("schlenk bomb")) {
            vessel_type = "Flask"
        } else if (normalizedVesselType.includes("jar")) {
            vessel_type = "Jar"
        } else if (normalizedVesselType.includes("beaker")) {
            vessel_type = "Beaker"
        } else if (normalizedVesselType.includes("centrifuge")) {
            vessel_type = "Centrifuge-tube"
        } else {
            vessel_type = "Other"
            vessel_note = vessel._type;
        }
    }
    const vessels: Vessel[] = [
        {
            id: vesselId,
            volume: undefined,
            volumeUnit: "mL",
            material: vessel_material,
            type: vessel_type,
            purpose: 'Reaction',
            note: vessel_note

        }
    ]

    let workup_details = stringifySteps(((synthesisEntry.Procedure as ProcedureSectionsObject).Workup as ProcedureSectionObject).Step as StepEntryObject[])

    // write all the data into the MPIF structures
    const metadata: MPIFMetadata = {
        dataName: mpifParams.metadata.dataName,
        creationDate: process.env.MPIF_CREATION_DATE || mpifParams.metadata.creationDate || new Date().toISOString().split('T')[0],
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

    const synthesisGeneral: SynthesisGeneral = {
        performedDate: synthesisEntry.Metadata._date as string || mpifParams.synthesisGeneral.performedDate.toString() || "undefined",
        labTemperature: mpifParams.synthesisGeneral.labTemperature,
        labHumidity: mpifParams.synthesisGeneral.labHumidity,
        reactionType: mpifParams.synthesisGeneral.reactionType,
        reactionTemperature: reactionTemp,
        temperatureController: mpifParams.synthesisGeneral.temperatureController,
        reactionTime: reactionTime,
        reactionTimeUnit: reactionTimeUnit,
        reactionAtmosphere: mpifParams.synthesisGeneral.reactionAtmosphere || '',
        reactionContainer: vesselId,
        reactionNote: reactionNote,
        productAmount: productAmount,
        productAmountUnit: productAmountUnit,
        productYield: mpifParams.productInfo.productYield,
        scale: mpifParams.synthesisGeneral.scale,
    }

    const steps: ProcedureStep[] = workup_details ? [
        {
            id: 'workup',
            type: 'Work-up',
            atmosphere: mpifParams.steps.workupAtmosphere || 'Air',
            detail: workup_details
        }
    ] : [];

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
    const outputFilePath = outputFolderPath + "/" + `output_${experimentId}.mpif`; // replace with desired output path
    // first generate the folder if needed
    if (!fs.existsSync(outputFolderPath)) {
        fs.mkdirSync(outputFolderPath, { recursive: true });
    }
    fs.writeFileSync(outputFilePath, mpifString);

});
}

const paramsSchema = path.join(schemasDirectory, "mpif_params.schema.json");
const conversionSources = JSON.parse(
    fs.readFileSync(path.join(dataDirectory, "conversion_sources.json"), 'utf-8')
) as ConversionSources;

for (const source of conversionSources.mofsy2mpif || []) {
    const procedurePath = resolveRepoPath(source.procedure);
    const characterizationPath = resolveRepoPath(source.characterization);
    const mpifParamsPath = resolveRepoPath(source.mpifParams);
    if (!fs.existsSync(procedurePath) || !fs.existsSync(characterizationPath) || !fs.existsSync(mpifParamsPath)) {
        console.log(
            `Skipping ${source.id} because one or more input files are missing.`,
        );
        continue;
    }

    mofsyToMpif(
        procedurePath,
        characterizationPath,
        resolveRepoPath(source.mpifOutputFolder),
        mpifParamsPath,
        paramsSchema
    );
}
