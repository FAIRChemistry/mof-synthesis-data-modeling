import os
from typing import Any

from fair_synthesis.formatting.utils import load_json


ConversionConfig = dict[str, Any]
ConversionSource = dict[str, Any]


def get_repo_root() -> str:
    current_file_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(current_file_dir, "..", ".."))


def load_conversion_config(repo_root: str | None = None) -> ConversionConfig:
    resolved_repo_root = repo_root or get_repo_root()
    return load_json(os.path.join(resolved_repo_root, "data", "conversion_sources.json"))


def get_source_by_id(config: ConversionConfig, source_id: str) -> ConversionSource:
    for source in config.get("sources", []):
        if source.get("id") == source_id:
            return source
    raise KeyError(f"Unknown conversion source: {source_id}")


def get_workflow_steps(config: ConversionConfig, source: ConversionSource) -> list[str]:
    workflow_id = source["workflow"]
    workflows = config.get("workflows", {})
    if workflow_id not in workflows:
        raise KeyError(f"Unknown workflow: {workflow_id}")
    return workflows[workflow_id]


def workflow_contains_step(
    config: ConversionConfig,
    source: ConversionSource,
    step_id: str,
) -> bool:
    return step_id in get_workflow_steps(config, source)


def get_source_root(repo_root: str, source: ConversionSource) -> str:
    return os.path.join(repo_root, source["root"])


def get_source_input_path(repo_root: str, source: ConversionSource) -> str:
    return os.path.join(get_source_root(repo_root, source), source["input"])


def get_source_optional(source: ConversionSource) -> bool:
    return bool(source.get("optional", False))


def get_source_options(source: ConversionSource) -> dict[str, Any]:
    return source.get("options", {})


def get_source_aux_path(repo_root: str, source: ConversionSource, key: str) -> str | None:
    relative_path = source.get(key)
    if not relative_path:
        return None
    return os.path.join(get_source_root(repo_root, source), relative_path)


def get_converted_dir(repo_root: str, config: ConversionConfig, source: ConversionSource) -> str:
    converted_folder = config["conventions"]["convertedFolder"]
    return os.path.join(get_source_root(repo_root, source), converted_folder)


def get_artifact_path(
    repo_root: str,
    config: ConversionConfig,
    source: ConversionSource,
    artifact_id: str,
) -> str:
    artifact_config = config["conventions"]["artifacts"][artifact_id]
    converted_dir = get_converted_dir(repo_root, config, source)
    fixed_name = artifact_config.get("fixedName")
    if fixed_name:
        return os.path.join(converted_dir, fixed_name)

    basename = source["basename"]
    prefix = artifact_config.get("prefix", "")
    suffix = artifact_config.get("suffix", "")
    extension = artifact_config.get("extension", "")
    return os.path.join(converted_dir, f"{prefix}{basename}{suffix}{extension}")


def ensure_converted_dir(repo_root: str, config: ConversionConfig, source: ConversionSource) -> str:
    converted_dir = get_converted_dir(repo_root, config, source)
    os.makedirs(converted_dir, exist_ok=True)
    return converted_dir


def iter_sources_for_step(
    config: ConversionConfig,
    step_id: str,
) -> list[ConversionSource]:
    return [
        source
        for source in config.get("sources", [])
        if workflow_contains_step(config, source, step_id)
    ]
