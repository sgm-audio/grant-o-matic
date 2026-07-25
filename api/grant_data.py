"""
Helpers for resolving and loading grant JSON data.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, List, Optional


DEFAULT_GRANTS_FILENAME = "all_grants.json"


def resolve_grant_data_dir(explicit_path: Optional[str] = None) -> Path:
    """
    Resolve the directory that contains grant JSON files.

    Priority:
    1. explicit_path argument
    2. GRANT_DATA_PATH environment variable
    3. repository ``data/`` directory (sibling of ``api/``)
    """
    if explicit_path:
        return Path(explicit_path).expanduser().resolve()

    env_path = os.environ.get("GRANT_DATA_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()

    return (Path(__file__).resolve().parent.parent / "data").resolve()


def resolve_grants_file(
    data_dir: Optional[str | Path] = None,
    filename: str = DEFAULT_GRANTS_FILENAME,
) -> Path:
    """Return the full path to the primary grants JSON file."""
    base = Path(data_dir) if data_dir is not None else resolve_grant_data_dir()
    return (base / filename).resolve()


def load_grants_from_path(filepath: str | Path) -> List[dict[str, Any]]:
    """
    Load grants from a JSON file.

    Returns an empty list if the file is missing or invalid.
    """
    path = Path(filepath)
    if not path.is_file():
        return []

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return data


def load_grants(
    data_dir: Optional[str] = None,
    filename: str = DEFAULT_GRANTS_FILENAME,
) -> List[dict[str, Any]]:
    """Load grants using GRANT_DATA_PATH / default data directory resolution."""
    grants_file = resolve_grants_file(data_dir=data_dir, filename=filename)
    return load_grants_from_path(grants_file)
