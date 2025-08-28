from enum import Enum
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Unit(Enum):
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
    SECOND = "second"
    TON = "ton"
    WEEK = "week"


class Quantity:
    unit: Optional[Unit]
    value: Optional[float]

    def __init__(self, unit: Optional[Unit], value: Optional[float]) -> None:
        self.unit = unit
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Quantity':
        assert isinstance(obj, dict)
        unit = from_union([Unit, from_none], obj.get("Unit"))
        value = from_union([from_float, from_none], obj.get("Value"))
        return Quantity(unit, value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.unit is not None:
            result["Unit"] = from_union([lambda x: to_enum(Unit, x), from_none], self.unit)
        if self.value is not None:
            result["Value"] = from_union([to_float, from_none], self.value)
        return result


class SampleHolder:
    diameter: Optional[Quantity]
    type: Optional[str]

    def __init__(self, diameter: Optional[Quantity], type: Optional[str]) -> None:
        self.diameter = diameter
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'SampleHolder':
        assert isinstance(obj, dict)
        diameter = from_union([Quantity.from_dict, from_none], obj.get("_diameter"))
        type = from_union([from_str, from_none], obj.get("_type"))
        return SampleHolder(diameter, type)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.diameter is not None:
            result["_diameter"] = from_union([lambda x: to_class(Quantity, x), from_none], self.diameter)
        if self.type is not None:
            result["_type"] = from_union([from_str, from_none], self.type)
        return result


class XRaySource(Enum):
    CO_KΑ1 = "Co Kα1"
    CU_KΑ1 = "Cu Kα1"


class Characterization:
    relative_file_path: Optional[str]
    x_ray_source: Optional[XRaySource]
    sample_holder: Optional[SampleHolder]
    weight: Optional[Quantity]
    purity: Optional[bool]

    def __init__(self, relative_file_path: Optional[str], x_ray_source: Optional[XRaySource], sample_holder: Optional[SampleHolder], weight: Optional[Quantity], purity: Optional[bool]) -> None:
        self.relative_file_path = relative_file_path
        self.x_ray_source = x_ray_source
        self.sample_holder = sample_holder
        self.weight = weight
        self.purity = purity

    @staticmethod
    def from_dict(obj: Any) -> 'Characterization':
        assert isinstance(obj, dict)
        relative_file_path = from_union([from_str, from_none], obj.get("_relative_file_path"))
        x_ray_source = from_union([XRaySource, from_none], obj.get("_x-ray_source"))
        sample_holder = from_union([SampleHolder.from_dict, from_none], obj.get("sample_holder"))
        weight = from_union([Quantity.from_dict, from_none], obj.get("_weight"))
        purity = from_union([from_bool, from_none], obj.get("_purity"))
        return Characterization(relative_file_path, x_ray_source, sample_holder, weight, purity)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.relative_file_path is not None:
            result["_relative_file_path"] = from_union([from_str, from_none], self.relative_file_path)
        if self.x_ray_source is not None:
            result["_x-ray_source"] = from_union([lambda x: to_enum(XRaySource, x), from_none], self.x_ray_source)
        if self.sample_holder is not None:
            result["sample_holder"] = from_union([lambda x: to_class(SampleHolder, x), from_none], self.sample_holder)
        if self.weight is not None:
            result["_weight"] = from_union([lambda x: to_class(Quantity, x), from_none], self.weight)
        if self.purity is not None:
            result["_purity"] = from_union([from_bool, from_none], self.purity)
        return result


class Metadata:
    description: str

    def __init__(self, description: str) -> None:
        self.description = description

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        assert isinstance(obj, dict)
        description = from_str(obj.get("_description"))
        return Metadata(description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_description"] = from_str(self.description)
        return result


class CharacterizationEntry:
    characterization: List[Characterization]
    metadata: Metadata

    def __init__(self, characterization: List[Characterization], metadata: Metadata) -> None:
        self.characterization = characterization
        self.metadata = metadata

    @staticmethod
    def from_dict(obj: Any) -> 'CharacterizationEntry':
        assert isinstance(obj, dict)
        characterization = from_list(Characterization.from_dict, obj.get("Characterization"))
        metadata = Metadata.from_dict(obj.get("Metadata"))
        return CharacterizationEntry(characterization, metadata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Characterization"] = from_list(lambda x: to_class(Characterization, x), self.characterization)
        result["Metadata"] = to_class(Metadata, self.metadata)
        return result


class ProductCharacterization:
    product_characterization: List[CharacterizationEntry]

    def __init__(self, product_characterization: List[CharacterizationEntry]) -> None:
        self.product_characterization = product_characterization

    @staticmethod
    def from_dict(obj: Any) -> 'ProductCharacterization':
        assert isinstance(obj, dict)
        product_characterization = from_list(CharacterizationEntry.from_dict, obj.get("ProductCharacterization"))
        return ProductCharacterization(product_characterization)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ProductCharacterization"] = from_list(lambda x: to_class(CharacterizationEntry, x), self.product_characterization)
        return result


def product_characterization_from_dict(s: Any) -> ProductCharacterization:
    return ProductCharacterization.from_dict(s)


def product_characterization_to_dict(x: ProductCharacterization) -> Any:
    return to_class(ProductCharacterization, x)
