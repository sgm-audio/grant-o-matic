"""
Fixture-based scraper tests (no live network).
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(ROOT))

from canada_council import CanadaCouncilScraper  # noqa: E402
from common import generate_grant_id, parse_iso_dates_from_text, parse_money_amounts  # noqa: E402
from factor import FactorScraper  # noqa: E402
from pipeline import merge_grants, run_scrape_and_persist  # noqa: E402

FIXTURES = ROOT / "fixtures"


class CommonHelperTests(unittest.TestCase):
    def test_generate_id_stable(self):
        url = "https://canadacouncil.ca/funding/grants/explore-and-create"
        self.assertEqual(generate_grant_id(url), generate_grant_id(url))
        self.assertEqual(len(generate_grant_id(url)), 8)

    def test_parse_money(self):
        self.assertEqual(parse_money_amounts("up to $5,000 and $25,000"), [5000.0, 25000.0])

    def test_parse_dates(self):
        self.assertEqual(
            parse_iso_dates_from_text("The application deadline is September 10, 2026."),
            ["2026-09-10"],
        )


class CanadaCouncilFixtureTests(unittest.TestCase):
    def setUp(self):
        self.scraper = CanadaCouncilScraper()
        self.index = (FIXTURES / "canada_council" / "grants_index.html").read_text(encoding="utf-8")

    def test_parse_program_links(self):
        links = self.scraper.parse_program_links(self.index)
        urls = {item["url"] for item in links}
        self.assertIn("https://canadacouncil.ca/funding/grants/explore-and-create", urls)
        self.assertIn("https://canadacouncil.ca/funding/grants/engage-and-sustain", urls)
        self.assertGreaterEqual(len(links), 5)

    def test_parse_program_page(self):
        html = (FIXTURES / "canada_council" / "explore-and-create.html").read_text(encoding="utf-8")
        grant = self.scraper.parse_program_page(
            html, "https://canadacouncil.ca/funding/grants/explore-and-create"
        )
        self.assertEqual(grant["administering_agency"], "Canada Council for the Arts")
        self.assertEqual(grant["program_name"], "Explore and Create")
        self.assertTrue(grant["description"])
        self.assertIsNone(grant["funding_details"]["max_amount"])
        self.assertIsNone(grant["deadline_info"]["next_deadline"])
        self.assertTrue(grant["url"].startswith("https://canadacouncil.ca/"))

    def test_scrape_all_from_fixtures(self):
        grants = self.scraper.scrape_all_grants(fixture_dir=FIXTURES / "canada_council")
        self.assertGreaterEqual(len(grants), 5)
        agencies = {g["administering_agency"] for g in grants}
        self.assertEqual(agencies, {"Canada Council for the Arts"})


class FactorFixtureTests(unittest.TestCase):
    def setUp(self):
        self.scraper = FactorScraper()

    def test_parse_artist_program_links(self):
        html = (FIXTURES / "factor" / "artist-programs.html").read_text(encoding="utf-8")
        links = self.scraper.parse_artist_program_links(html)
        urls = {item["url"] for item in links}
        self.assertTrue(any("artist-development" in u for u in urls))
        self.assertTrue(any("juried-sound-recording-album" in u for u in urls))

    def test_parse_album_program(self):
        html = (FIXTURES / "factor" / "juried-sound-recording-album.html").read_text(encoding="utf-8")
        grant = self.scraper.parse_program_page(
            html,
            "https://www.factor.ca/programs/artist-programs/juried-sound-recording-album/",
        )
        self.assertEqual(grant["administering_agency"], "FACTOR")
        self.assertIn("Juried Sound Recording", grant["program_name"])
        self.assertEqual(grant["funding_details"]["max_amount"], 10000.0)
        self.assertEqual(grant["deadline_info"]["next_deadline"], "2026-09-10")
        self.assertTrue(grant["url"].startswith("https://www.factor.ca/"))

    def test_scrape_all_from_fixtures(self):
        grants = self.scraper.scrape_all_grants(fixture_dir=FIXTURES / "factor")
        self.assertGreaterEqual(len(grants), 4)
        names = {g["program_name"] for g in grants}
        self.assertTrue(any("Artist Development" in n for n in names))


class PipelineTests(unittest.TestCase):
    def test_merge_and_persist_fixtures(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_scrape_and_persist(
                use_fixtures=True,
                fixture_root=FIXTURES,
                data_dir=tmp,
            )
            self.assertGreaterEqual(result["count"], 9)
            self.assertIn("Canada Council for the Arts", result["agencies"])
            self.assertIn("FACTOR", result["agencies"])
            path = Path(result["path"])
            self.assertTrue(path.is_file())
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(len(loaded), result["count"])

    def test_merge_by_id(self):
        a = [{"id": "1", "program_name": "A"}]
        b = [{"id": "1", "program_name": "B"}, {"id": "2", "program_name": "C"}]
        merged = merge_grants(a, b)
        self.assertEqual(len(merged), 2)
        self.assertEqual(next(g for g in merged if g["id"] == "1")["program_name"], "B")


if __name__ == "__main__":
    unittest.main()
