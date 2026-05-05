from typing import Optional, Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


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


class ReactionElement:
    duration: str
    id: str
    name: str
    plain_text_description: Optional[str]
    plain_text_observation: Optional[str]
    products: List[ProductElement]
    purification_solvents: List[ProductElement]
    short_label: str
    solvents: List[ProductElement]
    starting_materials: List[ProductElement]
    temperature: Optional[TemperatureClass]
    vessel_size: Optional[VesselSizeClass]

    def __init__(self, duration: str, id: str, name: str, plain_text_description: Optional[str], plain_text_observation: Optional[str], products: List[ProductElement], purification_solvents: List[ProductElement], short_label: str, solvents: List[ProductElement], starting_materials: List[ProductElement], temperature: Optional[TemperatureClass], vessel_size: Optional[VesselSizeClass]) -> None:
        self.duration = duration
        self.id = id
        self.name = name
        self.plain_text_description = plain_text_description
        self.plain_text_observation = plain_text_observation
        self.products = products
        self.purification_solvents = purification_solvents
        self.short_label = short_label
        self.solvents = solvents
        self.starting_materials = starting_materials
        self.temperature = temperature
        self.vessel_size = vessel_size

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionElement':
        assert isinstance(obj, dict)
        duration = from_str(obj.get("duration"))
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        plain_text_description = from_union([from_none, from_str], obj.get("plain_text_description"))
        plain_text_observation = from_union([from_none, from_str], obj.get("plain_text_observation"))
        products = from_list(ProductElement.from_dict, obj.get("products"))
        purification_solvents = from_list(ProductElement.from_dict, obj.get("purification_solvents"))
        short_label = from_str(obj.get("short_label"))
        solvents = from_list(ProductElement.from_dict, obj.get("solvents"))
        starting_materials = from_list(ProductElement.from_dict, obj.get("starting_materials"))
        temperature = from_union([TemperatureClass.from_dict, from_none], obj.get("temperature"))
        vessel_size = from_union([VesselSizeClass.from_dict, from_none], obj.get("vessel_size"))
        return ReactionElement(duration, id, name, plain_text_description, plain_text_observation, products, purification_solvents, short_label, solvents, starting_materials, temperature, vessel_size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["duration"] = from_str(self.duration)
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        result["plain_text_description"] = from_union([from_none, from_str], self.plain_text_description)
        result["plain_text_observation"] = from_union([from_none, from_str], self.plain_text_observation)
        result["products"] = from_list(lambda x: to_class(ProductElement, x), self.products)
        result["purification_solvents"] = from_list(lambda x: to_class(ProductElement, x), self.purification_solvents)
        result["short_label"] = from_str(self.short_label)
        result["solvents"] = from_list(lambda x: to_class(ProductElement, x), self.solvents)
        result["starting_materials"] = from_list(lambda x: to_class(ProductElement, x), self.starting_materials)
        result["temperature"] = from_union([lambda x: to_class(TemperatureClass, x), from_none], self.temperature)
        result["vessel_size"] = from_union([lambda x: to_class(VesselSizeClass, x), from_none], self.vessel_size)
        return result


class ChemotionCleanedSchema:
    reactions: List[ReactionElement]

    def __init__(self, reactions: List[ReactionElement]) -> None:
        self.reactions = reactions

    @staticmethod
    def from_dict(obj: Any) -> 'ChemotionCleanedSchema':
        assert isinstance(obj, dict)
        reactions = from_list(ReactionElement.from_dict, obj.get("reactions"))
        return ChemotionCleanedSchema(reactions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reactions"] = from_list(lambda x: to_class(ReactionElement, x), self.reactions)
        return result


def chemotion_cleaned_schema_from_dict(s: Any) -> ChemotionCleanedSchema:
    return ChemotionCleanedSchema.from_dict(s)


def chemotion_cleaned_schema_to_dict(x: ChemotionCleanedSchema) -> Any:
    return to_class(ChemotionCleanedSchema, x)

