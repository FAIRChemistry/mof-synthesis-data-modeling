from typing import Union, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Experiment:
    the_0__date: str
    the_0__vial_no: str
    the_1__metal_salt_mass: float
    the_1__metal_salt_mass_unit: str
    the_1__metal_salt_name: str
    the_2__linker_mass: float
    the_2__linker_mass_unit: str
    the_2__linker_name: str
    the_3__solvent: str
    the_3__solvent_amount: int
    the_3__solvent_unit: str
    the_4__modulator: Union[bool, str]
    the_4__modulator_amount: Union[int, str]
    the_4__modulator_unit: str
    the_5__sonicator_time: float
    the_5__sonicator_time_unit: str
    the_6__place: str
    the_6__reaction_time: int
    the_6__reaction_time_unit: str
    the_6__reaction_vessel: str
    the_6__temperature: int
    the_6__temperature_unit: str
    the_7__washing_solids: str
    the_8__activation_temperature: int
    the_8__activation_temperature_unit: str
    the_8__drying_solids: str
    the_8__drying_solids_time: int
    the_8__drying_time_unit: str
    the_9__mof: str
    the_9__phase_purity: bool

    def __init__(self, the_0__date: str, the_0__vial_no: str, the_1__metal_salt_mass: float, the_1__metal_salt_mass_unit: str, the_1__metal_salt_name: str, the_2__linker_mass: float, the_2__linker_mass_unit: str, the_2__linker_name: str, the_3__solvent: str, the_3__solvent_amount: int, the_3__solvent_unit: str, the_4__modulator: Union[bool, str], the_4__modulator_amount: Union[int, str], the_4__modulator_unit: str, the_5__sonicator_time: float, the_5__sonicator_time_unit: str, the_6__place: str, the_6__reaction_time: int, the_6__reaction_time_unit: str, the_6__reaction_vessel: str, the_6__temperature: int, the_6__temperature_unit: str, the_7__washing_solids: str, the_8__activation_temperature: int, the_8__activation_temperature_unit: str, the_8__drying_solids: str, the_8__drying_solids_time: int, the_8__drying_time_unit: str, the_9__mof: str, the_9__phase_purity: bool) -> None:
        self.the_0__date = the_0__date
        self.the_0__vial_no = the_0__vial_no
        self.the_1__metal_salt_mass = the_1__metal_salt_mass
        self.the_1__metal_salt_mass_unit = the_1__metal_salt_mass_unit
        self.the_1__metal_salt_name = the_1__metal_salt_name
        self.the_2__linker_mass = the_2__linker_mass
        self.the_2__linker_mass_unit = the_2__linker_mass_unit
        self.the_2__linker_name = the_2__linker_name
        self.the_3__solvent = the_3__solvent
        self.the_3__solvent_amount = the_3__solvent_amount
        self.the_3__solvent_unit = the_3__solvent_unit
        self.the_4__modulator = the_4__modulator
        self.the_4__modulator_amount = the_4__modulator_amount
        self.the_4__modulator_unit = the_4__modulator_unit
        self.the_5__sonicator_time = the_5__sonicator_time
        self.the_5__sonicator_time_unit = the_5__sonicator_time_unit
        self.the_6__place = the_6__place
        self.the_6__reaction_time = the_6__reaction_time
        self.the_6__reaction_time_unit = the_6__reaction_time_unit
        self.the_6__reaction_vessel = the_6__reaction_vessel
        self.the_6__temperature = the_6__temperature
        self.the_6__temperature_unit = the_6__temperature_unit
        self.the_7__washing_solids = the_7__washing_solids
        self.the_8__activation_temperature = the_8__activation_temperature
        self.the_8__activation_temperature_unit = the_8__activation_temperature_unit
        self.the_8__drying_solids = the_8__drying_solids
        self.the_8__drying_solids_time = the_8__drying_solids_time
        self.the_8__drying_time_unit = the_8__drying_time_unit
        self.the_9__mof = the_9__mof
        self.the_9__phase_purity = the_9__phase_purity

    @staticmethod
    def from_dict(obj: Any) -> 'Experiment':
        assert isinstance(obj, dict)
        the_0__date = from_str(obj.get("0_date"))
        the_0__vial_no = from_str(obj.get("0_vial_no"))
        the_1__metal_salt_mass = from_float(obj.get("1_metal_salt_mass"))
        the_1__metal_salt_mass_unit = from_str(obj.get("1_metal_salt_mass_unit"))
        the_1__metal_salt_name = from_str(obj.get("1_metal_salt_name"))
        the_2__linker_mass = from_float(obj.get("2_linker_mass"))
        the_2__linker_mass_unit = from_str(obj.get("2_linker_mass_unit"))
        the_2__linker_name = from_str(obj.get("2_linker_name"))
        the_3__solvent = from_str(obj.get("3_solvent"))
        the_3__solvent_amount = from_int(obj.get("3_solvent_amount"))
        the_3__solvent_unit = from_str(obj.get("3_solvent_unit"))
        the_4__modulator = from_union([from_bool, from_str], obj.get("4_modulator"))
        the_4__modulator_amount = from_union([from_int, from_str], obj.get("4_modulator_amount"))
        the_4__modulator_unit = from_str(obj.get("4_modulator_unit"))
        the_5__sonicator_time = from_float(obj.get("5_sonicator_time"))
        the_5__sonicator_time_unit = from_str(obj.get("5_sonicator_time_unit"))
        the_6__place = from_str(obj.get("6_place"))
        the_6__reaction_time = from_int(obj.get("6_reaction_time"))
        the_6__reaction_time_unit = from_str(obj.get("6_reaction_time_unit"))
        the_6__reaction_vessel = from_str(obj.get("6_reaction_vessel"))
        the_6__temperature = from_int(obj.get("6_temperature"))
        the_6__temperature_unit = from_str(obj.get("6_temperature_unit"))
        the_7__washing_solids = from_str(obj.get("7_washing_solids"))
        the_8__activation_temperature = from_int(obj.get("8_activation_temperature"))
        the_8__activation_temperature_unit = from_str(obj.get("8_activation_temperature_unit"))
        the_8__drying_solids = from_str(obj.get("8_drying_solids"))
        the_8__drying_solids_time = from_int(obj.get("8_drying_solids_time"))
        the_8__drying_time_unit = from_str(obj.get("8_drying_time_unit"))
        the_9__mof = from_str(obj.get("9_mof"))
        the_9__phase_purity = from_bool(obj.get("9_phase_purity"))
        return Experiment(the_0__date, the_0__vial_no, the_1__metal_salt_mass, the_1__metal_salt_mass_unit, the_1__metal_salt_name, the_2__linker_mass, the_2__linker_mass_unit, the_2__linker_name, the_3__solvent, the_3__solvent_amount, the_3__solvent_unit, the_4__modulator, the_4__modulator_amount, the_4__modulator_unit, the_5__sonicator_time, the_5__sonicator_time_unit, the_6__place, the_6__reaction_time, the_6__reaction_time_unit, the_6__reaction_vessel, the_6__temperature, the_6__temperature_unit, the_7__washing_solids, the_8__activation_temperature, the_8__activation_temperature_unit, the_8__drying_solids, the_8__drying_solids_time, the_8__drying_time_unit, the_9__mof, the_9__phase_purity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["0_date"] = from_str(self.the_0__date)
        result["0_vial_no"] = from_str(self.the_0__vial_no)
        result["1_metal_salt_mass"] = to_float(self.the_1__metal_salt_mass)
        result["1_metal_salt_mass_unit"] = from_str(self.the_1__metal_salt_mass_unit)
        result["1_metal_salt_name"] = from_str(self.the_1__metal_salt_name)
        result["2_linker_mass"] = to_float(self.the_2__linker_mass)
        result["2_linker_mass_unit"] = from_str(self.the_2__linker_mass_unit)
        result["2_linker_name"] = from_str(self.the_2__linker_name)
        result["3_solvent"] = from_str(self.the_3__solvent)
        result["3_solvent_amount"] = from_int(self.the_3__solvent_amount)
        result["3_solvent_unit"] = from_str(self.the_3__solvent_unit)
        result["4_modulator"] = from_union([from_bool, from_str], self.the_4__modulator)
        result["4_modulator_amount"] = from_union([from_int, from_str], self.the_4__modulator_amount)
        result["4_modulator_unit"] = from_str(self.the_4__modulator_unit)
        result["5_sonicator_time"] = to_float(self.the_5__sonicator_time)
        result["5_sonicator_time_unit"] = from_str(self.the_5__sonicator_time_unit)
        result["6_place"] = from_str(self.the_6__place)
        result["6_reaction_time"] = from_int(self.the_6__reaction_time)
        result["6_reaction_time_unit"] = from_str(self.the_6__reaction_time_unit)
        result["6_reaction_vessel"] = from_str(self.the_6__reaction_vessel)
        result["6_temperature"] = from_int(self.the_6__temperature)
        result["6_temperature_unit"] = from_str(self.the_6__temperature_unit)
        result["7_washing_solids"] = from_str(self.the_7__washing_solids)
        result["8_activation_temperature"] = from_int(self.the_8__activation_temperature)
        result["8_activation_temperature_unit"] = from_str(self.the_8__activation_temperature_unit)
        result["8_drying_solids"] = from_str(self.the_8__drying_solids)
        result["8_drying_solids_time"] = from_int(self.the_8__drying_solids_time)
        result["8_drying_time_unit"] = from_str(self.the_8__drying_time_unit)
        result["9_mof"] = from_str(self.the_9__mof)
        result["9_phase_purity"] = from_bool(self.the_9__phase_purity)
        return result


class Mil:
    esenmof: List[Experiment]

    def __init__(self, esenmof: List[Experiment]) -> None:
        self.esenmof = esenmof

    @staticmethod
    def from_dict(obj: Any) -> 'Mil':
        assert isinstance(obj, dict)
        esenmof = from_list(Experiment.from_dict, obj.get("esenmof"))
        return Mil(esenmof)

    def to_dict(self) -> dict:
        result: dict = {}
        result["esenmof"] = from_list(lambda x: to_class(Experiment, x), self.esenmof)
        return result


def mil_from_dict(s: Any) -> Mil:
    return Mil.from_dict(s)


def mil_to_dict(x: Mil) -> Any:
    return to_class(Mil, x)
