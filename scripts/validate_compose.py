#!/usr/bin/env python3
"""Lightweight validation that docker-compose.yml declares API + frontend services."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


REQUIRED_SERVICES = ("api", "frontend")


def validate_compose(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        # Minimal fallback: ensure service keys appear as top-level headings under services
        if "services:" not in text:
            raise AssertionError(f"{path}: missing services key")
        for name in REQUIRED_SERVICES:
            if f"{name}:" not in text:
                raise AssertionError(f"{path}: missing service '{name}'")
        return

    assert isinstance(data, dict), f"{path}: expected mapping"
    services = data.get("services")
    assert isinstance(services, dict), f"{path}: services must be a mapping"
    for name in REQUIRED_SERVICES:
        assert name in services, f"{path}: missing service '{name}'"
        assert "build" in services[name] or "image" in services[name], (
            f"{path}: service '{name}' needs build or image"
        )
    assert "ports" in services["api"], f"{path}: api missing ports"
    assert "ports" in services["frontend"], f"{path}: frontend missing ports"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    compose = root / "docker-compose.yml"
    assert compose.is_file(), f"missing {compose}"
    validate_compose(compose)
    print("docker-compose.yml looks valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
