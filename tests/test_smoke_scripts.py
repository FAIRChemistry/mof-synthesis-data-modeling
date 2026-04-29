import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


SMOKE_COMMANDS = [
    (
        "mofsy2mpif",
        ["node", "--experimental-transform-types", "scripts/mofsy2mpif/src/mofsy2mpif.ts"],
    ),
    (
        "format_and_serialize_all",
        [sys.executable, "scripts/format_and_serialize_all.py"],
    ),
    (
        "mofsy_api_example",
        [sys.executable, "scripts/mofsy_api_example.py"],
    ),
]


@pytest.mark.parametrize(("name", "command"), SMOKE_COMMANDS)
def test_smoke_script_runs_without_failure(
    name: str,
    command: list[str],
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    shutil.copytree(
        REPO_ROOT,
        worktree,
        ignore=shutil.ignore_patterns(
            ".git",
            ".idea",
            ".pytest_cache",
            "__pycache__",
            "*.pyc",
        ),
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(worktree / "src")
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("MPLCONFIGDIR", "/tmp/fairsynthesis-matplotlib")
    env.setdefault("XDG_CACHE_HOME", "/tmp/fairsynthesis-xdg-cache")
    env.setdefault("MPIF_CREATION_DATE", "2026-01-26")

    result = subprocess.run(
        command,
        cwd=worktree,
        env=env,
        text=True,
        capture_output=True,
        timeout=180,
    )

    assert result.returncode == 0, (
        f"{name} failed with exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
