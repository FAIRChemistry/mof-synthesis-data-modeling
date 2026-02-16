from uuid import UUID
from typing import Optional, Any, Dict, List, TypeVar, Callable, Type, cast
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


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


class Attachment:
    attachable_id: UUID
    attachable_type: str
    bucket: Optional[str]
    checksum: str
    content_type: str
    created_at: datetime
    created_by: UUID
    created_for: UUID
    filename: str
    folder: Optional[str]
    identifier: UUID
    key: UUID
    storage: str
    thumb: bool
    updated_at: datetime
    version: Optional[str]

    def __init__(self, attachable_id: UUID, attachable_type: str, bucket: Optional[str], checksum: str, content_type: str, created_at: datetime, created_by: UUID, created_for: UUID, filename: str, folder: Optional[str], identifier: UUID, key: UUID, storage: str, thumb: bool, updated_at: datetime, version: Optional[str]) -> None:
        self.attachable_id = attachable_id
        self.attachable_type = attachable_type
        self.bucket = bucket
        self.checksum = checksum
        self.content_type = content_type
        self.created_at = created_at
        self.created_by = created_by
        self.created_for = created_for
        self.filename = filename
        self.folder = folder
        self.identifier = identifier
        self.key = key
        self.storage = storage
        self.thumb = thumb
        self.updated_at = updated_at
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'Attachment':
        assert isinstance(obj, dict)
        attachable_id = UUID(obj.get("attachable_id"))
        attachable_type = from_str(obj.get("attachable_type"))
        bucket = from_union([from_none, from_str], obj.get("bucket"))
        checksum = from_str(obj.get("checksum"))
        content_type = from_str(obj.get("content_type"))
        created_at = from_datetime(obj.get("created_at"))
        created_by = UUID(obj.get("created_by"))
        created_for = UUID(obj.get("created_for"))
        filename = from_str(obj.get("filename"))
        folder = from_union([from_none, from_str], obj.get("folder"))
        identifier = UUID(obj.get("identifier"))
        key = UUID(obj.get("key"))
        storage = from_str(obj.get("storage"))
        thumb = from_bool(obj.get("thumb"))
        updated_at = from_datetime(obj.get("updated_at"))
        version = from_union([from_none, from_str], obj.get("version"))
        return Attachment(attachable_id, attachable_type, bucket, checksum, content_type, created_at, created_by, created_for, filename, folder, identifier, key, storage, thumb, updated_at, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["attachable_id"] = str(self.attachable_id)
        result["attachable_type"] = from_str(self.attachable_type)
        result["bucket"] = from_union([from_none, from_str], self.bucket)
        result["checksum"] = from_str(self.checksum)
        result["content_type"] = from_str(self.content_type)
        result["created_at"] = self.created_at.isoformat()
        result["created_by"] = str(self.created_by)
        result["created_for"] = str(self.created_for)
        result["filename"] = from_str(self.filename)
        result["folder"] = from_union([from_none, from_str], self.folder)
        result["identifier"] = str(self.identifier)
        result["key"] = str(self.key)
        result["storage"] = from_str(self.storage)
        result["thumb"] = from_bool(self.thumb)
        result["updated_at"] = self.updated_at.isoformat()
        result["version"] = from_union([from_none, from_str], self.version)
        return result


class Collection:
    ancestry: str
    created_at: datetime
    deleted_at: Optional[datetime]
    is_locked: bool
    is_shared: bool
    is_synchronized: bool
    label: str
    permission_level: int
    position: int
    reaction_detail_level: int
    sample_detail_level: int
    screen_detail_level: int
    shared_by_id: Optional[str]
    updated_at: datetime
    user_id: UUID
    wellplate_detail_level: int

    def __init__(self, ancestry: str, created_at: datetime, deleted_at: Optional[datetime], is_locked: bool, is_shared: bool, is_synchronized: bool, label: str, permission_level: int, position: int, reaction_detail_level: int, sample_detail_level: int, screen_detail_level: int, shared_by_id: Optional[str], updated_at: datetime, user_id: UUID, wellplate_detail_level: int) -> None:
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
        self.sample_detail_level = sample_detail_level
        self.screen_detail_level = screen_detail_level
        self.shared_by_id = shared_by_id
        self.updated_at = updated_at
        self.user_id = user_id
        self.wellplate_detail_level = wellplate_detail_level

    @staticmethod
    def from_dict(obj: Any) -> 'Collection':
        assert isinstance(obj, dict)
        ancestry = from_str(obj.get("ancestry"))
        created_at = from_datetime(obj.get("created_at"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        is_locked = from_bool(obj.get("is_locked"))
        is_shared = from_bool(obj.get("is_shared"))
        is_synchronized = from_bool(obj.get("is_synchronized"))
        label = from_str(obj.get("label"))
        permission_level = from_int(obj.get("permission_level"))
        position = from_int(obj.get("position"))
        reaction_detail_level = from_int(obj.get("reaction_detail_level"))
        sample_detail_level = from_int(obj.get("sample_detail_level"))
        screen_detail_level = from_int(obj.get("screen_detail_level"))
        shared_by_id = from_union([from_none, from_str], obj.get("shared_by_id"))
        updated_at = from_datetime(obj.get("updated_at"))
        user_id = UUID(obj.get("user_id"))
        wellplate_detail_level = from_int(obj.get("wellplate_detail_level"))
        return Collection(ancestry, created_at, deleted_at, is_locked, is_shared, is_synchronized, label, permission_level, position, reaction_detail_level, sample_detail_level, screen_detail_level, shared_by_id, updated_at, user_id, wellplate_detail_level)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ancestry"] = from_str(self.ancestry)
        result["created_at"] = self.created_at.isoformat()
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["is_locked"] = from_bool(self.is_locked)
        result["is_shared"] = from_bool(self.is_shared)
        result["is_synchronized"] = from_bool(self.is_synchronized)
        result["label"] = from_str(self.label)
        result["permission_level"] = from_int(self.permission_level)
        result["position"] = from_int(self.position)
        result["reaction_detail_level"] = from_int(self.reaction_detail_level)
        result["sample_detail_level"] = from_int(self.sample_detail_level)
        result["screen_detail_level"] = from_int(self.screen_detail_level)
        result["shared_by_id"] = from_union([from_none, from_str], self.shared_by_id)
        result["updated_at"] = self.updated_at.isoformat()
        result["user_id"] = str(self.user_id)
        result["wellplate_detail_level"] = from_int(self.wellplate_detail_level)
        return result


class CollectionsReaction:
    collection_id: UUID
    deleted_at: Optional[datetime]
    reaction_id: UUID

    def __init__(self, collection_id: UUID, deleted_at: Optional[datetime], reaction_id: UUID) -> None:
        self.collection_id = collection_id
        self.deleted_at = deleted_at
        self.reaction_id = reaction_id

    @staticmethod
    def from_dict(obj: Any) -> 'CollectionsReaction':
        assert isinstance(obj, dict)
        collection_id = UUID(obj.get("collection_id"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        reaction_id = UUID(obj.get("reaction_id"))
        return CollectionsReaction(collection_id, deleted_at, reaction_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["collection_id"] = str(self.collection_id)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["reaction_id"] = str(self.reaction_id)
        return result


class CollectionsSample:
    collection_id: UUID
    deleted_at: Optional[datetime]
    sample_id: UUID

    def __init__(self, collection_id: UUID, deleted_at: Optional[datetime], sample_id: UUID) -> None:
        self.collection_id = collection_id
        self.deleted_at = deleted_at
        self.sample_id = sample_id

    @staticmethod
    def from_dict(obj: Any) -> 'CollectionsSample':
        assert isinstance(obj, dict)
        collection_id = UUID(obj.get("collection_id"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        sample_id = UUID(obj.get("sample_id"))
        return CollectionsSample(collection_id, deleted_at, sample_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["collection_id"] = str(self.collection_id)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["sample_id"] = str(self.sample_id)
        return result


class Container:
    ancestry: str
    containable_id: Optional[UUID]
    containable_type: Optional[str]
    container_type: Optional[str]
    created_at: datetime
    description: Optional[str]
    extended_metadata: Dict[str, Any]
    name: Optional[str]
    parent_id: Optional[str]
    updated_at: datetime

    def __init__(self, ancestry: str, containable_id: Optional[UUID], containable_type: Optional[str], container_type: Optional[str], created_at: datetime, description: Optional[str], extended_metadata: Dict[str, Any], name: Optional[str], parent_id: Optional[str], updated_at: datetime) -> None:
        self.ancestry = ancestry
        self.containable_id = containable_id
        self.containable_type = containable_type
        self.container_type = container_type
        self.created_at = created_at
        self.description = description
        self.extended_metadata = extended_metadata
        self.name = name
        self.parent_id = parent_id
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Container':
        assert isinstance(obj, dict)
        ancestry = from_str(obj.get("ancestry"))
        containable_id = from_union([from_none, lambda x: UUID(x)], obj.get("containable_id"))
        containable_type = from_union([from_none, from_str], obj.get("containable_type"))
        container_type = from_union([from_none, from_str], obj.get("container_type"))
        created_at = from_datetime(obj.get("created_at"))
        description = from_union([from_none, from_str], obj.get("description"))
        extended_metadata = from_dict(lambda x: x, obj.get("extended_metadata"))
        name = from_union([from_none, from_str], obj.get("name"))
        parent_id = from_union([from_none, from_str], obj.get("parent_id"))
        updated_at = from_datetime(obj.get("updated_at"))
        return Container(ancestry, containable_id, containable_type, container_type, created_at, description, extended_metadata, name, parent_id, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ancestry"] = from_str(self.ancestry)
        result["containable_id"] = from_union([from_none, lambda x: str(x)], self.containable_id)
        result["containable_type"] = from_union([from_none, from_str], self.containable_type)
        result["container_type"] = from_union([from_none, from_str], self.container_type)
        result["created_at"] = self.created_at.isoformat()
        result["description"] = from_union([from_none, from_str], self.description)
        result["extended_metadata"] = from_dict(lambda x: x, self.extended_metadata)
        result["name"] = from_union([from_none, from_str], self.name)
        result["parent_id"] = from_union([from_none, from_str], self.parent_id)
        result["updated_at"] = self.updated_at.isoformat()
        return result


class Fingerprint:
    fp0: str
    fp1: str
    fp10: str
    fp11: str
    fp12: str
    fp13: str
    fp14: str
    fp15: str
    fp2: str
    fp3: str
    fp4: str
    fp5: str
    fp6: str
    fp7: str
    fp8: str
    fp9: str

    def __init__(self, fp0: str, fp1: str, fp10: str, fp11: str, fp12: str, fp13: str, fp14: str, fp15: str, fp2: str, fp3: str, fp4: str, fp5: str, fp6: str, fp7: str, fp8: str, fp9: str) -> None:
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

    @staticmethod
    def from_dict(obj: Any) -> 'Fingerprint':
        assert isinstance(obj, dict)
        fp0 = from_str(obj.get("fp0"))
        fp1 = from_str(obj.get("fp1"))
        fp10 = from_str(obj.get("fp10"))
        fp11 = from_str(obj.get("fp11"))
        fp12 = from_str(obj.get("fp12"))
        fp13 = from_str(obj.get("fp13"))
        fp14 = from_str(obj.get("fp14"))
        fp15 = from_str(obj.get("fp15"))
        fp2 = from_str(obj.get("fp2"))
        fp3 = from_str(obj.get("fp3"))
        fp4 = from_str(obj.get("fp4"))
        fp5 = from_str(obj.get("fp5"))
        fp6 = from_str(obj.get("fp6"))
        fp7 = from_str(obj.get("fp7"))
        fp8 = from_str(obj.get("fp8"))
        fp9 = from_str(obj.get("fp9"))
        return Fingerprint(fp0, fp1, fp10, fp11, fp12, fp13, fp14, fp15, fp2, fp3, fp4, fp5, fp6, fp7, fp8, fp9)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fp0"] = from_str(self.fp0)
        result["fp1"] = from_str(self.fp1)
        result["fp10"] = from_str(self.fp10)
        result["fp11"] = from_str(self.fp11)
        result["fp12"] = from_str(self.fp12)
        result["fp13"] = from_str(self.fp13)
        result["fp14"] = from_str(self.fp14)
        result["fp15"] = from_str(self.fp15)
        result["fp2"] = from_str(self.fp2)
        result["fp3"] = from_str(self.fp3)
        result["fp4"] = from_str(self.fp4)
        result["fp5"] = from_str(self.fp5)
        result["fp6"] = from_str(self.fp6)
        result["fp7"] = from_str(self.fp7)
        result["fp8"] = from_str(self.fp8)
        result["fp9"] = from_str(self.fp9)
        return result


class PurpleEln:
    base_revision: str
    current_revision: str
    version: str

    def __init__(self, base_revision: str, current_revision: str, version: str) -> None:
        self.base_revision = base_revision
        self.current_revision = current_revision
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'PurpleEln':
        assert isinstance(obj, dict)
        base_revision = from_str(obj.get("base_revision"))
        current_revision = from_str(obj.get("current_revision"))
        version = from_str(obj.get("version"))
        return PurpleEln(base_revision, current_revision, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["base_revision"] = from_str(self.base_revision)
        result["current_revision"] = from_str(self.current_revision)
        result["version"] = from_str(self.version)
        return result


class LabimotionDatasetKlassPropertiesRelease:
    eln: PurpleEln
    klass: str
    layers: Dict[str, Any]
    select_options: Dict[str, Any]
    uuid: UUID

    def __init__(self, eln: PurpleEln, klass: str, layers: Dict[str, Any], select_options: Dict[str, Any], uuid: UUID) -> None:
        self.eln = eln
        self.klass = klass
        self.layers = layers
        self.select_options = select_options
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'LabimotionDatasetKlassPropertiesRelease':
        assert isinstance(obj, dict)
        eln = PurpleEln.from_dict(obj.get("eln"))
        klass = from_str(obj.get("klass"))
        layers = from_dict(lambda x: x, obj.get("layers"))
        select_options = from_dict(lambda x: x, obj.get("select_options"))
        uuid = UUID(obj.get("uuid"))
        return LabimotionDatasetKlassPropertiesRelease(eln, klass, layers, select_options, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eln"] = to_class(PurpleEln, self.eln)
        result["klass"] = from_str(self.klass)
        result["layers"] = from_dict(lambda x: x, self.layers)
        result["select_options"] = from_dict(lambda x: x, self.select_options)
        result["uuid"] = str(self.uuid)
        return result


class FluffyEln:
    base_revision: str
    current_revision: str
    version: str

    def __init__(self, base_revision: str, current_revision: str, version: str) -> None:
        self.base_revision = base_revision
        self.current_revision = current_revision
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'FluffyEln':
        assert isinstance(obj, dict)
        base_revision = from_str(obj.get("base_revision"))
        current_revision = from_str(obj.get("current_revision"))
        version = from_str(obj.get("version"))
        return FluffyEln(base_revision, current_revision, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["base_revision"] = from_str(self.base_revision)
        result["current_revision"] = from_str(self.current_revision)
        result["version"] = from_str(self.version)
        return result


class LabimotionDatasetKlassPropertiesTemplate:
    eln: FluffyEln
    klass: str
    layers: Dict[str, Any]
    select_options: Dict[str, Any]
    uuid: UUID

    def __init__(self, eln: FluffyEln, klass: str, layers: Dict[str, Any], select_options: Dict[str, Any], uuid: UUID) -> None:
        self.eln = eln
        self.klass = klass
        self.layers = layers
        self.select_options = select_options
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'LabimotionDatasetKlassPropertiesTemplate':
        assert isinstance(obj, dict)
        eln = FluffyEln.from_dict(obj.get("eln"))
        klass = from_str(obj.get("klass"))
        layers = from_dict(lambda x: x, obj.get("layers"))
        select_options = from_dict(lambda x: x, obj.get("select_options"))
        uuid = UUID(obj.get("uuid"))
        return LabimotionDatasetKlassPropertiesTemplate(eln, klass, layers, select_options, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eln"] = to_class(FluffyEln, self.eln)
        result["klass"] = from_str(self.klass)
        result["layers"] = from_dict(lambda x: x, self.layers)
        result["select_options"] = from_dict(lambda x: x, self.select_options)
        result["uuid"] = str(self.uuid)
        return result


class LabimotionDatasetKlass:
    created_at: datetime
    created_by: UUID
    deleted_at: Optional[datetime]
    desc: str
    identifier: Optional[str]
    is_active: bool
    label: str
    ols_term_id: str
    place: int
    properties_release: LabimotionDatasetKlassPropertiesRelease
    properties_template: LabimotionDatasetKlassPropertiesTemplate
    released_at: datetime
    sync_time: Optional[datetime]
    updated_at: datetime
    updated_by: Optional[datetime]
    uuid: UUID

    def __init__(self, created_at: datetime, created_by: UUID, deleted_at: Optional[datetime], desc: str, identifier: Optional[str], is_active: bool, label: str, ols_term_id: str, place: int, properties_release: LabimotionDatasetKlassPropertiesRelease, properties_template: LabimotionDatasetKlassPropertiesTemplate, released_at: datetime, sync_time: Optional[datetime], updated_at: datetime, updated_by: Optional[datetime], uuid: UUID) -> None:
        self.created_at = created_at
        self.created_by = created_by
        self.deleted_at = deleted_at
        self.desc = desc
        self.identifier = identifier
        self.is_active = is_active
        self.label = label
        self.ols_term_id = ols_term_id
        self.place = place
        self.properties_release = properties_release
        self.properties_template = properties_template
        self.released_at = released_at
        self.sync_time = sync_time
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'LabimotionDatasetKlass':
        assert isinstance(obj, dict)
        created_at = from_datetime(obj.get("created_at"))
        created_by = UUID(obj.get("created_by"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        desc = from_str(obj.get("desc"))
        identifier = from_union([from_none, from_str], obj.get("identifier"))
        is_active = from_bool(obj.get("is_active"))
        label = from_str(obj.get("label"))
        ols_term_id = from_str(obj.get("ols_term_id"))
        place = from_int(obj.get("place"))
        properties_release = LabimotionDatasetKlassPropertiesRelease.from_dict(obj.get("properties_release"))
        properties_template = LabimotionDatasetKlassPropertiesTemplate.from_dict(obj.get("properties_template"))
        released_at = from_datetime(obj.get("released_at"))
        sync_time = from_union([from_none, from_datetime], obj.get("sync_time"))
        updated_at = from_datetime(obj.get("updated_at"))
        updated_by = from_union([from_none, from_datetime], obj.get("updated_by"))
        uuid = UUID(obj.get("uuid"))
        return LabimotionDatasetKlass(created_at, created_by, deleted_at, desc, identifier, is_active, label, ols_term_id, place, properties_release, properties_template, released_at, sync_time, updated_at, updated_by, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created_at"] = self.created_at.isoformat()
        result["created_by"] = str(self.created_by)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["desc"] = from_str(self.desc)
        result["identifier"] = from_union([from_none, from_str], self.identifier)
        result["is_active"] = from_bool(self.is_active)
        result["label"] = from_str(self.label)
        result["ols_term_id"] = from_str(self.ols_term_id)
        result["place"] = from_int(self.place)
        result["properties_release"] = to_class(LabimotionDatasetKlassPropertiesRelease, self.properties_release)
        result["properties_template"] = to_class(LabimotionDatasetKlassPropertiesTemplate, self.properties_template)
        result["released_at"] = self.released_at.isoformat()
        result["sync_time"] = from_union([from_none, lambda x: x.isoformat()], self.sync_time)
        result["updated_at"] = self.updated_at.isoformat()
        result["updated_by"] = from_union([from_none, lambda x: x.isoformat()], self.updated_by)
        result["uuid"] = str(self.uuid)
        return result


class TentacledEln:
    base_revision: str
    current_revision: str
    version: str

    def __init__(self, base_revision: str, current_revision: str, version: str) -> None:
        self.base_revision = base_revision
        self.current_revision = current_revision
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'TentacledEln':
        assert isinstance(obj, dict)
        base_revision = from_str(obj.get("base_revision"))
        current_revision = from_str(obj.get("current_revision"))
        version = from_str(obj.get("version"))
        return TentacledEln(base_revision, current_revision, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["base_revision"] = from_str(self.base_revision)
        result["current_revision"] = from_str(self.current_revision)
        result["version"] = from_str(self.version)
        return result


class LabimotionElementKlassPropertiesRelease:
    eln: TentacledEln
    klass: str
    select_options: Dict[str, Any]
    uuid: UUID

    def __init__(self, eln: TentacledEln, klass: str, select_options: Dict[str, Any], uuid: UUID) -> None:
        self.eln = eln
        self.klass = klass
        self.select_options = select_options
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'LabimotionElementKlassPropertiesRelease':
        assert isinstance(obj, dict)
        eln = TentacledEln.from_dict(obj.get("eln"))
        klass = from_str(obj.get("klass"))
        select_options = from_dict(lambda x: x, obj.get("select_options"))
        uuid = UUID(obj.get("uuid"))
        return LabimotionElementKlassPropertiesRelease(eln, klass, select_options, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eln"] = to_class(TentacledEln, self.eln)
        result["klass"] = from_str(self.klass)
        result["select_options"] = from_dict(lambda x: x, self.select_options)
        result["uuid"] = str(self.uuid)
        return result


class StickyEln:
    base_revision: str
    current_revision: str
    version: str

    def __init__(self, base_revision: str, current_revision: str, version: str) -> None:
        self.base_revision = base_revision
        self.current_revision = current_revision
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'StickyEln':
        assert isinstance(obj, dict)
        base_revision = from_str(obj.get("base_revision"))
        current_revision = from_str(obj.get("current_revision"))
        version = from_str(obj.get("version"))
        return StickyEln(base_revision, current_revision, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["base_revision"] = from_str(self.base_revision)
        result["current_revision"] = from_str(self.current_revision)
        result["version"] = from_str(self.version)
        return result


class LabimotionElementKlassPropertiesTemplate:
    eln: StickyEln
    klass: str
    select_options: Dict[str, Any]
    uuid: UUID

    def __init__(self, eln: StickyEln, klass: str, select_options: Dict[str, Any], uuid: UUID) -> None:
        self.eln = eln
        self.klass = klass
        self.select_options = select_options
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'LabimotionElementKlassPropertiesTemplate':
        assert isinstance(obj, dict)
        eln = StickyEln.from_dict(obj.get("eln"))
        klass = from_str(obj.get("klass"))
        select_options = from_dict(lambda x: x, obj.get("select_options"))
        uuid = UUID(obj.get("uuid"))
        return LabimotionElementKlassPropertiesTemplate(eln, klass, select_options, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eln"] = to_class(StickyEln, self.eln)
        result["klass"] = from_str(self.klass)
        result["select_options"] = from_dict(lambda x: x, self.select_options)
        result["uuid"] = str(self.uuid)
        return result


class LabimotionElementKlass:
    created_at: datetime
    created_by: Optional[str]
    deleted_at: Optional[datetime]
    desc: str
    icon_name: str
    is_active: bool
    is_generic: bool
    klass_prefix: str
    label: str
    name: str
    place: int
    properties_release: LabimotionElementKlassPropertiesRelease
    properties_template: LabimotionElementKlassPropertiesTemplate
    released_at: datetime
    updated_at: datetime
    uuid: UUID

    def __init__(self, created_at: datetime, created_by: Optional[str], deleted_at: Optional[datetime], desc: str, icon_name: str, is_active: bool, is_generic: bool, klass_prefix: str, label: str, name: str, place: int, properties_release: LabimotionElementKlassPropertiesRelease, properties_template: LabimotionElementKlassPropertiesTemplate, released_at: datetime, updated_at: datetime, uuid: UUID) -> None:
        self.created_at = created_at
        self.created_by = created_by
        self.deleted_at = deleted_at
        self.desc = desc
        self.icon_name = icon_name
        self.is_active = is_active
        self.is_generic = is_generic
        self.klass_prefix = klass_prefix
        self.label = label
        self.name = name
        self.place = place
        self.properties_release = properties_release
        self.properties_template = properties_template
        self.released_at = released_at
        self.updated_at = updated_at
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'LabimotionElementKlass':
        assert isinstance(obj, dict)
        created_at = from_datetime(obj.get("created_at"))
        created_by = from_union([from_none, from_str], obj.get("created_by"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        desc = from_str(obj.get("desc"))
        icon_name = from_str(obj.get("icon_name"))
        is_active = from_bool(obj.get("is_active"))
        is_generic = from_bool(obj.get("is_generic"))
        klass_prefix = from_str(obj.get("klass_prefix"))
        label = from_str(obj.get("label"))
        name = from_str(obj.get("name"))
        place = from_int(obj.get("place"))
        properties_release = LabimotionElementKlassPropertiesRelease.from_dict(obj.get("properties_release"))
        properties_template = LabimotionElementKlassPropertiesTemplate.from_dict(obj.get("properties_template"))
        released_at = from_datetime(obj.get("released_at"))
        updated_at = from_datetime(obj.get("updated_at"))
        uuid = UUID(obj.get("uuid"))
        return LabimotionElementKlass(created_at, created_by, deleted_at, desc, icon_name, is_active, is_generic, klass_prefix, label, name, place, properties_release, properties_template, released_at, updated_at, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created_at"] = self.created_at.isoformat()
        result["created_by"] = from_union([from_none, from_str], self.created_by)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["desc"] = from_str(self.desc)
        result["icon_name"] = from_str(self.icon_name)
        result["is_active"] = from_bool(self.is_active)
        result["is_generic"] = from_bool(self.is_generic)
        result["klass_prefix"] = from_str(self.klass_prefix)
        result["label"] = from_str(self.label)
        result["name"] = from_str(self.name)
        result["place"] = from_int(self.place)
        result["properties_release"] = to_class(LabimotionElementKlassPropertiesRelease, self.properties_release)
        result["properties_template"] = to_class(LabimotionElementKlassPropertiesTemplate, self.properties_template)
        result["released_at"] = self.released_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        result["uuid"] = str(self.uuid)
        return result


class Molecule:
    boiling_point: Optional[float]
    created_at: datetime
    deleted_at: Optional[datetime]
    density: float
    exact_molecular_weight: Optional[float]
    inchikey: str
    inchistring: Optional[str]
    is_partial: bool
    iupac_name: Optional[str]
    melting_point: Optional[float]
    molecular_weight: Optional[float]
    molecule_svg_file: Optional[str]
    molfile: Optional[str]
    names: List[str]
    sum_formular: Optional[str]
    updated_at: datetime

    def __init__(self, boiling_point: Optional[float], created_at: datetime, deleted_at: Optional[datetime], density: float, exact_molecular_weight: Optional[float], inchikey: str, inchistring: Optional[str], is_partial: bool, iupac_name: Optional[str], melting_point: Optional[float], molecular_weight: Optional[float], molecule_svg_file: Optional[str], molfile: Optional[str], names: List[str], sum_formular: Optional[str], updated_at: datetime) -> None:
        self.boiling_point = boiling_point
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
        self.names = names
        self.sum_formular = sum_formular
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Molecule':
        assert isinstance(obj, dict)
        boiling_point = from_union([from_none, from_float], obj.get("boiling_point"))
        created_at = from_datetime(obj.get("created_at"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        density = from_float(obj.get("density"))
        exact_molecular_weight = from_union([from_none, from_float], obj.get("exact_molecular_weight"))
        inchikey = from_str(obj.get("inchikey"))
        inchistring = from_union([from_none, from_str], obj.get("inchistring"))
        is_partial = from_bool(obj.get("is_partial"))
        iupac_name = from_union([from_none, from_str], obj.get("iupac_name"))
        melting_point = from_union([from_none, from_float], obj.get("melting_point"))
        molecular_weight = from_union([from_none, from_float], obj.get("molecular_weight"))
        molecule_svg_file = from_union([from_none, from_str], obj.get("molecule_svg_file"))
        molfile = from_union([from_none, from_str], obj.get("molfile"))
        names = from_list(from_str, obj.get("names"))
        sum_formular = from_union([from_none, from_str], obj.get("sum_formular"))
        updated_at = from_datetime(obj.get("updated_at"))
        return Molecule(boiling_point, created_at, deleted_at, density, exact_molecular_weight, inchikey, inchistring, is_partial, iupac_name, melting_point, molecular_weight, molecule_svg_file, molfile, names, sum_formular, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["boiling_point"] = from_union([from_none, to_float], self.boiling_point)
        result["created_at"] = self.created_at.isoformat()
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["density"] = to_float(self.density)
        result["exact_molecular_weight"] = from_union([from_none, to_float], self.exact_molecular_weight)
        result["inchikey"] = from_str(self.inchikey)
        result["inchistring"] = from_union([from_none, from_str], self.inchistring)
        result["is_partial"] = from_bool(self.is_partial)
        result["iupac_name"] = from_union([from_none, from_str], self.iupac_name)
        result["melting_point"] = from_union([from_none, to_float], self.melting_point)
        result["molecular_weight"] = from_union([from_none, to_float], self.molecular_weight)
        result["molecule_svg_file"] = from_union([from_none, from_str], self.molecule_svg_file)
        result["molfile"] = from_union([from_none, from_str], self.molfile)
        result["names"] = from_list(from_str, self.names)
        result["sum_formular"] = from_union([from_none, from_str], self.sum_formular)
        result["updated_at"] = self.updated_at.isoformat()
        return result


class MoleculeName:
    created_at: datetime
    deleted_at: Optional[datetime]
    description: str
    molecule_id: UUID
    name: str
    updated_at: datetime
    user_id: Optional[str]

    def __init__(self, created_at: datetime, deleted_at: Optional[datetime], description: str, molecule_id: UUID, name: str, updated_at: datetime, user_id: Optional[str]) -> None:
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
        created_at = from_datetime(obj.get("created_at"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        description = from_str(obj.get("description"))
        molecule_id = UUID(obj.get("molecule_id"))
        name = from_str(obj.get("name"))
        updated_at = from_datetime(obj.get("updated_at"))
        user_id = from_union([from_none, from_str], obj.get("user_id"))
        return MoleculeName(created_at, deleted_at, description, molecule_id, name, updated_at, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created_at"] = self.created_at.isoformat()
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["description"] = from_str(self.description)
        result["molecule_id"] = str(self.molecule_id)
        result["name"] = from_str(self.name)
        result["updated_at"] = self.updated_at.isoformat()
        result["user_id"] = from_union([from_none, from_str], self.user_id)
        return result


class Attributes:
    script: Optional[str]

    def __init__(self, script: Optional[str]) -> None:
        self.script = script

    @staticmethod
    def from_dict(obj: Any) -> 'Attributes':
        assert isinstance(obj, dict)
        script = from_union([from_str, from_none], obj.get("script"))
        return Attributes(script)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.script is not None:
            result["script"] = from_union([from_str, from_none], self.script)
        return result


class DescriptionOp:
    attributes: Optional[Attributes]
    insert: str

    def __init__(self, attributes: Optional[Attributes], insert: str) -> None:
        self.attributes = attributes
        self.insert = insert

    @staticmethod
    def from_dict(obj: Any) -> 'DescriptionOp':
        assert isinstance(obj, dict)
        attributes = from_union([Attributes.from_dict, from_none], obj.get("attributes"))
        insert = from_str(obj.get("insert"))
        return DescriptionOp(attributes, insert)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.attributes is not None:
            result["attributes"] = from_union([lambda x: to_class(Attributes, x), from_none], self.attributes)
        result["insert"] = from_str(self.insert)
        return result


class Description:
    ops: List[DescriptionOp]

    def __init__(self, ops: List[DescriptionOp]) -> None:
        self.ops = ops

    @staticmethod
    def from_dict(obj: Any) -> 'Description':
        assert isinstance(obj, dict)
        ops = from_list(DescriptionOp.from_dict, obj.get("ops"))
        return Description(ops)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ops"] = from_list(lambda x: to_class(DescriptionOp, x), self.ops)
        return result


class ObservationOp:
    insert: str

    def __init__(self, insert: str) -> None:
        self.insert = insert

    @staticmethod
    def from_dict(obj: Any) -> 'ObservationOp':
        assert isinstance(obj, dict)
        insert = from_str(obj.get("insert"))
        return ObservationOp(insert)

    def to_dict(self) -> dict:
        result: dict = {}
        result["insert"] = from_str(self.insert)
        return result


class Observation:
    ops: List[ObservationOp]

    def __init__(self, ops: List[ObservationOp]) -> None:
        self.ops = ops

    @staticmethod
    def from_dict(obj: Any) -> 'Observation':
        assert isinstance(obj, dict)
        ops = from_list(ObservationOp.from_dict, obj.get("ops"))
        return Observation(ops)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ops"] = from_list(lambda x: to_class(ObservationOp, x), self.ops)
        return result


class Temperature:
    data: List[Any]
    user_text: str
    value_unit: str

    def __init__(self, data: List[Any], user_text: str, value_unit: str) -> None:
        self.data = data
        self.user_text = user_text
        self.value_unit = value_unit

    @staticmethod
    def from_dict(obj: Any) -> 'Temperature':
        assert isinstance(obj, dict)
        data = from_list(lambda x: x, obj.get("data"))
        user_text = from_str(obj.get("userText"))
        value_unit = from_str(obj.get("valueUnit"))
        return Temperature(data, user_text, value_unit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(lambda x: x, self.data)
        result["userText"] = from_str(self.user_text)
        result["valueUnit"] = from_str(self.value_unit)
        return result


class Reaction:
    created_at: datetime
    dangerous_products: List[Any]
    description: Description
    name: str
    observation: Observation
    purification: List[str]
    reaction_svg_file: str
    rf_value: str
    solvent: str
    status: str
    temperature: Temperature
    timestamp_start: str
    timestamp_stop: str
    tlc_description: str
    tlc_solvents: str
    updated_at: datetime

    def __init__(self, created_at: datetime, dangerous_products: List[Any], description: Description, name: str, observation: Observation, purification: List[str], reaction_svg_file: str, rf_value: str, solvent: str, status: str, temperature: Temperature, timestamp_start: str, timestamp_stop: str, tlc_description: str, tlc_solvents: str, updated_at: datetime) -> None:
        self.created_at = created_at
        self.dangerous_products = dangerous_products
        self.description = description
        self.name = name
        self.observation = observation
        self.purification = purification
        self.reaction_svg_file = reaction_svg_file
        self.rf_value = rf_value
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
        created_at = from_datetime(obj.get("created_at"))
        dangerous_products = from_list(lambda x: x, obj.get("dangerous_products"))
        description = Description.from_dict(obj.get("description"))
        name = from_str(obj.get("name"))
        observation = Observation.from_dict(obj.get("observation"))
        purification = from_list(from_str, obj.get("purification"))
        reaction_svg_file = from_str(obj.get("reaction_svg_file"))
        rf_value = from_str(obj.get("rf_value"))
        solvent = from_str(obj.get("solvent"))
        status = from_str(obj.get("status"))
        temperature = Temperature.from_dict(obj.get("temperature"))
        timestamp_start = from_str(obj.get("timestamp_start"))
        timestamp_stop = from_str(obj.get("timestamp_stop"))
        tlc_description = from_str(obj.get("tlc_description"))
        tlc_solvents = from_str(obj.get("tlc_solvents"))
        updated_at = from_datetime(obj.get("updated_at"))
        return Reaction(created_at, dangerous_products, description, name, observation, purification, reaction_svg_file, rf_value, solvent, status, temperature, timestamp_start, timestamp_stop, tlc_description, tlc_solvents, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["created_at"] = self.created_at.isoformat()
        result["dangerous_products"] = from_list(lambda x: x, self.dangerous_products)
        result["description"] = to_class(Description, self.description)
        result["name"] = from_str(self.name)
        result["observation"] = to_class(Observation, self.observation)
        result["purification"] = from_list(from_str, self.purification)
        result["reaction_svg_file"] = from_str(self.reaction_svg_file)
        result["rf_value"] = from_str(self.rf_value)
        result["solvent"] = from_str(self.solvent)
        result["status"] = from_str(self.status)
        result["temperature"] = to_class(Temperature, self.temperature)
        result["timestamp_start"] = from_str(self.timestamp_start)
        result["timestamp_stop"] = from_str(self.timestamp_stop)
        result["tlc_description"] = from_str(self.tlc_description)
        result["tlc_solvents"] = from_str(self.tlc_solvents)
        result["updated_at"] = self.updated_at.isoformat()
        return result


class ReactionsProductSample:
    coefficient: Optional[float]
    deleted_at: Optional[datetime]
    equivalent: Optional[float]
    position: int
    reaction_id: UUID
    reference: bool
    sample_id: UUID
    show_label: bool
    waste: Optional[bool]

    def __init__(self, coefficient: Optional[float], deleted_at: Optional[datetime], equivalent: Optional[float], position: int, reaction_id: UUID, reference: bool, sample_id: UUID, show_label: bool, waste: Optional[bool]) -> None:
        self.coefficient = coefficient
        self.deleted_at = deleted_at
        self.equivalent = equivalent
        self.position = position
        self.reaction_id = reaction_id
        self.reference = reference
        self.sample_id = sample_id
        self.show_label = show_label
        self.waste = waste

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionsProductSample':
        assert isinstance(obj, dict)
        coefficient = from_union([from_none, from_float], obj.get("coefficient"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        equivalent = from_union([from_none, from_float], obj.get("equivalent"))
        position = from_int(obj.get("position"))
        reaction_id = UUID(obj.get("reaction_id"))
        reference = from_bool(obj.get("reference"))
        sample_id = UUID(obj.get("sample_id"))
        show_label = from_bool(obj.get("show_label"))
        waste = from_union([from_none, from_bool], obj.get("waste"))
        return ReactionsProductSample(coefficient, deleted_at, equivalent, position, reaction_id, reference, sample_id, show_label, waste)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coefficient"] = from_union([from_none, to_float], self.coefficient)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["equivalent"] = from_union([from_none, to_float], self.equivalent)
        result["position"] = from_int(self.position)
        result["reaction_id"] = str(self.reaction_id)
        result["reference"] = from_bool(self.reference)
        result["sample_id"] = str(self.sample_id)
        result["show_label"] = from_bool(self.show_label)
        result["waste"] = from_union([from_none, from_bool], self.waste)
        return result


class ReactionsReactantSample:
    coefficient: Optional[float]
    deleted_at: Optional[datetime]
    equivalent: Optional[float]
    position: int
    reaction_id: UUID
    reference: bool
    sample_id: UUID
    show_label: bool
    waste: Optional[bool]

    def __init__(self, coefficient: Optional[float], deleted_at: Optional[datetime], equivalent: Optional[float], position: int, reaction_id: UUID, reference: bool, sample_id: UUID, show_label: bool, waste: Optional[bool]) -> None:
        self.coefficient = coefficient
        self.deleted_at = deleted_at
        self.equivalent = equivalent
        self.position = position
        self.reaction_id = reaction_id
        self.reference = reference
        self.sample_id = sample_id
        self.show_label = show_label
        self.waste = waste

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionsReactantSample':
        assert isinstance(obj, dict)
        coefficient = from_union([from_none, from_float], obj.get("coefficient"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        equivalent = from_union([from_none, from_float], obj.get("equivalent"))
        position = from_int(obj.get("position"))
        reaction_id = UUID(obj.get("reaction_id"))
        reference = from_bool(obj.get("reference"))
        sample_id = UUID(obj.get("sample_id"))
        show_label = from_bool(obj.get("show_label"))
        waste = from_union([from_none, from_bool], obj.get("waste"))
        return ReactionsReactantSample(coefficient, deleted_at, equivalent, position, reaction_id, reference, sample_id, show_label, waste)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coefficient"] = from_union([from_none, to_float], self.coefficient)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["equivalent"] = from_union([from_none, to_float], self.equivalent)
        result["position"] = from_int(self.position)
        result["reaction_id"] = str(self.reaction_id)
        result["reference"] = from_bool(self.reference)
        result["sample_id"] = str(self.sample_id)
        result["show_label"] = from_bool(self.show_label)
        result["waste"] = from_union([from_none, from_bool], self.waste)
        return result


class ReactionsSolventSample:
    coefficient: float
    deleted_at: Optional[datetime]
    equivalent: Optional[float]
    position: int
    reaction_id: UUID
    reference: bool
    sample_id: UUID
    show_label: bool
    waste: bool

    def __init__(self, coefficient: float, deleted_at: Optional[datetime], equivalent: Optional[float], position: int, reaction_id: UUID, reference: bool, sample_id: UUID, show_label: bool, waste: bool) -> None:
        self.coefficient = coefficient
        self.deleted_at = deleted_at
        self.equivalent = equivalent
        self.position = position
        self.reaction_id = reaction_id
        self.reference = reference
        self.sample_id = sample_id
        self.show_label = show_label
        self.waste = waste

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionsSolventSample':
        assert isinstance(obj, dict)
        coefficient = from_float(obj.get("coefficient"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        equivalent = from_union([from_none, from_float], obj.get("equivalent"))
        position = from_int(obj.get("position"))
        reaction_id = UUID(obj.get("reaction_id"))
        reference = from_bool(obj.get("reference"))
        sample_id = UUID(obj.get("sample_id"))
        show_label = from_bool(obj.get("show_label"))
        waste = from_bool(obj.get("waste"))
        return ReactionsSolventSample(coefficient, deleted_at, equivalent, position, reaction_id, reference, sample_id, show_label, waste)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coefficient"] = to_float(self.coefficient)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["equivalent"] = from_union([from_none, to_float], self.equivalent)
        result["position"] = from_int(self.position)
        result["reaction_id"] = str(self.reaction_id)
        result["reference"] = from_bool(self.reference)
        result["sample_id"] = str(self.sample_id)
        result["show_label"] = from_bool(self.show_label)
        result["waste"] = from_bool(self.waste)
        return result


class ReactionsStartingMaterialSample:
    coefficient: Optional[float]
    deleted_at: Optional[datetime]
    equivalent: Optional[float]
    position: int
    reaction_id: UUID
    reference: bool
    sample_id: UUID
    show_label: bool
    waste: Optional[bool]

    def __init__(self, coefficient: Optional[float], deleted_at: Optional[datetime], equivalent: Optional[float], position: int, reaction_id: UUID, reference: bool, sample_id: UUID, show_label: bool, waste: Optional[bool]) -> None:
        self.coefficient = coefficient
        self.deleted_at = deleted_at
        self.equivalent = equivalent
        self.position = position
        self.reaction_id = reaction_id
        self.reference = reference
        self.sample_id = sample_id
        self.show_label = show_label
        self.waste = waste

    @staticmethod
    def from_dict(obj: Any) -> 'ReactionsStartingMaterialSample':
        assert isinstance(obj, dict)
        coefficient = from_union([from_none, from_float], obj.get("coefficient"))
        deleted_at = from_union([from_none, from_datetime], obj.get("deleted_at"))
        equivalent = from_union([from_none, from_float], obj.get("equivalent"))
        position = from_int(obj.get("position"))
        reaction_id = UUID(obj.get("reaction_id"))
        reference = from_bool(obj.get("reference"))
        sample_id = UUID(obj.get("sample_id"))
        show_label = from_bool(obj.get("show_label"))
        waste = from_union([from_none, from_bool], obj.get("waste"))
        return ReactionsStartingMaterialSample(coefficient, deleted_at, equivalent, position, reaction_id, reference, sample_id, show_label, waste)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coefficient"] = from_union([from_none, to_float], self.coefficient)
        result["deleted_at"] = from_union([from_none, lambda x: x.isoformat()], self.deleted_at)
        result["equivalent"] = from_union([from_none, to_float], self.equivalent)
        result["position"] = from_int(self.position)
        result["reaction_id"] = str(self.reaction_id)
        result["reference"] = from_bool(self.reference)
        result["sample_id"] = str(self.sample_id)
        result["show_label"] = from_bool(self.show_label)
        result["waste"] = from_union([from_none, from_bool], self.waste)
        return result


class Sample:
    ancestry: str
    created_at: datetime
    created_by: UUID
    deprecated_solvent: str
    description: str
    external_label: str
    impurities: str
    is_top_secret: bool
    location: str
    molecule_id: UUID
    molfile: str
    name: Optional[str]
    purity: float
    target_amount_unit: str
    target_amount_value: Optional[float]
    updated_at: datetime

    def __init__(self, ancestry: str, created_at: datetime, created_by: UUID, deprecated_solvent: str, description: str, external_label: str, impurities: str, is_top_secret: bool, location: str, molecule_id: UUID, molfile: str, name: Optional[str], purity: float, target_amount_unit: str, target_amount_value: Optional[float], updated_at: datetime) -> None:
        self.ancestry = ancestry
        self.created_at = created_at
        self.created_by = created_by
        self.deprecated_solvent = deprecated_solvent
        self.description = description
        self.external_label = external_label
        self.impurities = impurities
        self.is_top_secret = is_top_secret
        self.location = location
        self.molecule_id = molecule_id
        self.molfile = molfile
        self.name = name
        self.purity = purity
        self.target_amount_unit = target_amount_unit
        self.target_amount_value = target_amount_value
        self.updated_at = updated_at

    @staticmethod
    def from_dict(obj: Any) -> 'Sample':
        assert isinstance(obj, dict)
        ancestry = from_str(obj.get("ancestry"))
        created_at = from_datetime(obj.get("created_at"))
        created_by = UUID(obj.get("created_by"))
        deprecated_solvent = from_str(obj.get("deprecated_solvent"))
        description = from_str(obj.get("description"))
        external_label = from_str(obj.get("external_label"))
        impurities = from_str(obj.get("impurities"))
        is_top_secret = from_bool(obj.get("is_top_secret"))
        location = from_str(obj.get("location"))
        molecule_id = UUID(obj.get("molecule_id"))
        molfile = from_str(obj.get("molfile"))
        name = from_union([from_none, from_str], obj.get("name"))
        purity = from_float(obj.get("purity"))
        target_amount_unit = from_str(obj.get("target_amount_unit"))
        target_amount_value = from_union([from_none, from_float], obj.get("target_amount_value"))
        updated_at = from_datetime(obj.get("updated_at"))
        return Sample(ancestry, created_at, created_by, deprecated_solvent, description, external_label, impurities, is_top_secret, location, molecule_id, molfile, name, purity, target_amount_unit, target_amount_value, updated_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ancestry"] = from_str(self.ancestry)
        result["created_at"] = self.created_at.isoformat()
        result["created_by"] = str(self.created_by)
        result["deprecated_solvent"] = from_str(self.deprecated_solvent)
        result["description"] = from_str(self.description)
        result["external_label"] = from_str(self.external_label)
        result["impurities"] = from_str(self.impurities)
        result["is_top_secret"] = from_bool(self.is_top_secret)
        result["location"] = from_str(self.location)
        result["molecule_id"] = str(self.molecule_id)
        result["molfile"] = from_str(self.molfile)
        result["name"] = from_union([from_none, from_str], self.name)
        result["purity"] = to_float(self.purity)
        result["target_amount_unit"] = from_str(self.target_amount_unit)
        result["target_amount_value"] = from_union([from_none, to_float], self.target_amount_value)
        result["updated_at"] = self.updated_at.isoformat()
        return result


class ChemotionFixed:
    attachment: Dict[str, Attachment]
    collection: Dict[str, Collection]
    collections_reaction: Dict[str, CollectionsReaction]
    collections_sample: Dict[str, CollectionsSample]
    container: Dict[str, Container]
    fingerprint: Dict[str, Fingerprint]
    labimotion_dataset_klass: Dict[str, LabimotionDatasetKlass]
    labimotion_element_klass: Dict[str, LabimotionElementKlass]
    molecule: Dict[str, Molecule]
    molecule_name: Dict[str, MoleculeName]
    reaction: Dict[str, Reaction]
    reactions_product_sample: Dict[str, ReactionsProductSample]
    reactions_reactant_sample: Dict[str, ReactionsReactantSample]
    reactions_solvent_sample: Dict[str, ReactionsSolventSample]
    reactions_starting_material_sample: Dict[str, ReactionsStartingMaterialSample]
    sample: Dict[str, Sample]

    def __init__(self, attachment: Dict[str, Attachment], collection: Dict[str, Collection], collections_reaction: Dict[str, CollectionsReaction], collections_sample: Dict[str, CollectionsSample], container: Dict[str, Container], fingerprint: Dict[str, Fingerprint], labimotion_dataset_klass: Dict[str, LabimotionDatasetKlass], labimotion_element_klass: Dict[str, LabimotionElementKlass], molecule: Dict[str, Molecule], molecule_name: Dict[str, MoleculeName], reaction: Dict[str, Reaction], reactions_product_sample: Dict[str, ReactionsProductSample], reactions_reactant_sample: Dict[str, ReactionsReactantSample], reactions_solvent_sample: Dict[str, ReactionsSolventSample], reactions_starting_material_sample: Dict[str, ReactionsStartingMaterialSample], sample: Dict[str, Sample]) -> None:
        self.attachment = attachment
        self.collection = collection
        self.collections_reaction = collections_reaction
        self.collections_sample = collections_sample
        self.container = container
        self.fingerprint = fingerprint
        self.labimotion_dataset_klass = labimotion_dataset_klass
        self.labimotion_element_klass = labimotion_element_klass
        self.molecule = molecule
        self.molecule_name = molecule_name
        self.reaction = reaction
        self.reactions_product_sample = reactions_product_sample
        self.reactions_reactant_sample = reactions_reactant_sample
        self.reactions_solvent_sample = reactions_solvent_sample
        self.reactions_starting_material_sample = reactions_starting_material_sample
        self.sample = sample

    @staticmethod
    def from_dict(obj: Any) -> 'ChemotionFixed':
        assert isinstance(obj, dict)
        attachment = from_dict(Attachment.from_dict, obj.get("Attachment"))
        collection = from_dict(Collection.from_dict, obj.get("Collection"))
        collections_reaction = from_dict(CollectionsReaction.from_dict, obj.get("CollectionsReaction"))
        collections_sample = from_dict(CollectionsSample.from_dict, obj.get("CollectionsSample"))
        container = from_dict(Container.from_dict, obj.get("Container"))
        fingerprint = from_dict(Fingerprint.from_dict, obj.get("Fingerprint"))
        labimotion_dataset_klass = from_dict(LabimotionDatasetKlass.from_dict, obj.get("Labimotion::DatasetKlass"))
        labimotion_element_klass = from_dict(LabimotionElementKlass.from_dict, obj.get("Labimotion::ElementKlass"))
        molecule = from_dict(Molecule.from_dict, obj.get("Molecule"))
        molecule_name = from_dict(MoleculeName.from_dict, obj.get("MoleculeName"))
        reaction = from_dict(Reaction.from_dict, obj.get("Reaction"))
        reactions_product_sample = from_dict(ReactionsProductSample.from_dict, obj.get("ReactionsProductSample"))
        reactions_reactant_sample = from_dict(ReactionsReactantSample.from_dict, obj.get("ReactionsReactantSample"))
        reactions_solvent_sample = from_dict(ReactionsSolventSample.from_dict, obj.get("ReactionsSolventSample"))
        reactions_starting_material_sample = from_dict(ReactionsStartingMaterialSample.from_dict, obj.get("ReactionsStartingMaterialSample"))
        sample = from_dict(Sample.from_dict, obj.get("Sample"))
        return ChemotionFixed(attachment, collection, collections_reaction, collections_sample, container, fingerprint, labimotion_dataset_klass, labimotion_element_klass, molecule, molecule_name, reaction, reactions_product_sample, reactions_reactant_sample, reactions_solvent_sample, reactions_starting_material_sample, sample)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Attachment"] = from_dict(lambda x: to_class(Attachment, x), self.attachment)
        result["Collection"] = from_dict(lambda x: to_class(Collection, x), self.collection)
        result["CollectionsReaction"] = from_dict(lambda x: to_class(CollectionsReaction, x), self.collections_reaction)
        result["CollectionsSample"] = from_dict(lambda x: to_class(CollectionsSample, x), self.collections_sample)
        result["Container"] = from_dict(lambda x: to_class(Container, x), self.container)
        result["Fingerprint"] = from_dict(lambda x: to_class(Fingerprint, x), self.fingerprint)
        result["Labimotion::DatasetKlass"] = from_dict(lambda x: to_class(LabimotionDatasetKlass, x), self.labimotion_dataset_klass)
        result["Labimotion::ElementKlass"] = from_dict(lambda x: to_class(LabimotionElementKlass, x), self.labimotion_element_klass)
        result["Molecule"] = from_dict(lambda x: to_class(Molecule, x), self.molecule)
        result["MoleculeName"] = from_dict(lambda x: to_class(MoleculeName, x), self.molecule_name)
        result["Reaction"] = from_dict(lambda x: to_class(Reaction, x), self.reaction)
        result["ReactionsProductSample"] = from_dict(lambda x: to_class(ReactionsProductSample, x), self.reactions_product_sample)
        result["ReactionsReactantSample"] = from_dict(lambda x: to_class(ReactionsReactantSample, x), self.reactions_reactant_sample)
        result["ReactionsSolventSample"] = from_dict(lambda x: to_class(ReactionsSolventSample, x), self.reactions_solvent_sample)
        result["ReactionsStartingMaterialSample"] = from_dict(lambda x: to_class(ReactionsStartingMaterialSample, x), self.reactions_starting_material_sample)
        result["Sample"] = from_dict(lambda x: to_class(Sample, x), self.sample)
        return result


def chemotion_fixed_from_dict(s: Any) -> ChemotionFixed:
    return ChemotionFixed.from_dict(s)


def chemotion_fixed_to_dict(x: ChemotionFixed) -> Any:
    return to_class(ChemotionFixed, x)