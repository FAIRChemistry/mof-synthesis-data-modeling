from enum import Enum
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class Degassing(Enum):
    AR = "Ar"
    FPT = "FPT"


class Sample:
    id: str
    inchikey: Optional[str]
    inchistring: Optional[str]
    molecular_weight: Optional[float]
    name: str
    real_amount_unit: Optional[str]
    real_amount_value: Optional[float]
    short_label: Optional[str]
    target_amount_unit: Optional[str]
    target_amount_value: Optional[float]

    def __init__(self, id: str, inchikey: Optional[str], inchistring: Optional[str], molecular_weight: Optional[float], name: str, real_amount_unit: Optional[str], real_amount_value: Optional[float], short_label: Optional[str], target_amount_unit: Optional[str], target_amount_value: Optional[float]) -> None:
        self.id = id
        self.inchikey = inchikey
        self.inchistring = inchistring
        self.molecular_weight = molecular_weight
        self.name = name
        self.real_amount_unit = real_amount_unit
        self.real_amount_value = real_amount_value
        self.short_label = short_label
        self.target_amount_unit = target_amount_unit
        self.target_amount_value = target_amount_value

    @staticmethod
    def from_dict(obj: Any) -> 'Sample':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        inchikey = from_union([from_none, from_str], obj.get("inchikey"))
        inchistring = from_union([from_none, from_str], obj.get("inchistring"))
        molecular_weight = from_union([from_none, from_float], obj.get("molecular_weight"))
        name = from_str(obj.get("name"))
        real_amount_unit = from_union([from_none, from_str], obj.get("real_amount_unit"))
        real_amount_value = from_union([from_none, from_float], obj.get("real_amount_value"))
        short_label = from_union([from_none, from_str], obj.get("short_label"))
        target_amount_unit = from_union([from_none, from_str], obj.get("target_amount_unit"))
        target_amount_value = from_union([from_none, from_float], obj.get("target_amount_value"))
        return Sample(id, inchikey, inchistring, molecular_weight, name, real_amount_unit, real_amount_value, short_label, target_amount_unit, target_amount_value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["inchikey"] = from_union([from_none, from_str], self.inchikey)
        result["inchistring"] = from_union([from_none, from_str], self.inchistring)
        result["molecular_weight"] = from_union([from_none, to_float], self.molecular_weight)
        result["name"] = from_str(self.name)
        result["real_amount_unit"] = from_union([from_none, from_str], self.real_amount_unit)
        result["real_amount_value"] = from_union([from_none, to_float], self.real_amount_value)
        result["short_label"] = from_union([from_none, from_str], self.short_label)
        result["target_amount_unit"] = from_union([from_none, from_str], self.target_amount_unit)
        result["target_amount_value"] = from_union([from_none, to_float], self.target_amount_value)
        return result


class ProductElement:
    equivalent: Optional[float]
    position: Optional[int]
    reference: bool
    sample: Sample

    def __init__(self, equivalent: Optional[float], position: Optional[int], reference: bool, sample: Sample) -> None:
        self.equivalent = equivalent
        self.position = position
        self.reference = reference
        self.sample = sample

    @staticmethod
    def from_dict(obj: Any) -> 'ProductElement':
        assert isinstance(obj, dict)
        equivalent = from_union([from_none, from_float], obj.get("equivalent"))
        position = from_union([from_none, from_int], obj.get("position"))
        reference = from_bool(obj.get("reference"))
        sample = Sample.from_dict(obj.get("sample"))
        return ProductElement(equivalent, position, reference, sample)

    def to_dict(self) -> dict:
        result: dict = {}
        result["equivalent"] = from_union([from_none, to_float], self.equivalent)
        result["position"] = from_union([from_none, from_int], self.position)
        result["reference"] = from_bool(self.reference)
        result["sample"] = to_class(Sample, self.sample)
        return result


class Rinse(Enum):
    ACETONE = "acetone"
    CH_CL3 = "CHCl3"
    DIOXANE_NITROBENZENE = "dioxane/nitrobenzene"
    DMF = "DMF"
    ET3_N = "Et3N"
    ET_OH = "EtOH"
    ME_CN = "MeCN"
    ME_OH = "MeOH"
    NA_CL_AQ = "NaCl aq"


class TemperatureClass:
    data: List[Any]
    user_text: str
    value_unit: str

    def __init__(self, data: List[Any], user_text: str, value_unit: str) -> None:
        self.data = data
        self.user_text = user_text
        self.value_unit = value_unit

    @staticmethod
    def from_dict(obj: Any) -> 'TemperatureClass':
        assert isinstance(obj, dict)
        data = from_list(lambda x: x, obj.get("data"))
        user_text = from_str(obj.get("userText"))
        value_unit = from_str(obj.get("valueUnit"))
        return TemperatureClass(data, user_text, value_unit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(lambda x: x, self.data)
        result["userText"] = from_str(self.user_text)
        result["valueUnit"] = from_str(self.value_unit)
        return result


class Vessel(Enum):
    MICROWAVE_VIAL = "microwave vial"
    SCHLENK_BOMB = "Schlenk bomb"


class VesselSizeClass:
    amount: float
    unit: str

    def __init__(self, amount: float, unit: str) -> None:
        self.amount = amount
        self.unit = unit

    @staticmethod
    def from_dict(obj: Any) -> 'VesselSizeClass':
        assert isinstance(obj, dict)
        amount = from_float(obj.get("amount"))
        unit = from_str(obj.get("unit"))
        return VesselSizeClass(amount, unit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = to_float(self.amount)
        result["unit"] = from_str(self.unit)
        return result


class WaitAfterRinseUnit(Enum):
    H = "h"


class WashSolid(Enum):
    ME_OH_SC_CO2 = "MeOH+scCO2"
    SC_CO2 = "scCO2"


class ReactionElement:
    degassing: Optional[Degassing]
    duration: str
    evaporate: Optional[bool]
    id: str
    name: str
    plain_text_description: Optional[str]
    plain_text_observation: Optional[str]
    products: List[ProductElement]
    purification_solvents: List[ProductElement]
    rinse: Optional[List[Rinse]]
    short_label: str
    solvents: List[ProductElement]
    starting_materials: List[ProductElement]
    temperature: Optional[TemperatureClass]
    vessel: Optional[Vessel]
    vessel_size: Optional[VesselSizeClass]
    wait_after_rinse: Optional[float]
    wait_after_rinse_unit: Optional[WaitAfterRinseUnit]
    wash_solid: Optional[WashSolid]

    def __init__(self, degassing: Optional[Degassing], duration: str, evaporate: Optional[bool], id: str, name: str, plain_text_description: Optional[str], plain_text_observation: Optional[str], products: List[ProductElement], purification_solvents: List[ProductElement], rinse: Optional[List[Rinse]], short_label: str, solvents: List[ProductElement], starting_materials: List[ProductElement], temperature: Optional[TemperatureClass], vessel: Optional[Vessel], vessel_size: Optional[VesselSizeClass], wait_after_rinse: Optional[float], wait_after_rinse_unit: Optional[WaitAfterRinseUnit], wash_solid: Optional[WashSolid]) -> None:
        self.degassing = degassing
        self.duration = duration
        self.evaporate = evaporate
        self.id = id
        self.name = name
        self.plain_text_description = plain_text_description
        self.plain_text_observation = plain_text_observation
        self.products = products
        self.purification_solvents = purification_solvents
        self.rinse = rinse
        self.short_label = short_label
        self.solvents = solvents
        self.starting_materials = starting_materials
        self.temperature = temperature
        self.vessel = vessel
        self.vessel_size = vessel_size
        self.wait_after_rinse = wait_after_rinse
        self.wait_after_rinse_unit = wait_after_rinse_unit
        self.wash_solid = wash_solid

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionElement':
        assert isinstance(obj, dict)
        degassing = from_union([from_none, Degassing], obj.get("degassing"))
        duration = from_str(obj.get("duration"))
        evaporate = from_union([from_none, from_bool], obj.get("evaporate"))
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        plain_text_description = from_union([from_none, from_str], obj.get("plain_text_description"))
        plain_text_observation = from_union([from_none, from_str], obj.get("plain_text_observation"))
        products = from_list(ProductElement.from_dict, obj.get("products"))
        purification_solvents = from_list(ProductElement.from_dict, obj.get("purification_solvents"))
        rinse = from_union([lambda x: from_list(Rinse, x), from_none], obj.get("rinse"))
        short_label = from_str(obj.get("short_label"))
        solvents = from_list(ProductElement.from_dict, obj.get("solvents"))
        starting_materials = from_list(ProductElement.from_dict, obj.get("starting_materials"))
        temperature = from_union([TemperatureClass.from_dict, from_none], obj.get("temperature"))
        vessel = from_union([from_none, Vessel], obj.get("vessel"))
        vessel_size = from_union([VesselSizeClass.from_dict, from_none], obj.get("vessel_size"))
        wait_after_rinse = from_union([from_none, from_float], obj.get("wait_after_rinse"))
        wait_after_rinse_unit = from_union([from_none, WaitAfterRinseUnit], obj.get("wait_after_rinse_unit"))
        wash_solid = from_union([from_none, WashSolid], obj.get("wash_solid"))
        return ReactionElement(degassing, duration, evaporate, id, name, plain_text_description, plain_text_observation, products, purification_solvents, rinse, short_label, solvents, starting_materials, temperature, vessel, vessel_size, wait_after_rinse, wait_after_rinse_unit, wash_solid)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.degassing is not None:
            result["degassing"] = from_union([from_none, lambda x: to_enum(Degassing, x)], self.degassing)
        result["duration"] = from_str(self.duration)
        if self.evaporate is not None:
            result["evaporate"] = from_union([from_none, from_bool], self.evaporate)
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        result["plain_text_description"] = from_union([from_none, from_str], self.plain_text_description)
        result["plain_text_observation"] = from_union([from_none, from_str], self.plain_text_observation)
        result["products"] = from_list(lambda x: to_class(ProductElement, x), self.products)
        result["purification_solvents"] = from_list(lambda x: to_class(ProductElement, x), self.purification_solvents)
        if self.rinse is not None:
            result["rinse"] = from_union([lambda x: from_list(lambda x: to_enum(Rinse, x), x), from_none], self.rinse)
        result["short_label"] = from_str(self.short_label)
        result["solvents"] = from_list(lambda x: to_class(ProductElement, x), self.solvents)
        result["starting_materials"] = from_list(lambda x: to_class(ProductElement, x), self.starting_materials)
        result["temperature"] = from_union([lambda x: to_class(TemperatureClass, x), from_none], self.temperature)
        if self.vessel is not None:
            result["vessel"] = from_union([from_none, lambda x: to_enum(Vessel, x)], self.vessel)
        result["vessel_size"] = from_union([lambda x: to_class(VesselSizeClass, x), from_none], self.vessel_size)
        if self.wait_after_rinse is not None:
            result["wait_after_rinse"] = from_union([from_none, to_float], self.wait_after_rinse)
        if self.wait_after_rinse_unit is not None:
            result["wait_after_rinse_unit"] = from_union([from_none, lambda x: to_enum(WaitAfterRinseUnit, x)], self.wait_after_rinse_unit)
        if self.wash_solid is not None:
            result["wash_solid"] = from_union([from_none, lambda x: to_enum(WashSolid, x)], self.wash_solid)
        return result


class ChemotionEnrichedSchema:
    reactions: List[ReactionElement]

    def __init__(self, reactions: List[ReactionElement]) -> None:
        self.reactions = reactions

    @staticmethod
    def from_dict(obj: Any) -> 'ChemotionEnrichedSchema':
        assert isinstance(obj, dict)
        reactions = from_list(ReactionElement.from_dict, obj.get("reactions"))
        return ChemotionEnrichedSchema(reactions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reactions"] = from_list(lambda x: to_class(ReactionElement, x), self.reactions)
        return result


def chemotion_enriched_schema_from_dict(s: Any) -> ChemotionEnrichedSchema:
    return ChemotionEnrichedSchema.from_dict(s)


def chemotion_enriched_schema_to_dict(x: ChemotionEnrichedSchema) -> Any:
    return to_class(ChemotionEnrichedSchema, x)

