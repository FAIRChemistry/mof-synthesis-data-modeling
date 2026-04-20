from typing import Any, Dict, Optional, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Collection:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'Collection':
        assert isinstance(obj, dict)
        return Collection()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class Sample:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'Sample':
        assert isinstance(obj, dict)
        return Sample()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class Schema:
    attachment: Optional[Dict[str, Any]]
    chemical: Optional[Dict[str, Any]]
    collection: Optional[Collection]
    collections_reaction: Optional[Dict[str, Any]]
    collections_research_plan: Optional[Dict[str, Any]]
    collections_sample: Optional[Dict[str, Any]]
    collections_screen: Optional[Dict[str, Any]]
    collections_wellplate: Optional[Dict[str, Any]]
    container: Optional[Dict[str, Any]]
    fingerprint: Optional[Dict[str, Any]]
    labimotion_dataset_klass: Optional[Dict[str, Any]]
    labimotion_element_klass: Optional[Dict[str, Any]]
    labimotion_segment_klass: Optional[Dict[str, Any]]
    literal: Optional[Dict[str, Any]]
    literature: Optional[Dict[str, Any]]
    molecule: Optional[Dict[str, Any]]
    molecule_name: Optional[Dict[str, Any]]
    reaction: Optional[Dict[str, Any]]
    reactions_product_sample: Optional[Dict[str, Any]]
    reactions_purification_solvent_sample: Optional[Dict[str, Any]]
    reactions_reactant_sample: Optional[Dict[str, Any]]
    reactions_solvent_sample: Optional[Dict[str, Any]]
    reactions_starting_material_sample: Optional[Dict[str, Any]]
    research_plan: Optional[Dict[str, Any]]
    residue: Optional[Dict[str, Any]]
    sample: Optional[Sample]
    screen: Optional[Dict[str, Any]]
    screens_wellplate: Optional[Dict[str, Any]]
    well: Optional[Dict[str, Any]]
    wellplate: Optional[Dict[str, Any]]

    def __init__(self, attachment: Optional[Dict[str, Any]], chemical: Optional[Dict[str, Any]], collection: Optional[Collection], collections_reaction: Optional[Dict[str, Any]], collections_research_plan: Optional[Dict[str, Any]], collections_sample: Optional[Dict[str, Any]], collections_screen: Optional[Dict[str, Any]], collections_wellplate: Optional[Dict[str, Any]], container: Optional[Dict[str, Any]], fingerprint: Optional[Dict[str, Any]], labimotion_dataset_klass: Optional[Dict[str, Any]], labimotion_element_klass: Optional[Dict[str, Any]], labimotion_segment_klass: Optional[Dict[str, Any]], literal: Optional[Dict[str, Any]], literature: Optional[Dict[str, Any]], molecule: Optional[Dict[str, Any]], molecule_name: Optional[Dict[str, Any]], reaction: Optional[Dict[str, Any]], reactions_product_sample: Optional[Dict[str, Any]], reactions_purification_solvent_sample: Optional[Dict[str, Any]], reactions_reactant_sample: Optional[Dict[str, Any]], reactions_solvent_sample: Optional[Dict[str, Any]], reactions_starting_material_sample: Optional[Dict[str, Any]], research_plan: Optional[Dict[str, Any]], residue: Optional[Dict[str, Any]], sample: Optional[Sample], screen: Optional[Dict[str, Any]], screens_wellplate: Optional[Dict[str, Any]], well: Optional[Dict[str, Any]], wellplate: Optional[Dict[str, Any]]) -> None:
        self.attachment = attachment
        self.chemical = chemical
        self.collection = collection
        self.collections_reaction = collections_reaction
        self.collections_research_plan = collections_research_plan
        self.collections_sample = collections_sample
        self.collections_screen = collections_screen
        self.collections_wellplate = collections_wellplate
        self.container = container
        self.fingerprint = fingerprint
        self.labimotion_dataset_klass = labimotion_dataset_klass
        self.labimotion_element_klass = labimotion_element_klass
        self.labimotion_segment_klass = labimotion_segment_klass
        self.literal = literal
        self.literature = literature
        self.molecule = molecule
        self.molecule_name = molecule_name
        self.reaction = reaction
        self.reactions_product_sample = reactions_product_sample
        self.reactions_purification_solvent_sample = reactions_purification_solvent_sample
        self.reactions_reactant_sample = reactions_reactant_sample
        self.reactions_solvent_sample = reactions_solvent_sample
        self.reactions_starting_material_sample = reactions_starting_material_sample
        self.research_plan = research_plan
        self.residue = residue
        self.sample = sample
        self.screen = screen
        self.screens_wellplate = screens_wellplate
        self.well = well
        self.wellplate = wellplate

    @staticmethod
    def from_dict(obj: Any) -> 'Schema':
        assert isinstance(obj, dict)
        attachment = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Attachment"))
        chemical = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Chemical"))
        collection = from_union([Collection.from_dict, from_none], obj.get("Collection"))
        collections_reaction = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("CollectionsReaction"))
        collections_research_plan = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("CollectionsResearchPlan"))
        collections_sample = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("CollectionsSample"))
        collections_screen = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("CollectionsScreen"))
        collections_wellplate = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("CollectionsWellplate"))
        container = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Container"))
        fingerprint = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Fingerprint"))
        labimotion_dataset_klass = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Labimotion::DatasetKlass"))
        labimotion_element_klass = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Labimotion::ElementKlass"))
        labimotion_segment_klass = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Labimotion::SegmentKlass"))
        literal = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Literal"))
        literature = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Literature"))
        molecule = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Molecule"))
        molecule_name = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("MoleculeName"))
        reaction = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Reaction"))
        reactions_product_sample = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("ReactionsProductSample"))
        reactions_purification_solvent_sample = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("ReactionsPurificationSolventSample"))
        reactions_reactant_sample = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("ReactionsReactantSample"))
        reactions_solvent_sample = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("ReactionsSolventSample"))
        reactions_starting_material_sample = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("ReactionsStartingMaterialSample"))
        research_plan = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("ResearchPlan"))
        residue = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Residue"))
        sample = from_union([Sample.from_dict, from_none], obj.get("Sample"))
        screen = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Screen"))
        screens_wellplate = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("ScreensWellplate"))
        well = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Well"))
        wellplate = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("Wellplate"))
        return Schema(attachment, chemical, collection, collections_reaction, collections_research_plan, collections_sample, collections_screen, collections_wellplate, container, fingerprint, labimotion_dataset_klass, labimotion_element_klass, labimotion_segment_klass, literal, literature, molecule, molecule_name, reaction, reactions_product_sample, reactions_purification_solvent_sample, reactions_reactant_sample, reactions_solvent_sample, reactions_starting_material_sample, research_plan, residue, sample, screen, screens_wellplate, well, wellplate)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.attachment is not None:
            result["Attachment"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.attachment)
        if self.chemical is not None:
            result["Chemical"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.chemical)
        if self.collection is not None:
            result["Collection"] = from_union([lambda x: to_class(Collection, x), from_none], self.collection)
        if self.collections_reaction is not None:
            result["CollectionsReaction"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.collections_reaction)
        if self.collections_research_plan is not None:
            result["CollectionsResearchPlan"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.collections_research_plan)
        if self.collections_sample is not None:
            result["CollectionsSample"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.collections_sample)
        if self.collections_screen is not None:
            result["CollectionsScreen"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.collections_screen)
        if self.collections_wellplate is not None:
            result["CollectionsWellplate"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.collections_wellplate)
        if self.container is not None:
            result["Container"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.container)
        if self.fingerprint is not None:
            result["Fingerprint"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.fingerprint)
        if self.labimotion_dataset_klass is not None:
            result["Labimotion::DatasetKlass"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.labimotion_dataset_klass)
        if self.labimotion_element_klass is not None:
            result["Labimotion::ElementKlass"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.labimotion_element_klass)
        if self.labimotion_segment_klass is not None:
            result["Labimotion::SegmentKlass"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.labimotion_segment_klass)
        if self.literal is not None:
            result["Literal"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.literal)
        if self.literature is not None:
            result["Literature"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.literature)
        if self.molecule is not None:
            result["Molecule"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.molecule)
        if self.molecule_name is not None:
            result["MoleculeName"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.molecule_name)
        if self.reaction is not None:
            result["Reaction"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.reaction)
        if self.reactions_product_sample is not None:
            result["ReactionsProductSample"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.reactions_product_sample)
        if self.reactions_purification_solvent_sample is not None:
            result["ReactionsPurificationSolventSample"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.reactions_purification_solvent_sample)
        if self.reactions_reactant_sample is not None:
            result["ReactionsReactantSample"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.reactions_reactant_sample)
        if self.reactions_solvent_sample is not None:
            result["ReactionsSolventSample"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.reactions_solvent_sample)
        if self.reactions_starting_material_sample is not None:
            result["ReactionsStartingMaterialSample"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.reactions_starting_material_sample)
        if self.research_plan is not None:
            result["ResearchPlan"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.research_plan)
        if self.residue is not None:
            result["Residue"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.residue)
        if self.sample is not None:
            result["Sample"] = from_union([lambda x: to_class(Sample, x), from_none], self.sample)
        if self.screen is not None:
            result["Screen"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.screen)
        if self.screens_wellplate is not None:
            result["ScreensWellplate"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.screens_wellplate)
        if self.well is not None:
            result["Well"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.well)
        if self.wellplate is not None:
            result["Wellplate"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.wellplate)
        return result


def schema_from_dict(s: Any) -> Schema:
    return Schema.from_dict(s)


def schema_to_dict(x: Schema) -> Any:
    return to_class(Schema, x)
