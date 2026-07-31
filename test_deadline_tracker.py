"""
Unit tests for DeadlineTracker (date parsing, upcoming/passed, ICS).
"""
from __future__ import annotations

import datetime
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from deadline_tracker import DeadlineTracker  # noqa: E402


SAMPLE_GRANTS = [
    {
        "id": "g1",
        "program_name": "Program Soon",
        "administering_agency": "FACTOR",
        "url": "https://www.factor.ca/programs/artist-programs/artist-development/",
        "deadline_info": {
            "frequency": "Scheduled",
            "next_deadline": (datetime.date.today() + datetime.timedelta(days=5)).isoformat(),
            "application_window": "See factor.ca",
        },
    },
    {
        "id": "g2",
        "program_name": "Program Far",
        "administering_agency": "FACTOR",
        "url": "https://www.factor.ca/programs/artist-programs/video/",
        "deadline_info": {
            "frequency": "Rolling",
            "next_deadline": (datetime.date.today() + datetime.timedelta(days=90)).isoformat(),
            "application_window": None,
        },
    },
    {
        "id": "g3",
        "program_name": "Program Past",
        "administering_agency": "Canada Council for the Arts",
        "url": "https://canadacouncil.ca/funding/grants/explore-and-create",
        "deadline_info": {
            "frequency": "Scheduled",
            "next_deadline": (datetime.date.today() - datetime.timedelta(days=3)).isoformat(),
            "application_window": None,
        },
    },
    {
        "id": "g4",
        "program_name": "No Deadline",
        "administering_agency": "Canada Council for the Arts",
        "url": "https://canadacouncil.ca/funding/grants/engage-and-sustain",
        "deadline_info": {
            "frequency": "See deadlines page",
            "next_deadline": None,
            "application_window": "https://canadacouncil.ca/funding/grants/deadlines",
        },
    },
]


class DeadlineTrackerTests(unittest.TestCase):
    def setUp(self):
        self.tracker = DeadlineTracker()
        self.tracker.load_deadlines_from_grants(SAMPLE_GRANTS)

    def test_loads_only_parsable_deadlines(self):
        self.assertEqual(len(self.tracker.deadlines), 3)

    def test_upcoming_within_window(self):
        upcoming = self.tracker.get_upcoming_deadlines(days_ahead=14)
        ids = [d["id"] for d in upcoming]
        self.assertEqual(ids, ["g1"])
        self.assertEqual(upcoming[0]["days_until"], 5)

    def test_passed_deadlines(self):
        passed = self.tracker.get_passed_deadlines(days_back=14)
        self.assertEqual([d["id"] for d in passed], ["g3"])

    def test_all_deadlines_sorted(self):
        all_deadlines = self.tracker.get_all_deadlines()
        self.assertEqual([d["id"] for d in all_deadlines], ["g3", "g1", "g2"])
        self.assertEqual(all_deadlines[0]["status"], "passed")
        self.assertEqual(all_deadlines[1]["status"], "upcoming")

    def test_invalid_date_skipped(self):
        tracker = DeadlineTracker()
        tracker.load_deadlines_from_grants(
            [
                {
                    "id": "bad",
                    "program_name": "Bad",
                    "administering_agency": "FACTOR",
                    "deadline_info": {"next_deadline": "not-a-date"},
                    "url": "https://www.factor.ca/",
                }
            ]
        )
        self.assertEqual(tracker.deadlines, [])

    def test_generate_ics_contains_event(self):
        ics = self.tracker.generate_ics(days_ahead=14)
        self.assertIn("BEGIN:VCALENDAR", ics)
        self.assertIn("BEGIN:VEVENT", ics)
        self.assertIn("Program Soon deadline", ics)
        self.assertIn("https://www.factor.ca/programs/artist-programs/artist-development/", ics)
        self.assertIn("END:VCALENDAR", ics)

    def test_reload_replaces_deadlines(self):
        self.tracker.load_deadlines_from_grants(SAMPLE_GRANTS[:1])
        self.assertEqual(len(self.tracker.deadlines), 1)
        self.assertEqual(self.tracker.deadlines[0]["id"], "g1")


if __name__ == "__main__":
    unittest.main()
