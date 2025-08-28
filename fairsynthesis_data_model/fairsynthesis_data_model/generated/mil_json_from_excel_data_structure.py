from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Esenmofsynthesis:
    date: str
    linker_mass: int
    linker_mass_unit: str
    linker_name: str
    metal_salt_mass: int
    metal_salt_mass_unit: str
    metal_salt_name: str
    phase_purity: bool
    place: str
    solvent: str
    temperature: int
    temperature_unit: str
    time: int
    time_unit: str
    vial_no: str

    def __init__(self, date: str, linker_mass: int, linker_mass_unit: str, linker_name: str, metal_salt_mass: int, metal_salt_mass_unit: str, metal_salt_name: str, phase_purity: bool, place: str, solvent: str, temperature: int, temperature_unit: str, time: int, time_unit: str, vial_no: str) -> None:
        self.date = date
        self.linker_mass = linker_mass
        self.linker_mass_unit = linker_mass_unit
        self.linker_name = linker_name
        self.metal_salt_mass = metal_salt_mass
        self.metal_salt_mass_unit = metal_salt_mass_unit
        self.metal_salt_name = metal_salt_name
        self.phase_purity = phase_purity
        self.place = place
        self.solvent = solvent
        self.temperature = temperature
        self.temperature_unit = temperature_unit
        self.time = time
        self.time_unit = time_unit
        self.vial_no = vial_no

    @staticmethod
    def from_dict(obj: Any) -> 'Esenmofsynthesis':
        assert isinstance(obj, dict)
        date = from_str(obj.get("date"))
        linker_mass = from_int(obj.get("linker_mass"))
        linker_mass_unit = from_str(obj.get("linker_mass_unit"))
        linker_name = from_str(obj.get("linker_name"))
        metal_salt_mass = from_int(obj.get("metal_salt_mass"))
        metal_salt_mass_unit = from_str(obj.get("metal_salt_mass_unit"))
        metal_salt_name = from_str(obj.get("metal_salt_name"))
        phase_purity = from_bool(obj.get("phase_purity"))
        place = from_str(obj.get("place"))
        solvent = from_str(obj.get("solvent"))
        temperature = from_int(obj.get("temperature"))
        temperature_unit = from_str(obj.get("temperature_unit"))
        time = from_int(obj.get("time"))
        time_unit = from_str(obj.get("time_unit"))
        vial_no = from_str(obj.get("vial_no"))
        return Esenmofsynthesis(date, linker_mass, linker_mass_unit, linker_name, metal_salt_mass, metal_salt_mass_unit, metal_salt_name, phase_purity, place, solvent, temperature, temperature_unit, time, time_unit, vial_no)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_str(self.date)
        result["linker_mass"] = from_int(self.linker_mass)
        result["linker_mass_unit"] = from_str(self.linker_mass_unit)
        result["linker_name"] = from_str(self.linker_name)
        result["metal_salt_mass"] = from_int(self.metal_salt_mass)
        result["metal_salt_mass_unit"] = from_str(self.metal_salt_mass_unit)
        result["metal_salt_name"] = from_str(self.metal_salt_name)
        result["phase_purity"] = from_bool(self.phase_purity)
        result["place"] = from_str(self.place)
        result["solvent"] = from_str(self.solvent)
        result["temperature"] = from_int(self.temperature)
        result["temperature_unit"] = from_str(self.temperature_unit)
        result["time"] = from_int(self.time)
        result["time_unit"] = from_str(self.time_unit)
        result["vial_no"] = from_str(self.vial_no)
        return result


class Mil:
    esenmofsynthesis: List[Esenmofsynthesis]

    def __init__(self, esenmofsynthesis: List[Esenmofsynthesis]) -> None:
        self.esenmofsynthesis = esenmofsynthesis

    @staticmethod
    def from_dict(obj: Any) -> 'Mil':
        assert isinstance(obj, dict)
        esenmofsynthesis = from_list(Esenmofsynthesis.from_dict, obj.get("esenmofsynthesis"))
        return Mil(esenmofsynthesis)

    def to_dict(self) -> dict:
        result: dict = {}
        result["esenmofsynthesis"] = from_list(lambda x: to_class(Esenmofsynthesis, x), self.esenmofsynthesis)
        return result


def mil_from_dict(s: Any) -> Mil:
    return Mil.from_dict(s)


def mil_to_dict(x: Mil) -> Any:
    return to_class(Mil, x)
