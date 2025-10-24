from typing import Optional, Any, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Mocof1Param:
    acid_amount_umol: float
    acid_structure: str
    activation_under_vacuum: bool
    activation_with_sc_co2: bool
    aldehyde_monomer_amount_umol: float
    aldehyde_monomer_structure: str
    aminoporphyrin_monomer_amount_umol: float
    aminoporphyrin_monomer_source: str
    aminoporphyrin_monomer_type: str
    degassing: bool
    duration_h: float
    me_oh_in_sc_co2_activation: bool
    other_additives: Optional[str]
    solvent_1__name: str
    solvent_1__volume_u_l: float
    solvent_2__name: str
    solvent_2__volume_u_l: float
    temperature_c: float
    vessel: str
    water_amount_umol: float
    workup_with_na_cl: bool

    def __init__(self, acid_amount_umol: float, acid_structure: str, activation_under_vacuum: bool, activation_with_sc_co2: bool, aldehyde_monomer_amount_umol: float, aldehyde_monomer_structure: str, aminoporphyrin_monomer_amount_umol: float, aminoporphyrin_monomer_source: str, aminoporphyrin_monomer_type: str, degassing: bool, duration_h: float, me_oh_in_sc_co2_activation: bool, other_additives: Optional[str], solvent_1__name: str, solvent_1__volume_u_l: float, solvent_2__name: str, solvent_2__volume_u_l: float, temperature_c: float, vessel: str, water_amount_umol: float, workup_with_na_cl: bool) -> None:
        self.acid_amount_umol = acid_amount_umol
        self.acid_structure = acid_structure
        self.activation_under_vacuum = activation_under_vacuum
        self.activation_with_sc_co2 = activation_with_sc_co2
        self.aldehyde_monomer_amount_umol = aldehyde_monomer_amount_umol
        self.aldehyde_monomer_structure = aldehyde_monomer_structure
        self.aminoporphyrin_monomer_amount_umol = aminoporphyrin_monomer_amount_umol
        self.aminoporphyrin_monomer_source = aminoporphyrin_monomer_source
        self.aminoporphyrin_monomer_type = aminoporphyrin_monomer_type
        self.degassing = degassing
        self.duration_h = duration_h
        self.me_oh_in_sc_co2_activation = me_oh_in_sc_co2_activation
        self.other_additives = other_additives
        self.solvent_1__name = solvent_1__name
        self.solvent_1__volume_u_l = solvent_1__volume_u_l
        self.solvent_2__name = solvent_2__name
        self.solvent_2__volume_u_l = solvent_2__volume_u_l
        self.temperature_c = temperature_c
        self.vessel = vessel
        self.water_amount_umol = water_amount_umol
        self.workup_with_na_cl = workup_with_na_cl

    @staticmethod
    def from_dict(obj: Any) -> 'Mocof1Param':
        assert isinstance(obj, dict)
        acid_amount_umol = from_float(obj.get("acid_amount_umol"))
        acid_structure = from_str(obj.get("acid_structure"))
        activation_under_vacuum = from_bool(obj.get("activation_under_vacuum"))
        activation_with_sc_co2 = from_bool(obj.get("activation_with_scCO2"))
        aldehyde_monomer_amount_umol = from_float(obj.get("aldehyde_monomer_amount_umol"))
        aldehyde_monomer_structure = from_str(obj.get("aldehyde_monomer_structure"))
        aminoporphyrin_monomer_amount_umol = from_float(obj.get("aminoporphyrin_monomer_amount_umol"))
        aminoporphyrin_monomer_source = from_str(obj.get("aminoporphyrin_monomer_source"))
        aminoporphyrin_monomer_type = from_str(obj.get("aminoporphyrin_monomer_type"))
        degassing = from_bool(obj.get("degassing"))
        duration_h = from_float(obj.get("duration_h"))
        me_oh_in_sc_co2_activation = from_bool(obj.get("MeOH_in_scCO2_activation"))
        other_additives = from_union([from_none, from_str], obj.get("other_additives"))
        solvent_1__name = from_str(obj.get("solvent_1_name"))
        solvent_1__volume_u_l = from_float(obj.get("solvent_1_volume_uL"))
        solvent_2__name = from_str(obj.get("solvent_2_name"))
        solvent_2__volume_u_l = from_float(obj.get("solvent_2_volume_uL"))
        temperature_c = from_float(obj.get("temperature_C"))
        vessel = from_str(obj.get("vessel"))
        water_amount_umol = from_float(obj.get("water_amount_umol"))
        workup_with_na_cl = from_bool(obj.get("workup_with_NaCl"))
        return Mocof1Param(acid_amount_umol, acid_structure, activation_under_vacuum, activation_with_sc_co2, aldehyde_monomer_amount_umol, aldehyde_monomer_structure, aminoporphyrin_monomer_amount_umol, aminoporphyrin_monomer_source, aminoporphyrin_monomer_type, degassing, duration_h, me_oh_in_sc_co2_activation, other_additives, solvent_1__name, solvent_1__volume_u_l, solvent_2__name, solvent_2__volume_u_l, temperature_c, vessel, water_amount_umol, workup_with_na_cl)

    def to_dict(self) -> dict:
        result: dict = {}
        result["acid_amount_umol"] = to_float(self.acid_amount_umol)
        result["acid_structure"] = from_str(self.acid_structure)
        result["activation_under_vacuum"] = from_bool(self.activation_under_vacuum)
        result["activation_with_scCO2"] = from_bool(self.activation_with_sc_co2)
        result["aldehyde_monomer_amount_umol"] = to_float(self.aldehyde_monomer_amount_umol)
        result["aldehyde_monomer_structure"] = from_str(self.aldehyde_monomer_structure)
        result["aminoporphyrin_monomer_amount_umol"] = to_float(self.aminoporphyrin_monomer_amount_umol)
        result["aminoporphyrin_monomer_source"] = from_str(self.aminoporphyrin_monomer_source)
        result["aminoporphyrin_monomer_type"] = from_str(self.aminoporphyrin_monomer_type)
        result["degassing"] = from_bool(self.degassing)
        result["duration_h"] = to_float(self.duration_h)
        result["MeOH_in_scCO2_activation"] = from_bool(self.me_oh_in_sc_co2_activation)
        result["other_additives"] = from_union([from_none, from_str], self.other_additives)
        result["solvent_1_name"] = from_str(self.solvent_1__name)
        result["solvent_1_volume_uL"] = to_float(self.solvent_1__volume_u_l)
        result["solvent_2_name"] = from_str(self.solvent_2__name)
        result["solvent_2_volume_uL"] = to_float(self.solvent_2__volume_u_l)
        result["temperature_C"] = to_float(self.temperature_c)
        result["vessel"] = from_str(self.vessel)
        result["water_amount_umol"] = to_float(self.water_amount_umol)
        result["workup_with_NaCl"] = from_bool(self.workup_with_na_cl)
        return result


def mocof1_params_from_dict(s: Any) -> Dict[str, Mocof1Param]:
    return from_dict(Mocof1Param.from_dict, s)


def mocof1_params_to_dict(x: Dict[str, Mocof1Param]) -> Any:
    return from_dict(lambda x: to_class(Mocof1Param, x), x)
