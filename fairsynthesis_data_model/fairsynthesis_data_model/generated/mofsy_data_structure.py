from typing import Optional, Any, List, Union, TypeVar, Callable, Type, cast
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


class ComponentElement:
    chemical: Optional[str]
    comment: Optional[str]
    id: str
    type: Optional[str]

    def __init__(self, chemical: Optional[str], comment: Optional[str], id: str, type: Optional[str]) -> None:
        self.chemical = chemical
        self.comment = comment
        self.id = id
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'ComponentElement':
        assert isinstance(obj, dict)
        chemical = from_union([from_str, from_none], obj.get("_chemical"))
        comment = from_union([from_str, from_none], obj.get("_comment"))
        id = from_str(obj.get("_id"))
        type = from_union([from_str, from_none], obj.get("_type"))
        return ComponentElement(chemical, comment, id, type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.chemical is not None:
            result["_chemical"] = from_union([from_str, from_none], self.chemical)
        if self.comment is not None:
            result["_comment"] = from_union([from_str, from_none], self.comment)
        result["_id"] = from_str(self.id)
        if self.type is not None:
            result["_type"] = from_union([from_str, from_none], self.type)
        return result


class Hardware:
    component: Optional[List[ComponentElement]]

    def __init__(self, component: Optional[List[ComponentElement]]) -> None:
        self.component = component

    @staticmethod
    def from_dict(obj: Any) -> 'Hardware':
        assert isinstance(obj, dict)
        component = from_union([lambda x: from_list(ComponentElement.from_dict, x), from_none], obj.get("Component"))
        return Hardware(component)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.component is not None:
            result["Component"] = from_union([lambda x: from_list(lambda x: to_class(ComponentElement, x), x), from_none], self.component)
        return result


class Metadata:
    description: str
    product: Optional[str]
    product_inchi: Optional[str]

    def __init__(self, description: str, product: Optional[str], product_inchi: Optional[str]) -> None:
        self.description = description
        self.product = product
        self.product_inchi = product_inchi

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        assert isinstance(obj, dict)
        description = from_str(obj.get("_description"))
        product = from_union([from_str, from_none], obj.get("_product"))
        product_inchi = from_union([from_str, from_none], obj.get("_product_inchi"))
        return Metadata(description, product, product_inchi)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_description"] = from_str(self.description)
        if self.product is not None:
            result["_product"] = from_union([from_str, from_none], self.product)
        if self.product_inchi is not None:
            result["_product_inchi"] = from_union([from_str, from_none], self.product_inchi)
        return result


class Unit(Enum):
    BAR = "bar"
    CELSIUS = "celsius"
    CENTILITRE = "centilitre"
    CENTIMETER = "centimeter"
    DAY = "day"
    DECILITRE = "decilitre"
    DIMENSIONLESS = "dimensionless"
    GRAM = "gram"
    HOUR = "hour"
    ITEM = "item"
    KELVIN = "kelvin"
    KILOGRAM = "kilogram"
    LITRE = "litre"
    METER = "meter"
    MICROGRAM = "microgram"
    MICROLITRE = "microlitre"
    MICROMOLE = "micromole"
    MILLIGRAM = "milligram"
    MILLILITRE = "millilitre"
    MILLIMETER = "millimeter"
    MILLIMOLE = "millimole"
    MILLISECOND = "millisecond"
    MINUTE = "minute"
    MOLE = "mole"
    OHM = "ohm"
    PASCAL = "pascal"
    SECOND = "second"
    TON = "ton"
    WEEK = "week"


class Amount:
    unit: Optional[Unit]
    value: Optional[float]

    def __init__(self, unit: Optional[Unit], value: Optional[float]) -> None:
        self.unit = unit
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Amount':
        assert isinstance(obj, dict)
        unit = from_union([Unit, from_none], obj.get("Unit"))
        value = from_union([from_float, from_none], obj.get("Value"))
        return Amount(unit, value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.unit is not None:
            result["Unit"] = from_union([lambda x: to_enum(Unit, x), from_none], self.unit)
        if self.value is not None:
            result["Value"] = from_union([to_float, from_none], self.value)
        result["$xml_append"] = "${Value} ${Unit}"
        return result


class XMLType(Enum):
    ADD = "Add"
    DRY = "Dry"
    EVACUATE_AND_REFILL = "EvacuateAndRefill"
    EVAPORATE = "Evaporate"
    HEAT_CHILL = "HeatChill"
    SONICATE = "Sonicate"
    WAIT = "Wait"
    WASH_SOLID = "WashSolid"


class StepEntryClass:
    xml_type: Optional[XMLType]
    amount: Optional[Amount]
    comment: Optional[str]
    gas: Optional[str]
    pressure: Optional[Amount]
    reagent: Optional[str]
    solvent: Optional[str]
    stir: Optional[str]
    temp: Optional[Amount]
    time: Optional[Amount]
    vessel: Optional[str]

    def __init__(self, xml_type: Optional[XMLType], amount: Optional[Amount], comment: Optional[str], gas: Optional[str], pressure: Optional[Amount], reagent: Optional[str], solvent: Optional[str], stir: Optional[str], temp: Optional[Amount], time: Optional[Amount], vessel: Optional[str]) -> None:
        self.xml_type = xml_type
        self.amount = amount
        self.comment = comment
        self.gas = gas
        self.pressure = pressure
        self.reagent = reagent
        self.solvent = solvent
        self.stir = stir
        self.temp = temp
        self.time = time
        self.vessel = vessel

    @staticmethod
    def from_dict(obj: Any) -> 'StepEntryClass':
        assert isinstance(obj, dict)
        xml_type = from_union([XMLType, from_none], obj.get("$xml_type"))
        amount = from_union([Amount.from_dict, from_none], obj.get("_amount"))
        comment = from_union([from_str, from_none], obj.get("_comment"))
        gas = from_union([from_str, from_none], obj.get("_gas"))
        pressure = from_union([Amount.from_dict, from_none], obj.get("_pressure"))
        reagent = from_union([from_str, from_none], obj.get("_reagent"))
        solvent = from_union([from_str, from_none], obj.get("_solvent"))
        stir = from_union([from_str, from_none], obj.get("_stir"))
        temp = from_union([Amount.from_dict, from_none], obj.get("_temp"))
        time = from_union([Amount.from_dict, from_none], obj.get("_time"))
        vessel = from_union([from_str, from_none], obj.get("_vessel"))
        return StepEntryClass(xml_type, amount, comment, gas, pressure, reagent, solvent, stir, temp, time, vessel)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.xml_type is not None:
            result["$xml_type"] = from_union([lambda x: to_enum(XMLType, x), from_none], self.xml_type)
        if self.amount is not None:
            result["_amount"] = from_union([lambda x: to_class(Amount, x), from_none], self.amount)
        if self.comment is not None:
            result["_comment"] = from_union([from_str, from_none], self.comment)
        if self.gas is not None:
            result["_gas"] = from_union([from_str, from_none], self.gas)
        if self.pressure is not None:
            result["_pressure"] = from_union([lambda x: to_class(Amount, x), from_none], self.pressure)
        if self.reagent is not None:
            result["_reagent"] = from_union([from_str, from_none], self.reagent)
        if self.solvent is not None:
            result["_solvent"] = from_union([from_str, from_none], self.solvent)
        if self.stir is not None:
            result["_stir"] = from_union([from_str, from_none], self.stir)
        if self.temp is not None:
            result["_temp"] = from_union([lambda x: to_class(Amount, x), from_none], self.temp)
        if self.time is not None:
            result["_time"] = from_union([lambda x: to_class(Amount, x), from_none], self.time)
        if self.vessel is not None:
            result["_vessel"] = from_union([from_str, from_none], self.vessel)
        return result


class FlatProcedureClass:
    step: List[Optional[Union[float, int, bool, str, List[Any], StepEntryClass]]]

    def __init__(self, step: List[Optional[Union[float, int, bool, str, List[Any], StepEntryClass]]]) -> None:
        self.step = step

    @staticmethod
    def from_dict(obj: Any) -> 'FlatProcedureClass':
        assert isinstance(obj, dict)
        step = from_list(lambda x: from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), StepEntryClass.from_dict], x), obj.get("Step"))
        return FlatProcedureClass(step)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Step"] = from_list(lambda x: from_union([from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), lambda x: to_class(StepEntryClass, x)], x), self.step)
        return result


class Procedure:
    step: Optional[List[Optional[Union[float, int, bool, str, List[Any], StepEntryClass]]]]
    prep: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]
    reaction: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]
    workup: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]

    def __init__(self, step: Optional[List[Optional[Union[float, int, bool, str, List[Any], StepEntryClass]]]], prep: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]], reaction: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]], workup: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]) -> None:
        self.step = step
        self.prep = prep
        self.reaction = reaction
        self.workup = workup

    @staticmethod
    def from_dict(obj: Any) -> 'Procedure':
        assert isinstance(obj, dict)
        step = from_union([lambda x: from_list(lambda x: from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), StepEntryClass.from_dict], x), x), from_none], obj.get("Step"))
        prep = from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), FlatProcedureClass.from_dict], obj.get("Prep"))
        reaction = from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), FlatProcedureClass.from_dict], obj.get("Reaction"))
        workup = from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), FlatProcedureClass.from_dict], obj.get("Workup"))
        return Procedure(step, prep, reaction, workup)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.step is not None:
            result["Step"] = from_union([lambda x: from_list(lambda x: from_union([from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), lambda x: to_class(StepEntryClass, x)], x), x), from_none], self.step)
        if self.prep is not None:
            result["Prep"] = from_union([from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), lambda x: to_class(FlatProcedureClass, x)], self.prep)
        if self.reaction is not None:
            result["Reaction"] = from_union([from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), lambda x: to_class(FlatProcedureClass, x)], self.reaction)
        if self.workup is not None:
            result["Workup"] = from_union([from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x), lambda x: to_class(FlatProcedureClass, x)], self.workup)
        return result


class Role(Enum):
    ACID = "acid"
    ACTIVATING_AGENT = "activating-agent"
    BASE = "base"
    CATALYST = "catalyst"
    LIGAND = "ligand"
    QUENCHING_AGENT = "quenching-agent"
    REAGENT = "reagent"
    SOLVENT = "solvent"
    SUBSTRATE = "substrate"


class ReagentElement:
    cas: Optional[str]
    comment: Optional[str]
    id: Optional[str]
    inchi: Optional[str]
    name: Optional[str]
    purity: Optional[str]
    role: Optional[Role]

    def __init__(self, cas: Optional[str], comment: Optional[str], id: Optional[str], inchi: Optional[str], name: Optional[str], purity: Optional[str], role: Optional[Role]) -> None:
        self.cas = cas
        self.comment = comment
        self.id = id
        self.inchi = inchi
        self.name = name
        self.purity = purity
        self.role = role

    @staticmethod
    def from_dict(obj: Any) -> 'ReagentElement':
        assert isinstance(obj, dict)
        cas = from_union([from_str, from_none], obj.get("_cas"))
        comment = from_union([from_str, from_none], obj.get("_comment"))
        id = from_union([from_str, from_none], obj.get("_id"))
        inchi = from_union([from_str, from_none], obj.get("_inchi"))
        name = from_union([from_str, from_none], obj.get("_name"))
        purity = from_union([from_str, from_none], obj.get("_purity"))
        role = from_union([Role, from_none], obj.get("_role"))
        return ReagentElement(cas, comment, id, inchi, name, purity, role)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.cas is not None:
            result["_cas"] = from_union([from_str, from_none], self.cas)
        if self.comment is not None:
            result["_comment"] = from_union([from_str, from_none], self.comment)
        if self.id is not None:
            result["_id"] = from_union([from_str, from_none], self.id)
        if self.inchi is not None:
            result["_inchi"] = from_union([from_str, from_none], self.inchi)
        if self.name is not None:
            result["_name"] = from_union([from_str, from_none], self.name)
        if self.purity is not None:
            result["_purity"] = from_union([from_str, from_none], self.purity)
        if self.role is not None:
            result["_role"] = from_union([lambda x: to_enum(Role, x), from_none], self.role)
        return result


class Reagents:
    reagent: List[ReagentElement]

    def __init__(self, reagent: List[ReagentElement]) -> None:
        self.reagent = reagent

    @staticmethod
    def from_dict(obj: Any) -> 'Reagents':
        assert isinstance(obj, dict)
        reagent = from_list(ReagentElement.from_dict, obj.get("Reagent"))
        return Reagents(reagent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Reagent"] = from_list(lambda x: to_class(ReagentElement, x), self.reagent)
        return result


class SynthesisElement:
    hardware: Optional[Hardware]
    metadata: Metadata
    procedure: Procedure
    reagents: Reagents

    def __init__(self, hardware: Optional[Hardware], metadata: Metadata, procedure: Procedure, reagents: Reagents) -> None:
        self.hardware = hardware
        self.metadata = metadata
        self.procedure = procedure
        self.reagents = reagents

    @staticmethod
    def from_dict(obj: Any) -> 'SynthesisElement':
        assert isinstance(obj, dict)
        hardware = from_union([Hardware.from_dict, from_none], obj.get("Hardware"))
        metadata = Metadata.from_dict(obj.get("Metadata"))
        procedure = Procedure.from_dict(obj.get("Procedure"))
        reagents = Reagents.from_dict(obj.get("Reagents"))
        return SynthesisElement(hardware, metadata, procedure, reagents)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.hardware is not None:
            result["Hardware"] = from_union([lambda x: to_class(Hardware, x), from_none], self.hardware)
        result["Metadata"] = to_class(Metadata, self.metadata)
        result["Procedure"] = to_class(Procedure, self.procedure)
        result["Reagents"] = to_class(Reagents, self.reagents)
        return result


class Mofsy:
    synthesis: List[SynthesisElement]

    def __init__(self, synthesis: List[SynthesisElement]) -> None:
        self.synthesis = synthesis

    @staticmethod
    def from_dict(obj: Any) -> 'Mofsy':
        assert isinstance(obj, dict)
        synthesis = from_list(SynthesisElement.from_dict, obj.get("Synthesis"))
        return Mofsy(synthesis)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Synthesis"] = from_list(lambda x: to_class(SynthesisElement, x), self.synthesis)
        return result


def mofsy_from_dict(s: Any) -> Mofsy:
    return Mofsy.from_dict(s)


def mofsy_to_dict(x: Mofsy) -> Any:
    return to_class(Mofsy, x)
