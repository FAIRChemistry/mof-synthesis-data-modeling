// To parse this data:
//
//   import { Convert, Procedure } from "./file";
//
//   const procedure = Convert.toProcedure(json);
//
// These functions will throw an error if the JSON doesn't
// match the expected interface, even if the JSON is valid.

export interface Procedure {
    Synthesis: SynthesisElement[];
    [property: string]: any;
}

export interface SynthesisElement {
    Hardware?: Hardware;
    Metadata:  Metadata;
    Procedure: any[] | boolean | number | number | null | ProcedureWithDifferentSectionsObject | string;
    Reagents:  Reagents;
    [property: string]: any;
}

export interface Hardware {
    Component?: ComponentElement[];
    [property: string]: any;
}

export interface ComponentElement {
    _chemical?: string;
    _comment?:  string;
    _id:        string;
    _type?:     string;
    [property: string]: any;
}

export interface Metadata {
    _description:    string;
    _product?:       string;
    _product_inchi?: string;
    [property: string]: any;
}

export interface ProcedureWithDifferentSectionsObject {
    Prep?:     any[] | boolean | number | number | null | FlatProcedureObject | string;
    Reaction?: any[] | boolean | number | number | null | FlatProcedureObject | string;
    Workup?:   any[] | boolean | number | number | null | FlatProcedureObject | string;
    [property: string]: any;
}

export interface FlatProcedureObject {
    Step: Array<any[] | boolean | number | null | StepEntryObject | string>;
    [property: string]: any;
}

export interface StepEntryObject {
    _comment?: string;
    _vessel?:  string;
    $xml_type: XMLType;
    /**
     * amount of the involved chemical
     */
    _amount?: Quantity;
    /**
     * name of the involved chemical as listed in the "reagents"
     */
    _reagent?: string;
    /**
     * temperature in the case of HeatChill
     */
    _temp?: Empty;
    /**
     * time of the step in the case of HeatChill, Wait, Sonicate, or Dry
     */
    _time?: Time;
    /**
     * refilling gas in the case of EvacuateAndRefill
     */
    _gas?: Gas;
    /**
     * name of the solvent in the case of WashSolid
     */
    _solvent?: Solvent;
    /**
     * Ken please add the corresponding attributes if existing
     */
    _unknown?:  any;
    _pressure?: Pressure;
    [property: string]: any;
}

export enum XMLType {
    Add = "Add",
    Dry = "Dry",
    EvacuateAndRefill = "EvacuateAndRefill",
    Evaporate = "Evaporate",
    HeatChill = "HeatChill",
    Sonicate = "Sonicate",
    Wait = "Wait",
    WashSolid = "WashSolid",
}

/**
 * amount of the involved chemical
 */
export interface Quantity {
    Unit?:  AmountUnit;
    Value?: number;
    [property: string]: any;
}

export enum AmountUnit {
    Bar = "bar",
    Celsius = "celsius",
    Centilitre = "centilitre",
    Centimeter = "centimeter",
    Day = "day",
    Decilitre = "decilitre",
    Dimensionless = "dimensionless",
    Gram = "gram",
    Hour = "hour",
    Item = "item",
    Kelvin = "kelvin",
    Kilogram = "kilogram",
    Litre = "litre",
    Meter = "meter",
    Microgram = "microgram",
    Microlitre = "microlitre",
    Micromole = "micromole",
    Milligram = "milligram",
    Millilitre = "millilitre",
    Millimeter = "millimeter",
    Millimole = "millimole",
    Millisecond = "millisecond",
    Minute = "minute",
    Mole = "mole",
    Ohm = "ohm",
    Pascal = "pascal",
    Second = "second",
    Ton = "ton",
    Week = "week",
}

export enum Gas {
    Ar = "Ar",
}

/**
 * amount of the involved chemical
 */
export interface Pressure {
    Unit?:  PressureUnit;
    Value?: number;
    [property: string]: any;
}

export enum PressureUnit {
    Pascal = "pascal",
}

/**
 * name of the solvent in the case of WashSolid
 */
export enum Solvent {
    Acetone = "acetone",
    CHCl3 = "CHCl3",
    Dmf = "DMF",
    Et3N = "Et3N",
    EtOH = "EtOH",
    MeCN = "MeCN",
    MeOH = "MeOH",
    MeOHScCO2 = "MeOH+scCO2",
    NaClAq = "NaCl aq",
    ScCO2 = "scCO2",
}

/**
 * temperature in the case of HeatChill
 *
 * amount of the involved chemical
 */
export interface Empty {
    Unit?:  TempUnit;
    Value?: number;
    [property: string]: any;
}

export enum TempUnit {
    Celsius = "celsius",
}

/**
 * time of the step in the case of HeatChill, Wait, Sonicate, or Dry
 *
 * amount of the involved chemical
 */
export interface Time {
    Value?: number;
    Unit?:  AmountUnit;
    [property: string]: any;
}

export interface Reagents {
    Reagent: ReagentElement[];
    [property: string]: any;
}

export interface ReagentElement {
    _cas?:     string;
    _comment?: string;
    _id?:      string;
    _inchi?:   string;
    _name?:    string;
    _purity?:  string;
    _role?:    Role;
    [property: string]: any;
}

export enum Role {
    Acid = "acid",
    ActivatingAgent = "activating-agent",
    Base = "base",
    Catalyst = "catalyst",
    Ligand = "ligand",
    QuenchingAgent = "quenching-agent",
    Reagent = "reagent",
    Solvent = "solvent",
    Substrate = "substrate",
}

// Converts JSON strings to/from your types
// and asserts the results of JSON.parse at runtime
export class Convert {
    public static toProcedure(json: string): Procedure {
        return cast(JSON.parse(json), r("Procedure"));
    }

    public static procedureToJson(value: Procedure): string {
        return JSON.stringify(uncast(value, r("Procedure")), null, 2);
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
    "Procedure": o([
        { json: "Synthesis", js: "Synthesis", typ: a(r("SynthesisElement")) },
    ], "any"),
    "SynthesisElement": o([
        { json: "Hardware", js: "Hardware", typ: u(undefined, r("Hardware")) },
        { json: "Metadata", js: "Metadata", typ: r("Metadata") },
        { json: "Procedure", js: "Procedure", typ: u(a("any"), true, 3.14, 0, null, r("ProcedureWithDifferentSectionsObject"), "") },
        { json: "Reagents", js: "Reagents", typ: r("Reagents") },
    ], "any"),
    "Hardware": o([
        { json: "Component", js: "Component", typ: u(undefined, a(r("ComponentElement"))) },
    ], "any"),
    "ComponentElement": o([
        { json: "_chemical", js: "_chemical", typ: u(undefined, "") },
        { json: "_comment", js: "_comment", typ: u(undefined, "") },
        { json: "_id", js: "_id", typ: "" },
        { json: "_type", js: "_type", typ: u(undefined, "") },
    ], "any"),
    "Metadata": o([
        { json: "_description", js: "_description", typ: "" },
        { json: "_product", js: "_product", typ: u(undefined, "") },
        { json: "_product_inchi", js: "_product_inchi", typ: u(undefined, "") },
    ], "any"),
    "ProcedureWithDifferentSectionsObject": o([
        { json: "Prep", js: "Prep", typ: u(undefined, u(a("any"), true, 3.14, 0, null, r("FlatProcedureObject"), "")) },
        { json: "Reaction", js: "Reaction", typ: u(undefined, u(a("any"), true, 3.14, 0, null, r("FlatProcedureObject"), "")) },
        { json: "Workup", js: "Workup", typ: u(undefined, u(a("any"), true, 3.14, 0, null, r("FlatProcedureObject"), "")) },
    ], "any"),
    "FlatProcedureObject": o([
        { json: "Step", js: "Step", typ: a(u(a("any"), true, 3.14, null, r("StepEntryObject"), "")) },
    ], "any"),
    "StepEntryObject": o([
        { json: "_comment", js: "_comment", typ: u(undefined, "") },
        { json: "_vessel", js: "_vessel", typ: u(undefined, "") },
        { json: "$xml_type", js: "$xml_type", typ: r("XMLType") },
        { json: "_amount", js: "_amount", typ: u(undefined, r("Quantity")) },
        { json: "_reagent", js: "_reagent", typ: u(undefined, "") },
        { json: "_temp", js: "_temp", typ: u(undefined, r("Empty")) },
        { json: "_time", js: "_time", typ: u(undefined, r("Time")) },
        { json: "_gas", js: "_gas", typ: u(undefined, r("Gas")) },
        { json: "_solvent", js: "_solvent", typ: u(undefined, r("Solvent")) },
        { json: "_unknown", js: "_unknown", typ: u(undefined, "any") },
        { json: "_pressure", js: "_pressure", typ: u(undefined, r("Pressure")) },
    ], "any"),
    "Quantity": o([
        { json: "Unit", js: "Unit", typ: u(undefined, r("AmountUnit")) },
        { json: "Value", js: "Value", typ: u(undefined, 3.14) },
    ], "any"),
    "Pressure": o([
        { json: "Unit", js: "Unit", typ: u(undefined, r("PressureUnit")) },
        { json: "Value", js: "Value", typ: u(undefined, 3.14) },
    ], "any"),
    "Empty": o([
        { json: "Unit", js: "Unit", typ: u(undefined, r("TempUnit")) },
        { json: "Value", js: "Value", typ: u(undefined, 3.14) },
    ], "any"),
    "Time": o([
        { json: "Value", js: "Value", typ: u(undefined, 3.14) },
        { json: "Unit", js: "Unit", typ: u(undefined, r("AmountUnit")) },
    ], "any"),
    "Reagents": o([
        { json: "Reagent", js: "Reagent", typ: a(r("ReagentElement")) },
    ], "any"),
    "ReagentElement": o([
        { json: "_cas", js: "_cas", typ: u(undefined, "") },
        { json: "_comment", js: "_comment", typ: u(undefined, "") },
        { json: "_id", js: "_id", typ: u(undefined, "") },
        { json: "_inchi", js: "_inchi", typ: u(undefined, "") },
        { json: "_name", js: "_name", typ: u(undefined, "") },
        { json: "_purity", js: "_purity", typ: u(undefined, "") },
        { json: "_role", js: "_role", typ: u(undefined, r("Role")) },
    ], "any"),
    "XMLType": [
        "Add",
        "Dry",
        "EvacuateAndRefill",
        "Evaporate",
        "HeatChill",
        "Sonicate",
        "Wait",
        "WashSolid",
    ],
    "AmountUnit": [
        "bar",
        "celsius",
        "centilitre",
        "centimeter",
        "day",
        "decilitre",
        "dimensionless",
        "gram",
        "hour",
        "item",
        "kelvin",
        "kilogram",
        "litre",
        "meter",
        "microgram",
        "microlitre",
        "micromole",
        "milligram",
        "millilitre",
        "millimeter",
        "millimole",
        "millisecond",
        "minute",
        "mole",
        "ohm",
        "pascal",
        "second",
        "ton",
        "week",
    ],
    "Gas": [
        "Ar",
    ],
    "PressureUnit": [
        "pascal",
    ],
    "Solvent": [
        "acetone",
        "CHCl3",
        "DMF",
        "Et3N",
        "EtOH",
        "MeCN",
        "MeOH",
        "MeOH+scCO2",
        "NaCl aq",
        "scCO2",
    ],
    "TempUnit": [
        "celsius",
    ],
    "Role": [
        "acid",
        "activating-agent",
        "base",
        "catalyst",
        "ligand",
        "quenching-agent",
        "reagent",
        "solvent",
        "substrate",
    ],
};
