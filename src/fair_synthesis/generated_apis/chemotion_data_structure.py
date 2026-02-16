from typing import Optional, Any, List, Dict, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


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


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Collection:
    ancestry: Optional[str]
    created_at: Optional[datetime]
    deleted_at: None
    is_locked: Optional[bool]
    is_shared: Optional[bool]
    is_synchronized: Optional[bool]
    label: Optional[str]
    permission_level: Optional[int]
    position: Optional[int]
    reaction_detail_level: Optional[int]
    researchplan_detail_level: Optional[int]
    sample_detail_level: Optional[int]
    screen_detail_level: Optional[int]
    shared_by_id: Optional[str]
    updated_at: Optional[datetime]
    user_id: Optional[str]
    wellplate_detail_level: Optional[int]

    def __init__(self, ancestry: Optional[str], created_at: Optional[datetime], deleted_at: None, is_locked: Optional[bool], is_shared: Optional[bool], is_synchronized: Optional[bool], label: Optional[str], permission_level: Optional[int], position: Optional[int], reaction_detail_level: Optional[int], researchplan_detail_level: Optional[int], sample_detail_level: Optional[int], screen_detail_level: Optional[int], shared_by_id: Optional[str], updated_at: Optional[datetime], user_id: Optional[str], wellplate_detail_level: Optional[int]) -> None:
        self.ancestry = ancestry
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.is_locked = is_locked
        self.is_shared = is_shared
        self.is_synchronized = is_synchronized
        self.label = label
        self.permission_level = permission_level
        self.position = position
        self.reaction_detail_level = reaction_detail_level
        self.researchplan_detail_level = researchplan_detail_level
        self.sample_detail_level = sample_detail_level
        self.screen_detail_level = screen_detail_level
        self.shared_by_id = shared_by_id
        self.updated_at = updated_at
        self.user_id = user_id
        self.wellplate_detail_level = wellplate_detail_level

    @staticmethod
    def from_dict(obj: Any) -> 'Collection':
        assert isinstance(obj, dict)
        ancestry = from_union([from_str, from_none], obj.get("ancestry"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deleted_at = from_none(obj.get("deleted_at"))
        is_locked = from_union([from_bool, from_none], obj.get("is_locked"))
        is_shared = from_union([from_bool, from_none], obj.get("is_shared"))
        is_synchronized = from_union([from_bool, from_none], obj.get("is_synchronized"))
        label = from_union([from_str, from_none], obj.get("label"))
        permission_level = from_union([from_int, from_none], obj.get("permission_level"))
        position = from_union([from_int, from_none], obj.get("position"))
        reaction_detail_level = from_union([from_int, from_none], obj.get("reaction_detail_level"))
        researchplan_detail_level = from_union([from_int, from_none], obj.get("researchplan_detail_level"))
        sample_detail_level = from_union([from_int, from_none], obj.get("sample_detail_level"))
        screen_detail_level = from_union([from_int, from_none], obj.get("screen_detail_level"))
        shared_by_id = from_union([from_none, from_str], obj.get("shared_by_id"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        user_id = from_union([from_none, from_str], obj.get("user_id"))
        wellplate_detail_level = from_union([from_int, from_none], obj.get("wellplate_detail_level"))
        return Collection(ancestry, created_at, deleted_at, is_locked, is_shared, is_synchronized, label, permission_level, position, reaction_detail_level, researchplan_detail_level, sample_detail_level, screen_detail_level, shared_by_id, updated_at, user_id, wellplate_detail_level)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ancestry is not None:
            result["ancestry"] = from_union([from_str, from_none], self.ancestry)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.is_locked is not None:
            result["is_locked"] = from_union([from_bool, from_none], self.is_locked)
        if self.is_shared is not None:
            result["is_shared"] = from_union([from_bool, from_none], self.is_shared)
        if self.is_synchronized is not None:
            result["is_synchronized"] = from_union([from_bool, from_none], self.is_synchronized)
        if self.label is not None:
            result["label"] = from_union([from_str, from_none], self.label)
        if self.permission_level is not None:
            result["permission_level"] = from_union([from_int, from_none], self.permission_level)
        if self.position is not None:
            result["position"] = from_union([from_int, from_none], self.position)
        if self.reaction_detail_level is not None:
            result["reaction_detail_level"] = from_union([from_int, from_none], self.reaction_detail_level)
        if self.researchplan_detail_level is not None:
            result["researchplan_detail_level"] = from_union([from_int, from_none], self.researchplan_detail_level)
        if self.sample_detail_level is not None:
            result["sample_detail_level"] = from_union([from_int, from_none], self.sample_detail_level)
        if self.screen_detail_level is not None:
            result["screen_detail_level"] = from_union([from_int, from_none], self.screen_detail_level)
        if self.shared_by_id is not None:
            result["shared_by_id"] = from_union([from_none, from_str], self.shared_by_id)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.user_id is not None:
            result["user_id"] = from_union([from_none, from_str], self.user_id)
        if self.wellplate_detail_level is not None:
            result["wellplate_detail_level"] = from_union([from_int, from_none], self.wellplate_detail_level)
        return result


class CollectionsReaction:
    collection_id: Optional[str]
    deleted_at: None
    reaction_id: Optional[str]

    def __init__(self, collection_id: Optional[str], deleted_at: None, reaction_id: Optional[str]) -> None:
        self.collection_id = collection_id
        self.deleted_at = deleted_at
        self.reaction_id = reaction_id

    @staticmethod
    def from_dict(obj: Any) -> 'CollectionsReaction':
        assert isinstance(obj, dict)
        collection_id = from_union([from_none, from_str], obj.get("collection_id"))
        deleted_at = from_none(obj.get("deleted_at"))
        reaction_id = from_union([from_none, from_str], obj.get("reaction_id"))
        return CollectionsReaction(collection_id, deleted_at, reaction_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.collection_id is not None:
            result["collection_id"] = from_union([from_none, from_str], self.collection_id)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.reaction_id is not None:
            result["reaction_id"] = from_union([from_none, from_str], self.reaction_id)
        return result


class CollectionsSample:
    collection_id: Optional[str]
    deleted_at: None
    sample_id: Optional[str]

    def __init__(self, collection_id: Optional[str], deleted_at: None, sample_id: Optional[str]) -> None:
        self.collection_id = collection_id
        self.deleted_at = deleted_at
        self.sample_id = sample_id

    @staticmethod
    def from_dict(obj: Any) -> 'CollectionsSample':
        assert isinstance(obj, dict)
        collection_id = from_union([from_none, from_str], obj.get("collection_id"))
        deleted_at = from_none(obj.get("deleted_at"))
        sample_id = from_union([from_none, from_str], obj.get("sample_id"))
        return CollectionsSample(collection_id, deleted_at, sample_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.collection_id is not None:
            result["collection_id"] = from_union([from_none, from_str], self.collection_id)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.sample_id is not None:
            result["sample_id"] = from_union([from_none, from_str], self.sample_id)
        return result


class CollectionsWellplate:
    collection_id: Optional[str]
    deleted_at: None
    wellplate_id: Optional[str]

    def __init__(self, collection_id: Optional[str], deleted_at: None, wellplate_id: Optional[str]) -> None:
        self.collection_id = collection_id
        self.deleted_at = deleted_at
        self.wellplate_id = wellplate_id

    @staticmethod
    def from_dict(obj: Any) -> 'CollectionsWellplate':
        assert isinstance(obj, dict)
        collection_id = from_union([from_none, from_str], obj.get("collection_id"))
        deleted_at = from_none(obj.get("deleted_at"))
        wellplate_id = from_union([from_none, from_str], obj.get("wellplate_id"))
        return CollectionsWellplate(collection_id, deleted_at, wellplate_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.collection_id is not None:
            result["collection_id"] = from_union([from_none, from_str], self.collection_id)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.wellplate_id is not None:
            result["wellplate_id"] = from_union([from_none, from_str], self.wellplate_id)
        return result


class Fingerprint:
    created_at: Optional[datetime]
    deleted_at: None
    fp0: Optional[str]
    fp1: Optional[str]
    fp10: Optional[str]
    fp11: Optional[str]
    fp12: Optional[str]
    fp13: Optional[str]
    fp14: Optional[str]
    fp15: Optional[str]
    fp2: Optional[str]
    fp3: Optional[str]
    fp4: Optional[str]
    fp5: Optional[str]
    fp6: Optional[str]
    fp7: Optional[str]
    fp8: Optional[str]
    fp9: Optional[str]
    num_set_bits: Optional[int]
    updated_at: Optional[datetime]

    def __init__(self, created_at: Optional[datetime], deleted_at: None, fp0: Optional[str], fp1: Optional[str], fp10: Optional[str], fp11: Optional[str], fp12: Optional[str], fp13: Optional[str], fp14: Optional[str], fp15: Optional[str], fp2: Optional[str], fp3: Optional[str], fp4: Optional[str], fp5: Optional[str], fp6: Optional[str], fp7: Optional[str], fp8: Optional[str], fp9: Optional[str], num_set_bits: Optional[int], updated_at: Optional[datetime]) -> None:
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.fp0 = fp0
        self.fp1 = fp1
        self.fp10 = fp10
        self.fp11 = fp11
        self.fp12 = fp12
        self.fp13 = fp13
        self.fp14 = fp14
        self.fp15 = fp15
        self.fp2 = fp2
        self.fp3 = fp3
        self.fp4 = fp4
        self.fp5 = fp5
        self.fp6 = fp6
        self.fp7 = fp7
        self.fp8 = fp8
        self.fp9 = fp9
        self.num_set_bits = num_set_bits
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Fingerprint':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deleted_at = from_none(obj.get("deleted_at"))
        fp0 = from_union([from_str, from_none], obj.get("fp0"))
        fp1 = from_union([from_str, from_none], obj.get("fp1"))
        fp10 = from_union([from_str, from_none], obj.get("fp10"))
        fp11 = from_union([from_str, from_none], obj.get("fp11"))
        fp12 = from_union([from_str, from_none], obj.get("fp12"))
        fp13 = from_union([from_str, from_none], obj.get("fp13"))
        fp14 = from_union([from_str, from_none], obj.get("fp14"))
        fp15 = from_union([from_str, from_none], obj.get("fp15"))
        fp2 = from_union([from_str, from_none], obj.get("fp2"))
        fp3 = from_union([from_str, from_none], obj.get("fp3"))
        fp4 = from_union([from_str, from_none], obj.get("fp4"))
        fp5 = from_union([from_str, from_none], obj.get("fp5"))
        fp6 = from_union([from_str, from_none], obj.get("fp6"))
        fp7 = from_union([from_str, from_none], obj.get("fp7"))
        fp8 = from_union([from_str, from_none], obj.get("fp8"))
        fp9 = from_union([from_str, from_none], obj.get("fp9"))
        num_set_bits = from_union([from_int, from_none], obj.get("num_set_bits"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        return Fingerprint(created_at, deleted_at, fp0, fp1, fp10, fp11, fp12, fp13, fp14, fp15, fp2, fp3, fp4, fp5, fp6, fp7, fp8, fp9, num_set_bits, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.fp0 is not None:
            result["fp0"] = from_union([from_str, from_none], self.fp0)
        if self.fp1 is not None:
            result["fp1"] = from_union([from_str, from_none], self.fp1)
        if self.fp10 is not None:
            result["fp10"] = from_union([from_str, from_none], self.fp10)
        if self.fp11 is not None:
            result["fp11"] = from_union([from_str, from_none], self.fp11)
        if self.fp12 is not None:
            result["fp12"] = from_union([from_str, from_none], self.fp12)
        if self.fp13 is not None:
            result["fp13"] = from_union([from_str, from_none], self.fp13)
        if self.fp14 is not None:
            result["fp14"] = from_union([from_str, from_none], self.fp14)
        if self.fp15 is not None:
            result["fp15"] = from_union([from_str, from_none], self.fp15)
        if self.fp2 is not None:
            result["fp2"] = from_union([from_str, from_none], self.fp2)
        if self.fp3 is not None:
            result["fp3"] = from_union([from_str, from_none], self.fp3)
        if self.fp4 is not None:
            result["fp4"] = from_union([from_str, from_none], self.fp4)
        if self.fp5 is not None:
            result["fp5"] = from_union([from_str, from_none], self.fp5)
        if self.fp6 is not None:
            result["fp6"] = from_union([from_str, from_none], self.fp6)
        if self.fp7 is not None:
            result["fp7"] = from_union([from_str, from_none], self.fp7)
        if self.fp8 is not None:
            result["fp8"] = from_union([from_str, from_none], self.fp8)
        if self.fp9 is not None:
            result["fp9"] = from_union([from_str, from_none], self.fp9)
        if self.num_set_bits is not None:
            result["num_set_bits"] = from_union([from_int, from_none], self.num_set_bits)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        return result


class Molecule:
    boiling_point: Optional[float]
    cano_smiles: Optional[str]
    cas: Optional[List[Any]]
    created_at: Optional[datetime]
    deleted_at: None
    density: Optional[float]
    exact_molecular_weight: Optional[float]
    inchikey: Optional[str]
    inchistring: Optional[str]
    is_partial: Optional[bool]
    iupac_name: Optional[str]
    melting_point: Optional[float]
    molecular_weight: Optional[float]
    molecule_svg_file: Optional[str]
    molfile: Optional[str]
    molfile_version: Optional[str]
    names: Optional[List[Any]]
    sum_formular: Optional[str]
    updated_at: Optional[datetime]

    def __init__(self, boiling_point: Optional[float], cano_smiles: Optional[str], cas: Optional[List[Any]], created_at: Optional[datetime], deleted_at: None, density: Optional[float], exact_molecular_weight: Optional[float], inchikey: Optional[str], inchistring: Optional[str], is_partial: Optional[bool], iupac_name: Optional[str], melting_point: Optional[float], molecular_weight: Optional[float], molecule_svg_file: Optional[str], molfile: Optional[str], molfile_version: Optional[str], names: Optional[List[Any]], sum_formular: Optional[str], updated_at: Optional[datetime]) -> None:
        self.boiling_point = boiling_point
        self.cano_smiles = cano_smiles
        self.cas = cas
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.density = density
        self.exact_molecular_weight = exact_molecular_weight
        self.inchikey = inchikey
        self.inchistring = inchistring
        self.is_partial = is_partial
        self.iupac_name = iupac_name
        self.melting_point = melting_point
        self.molecular_weight = molecular_weight
        self.molecule_svg_file = molecule_svg_file
        self.molfile = molfile
        self.molfile_version = molfile_version
        self.names = names
        self.sum_formular = sum_formular
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Molecule':
        assert isinstance(obj, dict)
        boiling_point = from_union([from_none, from_float], obj.get("boiling_point"))
        cano_smiles = from_union([from_str, from_none], obj.get("cano_smiles"))
        cas = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("cas"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deleted_at = from_none(obj.get("deleted_at"))
        density = from_union([from_none, from_float], obj.get("density"))
        exact_molecular_weight = from_union([from_none, from_float], obj.get("exact_molecular_weight"))
        inchikey = from_union([from_str, from_none], obj.get("inchikey"))
        inchistring = from_union([from_str, from_none], obj.get("inchistring"))
        is_partial = from_union([from_bool, from_none], obj.get("is_partial"))
        iupac_name = from_union([from_str, from_none], obj.get("iupac_name"))
        melting_point = from_union([from_none, from_float], obj.get("melting_point"))
        molecular_weight = from_union([from_none, from_float], obj.get("molecular_weight"))
        molecule_svg_file = from_union([from_str, from_none], obj.get("molecule_svg_file"))
        molfile = from_union([from_str, from_none], obj.get("molfile"))
        molfile_version = from_union([from_str, from_none], obj.get("molfile_version"))
        names = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("names"))
        sum_formular = from_union([from_str, from_none], obj.get("sum_formular"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        return Molecule(boiling_point, cano_smiles, cas, created_at, deleted_at, density, exact_molecular_weight, inchikey, inchistring, is_partial, iupac_name, melting_point, molecular_weight, molecule_svg_file, molfile, molfile_version, names, sum_formular, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.boiling_point is not None:
            result["boiling_point"] = from_union([from_none, to_float], self.boiling_point)
        if self.cano_smiles is not None:
            result["cano_smiles"] = from_union([from_str, from_none], self.cano_smiles)
        if self.cas is not None:
            result["cas"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.cas)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.density is not None:
            result["density"] = from_union([from_none, to_float], self.density)
        if self.exact_molecular_weight is not None:
            result["exact_molecular_weight"] = from_union([from_none, to_float], self.exact_molecular_weight)
        if self.inchikey is not None:
            result["inchikey"] = from_union([from_str, from_none], self.inchikey)
        if self.inchistring is not None:
            result["inchistring"] = from_union([from_str, from_none], self.inchistring)
        if self.is_partial is not None:
            result["is_partial"] = from_union([from_bool, from_none], self.is_partial)
        if self.iupac_name is not None:
            result["iupac_name"] = from_union([from_str, from_none], self.iupac_name)
        if self.melting_point is not None:
            result["melting_point"] = from_union([from_none, to_float], self.melting_point)
        if self.molecular_weight is not None:
            result["molecular_weight"] = from_union([from_none, to_float], self.molecular_weight)
        if self.molecule_svg_file is not None:
            result["molecule_svg_file"] = from_union([from_str, from_none], self.molecule_svg_file)
        if self.molfile is not None:
            result["molfile"] = from_union([from_str, from_none], self.molfile)
        if self.molfile_version is not None:
            result["molfile_version"] = from_union([from_str, from_none], self.molfile_version)
        if self.names is not None:
            result["names"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.names)
        if self.sum_formular is not None:
            result["sum_formular"] = from_union([from_str, from_none], self.sum_formular)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        return result


class MoleculeName:
    created_at: Optional[datetime]
    deleted_at: None
    description: Optional[str]
    molecule_id: Optional[str]
    name: Optional[str]
    updated_at: Optional[datetime]
    user_id: Optional[str]

    def __init__(self, created_at: Optional[datetime], deleted_at: None, description: Optional[str], molecule_id: Optional[str], name: Optional[str], updated_at: Optional[datetime], user_id: Optional[str]) -> None:
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.description = description
        self.molecule_id = molecule_id
        self.name = name
        self.updated_at = updated_at
        self.user_id = user_id

    @staticmethod
    def from_dict(obj: Any) -> 'MoleculeName':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deleted_at = from_none(obj.get("deleted_at"))
        description = from_union([from_str, from_none], obj.get("description"))
        molecule_id = from_union([from_none, from_str], obj.get("molecule_id"))
        name = from_union([from_str, from_none], obj.get("name"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        user_id = from_union([from_none, from_str], obj.get("user_id"))
        return MoleculeName(created_at, deleted_at, description, molecule_id, name, updated_at, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.molecule_id is not None:
            result["molecule_id"] = from_union([from_none, from_str], self.molecule_id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.user_id is not None:
            result["user_id"] = from_union([from_none, from_str], self.user_id)
        return result


class ReactionDescription:
    ops: Optional[List[Any]]

    def __init__(self, ops: Optional[List[Any]]) -> None:
        self.ops = ops

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionDescription':
        assert isinstance(obj, dict)
        ops = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("ops"))
        return ReactionDescription(ops)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ops is not None:
            result["ops"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.ops)
        return result


class Observation:
    ops: Optional[List[Any]]

    def __init__(self, ops: Optional[List[Any]]) -> None:
        self.ops = ops

    @staticmethod
    def from_dict(obj: Any) -> 'Observation':
        assert isinstance(obj, dict)
        ops = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("ops"))
        return Observation(ops)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ops is not None:
            result["ops"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.ops)
        return result


class Temperature:
    data: Optional[List[Any]]
    user_text: Optional[str]
    value_unit: Optional[str]

    def __init__(self, data: Optional[List[Any]], user_text: Optional[str], value_unit: Optional[str]) -> None:
        self.data = data
        self.user_text = user_text
        self.value_unit = value_unit

    @staticmethod
    def from_dict(obj: Any) -> 'Temperature':
        assert isinstance(obj, dict)
        data = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("data"))
        user_text = from_union([from_str, from_none], obj.get("userText"))
        value_unit = from_union([from_str, from_none], obj.get("valueUnit"))
        return Temperature(data, user_text, value_unit)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.data is not None:
            result["data"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.data)
        if self.user_text is not None:
            result["userText"] = from_union([from_str, from_none], self.user_text)
        if self.value_unit is not None:
            result["valueUnit"] = from_union([from_str, from_none], self.value_unit)
        return result


class Reaction:
    created_at: Optional[datetime]
    created_by: Optional[str]
    dangerous_products: Optional[List[Any]]
    deleted_at: None
    description: Optional[ReactionDescription]
    duration: Optional[str]
    name: Optional[str]
    observation: Optional[Observation]
    origin: Optional[Dict[str, Any]]
    purification: Optional[List[Any]]
    reaction_svg_file: Optional[str]
    rf_value: Optional[str]
    rinchi_long_key: Optional[str]
    rinchi_short_key: Optional[str]
    rinchi_string: Optional[str]
    rinchi_web_key: Optional[str]
    role: Optional[str]
    short_label: Optional[str]
    solvent: Optional[str]
    status: Optional[str]
    temperature: Optional[Temperature]
    timestamp_start: Optional[str]
    timestamp_stop: Optional[str]
    tlc_description: Optional[str]
    tlc_solvents: Optional[str]
    updated_at: Optional[datetime]

    def __init__(self, created_at: Optional[datetime], created_by: Optional[str], dangerous_products: Optional[List[Any]], deleted_at: None, description: Optional[ReactionDescription], duration: Optional[str], name: Optional[str], observation: Optional[Observation], origin: Optional[Dict[str, Any]], purification: Optional[List[Any]], reaction_svg_file: Optional[str], rf_value: Optional[str], rinchi_long_key: Optional[str], rinchi_short_key: Optional[str], rinchi_string: Optional[str], rinchi_web_key: Optional[str], role: Optional[str], short_label: Optional[str], solvent: Optional[str], status: Optional[str], temperature: Optional[Temperature], timestamp_start: Optional[str], timestamp_stop: Optional[str], tlc_description: Optional[str], tlc_solvents: Optional[str], updated_at: Optional[datetime]) -> None:
        self.created_at = created_at
        self.created_by = created_by
        self.dangerous_products = dangerous_products
        self.deleted_at = deleted_at
        self.description = description
        self.duration = duration
        self.name = name
        self.observation = observation
        self.origin = origin
        self.purification = purification
        self.reaction_svg_file = reaction_svg_file
        self.rf_value = rf_value
        self.rinchi_long_key = rinchi_long_key
        self.rinchi_short_key = rinchi_short_key
        self.rinchi_string = rinchi_string
        self.rinchi_web_key = rinchi_web_key
        self.role = role
        self.short_label = short_label
        self.solvent = solvent
        self.status = status
        self.temperature = temperature
        self.timestamp_start = timestamp_start
        self.timestamp_stop = timestamp_stop
        self.tlc_description = tlc_description
        self.tlc_solvents = tlc_solvents
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Reaction':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        created_by = from_union([from_none, from_str], obj.get("created_by"))
        dangerous_products = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("dangerous_products"))
        deleted_at = from_none(obj.get("deleted_at"))
        description = from_union([ReactionDescription.from_dict, from_none], obj.get("description"))
        duration = from_union([from_str, from_none], obj.get("duration"))
        name = from_union([from_str, from_none], obj.get("name"))
        observation = from_union([Observation.from_dict, from_none], obj.get("observation"))
        origin = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("origin"))
        purification = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("purification"))
        reaction_svg_file = from_union([from_str, from_none], obj.get("reaction_svg_file"))
        rf_value = from_union([from_str, from_none], obj.get("rf_value"))
        rinchi_long_key = from_union([from_str, from_none], obj.get("rinchi_long_key"))
        rinchi_short_key = from_union([from_str, from_none], obj.get("rinchi_short_key"))
        rinchi_string = from_union([from_str, from_none], obj.get("rinchi_string"))
        rinchi_web_key = from_union([from_str, from_none], obj.get("rinchi_web_key"))
        role = from_union([from_str, from_none], obj.get("role"))
        short_label = from_union([from_str, from_none], obj.get("short_label"))
        solvent = from_union([from_str, from_none], obj.get("solvent"))
        status = from_union([from_str, from_none], obj.get("status"))
        temperature = from_union([Temperature.from_dict, from_none], obj.get("temperature"))
        timestamp_start = from_union([from_str, from_none], obj.get("timestamp_start"))
        timestamp_stop = from_union([from_str, from_none], obj.get("timestamp_stop"))
        tlc_description = from_union([from_str, from_none], obj.get("tlc_description"))
        tlc_solvents = from_union([from_str, from_none], obj.get("tlc_solvents"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        return Reaction(created_at, created_by, dangerous_products, deleted_at, description, duration, name, observation, origin, purification, reaction_svg_file, rf_value, rinchi_long_key, rinchi_short_key, rinchi_string, rinchi_web_key, role, short_label, solvent, status, temperature, timestamp_start, timestamp_stop, tlc_description, tlc_solvents, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.created_by is not None:
            result["created_by"] = from_union([from_none, from_str], self.created_by)
        if self.dangerous_products is not None:
            result["dangerous_products"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.dangerous_products)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.description is not None:
            result["description"] = from_union([lambda x: to_class(ReactionDescription, x), from_none], self.description)
        if self.duration is not None:
            result["duration"] = from_union([from_str, from_none], self.duration)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.observation is not None:
            result["observation"] = from_union([lambda x: to_class(Observation, x), from_none], self.observation)
        if self.origin is not None:
            result["origin"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.origin)
        if self.purification is not None:
            result["purification"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.purification)
        if self.reaction_svg_file is not None:
            result["reaction_svg_file"] = from_union([from_str, from_none], self.reaction_svg_file)
        if self.rf_value is not None:
            result["rf_value"] = from_union([from_str, from_none], self.rf_value)
        if self.rinchi_long_key is not None:
            result["rinchi_long_key"] = from_union([from_str, from_none], self.rinchi_long_key)
        if self.rinchi_short_key is not None:
            result["rinchi_short_key"] = from_union([from_str, from_none], self.rinchi_short_key)
        if self.rinchi_string is not None:
            result["rinchi_string"] = from_union([from_str, from_none], self.rinchi_string)
        if self.rinchi_web_key is not None:
            result["rinchi_web_key"] = from_union([from_str, from_none], self.rinchi_web_key)
        if self.role is not None:
            result["role"] = from_union([from_str, from_none], self.role)
        if self.short_label is not None:
            result["short_label"] = from_union([from_str, from_none], self.short_label)
        if self.solvent is not None:
            result["solvent"] = from_union([from_str, from_none], self.solvent)
        if self.status is not None:
            result["status"] = from_union([from_str, from_none], self.status)
        if self.temperature is not None:
            result["temperature"] = from_union([lambda x: to_class(Temperature, x), from_none], self.temperature)
        if self.timestamp_start is not None:
            result["timestamp_start"] = from_union([from_str, from_none], self.timestamp_start)
        if self.timestamp_stop is not None:
            result["timestamp_stop"] = from_union([from_str, from_none], self.timestamp_stop)
        if self.tlc_description is not None:
            result["tlc_description"] = from_union([from_str, from_none], self.tlc_description)
        if self.tlc_solvents is not None:
            result["tlc_solvents"] = from_union([from_str, from_none], self.tlc_solvents)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        return result


class ReactionSample:
    coefficient: Optional[float]
    deleted_at: None
    equivalent: Optional[float]
    position: Optional[int]
    reaction_id: Optional[str]
    reference: Optional[bool]
    sample_id: Optional[str]
    waste: Optional[bool]

    def __init__(self, coefficient: Optional[float], deleted_at: None, equivalent: Optional[float], position: Optional[int], reaction_id: Optional[str], reference: Optional[bool], sample_id: Optional[str], waste: Optional[bool]) -> None:
        self.coefficient = coefficient
        self.deleted_at = deleted_at
        self.equivalent = equivalent
        self.position = position
        self.reaction_id = reaction_id
        self.reference = reference
        self.sample_id = sample_id
        self.waste = waste

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionSample':
        assert isinstance(obj, dict)
        coefficient = from_union([from_none, from_float], obj.get("coefficient"))
        deleted_at = from_none(obj.get("deleted_at"))
        equivalent = from_union([from_none, from_float], obj.get("equivalent"))
        position = from_union([from_int, from_none], obj.get("position"))
        reaction_id = from_union([from_none, from_str], obj.get("reaction_id"))
        reference = from_union([from_bool, from_none], obj.get("reference"))
        sample_id = from_union([from_none, from_str], obj.get("sample_id"))
        waste = from_union([from_bool, from_none], obj.get("waste"))
        return ReactionSample(coefficient, deleted_at, equivalent, position, reaction_id, reference, sample_id, waste)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.coefficient is not None:
            result["coefficient"] = from_union([from_none, to_float], self.coefficient)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.equivalent is not None:
            result["equivalent"] = from_union([from_none, to_float], self.equivalent)
        if self.position is not None:
            result["position"] = from_union([from_int, from_none], self.position)
        if self.reaction_id is not None:
            result["reaction_id"] = from_union([from_none, from_str], self.reaction_id)
        if self.reference is not None:
            result["reference"] = from_union([from_bool, from_none], self.reference)
        if self.sample_id is not None:
            result["sample_id"] = from_union([from_none, from_str], self.sample_id)
        if self.waste is not None:
            result["waste"] = from_union([from_bool, from_none], self.waste)
        return result


class Residue:
    created_at: Optional[datetime]
    custom_info: Optional[Dict[str, Any]]
    residue_type: Optional[str]
    sample_id: Optional[str]
    updated_at: Optional[datetime]

    def __init__(self, created_at: Optional[datetime], custom_info: Optional[Dict[str, Any]], residue_type: Optional[str], sample_id: Optional[str], updated_at: Optional[datetime]) -> None:
        self.created_at = created_at
        self.custom_info = custom_info
        self.residue_type = residue_type
        self.sample_id = sample_id
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Residue':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        custom_info = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("custom_info"))
        residue_type = from_union([from_str, from_none], obj.get("residue_type"))
        sample_id = from_union([from_none, from_str], obj.get("sample_id"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        return Residue(created_at, custom_info, residue_type, sample_id, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.custom_info is not None:
            result["custom_info"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.custom_info)
        if self.residue_type is not None:
            result["residue_type"] = from_union([from_str, from_none], self.residue_type)
        if self.sample_id is not None:
            result["sample_id"] = from_union([from_none, from_str], self.sample_id)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        return result


class Sample:
    ancestry: Optional[str]
    boiling_point: Optional[float]
    created_at: Optional[datetime]
    created_by: Optional[str]
    deleted_at: None
    density: Optional[float]
    description: Optional[str]
    external_label: Optional[str]
    fingerprint_id: Optional[str]
    identifier: Optional[str]
    imported_readout: Optional[str]
    impurities: Optional[str]
    is_top_secret: Optional[bool]
    location: Optional[str]
    melting_point: Optional[float]
    molarity_unit: Optional[str]
    molarity_value: Optional[float]
    molecule_id: Optional[str]
    molecule_name_id: Optional[str]
    molfile: Optional[str]
    molfile_version: Optional[str]
    name: Optional[str]
    purity: Optional[float]
    real_amount_unit: Optional[str]
    real_amount_value: Optional[float]
    sample_svg_file: Optional[str]
    short_label: Optional[str]
    solvent: Optional[str]
    stereo: Optional[Dict[str, Any]]
    target_amount_unit: Optional[str]
    target_amount_value: Optional[float]
    updated_at: Optional[datetime]
    user_id: Optional[str]
    xref: Optional[Dict[str, Any]]

    def __init__(self, ancestry: Optional[str], boiling_point: Optional[float], created_at: Optional[datetime], created_by: Optional[str], deleted_at: None, density: Optional[float], description: Optional[str], external_label: Optional[str], fingerprint_id: Optional[str], identifier: Optional[str], imported_readout: Optional[str], impurities: Optional[str], is_top_secret: Optional[bool], location: Optional[str], melting_point: Optional[float], molarity_unit: Optional[str], molarity_value: Optional[float], molecule_id: Optional[str], molecule_name_id: Optional[str], molfile: Optional[str], molfile_version: Optional[str], name: Optional[str], purity: Optional[float], real_amount_unit: Optional[str], real_amount_value: Optional[float], sample_svg_file: Optional[str], short_label: Optional[str], solvent: Optional[str], stereo: Optional[Dict[str, Any]], target_amount_unit: Optional[str], target_amount_value: Optional[float], updated_at: Optional[datetime], user_id: Optional[str], xref: Optional[Dict[str, Any]]) -> None:
        self.ancestry = ancestry
        self.boiling_point = boiling_point
        self.created_at = created_at
        self.created_by = created_by
        self.deleted_at = deleted_at
        self.density = density
        self.description = description
        self.external_label = external_label
        self.fingerprint_id = fingerprint_id
        self.identifier = identifier
        self.imported_readout = imported_readout
        self.impurities = impurities
        self.is_top_secret = is_top_secret
        self.location = location
        self.melting_point = melting_point
        self.molarity_unit = molarity_unit
        self.molarity_value = molarity_value
        self.molecule_id = molecule_id
        self.molecule_name_id = molecule_name_id
        self.molfile = molfile
        self.molfile_version = molfile_version
        self.name = name
        self.purity = purity
        self.real_amount_unit = real_amount_unit
        self.real_amount_value = real_amount_value
        self.sample_svg_file = sample_svg_file
        self.short_label = short_label
        self.solvent = solvent
        self.stereo = stereo
        self.target_amount_unit = target_amount_unit
        self.target_amount_value = target_amount_value
        self.updated_at = updated_at
        self.user_id = user_id
        self.xref = xref

    @staticmethod
    def from_dict(obj: Any) -> 'Sample':
        assert isinstance(obj, dict)
        ancestry = from_union([from_str, from_none], obj.get("ancestry"))
        boiling_point = from_union([from_none, from_float], obj.get("boiling_point"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        created_by = from_union([from_none, from_str], obj.get("created_by"))
        deleted_at = from_none(obj.get("deleted_at"))
        density = from_union([from_none, from_float], obj.get("density"))
        description = from_union([from_none, from_str], obj.get("description"))
        external_label = from_union([from_str, from_none], obj.get("external_label"))
        fingerprint_id = from_union([from_none, from_str], obj.get("fingerprint_id"))
        identifier = from_union([from_none, from_str], obj.get("identifier"))
        imported_readout = from_union([from_none, from_str], obj.get("imported_readout"))
        impurities = from_union([from_none, from_str], obj.get("impurities"))
        is_top_secret = from_union([from_bool, from_none], obj.get("is_top_secret"))
        location = from_union([from_none, from_str], obj.get("location"))
        melting_point = from_union([from_none, from_float], obj.get("melting_point"))
        molarity_unit = from_union([from_none, from_str], obj.get("molarity_unit"))
        molarity_value = from_union([from_none, from_float], obj.get("molarity_value"))
        molecule_id = from_union([from_none, from_str], obj.get("molecule_id"))
        molecule_name_id = from_union([from_none, from_str], obj.get("molecule_name_id"))
        molfile = from_union([from_str, from_none], obj.get("molfile"))
        molfile_version = from_union([from_none, from_str], obj.get("molfile_version"))
        name = from_union([from_none, from_str], obj.get("name"))
        purity = from_union([from_none, from_float], obj.get("purity"))
        real_amount_unit = from_union([from_none, from_str], obj.get("real_amount_unit"))
        real_amount_value = from_union([from_none, from_float], obj.get("real_amount_value"))
        sample_svg_file = from_union([from_none, from_str], obj.get("sample_svg_file"))
        short_label = from_union([from_str, from_none], obj.get("short_label"))
        solvent = from_union([from_none, from_str], obj.get("solvent"))
        stereo = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("stereo"))
        target_amount_unit = from_union([from_str, from_none], obj.get("target_amount_unit"))
        target_amount_value = from_union([from_none, from_float], obj.get("target_amount_value"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        user_id = from_union([from_none, from_str], obj.get("user_id"))
        xref = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("xref"))
        return Sample(ancestry, boiling_point, created_at, created_by, deleted_at, density, description, external_label, fingerprint_id, identifier, imported_readout, impurities, is_top_secret, location, melting_point, molarity_unit, molarity_value, molecule_id, molecule_name_id, molfile, molfile_version, name, purity, real_amount_unit, real_amount_value, sample_svg_file, short_label, solvent, stereo, target_amount_unit, target_amount_value, updated_at, user_id, xref)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ancestry is not None:
            result["ancestry"] = from_union([from_str, from_none], self.ancestry)
        if self.boiling_point is not None:
            result["boiling_point"] = from_union([from_none, to_float], self.boiling_point)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.created_by is not None:
            result["created_by"] = from_union([from_none, from_str], self.created_by)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.density is not None:
            result["density"] = from_union([from_none, to_float], self.density)
        if self.description is not None:
            result["description"] = from_union([from_none, from_str], self.description)
        if self.external_label is not None:
            result["external_label"] = from_union([from_str, from_none], self.external_label)
        if self.fingerprint_id is not None:
            result["fingerprint_id"] = from_union([from_none, from_str], self.fingerprint_id)
        if self.identifier is not None:
            result["identifier"] = from_union([from_none, from_str], self.identifier)
        if self.imported_readout is not None:
            result["imported_readout"] = from_union([from_none, from_str], self.imported_readout)
        if self.impurities is not None:
            result["impurities"] = from_union([from_none, from_str], self.impurities)
        if self.is_top_secret is not None:
            result["is_top_secret"] = from_union([from_bool, from_none], self.is_top_secret)
        if self.location is not None:
            result["location"] = from_union([from_none, from_str], self.location)
        if self.melting_point is not None:
            result["melting_point"] = from_union([from_none, to_float], self.melting_point)
        if self.molarity_unit is not None:
            result["molarity_unit"] = from_union([from_none, from_str], self.molarity_unit)
        if self.molarity_value is not None:
            result["molarity_value"] = from_union([from_none, to_float], self.molarity_value)
        if self.molecule_id is not None:
            result["molecule_id"] = from_union([from_none, from_str], self.molecule_id)
        if self.molecule_name_id is not None:
            result["molecule_name_id"] = from_union([from_none, from_str], self.molecule_name_id)
        if self.molfile is not None:
            result["molfile"] = from_union([from_str, from_none], self.molfile)
        if self.molfile_version is not None:
            result["molfile_version"] = from_union([from_none, from_str], self.molfile_version)
        if self.name is not None:
            result["name"] = from_union([from_none, from_str], self.name)
        if self.purity is not None:
            result["purity"] = from_union([from_none, to_float], self.purity)
        if self.real_amount_unit is not None:
            result["real_amount_unit"] = from_union([from_none, from_str], self.real_amount_unit)
        if self.real_amount_value is not None:
            result["real_amount_value"] = from_union([from_none, to_float], self.real_amount_value)
        if self.sample_svg_file is not None:
            result["sample_svg_file"] = from_union([from_none, from_str], self.sample_svg_file)
        if self.short_label is not None:
            result["short_label"] = from_union([from_str, from_none], self.short_label)
        if self.solvent is not None:
            result["solvent"] = from_union([from_none, from_str], self.solvent)
        if self.stereo is not None:
            result["stereo"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.stereo)
        if self.target_amount_unit is not None:
            result["target_amount_unit"] = from_union([from_str, from_none], self.target_amount_unit)
        if self.target_amount_value is not None:
            result["target_amount_value"] = from_union([from_none, to_float], self.target_amount_value)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.user_id is not None:
            result["user_id"] = from_union([from_none, from_str], self.user_id)
        if self.xref is not None:
            result["xref"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.xref)
        return result


class ScreenDescription:
    ops: Optional[List[Any]]

    def __init__(self, ops: Optional[List[Any]]) -> None:
        self.ops = ops

    @staticmethod
    def from_dict(obj: Any) -> 'ScreenDescription':
        assert isinstance(obj, dict)
        ops = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("ops"))
        return ScreenDescription(ops)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ops is not None:
            result["ops"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.ops)
        return result


class Screen:
    collaborator: Optional[str]
    conditions: Optional[str]
    created_at: Optional[datetime]
    deleted_at: None
    description: Optional[ScreenDescription]
    name: Optional[str]
    requirements: Optional[str]
    result: Optional[str]
    updated_at: Optional[datetime]

    def __init__(self, collaborator: Optional[str], conditions: Optional[str], created_at: Optional[datetime], deleted_at: None, description: Optional[ScreenDescription], name: Optional[str], requirements: Optional[str], result: Optional[str], updated_at: Optional[datetime]) -> None:
        self.collaborator = collaborator
        self.conditions = conditions
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.description = description
        self.name = name
        self.requirements = requirements
        self.result = result
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Screen':
        assert isinstance(obj, dict)
        collaborator = from_union([from_str, from_none], obj.get("collaborator"))
        conditions = from_union([from_str, from_none], obj.get("conditions"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deleted_at = from_none(obj.get("deleted_at"))
        description = from_union([ScreenDescription.from_dict, from_none], obj.get("description"))
        name = from_union([from_str, from_none], obj.get("name"))
        requirements = from_union([from_str, from_none], obj.get("requirements"))
        result = from_union([from_str, from_none], obj.get("result"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        return Screen(collaborator, conditions, created_at, deleted_at, description, name, requirements, result, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.collaborator is not None:
            result["collaborator"] = from_union([from_str, from_none], self.collaborator)
        if self.conditions is not None:
            result["conditions"] = from_union([from_str, from_none], self.conditions)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.description is not None:
            result["description"] = from_union([lambda x: to_class(ScreenDescription, x), from_none], self.description)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.requirements is not None:
            result["requirements"] = from_union([from_str, from_none], self.requirements)
        if self.result is not None:
            result["result"] = from_union([from_str, from_none], self.result)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        return result


class Well:
    additive: Optional[str]
    created_at: Optional[datetime]
    deleted_at: None
    position_x: Optional[int]
    position_y: Optional[int]
    readout: Optional[str]
    sample_id: Optional[str]
    updated_at: Optional[datetime]
    wellplate_id: Optional[str]

    def __init__(self, additive: Optional[str], created_at: Optional[datetime], deleted_at: None, position_x: Optional[int], position_y: Optional[int], readout: Optional[str], sample_id: Optional[str], updated_at: Optional[datetime], wellplate_id: Optional[str]) -> None:
        self.additive = additive
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.position_x = position_x
        self.position_y = position_y
        self.readout = readout
        self.sample_id = sample_id
        self.updated_at = updated_at
        self.wellplate_id = wellplate_id

    @staticmethod
    def from_dict(obj: Any) -> 'Well':
        assert isinstance(obj, dict)
        additive = from_union([from_none, from_str], obj.get("additive"))
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deleted_at = from_none(obj.get("deleted_at"))
        position_x = from_union([from_int, from_none], obj.get("position_x"))
        position_y = from_union([from_int, from_none], obj.get("position_y"))
        readout = from_union([from_none, from_str], obj.get("readout"))
        sample_id = from_union([from_none, from_str], obj.get("sample_id"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        wellplate_id = from_union([from_none, from_str], obj.get("wellplate_id"))
        return Well(additive, created_at, deleted_at, position_x, position_y, readout, sample_id, updated_at, wellplate_id)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.additive is not None:
            result["additive"] = from_union([from_none, from_str], self.additive)
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.position_x is not None:
            result["position_x"] = from_union([from_int, from_none], self.position_x)
        if self.position_y is not None:
            result["position_y"] = from_union([from_int, from_none], self.position_y)
        if self.readout is not None:
            result["readout"] = from_union([from_none, from_str], self.readout)
        if self.sample_id is not None:
            result["sample_id"] = from_union([from_none, from_str], self.sample_id)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        if self.wellplate_id is not None:
            result["wellplate_id"] = from_union([from_none, from_str], self.wellplate_id)
        return result


class WellplateDescription:
    ops: Optional[List[Any]]

    def __init__(self, ops: Optional[List[Any]]) -> None:
        self.ops = ops

    @staticmethod
    def from_dict(obj: Any) -> 'WellplateDescription':
        assert isinstance(obj, dict)
        ops = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("ops"))
        return WellplateDescription(ops)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ops is not None:
            result["ops"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.ops)
        return result


class Wellplate:
    created_at: Optional[datetime]
    deleted_at: None
    description: Optional[WellplateDescription]
    name: Optional[str]
    size: Optional[int]
    updated_at: Optional[datetime]

    def __init__(self, created_at: Optional[datetime], deleted_at: None, description: Optional[WellplateDescription], name: Optional[str], size: Optional[int], updated_at: Optional[datetime]) -> None:
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.description = description
        self.name = name
        self.size = size
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Wellplate':
        assert isinstance(obj, dict)
        created_at = from_union([from_datetime, from_none], obj.get("created_at"))
        deleted_at = from_none(obj.get("deleted_at"))
        description = from_union([WellplateDescription.from_dict, from_none], obj.get("description"))
        name = from_union([from_str, from_none], obj.get("name"))
        size = from_union([from_int, from_none], obj.get("size"))
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        return Wellplate(created_at, deleted_at, description, name, size, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.created_at is not None:
            result["created_at"] = from_union([lambda x: x.isoformat(), from_none], self.created_at)
        if self.deleted_at is not None:
            result["deleted_at"] = from_none(self.deleted_at)
        if self.description is not None:
            result["description"] = from_union([lambda x: to_class(WellplateDescription, x), from_none], self.description)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.size is not None:
            result["size"] = from_union([from_int, from_none], self.size)
        if self.updated_at is not None:
            result["updated_at"] = from_union([lambda x: x.isoformat(), from_none], self.updated_at)
        return result


class Chemotion:
    collection: Optional[Dict[str, Collection]]
    collections_reaction: Optional[Dict[str, CollectionsReaction]]
    collections_sample: Optional[Dict[str, CollectionsSample]]
    collections_wellplate: Optional[Dict[str, CollectionsWellplate]]
    fingerprint: Optional[Dict[str, Fingerprint]]
    molecule: Optional[Dict[str, Molecule]]
    molecule_name: Optional[Dict[str, MoleculeName]]
    reaction: Optional[Dict[str, Reaction]]
    reactions_product_sample: Optional[Dict[str, ReactionSample]]
    reactions_purification_solvent_sample: Optional[Dict[str, ReactionSample]]
    reactions_reactant_sample: Optional[Dict[str, ReactionSample]]
    reactions_solvent_sample: Optional[Dict[str, ReactionSample]]
    reactions_starting_material_sample: Optional[Dict[str, ReactionSample]]
    residue: Optional[Dict[str, Residue]]
    sample: Optional[Dict[str, Sample]]
    screen: Optional[Dict[str, Screen]]
    well: Optional[Dict[str, Well]]
    wellplate: Optional[Dict[str, Wellplate]]

    def __init__(self, collection: Optional[Dict[str, Collection]], collections_reaction: Optional[Dict[str, CollectionsReaction]], collections_sample: Optional[Dict[str, CollectionsSample]], collections_wellplate: Optional[Dict[str, CollectionsWellplate]], fingerprint: Optional[Dict[str, Fingerprint]], molecule: Optional[Dict[str, Molecule]], molecule_name: Optional[Dict[str, MoleculeName]], reaction: Optional[Dict[str, Reaction]], reactions_product_sample: Optional[Dict[str, ReactionSample]], reactions_purification_solvent_sample: Optional[Dict[str, ReactionSample]], reactions_reactant_sample: Optional[Dict[str, ReactionSample]], reactions_solvent_sample: Optional[Dict[str, ReactionSample]], reactions_starting_material_sample: Optional[Dict[str, ReactionSample]], residue: Optional[Dict[str, Residue]], sample: Optional[Dict[str, Sample]], screen: Optional[Dict[str, Screen]], well: Optional[Dict[str, Well]], wellplate: Optional[Dict[str, Wellplate]]) -> None:
        self.collection = collection
        self.collections_reaction = collections_reaction
        self.collections_sample = collections_sample
        self.collections_wellplate = collections_wellplate
        self.fingerprint = fingerprint
        self.molecule = molecule
        self.molecule_name = molecule_name
        self.reaction = reaction
        self.reactions_product_sample = reactions_product_sample
        self.reactions_purification_solvent_sample = reactions_purification_solvent_sample
        self.reactions_reactant_sample = reactions_reactant_sample
        self.reactions_solvent_sample = reactions_solvent_sample
        self.reactions_starting_material_sample = reactions_starting_material_sample
        self.residue = residue
        self.sample = sample
        self.screen = screen
        self.well = well
        self.wellplate = wellplate

    @staticmethod
    def from_dict(obj: Any) -> 'Chemotion':
        assert isinstance(obj, dict)
        collection = from_union([lambda x: from_dict(Collection.from_dict, x), from_none], obj.get("Collection"))
        collections_reaction = from_union([lambda x: from_dict(CollectionsReaction.from_dict, x), from_none], obj.get("CollectionsReaction"))
        collections_sample = from_union([lambda x: from_dict(CollectionsSample.from_dict, x), from_none], obj.get("CollectionsSample"))
        collections_wellplate = from_union([lambda x: from_dict(CollectionsWellplate.from_dict, x), from_none], obj.get("CollectionsWellplate"))
        fingerprint = from_union([lambda x: from_dict(Fingerprint.from_dict, x), from_none], obj.get("Fingerprint"))
        molecule = from_union([lambda x: from_dict(Molecule.from_dict, x), from_none], obj.get("Molecule"))
        molecule_name = from_union([lambda x: from_dict(MoleculeName.from_dict, x), from_none], obj.get("MoleculeName"))
        reaction = from_union([lambda x: from_dict(Reaction.from_dict, x), from_none], obj.get("Reaction"))
        reactions_product_sample = from_union([lambda x: from_dict(ReactionSample.from_dict, x), from_none], obj.get("ReactionsProductSample"))
        reactions_purification_solvent_sample = from_union([lambda x: from_dict(ReactionSample.from_dict, x), from_none], obj.get("ReactionsPurificationSolventSample"))
        reactions_reactant_sample = from_union([lambda x: from_dict(ReactionSample.from_dict, x), from_none], obj.get("ReactionsReactantSample"))
        reactions_solvent_sample = from_union([lambda x: from_dict(ReactionSample.from_dict, x), from_none], obj.get("ReactionsSolventSample"))
        reactions_starting_material_sample = from_union([lambda x: from_dict(ReactionSample.from_dict, x), from_none], obj.get("ReactionsStartingMaterialSample"))
        residue = from_union([lambda x: from_dict(Residue.from_dict, x), from_none], obj.get("Residue"))
        sample = from_union([lambda x: from_dict(Sample.from_dict, x), from_none], obj.get("Sample"))
        screen = from_union([lambda x: from_dict(Screen.from_dict, x), from_none], obj.get("Screen"))
        well = from_union([lambda x: from_dict(Well.from_dict, x), from_none], obj.get("Well"))
        wellplate = from_union([lambda x: from_dict(Wellplate.from_dict, x), from_none], obj.get("Wellplate"))
        return Chemotion(collection, collections_reaction, collections_sample, collections_wellplate, fingerprint, molecule, molecule_name, reaction, reactions_product_sample, reactions_purification_solvent_sample, reactions_reactant_sample, reactions_solvent_sample, reactions_starting_material_sample, residue, sample, screen, well, wellplate)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.collection is not None:
            result["Collection"] = from_union([lambda x: from_dict(lambda x: to_class(Collection, x), x), from_none], self.collection)
        if self.collections_reaction is not None:
            result["CollectionsReaction"] = from_union([lambda x: from_dict(lambda x: to_class(CollectionsReaction, x), x), from_none], self.collections_reaction)
        if self.collections_sample is not None:
            result["CollectionsSample"] = from_union([lambda x: from_dict(lambda x: to_class(CollectionsSample, x), x), from_none], self.collections_sample)
        if self.collections_wellplate is not None:
            result["CollectionsWellplate"] = from_union([lambda x: from_dict(lambda x: to_class(CollectionsWellplate, x), x), from_none], self.collections_wellplate)
        if self.fingerprint is not None:
            result["Fingerprint"] = from_union([lambda x: from_dict(lambda x: to_class(Fingerprint, x), x), from_none], self.fingerprint)
        if self.molecule is not None:
            result["Molecule"] = from_union([lambda x: from_dict(lambda x: to_class(Molecule, x), x), from_none], self.molecule)
        if self.molecule_name is not None:
            result["MoleculeName"] = from_union([lambda x: from_dict(lambda x: to_class(MoleculeName, x), x), from_none], self.molecule_name)
        if self.reaction is not None:
            result["Reaction"] = from_union([lambda x: from_dict(lambda x: to_class(Reaction, x), x), from_none], self.reaction)
        if self.reactions_product_sample is not None:
            result["ReactionsProductSample"] = from_union([lambda x: from_dict(lambda x: to_class(ReactionSample, x), x), from_none], self.reactions_product_sample)
        if self.reactions_purification_solvent_sample is not None:
            result["ReactionsPurificationSolventSample"] = from_union([lambda x: from_dict(lambda x: to_class(ReactionSample, x), x), from_none], self.reactions_purification_solvent_sample)
        if self.reactions_reactant_sample is not None:
            result["ReactionsReactantSample"] = from_union([lambda x: from_dict(lambda x: to_class(ReactionSample, x), x), from_none], self.reactions_reactant_sample)
        if self.reactions_solvent_sample is not None:
            result["ReactionsSolventSample"] = from_union([lambda x: from_dict(lambda x: to_class(ReactionSample, x), x), from_none], self.reactions_solvent_sample)
        if self.reactions_starting_material_sample is not None:
            result["ReactionsStartingMaterialSample"] = from_union([lambda x: from_dict(lambda x: to_class(ReactionSample, x), x), from_none], self.reactions_starting_material_sample)
        if self.residue is not None:
            result["Residue"] = from_union([lambda x: from_dict(lambda x: to_class(Residue, x), x), from_none], self.residue)
        if self.sample is not None:
            result["Sample"] = from_union([lambda x: from_dict(lambda x: to_class(Sample, x), x), from_none], self.sample)
        if self.screen is not None:
            result["Screen"] = from_union([lambda x: from_dict(lambda x: to_class(Screen, x), x), from_none], self.screen)
        if self.well is not None:
            result["Well"] = from_union([lambda x: from_dict(lambda x: to_class(Well, x), x), from_none], self.well)
        if self.wellplate is not None:
            result["Wellplate"] = from_union([lambda x: from_dict(lambda x: to_class(Wellplate, x), x), from_none], self.wellplate)
        return result


def chemotion_from_dict(s: Any) -> Chemotion:
    return Chemotion.from_dict(s)


def chemotion_to_dict(x: Chemotion) -> Any:
    return to_class(Chemotion, x)