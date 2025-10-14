// To parse this data:
//
//   import { Convert, ProductCharacterization } from "./file";
//
//   const productCharacterization = Convert.toProductCharacterization(json);
//
// These functions will throw an error if the JSON doesn't
// match the expected interface, even if the JSON is valid.

export interface ProductCharacterization {
    ProductCharacterization: CharacterizationEntry[];
    [property: string]: any;
}

export interface CharacterizationEntry {
    Characterization: Characterization;
    Metadata:         Metadata;
    [property: string]: any;
}

export interface Characterization {
    purity: Purity[];
    pxrd:   Pxrd[];
    weight: Weighing[];
    [property: string]: any;
}

export interface Purity {
    _purity?: boolean;
    [property: string]: any;
}

export interface Pxrd {
    _relative_file_path: string;
    "_x-ray_source"?:    XRaySource;
    other_metadata?:     string;
    sample_holder?:      SampleHolder;
    [property: string]: any;
}

export enum XRaySource {
    CoKα1 = "Co Kα1",
    CuKα1 = "Cu Kα1",
}

export interface SampleHolder {
    _diameter?: Quantity;
    _type?:     string;
    [property: string]: any;
}

export interface Quantity {
    Unit?:  Unit;
    Value?: number;
    [property: string]: any;
}

export enum Unit {
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
    Second = "second",
    Ton = "ton",
    Week = "week",
}

export interface Weighing {
    _weight: Quantity;
    [property: string]: any;
}

export interface Metadata {
    _description: string;
    [property: string]: any;
}

// Converts JSON strings to/from your types
// and asserts the results of JSON.parse at runtime
export class Convert {
    public static toProductCharacterization(json: string): ProductCharacterization {
        return cast(JSON.parse(json), r("ProductCharacterization"));
    }

    public static productCharacterizationToJson(value: ProductCharacterization): string {
        return JSON.stringify(uncast(value, r("ProductCharacterization")), null, 2);
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
    "ProductCharacterization": o([
        { json: "ProductCharacterization", js: "ProductCharacterization", typ: a(r("CharacterizationEntry")) },
    ], "any"),
    "CharacterizationEntry": o([
        { json: "Characterization", js: "Characterization", typ: r("Characterization") },
        { json: "Metadata", js: "Metadata", typ: r("Metadata") },
    ], "any"),
    "Characterization": o([
        { json: "purity", js: "purity", typ: a(r("Purity")) },
        { json: "pxrd", js: "pxrd", typ: a(r("Pxrd")) },
        { json: "weight", js: "weight", typ: a(r("Weighing")) },
    ], "any"),
    "Purity": o([
        { json: "_purity", js: "_purity", typ: u(undefined, true) },
    ], "any"),
    "Pxrd": o([
        { json: "_relative_file_path", js: "_relative_file_path", typ: "" },
        { json: "_x-ray_source", js: "_x-ray_source", typ: u(undefined, r("XRaySource")) },
        { json: "other_metadata", js: "other_metadata", typ: u(undefined, "") },
        { json: "sample_holder", js: "sample_holder", typ: u(undefined, r("SampleHolder")) },
    ], "any"),
    "SampleHolder": o([
        { json: "_diameter", js: "_diameter", typ: u(undefined, r("Quantity")) },
        { json: "_type", js: "_type", typ: u(undefined, "") },
    ], "any"),
    "Quantity": o([
        { json: "Unit", js: "Unit", typ: u(undefined, r("Unit")) },
        { json: "Value", js: "Value", typ: u(undefined, 3.14) },
    ], "any"),
    "Weighing": o([
        { json: "_weight", js: "_weight", typ: r("Quantity") },
    ], "any"),
    "Metadata": o([
        { json: "_description", js: "_description", typ: "" },
    ], "any"),
    "XRaySource": [
        "Co Kα1",
        "Cu Kα1",
    ],
    "Unit": [
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
        "second",
        "ton",
        "week",
    ],
};
