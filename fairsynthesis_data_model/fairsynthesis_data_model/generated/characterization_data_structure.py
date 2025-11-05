from enum import Enum
from typing import Optional, Any, List, TypeVar, Type, Callable, cast


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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


class Name(Enum):
    COF_366_CO = "COF-366-Co"
    MOCOF_1 = "MOCOF-1"
    UNKNOWN = "unknown"


class Component:
    crystalline_phases: Optional[str]
    molar_fraction: int
    """molar fraction of the component in percentage"""

    name: Name
    component_yield: Optional[int]
    """yield of the component in percentage"""

    def __init__(self, crystalline_phases: Optional[str], molar_fraction: int, name: Name, component_yield: Optional[int]) -> None:
        self.crystalline_phases = crystalline_phases
        self.molar_fraction = molar_fraction
        self.name = name
        self.component_yield = component_yield

    @staticmethod
    def from_dict(obj: Any) -> 'Component':
        assert isinstance(obj, dict)
        crystalline_phases = from_union([from_str, from_none], obj.get("CrystallinePhases"))
        molar_fraction = from_int(obj.get("Molar_fraction"))
        name = Name(obj.get("Name"))
        component_yield = from_union([from_int, from_none], obj.get("Yield"))
        return Component(crystalline_phases, molar_fraction, name, component_yield)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.crystalline_phases is not None:
            result["CrystallinePhases"] = from_union([from_str, from_none], self.crystalline_phases)
        result["Molar_fraction"] = from_int(self.molar_fraction)
        result["Name"] = to_enum(Name, self.name)
        if self.component_yield is not None:
            result["Yield"] = from_union([from_int, from_none], self.component_yield)
        return result


class AnalysisResults:
    components: Optional[List[Component]]

    def __init__(self, components: Optional[List[Component]]) -> None:
        self.components = components

    @staticmethod
    def from_dict(obj: Any) -> 'AnalysisResults':
        assert isinstance(obj, dict)
        components = from_union([lambda x: from_list(Component.from_dict, x), from_none], obj.get("Components"))
        return AnalysisResults(components)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.components is not None:
            result["Components"] = from_union([lambda x: from_list(lambda x: to_class(Component, x), x), from_none], self.components)
        return result


class Unit(Enum):
    CENTIMETER = "centimeter"
    GRAM = "gram"
    METER = "meter"
    MICROGRAM = "microgram"
    MILLIGRAM = "milligram"
    MILLIMETER = "millimeter"


class Quantity:
    unit: Unit
    value: float

    def __init__(self, unit: Unit, value: float) -> None:
        self.unit = unit
        self.value = value

    @staticmethod
    def from_dict(obj: Any) -> 'Quantity':
        assert isinstance(obj, dict)
        unit = Unit(obj.get("Unit"))
        value = from_float(obj.get("Value"))
        return Quantity(unit, value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Unit"] = to_enum(Unit, self.unit)
        result["Value"] = to_float(self.value)
        return result


class SampleHolderType(Enum):
    HILGENBERG_GLASS_NO_14__CAPILLARY = "HILGENBERG_GLASS_NO_14_CAPILLARY"
    KAPTON_FILMS = "KAPTON_FILMS"


class SampleHolder:
    diameter: Quantity
    type: SampleHolderType

    def __init__(self, diameter: Quantity, type: SampleHolderType) -> None:
        self.diameter = diameter
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'SampleHolder':
        assert isinstance(obj, dict)
        diameter = Quantity.from_dict(obj.get("Diameter"))
        type = SampleHolderType(obj.get("Type"))
        return SampleHolder(diameter, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Diameter"] = to_class(Quantity, self.diameter)
        result["Type"] = to_enum(SampleHolderType, self.type)
        return result


class XRaySource(Enum):
    CO_KΑ1 = "Co Kα1"
    CU_KΑ1 = "Cu Kα1"


class Pxrd:
    other_metadata: Optional[str]
    relative_file_path: str
    sample_holder: SampleHolder
    x_ray_source: XRaySource

    def __init__(self, other_metadata: Optional[str], relative_file_path: str, sample_holder: SampleHolder, x_ray_source: XRaySource) -> None:
        self.other_metadata = other_metadata
        self.relative_file_path = relative_file_path
        self.sample_holder = sample_holder
        self.x_ray_source = x_ray_source

    @staticmethod
    def from_dict(obj: Any) -> 'Pxrd':
        assert isinstance(obj, dict)
        other_metadata = from_union([from_str, from_none], obj.get("Other_metadata"))
        relative_file_path = from_str(obj.get("Relative_file_path"))
        sample_holder = SampleHolder.from_dict(obj.get("Sample_holder"))
        x_ray_source = XRaySource(obj.get("X-ray_source"))
        return Pxrd(other_metadata, relative_file_path, sample_holder, x_ray_source)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.other_metadata is not None:
            result["Other_metadata"] = from_union([from_str, from_none], self.other_metadata)
        result["Relative_file_path"] = from_str(self.relative_file_path)
        result["Sample_holder"] = to_class(SampleHolder, self.sample_holder)
        result["X-ray_source"] = to_enum(XRaySource, self.x_ray_source)
        return result


class Weighing:
    weight: Quantity

    def __init__(self, weight: Quantity) -> None:
        self.weight = weight

    @staticmethod
    def from_dict(obj: Any) -> 'Weighing':
        assert isinstance(obj, dict)
        weight = Quantity.from_dict(obj.get("Weight"))
        return Weighing(weight)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Weight"] = to_class(Quantity, self.weight)
        return result


class CharacterizationClass:
    pxrd: List[Pxrd]
    weight: List[Weighing]

    def __init__(self, pxrd: List[Pxrd], weight: List[Weighing]) -> None:
        self.pxrd = pxrd
        self.weight = weight

    @staticmethod
    def from_dict(obj: Any) -> 'CharacterizationClass':
        assert isinstance(obj, dict)
        pxrd = from_list(Pxrd.from_dict, obj.get("Pxrd"))
        weight = from_list(Weighing.from_dict, obj.get("Weight"))
        return CharacterizationClass(pxrd, weight)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Pxrd"] = from_list(lambda x: to_class(Pxrd, x), self.pxrd)
        result["Weight"] = from_list(lambda x: to_class(Weighing, x), self.weight)
        return result


class CharacterizationEntry:
    analysis_results: Optional[AnalysisResults]
    characterization: CharacterizationClass
    experiment_id: str

    def __init__(self, analysis_results: Optional[AnalysisResults], characterization: CharacterizationClass, experiment_id: str) -> None:
        self.analysis_results = analysis_results
        self.characterization = characterization
        self.experiment_id = experiment_id

    @staticmethod
    def from_dict(obj: Any) -> 'CharacterizationEntry':
        assert isinstance(obj, dict)
        analysis_results = from_union([AnalysisResults.from_dict, from_none], obj.get("AnalysisResults"))
        characterization = CharacterizationClass.from_dict(obj.get("Characterization"))
        experiment_id = from_str(obj.get("ExperimentId"))
        return CharacterizationEntry(analysis_results, characterization, experiment_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.analysis_results is not None:
            result["AnalysisResults"] = from_union([lambda x: to_class(AnalysisResults, x), from_none], self.analysis_results)
        result["Characterization"] = to_class(CharacterizationClass, self.characterization)
        result["ExperimentId"] = from_str(self.experiment_id)
        return result


class Characterization:
    """characterization data and analysis results of products from the MOF synthesis test cases"""

    product_characterization: List[CharacterizationEntry]

    def __init__(self, product_characterization: List[CharacterizationEntry]) -> None:
        self.product_characterization = product_characterization

    @staticmethod
    def from_dict(obj: Any) -> 'Characterization':
        assert isinstance(obj, dict)
        product_characterization = from_list(CharacterizationEntry.from_dict, obj.get("ProductCharacterization"))
        return Characterization(product_characterization)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ProductCharacterization"] = from_list(lambda x: to_class(CharacterizationEntry, x), self.product_characterization)
        return result


def characterization_from_dict(s: Any) -> Characterization:
    return Characterization.from_dict(s)


def characterization_to_dict(x: Characterization) -> Any:
    return to_class(Characterization, x)
