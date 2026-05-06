import os
import subprocess

from fair_synthesis.conversion_config import (
    get_artifact_path,
    get_repo_root,
    get_source_aux_path,
    get_source_input_path,
    get_source_optional,
    get_workflow_steps,
    load_conversion_config,
)
from fair_synthesis.formatting.chemotion2mofsy import run_chemotion_source
from fair_synthesis.formatting.fe_terephthalate2mofsy import run_fe_terephthalate_source
from fair_synthesis.formatting.sciformation2mofsy import run_sciformation_source
from fair_synthesis.serialization.extract_interesting_params import (
    run_extract_interesting_params_for_source,
)
from fair_synthesis.serialization.mofsy2xdl import run_mofsy2xdl_for_source


def run_mofsy2mpif_for_source(repo_root: str, config: dict, source: dict) -> bool:
    procedure_path = get_artifact_path(repo_root, config, source, "procedure")
    characterization_path = get_artifact_path(repo_root, config, source, "characterization")
    output_folder_path = get_artifact_path(repo_root, config, source, "mpif_output_folder")
    params_path = get_source_aux_path(repo_root, source, "mpifParams")

    missing_paths = [
        path
        for path in (procedure_path, characterization_path, params_path)
        if path and not os.path.exists(path)
    ]
    if missing_paths:
        print(f"Skipping MPIF conversion for {source['id']} because inputs are missing.")
        return False

    result = subprocess.run(
        [
            "node",
            "--experimental-transform-types",
            "scripts/mofsy2mpif/src/mofsy2mpif.ts",
            "--procedure-path",
            procedure_path,
            "--characterization-path",
            characterization_path,
            "--output-folder-path",
            output_folder_path,
            "--params-path",
            params_path,
        ],
        cwd=repo_root,
        text=True,
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, result.args)
    return True


def main() -> int:
    repo_root = get_repo_root()
    config = load_conversion_config(repo_root)
    step_runners = {
        "sciformation_to_mofsy": lambda source: run_sciformation_source(repo_root, config, source),
        "chemotion_to_mofsy_with_text_extraction": lambda source: run_chemotion_source(
            repo_root, config, source, enrich_descriptions=True),
        "chemotion_to_mofsy_without_text_extraction": lambda source: run_chemotion_source(
            repo_root, config, source, enrich_descriptions=False),
        "fe_terephthalate_to_mofsy": lambda source: run_fe_terephthalate_source(repo_root, config, source),
        "mofsy_to_xdl": lambda source: run_mofsy2xdl_for_source(repo_root, config, source),
        "extract_mocof1_params": lambda source: run_extract_interesting_params_for_source(repo_root, config, source),
        "mofsy_to_mpif": lambda source: run_mofsy2mpif_for_source(repo_root, config, source),
    }

    for source in config.get("sources", []):
        input_path = get_source_input_path(repo_root, source)
        if not os.path.exists(input_path):
            if get_source_optional(source):
                print(f"Skipping optional source {source['id']} because input is missing: {input_path}")
                continue
            raise FileNotFoundError(f"Required input file is missing for source {source['id']}: {input_path}")

        for step_id in get_workflow_steps(config, source):
            runner = step_runners.get(step_id)
            if runner is None:
                raise KeyError(f"No runner registered for workflow step: {step_id}")
            runner(source)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
