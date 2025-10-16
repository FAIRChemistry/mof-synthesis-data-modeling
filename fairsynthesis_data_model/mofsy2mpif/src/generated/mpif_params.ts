// To parse this data:
//
//   import { Convert, MPIFParameters } from "./file";
//
//   const mPIFParameters = Convert.toMPIFParameters(json);
//
// These functions will throw an error if the JSON doesn't
// match the expected interface, even if the JSON is valid.

export interface MPIFParameters {
    metadata:         Metadata;
    productInfo:      ProductInfo;
    steps:            Steps;
    synthesisGeneral: SynthesisGeneral;
    [property: string]: any;
}

export interface Metadata {
    address:          string;
    creationDate:     Date;
    dataName:         string;
    email:            string;
    generatorVersion: string;
    name:             string;
    orcid:            string;
    phone?:           null | string;
    procedureStatus:  ProcedureStatus;
    publicationDOI:   string;
    [property: string]: any;
}

export enum ProcedureStatus {
    Failure = "failure",
    Success = "success",
    Test = "test",
}

export interface ProductInfo {
    casNumber?:         null | string;
    cif?:               null | string;
    color:              string;
    formula?:           null | string;
    formulaWeight?:     number | null;
    handlingAtmosphere: HandlingAtmosphere;
    handlingNote?:      null | string;
    state:              State;
    systematicName:     string;
    type:               Type;
    [property: string]: any;
}

export enum HandlingAtmosphere {
    Air = "air",
    Empty = "",
    Inert = "inert",
    Other = "other",
    OxygenFree = "oxygen-free",
    WaterFree = "water-free",
}

export enum State {
    Gas = "gas",
    Liquid = "liquid",
    Solid = "solid",
    Suspension = "suspension",
}

export enum Type {
    Composite = "composite",
    Inorganic = "inorganic",
    Organic = "organic",
    PorousFrameworkMaterial = "porous framework material",
}

export interface Steps {
    preparationAtmosphere: PreparationAtmosphere;
    reactionAtmosphere:    PreparationAtmosphere;
    workupAtmosphere:      PreparationAtmosphere;
    [property: string]: any;
}

export enum PreparationAtmosphere {
    Air = "Air",
    Dry = "Dry",
    Inert = "Inert",
    Vacuum = "Vacuum",
}

export interface SynthesisGeneral {
    labHumidity:           number;
    labTemperature:        number;
    performedDate:         Date;
    productAmount?:        number | null;
    productAmountUnit?:    string;
    productYield?:         number | null;
    reactionAtmosphere?:   ReactionAtmosphere;
    reactionNote?:         null | string;
    reactionType:          ReactionType;
    scale:                 Scale;
    temperatureController: TemperatureController;
    [property: string]: any;
}

export enum ReactionAtmosphere {
    Air = "air",
    Dry = "dry",
    Inert = "inert",
    Vacuum = "vacuum",
}

export enum ReactionType {
    Diffusion = "diffusion",
    Electrochemical = "electrochemical",
    Evaporation = "evaporation",
    Flow = "flow",
    Mechanochemical = "mechanochemical",
    Microwave = "microwave",
    Mix = "mix",
    Other = "other",
    Photochemical = "photochemical",
    Sonochemical = "sonochemical",
}

export enum Scale {
    Gram = "gram",
    Kilogram = "kilogram",
    Milligram = "milligram",
    Multigram = "multigram",
}

export enum TemperatureController {
    Ambient = "ambient",
    DryBath = "dry_bath",
    Furnace = "furnace",
    HotPlate = "hot_plate",
    LiquidBath = "liquid_bath",
    Microwave = "microwave",
    OilBath = "oil_bath",
    Other = "other",
    Oven = "oven",
    WaterBath = "water_bath",
}

// Converts JSON strings to/from your types
// and asserts the results of JSON.parse at runtime
export class Convert {
    public static toMPIFParameters(json: string): MPIFParameters {
        return cast(JSON.parse(json), r("MPIFParameters"));
    }

    public static mPIFParametersToJson(value: MPIFParameters): string {
        return JSON.stringify(uncast(value, r("MPIFParameters")), null, 2);
    }
}

function invalidValue(typ: any, val: any, key: any, parent: any = ''): never {
    const prettyTyp = prettyTypeName(typ);
    const parentText = parent ? ` on ${parent}` : '';
    const keyText = key ? ` for key "${key}"` : '';
    throw Error(`Invalid value${keyText}${parentText}. Expected ${prettyTyp} but got ${JSON.stringify(val)}`);
}

function prettyTypeName(typ: any): string {
    if (Array.isArray(typ)) {
        if (typ.length === 2 && typ[0] === undefined) {
            return `an optional ${prettyTypeName(typ[1])}`;
        } else {
            return `one of [${typ.map(a => { return prettyTypeName(a); }).join(", ")}]`;
        }
    } else if (typeof typ === "object" && typ.literal !== undefined) {
        return typ.literal;
    } else {
        return typeof typ;
    }
}

function jsonToJSProps(typ: any): any {
    if (typ.jsonToJS === undefined) {
        const map: any = {};
        typ.props.forEach((p: any) => map[p.json] = { key: p.js, typ: p.typ });
        typ.jsonToJS = map;
    }
    return typ.jsonToJS;
}

function jsToJSONProps(typ: any): any {
    if (typ.jsToJSON === undefined) {
        const map: any = {};
        typ.props.forEach((p: any) => map[p.js] = { key: p.json, typ: p.typ });
        typ.jsToJSON = map;
    }
    return typ.jsToJSON;
}

function transform(val: any, typ: any, getProps: any, key: any = '', parent: any = ''): any {
    function transformPrimitive(typ: string, val: any): any {
        if (typeof typ === typeof val) return val;
        return invalidValue(typ, val, key, parent);
    }

    function transformUnion(typs: any[], val: any): any {
        // val must validate against one typ in typs
        const l = typs.length;
        for (let i = 0; i < l; i++) {
            const typ = typs[i];
            try {
                return transform(val, typ, getProps);
            } catch (_) {}
        }
        return invalidValue(typs, val, key, parent);
    }

    function transformEnum(cases: string[], val: any): any {
        if (cases.indexOf(val) !== -1) return val;
        return invalidValue(cases.map(a => { return l(a); }), val, key, parent);
    }

    function transformArray(typ: any, val: any): any {
        // val must be an array with no invalid elements
        if (!Array.isArray(val)) return invalidValue(l("array"), val, key, parent);
        return val.map(el => transform(el, typ, getProps));
    }

    function transformDate(val: any): any {
        if (val === null) {
            return null;
        }
        const d = new Date(val);
        if (isNaN(d.valueOf())) {
            return invalidValue(l("Date"), val, key, parent);
        }
        return d;
    }

    function transformObject(props: { [k: string]: any }, additional: any, val: any): any {
        if (val === null || typeof val !== "object" || Array.isArray(val)) {
            return invalidValue(l(ref || "object"), val, key, parent);
        }
        const result: any = {};
        Object.getOwnPropertyNames(props).forEach(key => {
            const prop = props[key];
            const v = Object.prototype.hasOwnProperty.call(val, key) ? val[key] : undefined;
            result[prop.key] = transform(v, prop.typ, getProps, key, ref);
        });
        Object.getOwnPropertyNames(val).forEach(key => {
            if (!Object.prototype.hasOwnProperty.call(props, key)) {
                result[key] = transform(val[key], additional, getProps, key, ref);
            }
        });
        return result;
    }

    if (typ === "any") return val;
    if (typ === null) {
        if (val === null) return val;
        return invalidValue(typ, val, key, parent);
    }
    if (typ === false) return invalidValue(typ, val, key, parent);
    let ref: any = undefined;
    while (typeof typ === "object" && typ.ref !== undefined) {
        ref = typ.ref;
        typ = typeMap[typ.ref];
    }
    if (Array.isArray(typ)) return transformEnum(typ, val);
    if (typeof typ === "object") {
        return typ.hasOwnProperty("unionMembers") ? transformUnion(typ.unionMembers, val)
            : typ.hasOwnProperty("arrayItems")    ? transformArray(typ.arrayItems, val)
            : typ.hasOwnProperty("props")         ? transformObject(getProps(typ), typ.additional, val)
            : invalidValue(typ, val, key, parent);
    }
    // Numbers can be parsed by Date but shouldn't be.
    if (typ === Date && typeof val !== "number") return transformDate(val);
    return transformPrimitive(typ, val);
}

function cast<T>(val: any, typ: any): T {
    return transform(val, typ, jsonToJSProps);
}

function uncast<T>(val: T, typ: any): any {
    return transform(val, typ, jsToJSONProps);
}

function l(typ: any) {
    return { literal: typ };
}

function a(typ: any) {
    return { arrayItems: typ };
}

function u(...typs: any[]) {
    return { unionMembers: typs };
}

function o(props: any[], additional: any) {
    return { props, additional };
}

function m(additional: any) {
    return { props: [], additional };
}

function r(name: string) {
    return { ref: name };
}

const typeMap: any = {
    "MPIFParameters": o([
        { json: "metadata", js: "metadata", typ: r("Metadata") },
        { json: "productInfo", js: "productInfo", typ: r("ProductInfo") },
        { json: "steps", js: "steps", typ: r("Steps") },
        { json: "synthesisGeneral", js: "synthesisGeneral", typ: r("SynthesisGeneral") },
    ], "any"),
    "Metadata": o([
        { json: "address", js: "address", typ: "" },
        { json: "creationDate", js: "creationDate", typ: Date },
        { json: "dataName", js: "dataName", typ: "" },
        { json: "email", js: "email", typ: "" },
        { json: "generatorVersion", js: "generatorVersion", typ: "" },
        { json: "name", js: "name", typ: "" },
        { json: "orcid", js: "orcid", typ: "" },
        { json: "phone", js: "phone", typ: u(undefined, u(null, "")) },
        { json: "procedureStatus", js: "procedureStatus", typ: r("ProcedureStatus") },
        { json: "publicationDOI", js: "publicationDOI", typ: "" },
    ], "any"),
    "ProductInfo": o([
        { json: "casNumber", js: "casNumber", typ: u(undefined, u(null, "")) },
        { json: "cif", js: "cif", typ: u(undefined, u(null, "")) },
        { json: "color", js: "color", typ: "" },
        { json: "formula", js: "formula", typ: u(undefined, u(null, "")) },
        { json: "formulaWeight", js: "formulaWeight", typ: u(undefined, u(3.14, null)) },
        { json: "handlingAtmosphere", js: "handlingAtmosphere", typ: r("HandlingAtmosphere") },
        { json: "handlingNote", js: "handlingNote", typ: u(undefined, u(null, "")) },
        { json: "state", js: "state", typ: r("State") },
        { json: "systematicName", js: "systematicName", typ: "" },
        { json: "type", js: "type", typ: r("Type") },
    ], "any"),
    "Steps": o([
        { json: "preparationAtmosphere", js: "preparationAtmosphere", typ: r("PreparationAtmosphere") },
        { json: "reactionAtmosphere", js: "reactionAtmosphere", typ: r("PreparationAtmosphere") },
        { json: "workupAtmosphere", js: "workupAtmosphere", typ: r("PreparationAtmosphere") },
    ], "any"),
    "SynthesisGeneral": o([
        { json: "labHumidity", js: "labHumidity", typ: 0 },
        { json: "labTemperature", js: "labTemperature", typ: 0 },
        { json: "performedDate", js: "performedDate", typ: Date },
        { json: "productAmount", js: "productAmount", typ: u(undefined, u(3.14, null)) },
        { json: "productAmountUnit", js: "productAmountUnit", typ: u(undefined, "") },
        { json: "productYield", js: "productYield", typ: u(undefined, u(3.14, null)) },
        { json: "reactionAtmosphere", js: "reactionAtmosphere", typ: u(undefined, r("ReactionAtmosphere")) },
        { json: "reactionNote", js: "reactionNote", typ: u(undefined, u(null, "")) },
        { json: "reactionType", js: "reactionType", typ: r("ReactionType") },
        { json: "scale", js: "scale", typ: r("Scale") },
        { json: "temperatureController", js: "temperatureController", typ: r("TemperatureController") },
    ], "any"),
    "ProcedureStatus": [
        "failure",
        "success",
        "test",
    ],
    "HandlingAtmosphere": [
        "air",
        "",
        "inert",
        "other",
        "oxygen-free",
        "water-free",
    ],
    "State": [
        "gas",
        "liquid",
        "solid",
        "suspension",
    ],
    "Type": [
        "composite",
        "inorganic",
        "organic",
        "porous framework material",
    ],
    "PreparationAtmosphere": [
        "Air",
        "Dry",
        "Inert",
        "Vacuum",
    ],
    "ReactionAtmosphere": [
        "air",
        "dry",
        "inert",
        "vacuum",
    ],
    "ReactionType": [
        "diffusion",
        "electrochemical",
        "evaporation",
        "flow",
        "mechanochemical",
        "microwave",
        "mix",
        "other",
        "photochemical",
        "sonochemical",
    ],
    "Scale": [
        "gram",
        "kilogram",
        "milligram",
        "multigram",
    ],
    "TemperatureController": [
        "ambient",
        "dry_bath",
        "furnace",
        "hot_plate",
        "liquid_bath",
        "microwave",
        "oil_bath",
        "other",
        "oven",
        "water_bath",
    ],
};
