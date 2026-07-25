"""Unit tests for grant data path resolution and loading."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from grant_data import (
    load_grants,
    load_grants_from_path,
    resolve_grant_data_dir,
    resolve_grants_file,
)


class GrantDataTests(unittest.TestCase):
    def test_resolve_default_data_dir(self):
        env_backup = os.environ.pop("GRANT_DATA_PATH", None)
        try:
            data_dir = resolve_grant_data_dir()
            self.assertTrue(data_dir.name == "data")
            self.assertTrue((data_dir / "all_grants.json").is_file())
        finally:
            if env_backup is not None:
                os.environ["GRANT_DATA_PATH"] = env_backup

    def test_resolve_honors_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["GRANT_DATA_PATH"] = tmp
            try:
                self.assertEqual(resolve_grant_data_dir(), Path(tmp).resolve())
                self.assertEqual(
                    resolve_grants_file(),
                    (Path(tmp) / "all_grants.json").resolve(),
                )
            finally:
                del os.environ["GRANT_DATA_PATH"]

    def test_load_grants_from_repo_data(self):
        env_backup = os.environ.pop("GRANT_DATA_PATH", None)
        try:
            grants = load_grants()
            self.assertGreater(len(grants), 0)
            self.assertIn("id", grants[0])
            self.assertIn("program_name", grants[0])
        finally:
            if env_backup is not None:
                os.environ["GRANT_DATA_PATH"] = env_backup

    def test_load_grants_from_custom_path(self):
        sample = [{"id": "x", "program_name": "Test"}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "all_grants.json"
            path.write_text(json.dumps(sample), encoding="utf-8")
            loaded = load_grants(data_dir=tmp)
            self.assertEqual(loaded, sample)

    def test_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_grants_from_path(Path(tmp) / "missing.json"), [])


if __name__ == "__main__":
    unittest.main()
