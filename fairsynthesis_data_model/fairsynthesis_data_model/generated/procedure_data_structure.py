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
            result["Component"] = from_union(
                [lambda x: from_list(lambda x: to_class(ComponentElement, x), x), from_none], self.component)
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


class AmountUnit(Enum):
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


class Quantity:
    """amount of the involved chemical"""

    unit: Optional[AmountUnit]
    value: Optional[float]

    def __init__(self, unit: Optional[AmountUnit], value: Optional[float]) -> None:
        self.unit = unit
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Quantity':
        assert isinstance(obj, dict)
        unit = from_union([AmountUnit, from_none], obj.get("Unit"))
        value = from_union([from_float, from_none], obj.get("Value"))
        return Quantity(unit, value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.unit is not None:
            result["Unit"] = from_union([lambda x: to_enum(AmountUnit, x), from_none], self.unit)
        if self.value is not None:
            result["Value"] = from_union([to_float, from_none], self.value)
        result["$xml_append"] = "${Value} ${Unit}"
        return result


class Gas(Enum):
    AR = "Ar"


class PressureUnit(Enum):
    PASCAL = "pascal"


class Pressure:
    """amount of the involved chemical"""

    unit: Optional[PressureUnit]
    value: Optional[float]

    def __init__(self, unit: Optional[PressureUnit], value: Optional[float]) -> None:
        self.unit = unit
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Pressure':
        assert isinstance(obj, dict)
        unit = from_union([PressureUnit, from_none], obj.get("Unit"))
        value = from_union([from_float, from_none], obj.get("Value"))
        return Pressure(unit, value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.unit is not None:
            result["Unit"] = from_union([lambda x: to_enum(PressureUnit, x), from_none], self.unit)
        if self.value is not None:
            result["Value"] = from_union([to_float, from_none], self.value)
        result["$xml_append"] = "${Value} ${Unit}"
        return result


class Solvent(Enum):
    """name of the solvent in the case of WashSolid"""

    ACETONE = "acetone"
    CH_CL3 = "CHCl3"
    DMF = "DMF"
    ET3_N = "Et3N"
    ET_OH = "EtOH"
    ME_CN = "MeCN"
    ME_OH = "MeOH"
    ME_OH_SC_CO2 = "MeOH+scCO2"
    NA_CL_AQ = "NaCl aq"
    SC_CO2 = "scCO2"


class TempUnit(Enum):
    CELSIUS = "celsius"


class Empty:
    """temperature in the case of HeatChill

    amount of the involved chemical
    """
    unit: Optional[TempUnit]
    value: Optional[float]

    def __init__(self, unit: Optional[TempUnit], value: Optional[float]) -> None:
        self.unit = unit
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Empty':
        assert isinstance(obj, dict)
        unit = from_union([TempUnit, from_none], obj.get("Unit"))
        value = from_union([from_float, from_none], obj.get("Value"))
        return Empty(unit, value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.unit is not None:
            result["Unit"] = from_union([lambda x: to_enum(TempUnit, x), from_none], self.unit)
        if self.value is not None:
            result["Value"] = from_union([to_float, from_none], self.value)
        result["$xml_append"] = "${Value} ${Unit}"
        return result


class Time:
    """time of the step in the case of HeatChill, Wait, Sonicate, or Dry

    amount of the involved chemical
    """
    value: Optional[float]
    unit: Optional[AmountUnit]

    def __init__(self, value: Optional[float], unit: Optional[AmountUnit]) -> None:
        self.value = value
        self.unit = unit

    @staticmethod
    def from_dict(obj: Any) -> 'Time':
        assert isinstance(obj, dict)
        value = from_union([from_float, from_none], obj.get("Value"))
        unit = from_union([AmountUnit, from_none], obj.get("Unit"))
        return Time(value, unit)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.value is not None:
            result["Value"] = from_union([to_float, from_none], self.value)
        if self.unit is not None:
            result["Unit"] = from_union([lambda x: to_enum(AmountUnit, x), from_none], self.unit)
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
    comment: Optional[str]
    vessel: Optional[str]
    xml_type: XMLType
    amount: Optional[Quantity]
    """amount of the involved chemical"""

    reagent: Any
    """name of the involved chemical as listed in the "reagents\""""

    temp: Optional[Empty]
    """temperature in the case of HeatChill"""

    time: Optional[Time]
    """time of the step in the case of HeatChill, Wait, Sonicate, or Dry"""

    gas: Optional[Gas]
    """refilling gas in the case of EvacuateAndRefill"""

    solvent: Optional[Solvent]
    """name of the solvent in the case of WashSolid"""

    unknown: Any
    """Ken please add the corresponding attributes if existing"""

    pressure: Optional[Pressure]

    def __init__(self, comment: Optional[str], vessel: Optional[str], xml_type: XMLType, amount: Optional[Quantity],
                 reagent: Any, temp: Optional[Empty], time: Optional[Time], gas: Optional[Gas],
                 solvent: Optional[Solvent], unknown: Any, pressure: Optional[Pressure]) -> None:
        self.comment = comment
        self.vessel = vessel
        self.xml_type = xml_type
        self.amount = amount
        self.reagent = reagent
        self.temp = temp
        self.time = time
        self.gas = gas
        self.solvent = solvent
        self.unknown = unknown
        self.pressure = pressure

    @staticmethod
    def from_dict(obj: Any) -> 'StepEntryClass':
        assert isinstance(obj, dict)
        comment = from_union([from_str, from_none], obj.get("_comment"))
        vessel = from_union([from_str, from_none], obj.get("_vessel"))
        xml_type = XMLType(obj.get("$xml_type"))
        amount = from_union([Quantity.from_dict, from_none], obj.get("_amount"))
        reagent = obj.get("_reagent")
        temp = from_union([Empty.from_dict, from_none], obj.get("_temp"))
        time = from_union([Time.from_dict, from_none], obj.get("_time"))
        gas = from_union([Gas, from_none], obj.get("_gas"))
        solvent = from_union([Solvent, from_none], obj.get("_solvent"))
        unknown = obj.get("_unknown")
        pressure = from_union([Pressure.from_dict, from_none], obj.get("_pressure"))
        return StepEntryClass(comment, vessel, xml_type, amount, reagent, temp, time, gas, solvent, unknown, pressure)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.comment is not None:
            result["_comment"] = from_union([from_str, from_none], self.comment)
        if self.vessel is not None:
            result["_vessel"] = from_union([from_str, from_none], self.vessel)
        result["$xml_type"] = to_enum(XMLType, self.xml_type)
        if self.amount is not None:
            result["_amount"] = from_union([lambda x: to_class(Quantity, x), from_none], self.amount)
        if self.reagent is not None:
            result["_reagent"] = self.reagent
        if self.temp is not None:
            result["_temp"] = from_union([lambda x: to_class(Empty, x), from_none], self.temp)
        if self.time is not None:
            result["_time"] = from_union([lambda x: to_class(Time, x), from_none], self.time)
        if self.gas is not None:
            result["_gas"] = from_union([lambda x: to_enum(Gas, x), from_none], self.gas)
        if self.solvent is not None:
            result["_solvent"] = from_union([lambda x: to_enum(Solvent, x), from_none], self.solvent)
        if self.unknown is not None:
            result["_unknown"] = self.unknown
        if self.pressure is not None:
            result["_pressure"] = from_union([lambda x: to_class(Pressure, x), from_none], self.pressure)
        return result


class FlatProcedureClass:
    step: List[Optional[Union[float, int, bool, str, List[Any], StepEntryClass]]]

    def __init__(self, step: List[Optional[Union[float, int, bool, str, List[Any], StepEntryClass]]]) -> None:
        self.step = step

    @staticmethod
    def from_dict(obj: Any) -> 'FlatProcedureClass':
        assert isinstance(obj, dict)
        step = from_list(lambda x: from_union(
            [from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
             StepEntryClass.from_dict], x), obj.get("Step"))
        return FlatProcedureClass(step)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Step"] = from_list(lambda x: from_union(
            [from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
             lambda x: to_class(StepEntryClass, x)], x), self.step)
        return result


class ProcedureWithDifferentSectionsClass:
    prep: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]
    reaction: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]
    workup: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]

    def __init__(self, prep: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]],
                 reaction: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]],
                 workup: Optional[Union[float, int, bool, str, List[Any], FlatProcedureClass]]) -> None:
        self.prep = prep
        self.reaction = reaction
        self.workup = workup

    @staticmethod
    def from_dict(obj: Any) -> 'ProcedureWithDifferentSectionsClass':
        assert isinstance(obj, dict)
        prep = from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
                           FlatProcedureClass.from_dict], obj.get("Prep"))
        reaction = from_union(
            [from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
             FlatProcedureClass.from_dict], obj.get("Reaction"))
        workup = from_union([from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
                             FlatProcedureClass.from_dict], obj.get("Workup"))
        return ProcedureWithDifferentSectionsClass(prep, reaction, workup)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.prep is not None:
            result["Prep"] = from_union(
                [from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
                 lambda x: to_class(FlatProcedureClass, x)], self.prep)
        if self.reaction is not None:
            result["Reaction"] = from_union(
                [from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
                 lambda x: to_class(FlatProcedureClass, x)], self.reaction)
        if self.workup is not None:
            result["Workup"] = from_union(
                [from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
                 lambda x: to_class(FlatProcedureClass, x)], self.workup)
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

    def __init__(self, cas: Optional[str], comment: Optional[str], id: Optional[str], inchi: Optional[str],
                 name: Optional[str], purity: Optional[str], role: Optional[Role]) -> None:
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
    procedure: Optional[Union[float, int, bool, str, List[Any], ProcedureWithDifferentSectionsClass]]
    reagents: Reagents

    def __init__(self, hardware: Optional[Hardware], metadata: Metadata,
                 procedure: Optional[Union[float, int, bool, str, List[Any], ProcedureWithDifferentSectionsClass]],
                 reagents: Reagents) -> None:
        self.hardware = hardware
        self.metadata = metadata
        self.procedure = procedure
        self.reagents = reagents

    @staticmethod
    def from_dict(obj: Any) -> 'SynthesisElement':
        assert isinstance(obj, dict)
        hardware = from_union([Hardware.from_dict, from_none], obj.get("Hardware"))
        metadata = Metadata.from_dict(obj.get("Metadata"))
        procedure = from_union(
            [from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
             ProcedureWithDifferentSectionsClass.from_dict], obj.get("Procedure"))
        reagents = Reagents.from_dict(obj.get("Reagents"))
        return SynthesisElement(hardware, metadata, procedure, reagents)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.hardware is not None:
            result["Hardware"] = from_union([lambda x: to_class(Hardware, x), from_none], self.hardware)
        result["Metadata"] = to_class(Metadata, self.metadata)
        result["Procedure"] = from_union(
            [from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
             lambda x: to_class(ProcedureWithDifferentSectionsClass, x)], self.procedure)
        result["Reagents"] = to_class(Reagents, self.reagents)
        return result


class Procedure:
    synthesis: List[SynthesisElement]

    def __init__(self, synthesis: List[SynthesisElement]) -> None:
        self.synthesis = synthesis

    @staticmethod
    def from_dict(obj: Any) -> 'Procedure':
        assert isinstance(obj, dict)
        synthesis = from_list(SynthesisElement.from_dict, obj.get("Synthesis"))
        return Procedure(synthesis)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Synthesis"] = from_list(lambda x: to_class(SynthesisElement, x), self.synthesis)
        return result


def procedure_from_dict(s: Any) -> Procedure:
    return Procedure.from_dict(s)


def procedure_to_dict(x: Procedure) -> Any:
    return to_class(Procedure, x)
