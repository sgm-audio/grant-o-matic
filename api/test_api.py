"""
Simple test for the Grant-O-Matic API
"""
from fastapi.testclient import TestClient
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Sample grant data for testing
SAMPLE_GRANTS = [
    {
        "id": "grant001",
        "program_name": "Juried Sound Recording",
        "administering_agency": "FACTOR",
        "description": "Support for the creation and production of sound recordings by Canadian artists.",
        "eligibility_criteria": {
            "artist_type": ["individual", "group"],
            "residency_requirements": ["Canadian citizen", "Permanent resident"],
            "genre_restrictions": ["All genres"],
            "career_stage": ["Emerging", "Established"],
            "project_type": ["Recording", "Production"]
        },
        "deadline_info": {
            "frequency": "Quarterly",
            "next_deadline": "2024-03-15",
            "application_window": "2024-01-01 to 2024-03-15"
        },
        "funding_details": {
            "min_amount": 5000,
            "max_amount": 50000,
            "average_award": 20000,
            "funding_type": "Grant",
            "requires_matching_funds": True,
            "matching_requirements": "1:1 matching funds required"
        },
        "application_requirements": [
            "Project description",
            "Budget",
            "Work samples (audio)",
            "Artist bio",
            "Marketing plan",
            "Letters of support"
        ],
        "assessment_criteria": [
            "Artistic merit",
            "Market potential",
            "Project feasibility"
        ],
        "url": "https://factor.ca/programs/juried-sound-recording/",
        "last_updated": "2024-01-15",
        "status": "Active"
    },
    {
        "id": "grant002",
        "program_name": "Artist Development",
        "administering_agency": "FACTOR",
        "description": "Emerging artist development funding for recording and market development.",
        "eligibility_criteria": {
            "artist_type": ["individual", "group"],
            "residency_requirements": ["Canadian citizen", "Permanent resident"],
            "genre_restrictions": ["All genres"],
            "career_stage": ["Emerging"],
            "project_type": ["Recording", "Marketing", "Touring"]
        },
        "deadline_info": {
            "frequency": "Rolling",
            "next_deadline": "2024-06-30",
            "application_window": "Ongoing"
        },
        "funding_details": {
            "min_amount": 2000,
            "max_amount": 5000,
            "average_award": 3500,
            "funding_type": "Grant",
            "requires_matching_funds": True,
            "matching_requirements": "25% artist contribution (can be sweat equity)"
        },
        "application_requirements": [
            "Project description",
            "Budget",
            "Work samples",
            "Artist bio",
            "Marketing plan"
        ],
        "assessment_criteria": [
            "Artistic merit",
            "Career development potential",
            "Project feasibility"
        ],
        "url": "https://factor.ca/programs/artist-development/",
        "last_updated": "2024-01-10",
        "status": "Active"
    }
]

def create_test_app():
    """Create a test app with pre-loaded grant data"""
    # Import here to avoid circular imports
    from main import app
    from ai_model.enhanced_matching_engine import EnhancedGrantMatchingEngine

    # Override the matching engine with our test data
    import main
    main.matching_engine = EnhancedGrantMatchingEngine(SAMPLE_GRANTS)

    return app

def test_root_endpoint():
    """Test the root endpoint"""
    test_app = create_test_app()
    client = TestClient(test_app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Grant-O-Matic API" in data["message"]

def test_health_endpoint():
    """Test the health endpoint reports grants_loaded"""
    test_app = create_test_app()
    client = TestClient(test_app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["grants_loaded"] == len(SAMPLE_GRANTS)
    assert data["grants_loaded"] > 0

def test_grants_endpoint():
    """Smoke test for listing grants"""
    test_app = create_test_app()
    client = TestClient(test_app)
    response = client.get("/grants")
    assert response.status_code == 200
    data = response.json()
    assert "grants" in data
    assert "total_count" in data
    assert data["total_count"] == len(SAMPLE_GRANTS)
    assert len(data["grants"]) == len(SAMPLE_GRANTS)
    assert data["grants"][0]["id"] == "grant001"

def test_health_with_repo_grant_data():
    """Confirm /health grants_loaded matches data/all_grants.json via GRANT_DATA_PATH."""
    try:
        from api.grant_data import load_grants
    except ImportError:
        from grant_data import load_grants
    from ai_model.enhanced_matching_engine import EnhancedGrantMatchingEngine
    import main

    repo_data = os.path.join(os.path.dirname(__file__), "..", "data")
    os.environ["GRANT_DATA_PATH"] = os.path.abspath(repo_data)
    grants = load_grants()
    assert len(grants) > 0

    main.matching_engine = EnhancedGrantMatchingEngine(grants)
    client = TestClient(main.app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["grants_loaded"] == len(grants)

def test_match_endpoint():
    """Test the match endpoint with sample data"""
    test_app = create_test_app()
    client = TestClient(test_app)

    response = client.post("/match", json={
        "project_description": "I am an emerging electronic music producer based in Toronto working on my debut EP",
        "artist_type": "individual",
        "residency": "Canadian citizen",
        "genre": "electronic",
        "project_type": "Recording",
        "budget_amount": 15000.00
    })
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "grants" in data
    assert "total_count" in data
    assert "timestamp" in data
    # Should have at least one grant match
    assert len(data["grants"]) > 0
    # Check that the first grant has expected fields
    first_grant = data["grants"][0]
    assert "program_name" in first_grant
    assert "match_score" in first_grant
    assert "match_grade" in first_grant
    # Check that budget suggestion is included when budget is provided
    assert "budget_suggestion" in first_grant

def test_scrape_endpoint_reloads_grants():
    """POST /scrape with fixtures persists grants and reloads the engine (no live network)."""
    import tempfile
    from ai_model.enhanced_matching_engine import EnhancedGrantMatchingEngine
    import main

    with tempfile.TemporaryDirectory() as tmp:
        os.environ["GRANT_DATA_PATH"] = tmp
        main.matching_engine = EnhancedGrantMatchingEngine([])
        main.deadline_tracker.clear()
        main.scrape_status.update(
            {
                "status": "idle",
                "last_run": None,
                "last_error": None,
                "grants_count": 0,
                "agencies": [],
            }
        )
        client = TestClient(main.app)

        response = client.post("/scrape?use_fixtures=true")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "started"
        assert body["use_fixtures"] is True

        status = client.get("/scrape/status").json()
        assert status["status"] == "completed", status
        assert status["grants_count"] >= 9
        assert "FACTOR" in status["agencies"]
        assert "Canada Council for the Arts" in status["agencies"]

        grants_resp = client.get("/grants")
        assert grants_resp.status_code == 200
        grants_data = grants_resp.json()
        assert grants_data["total_count"] >= 9
        agencies = {g["administering_agency"] for g in grants_data["grants"]}
        assert "FACTOR" in agencies
        assert "Canada Council for the Arts" in agencies

        match_resp = client.post(
            "/match",
            json={
                "project_description": "Recording a debut EP as a Canadian musician",
                "artist_type": "individual",
                "project_type": "Recording",
                "limit": 5,
            },
        )
        assert match_resp.status_code == 200
        assert len(match_resp.json()["grants"]) > 0

        # Deadlines should reload from scraped grant data
        deadlines_resp = client.get("/deadlines?days_ahead=400")
        assert deadlines_resp.status_code == 200
        deadlines_data = deadlines_resp.json()
        assert deadlines_data["tracked_count"] >= 1
        assert deadlines_data["alert_channel"] == "ics"

def test_deadlines_endpoints_with_repo_data():
    """Deadlines and ICS export use loaded grant next_deadline values only."""
    from ai_model.enhanced_matching_engine import EnhancedGrantMatchingEngine
    from deadline_tracker import DeadlineTracker
    import main

    try:
        from api.grant_data import load_grants
    except ImportError:
        from grant_data import load_grants

    repo_data = os.path.join(os.path.dirname(__file__), "..", "data")
    os.environ["GRANT_DATA_PATH"] = os.path.abspath(repo_data)
    grants = load_grants()
    main.matching_engine = EnhancedGrantMatchingEngine(grants)
    main.deadline_tracker = DeadlineTracker()
    main.deadline_tracker.load_deadlines_from_grants(grants)

    client = TestClient(main.app)
    health = client.get("/health").json()
    assert health["deadlines_tracked"] == len(main.deadline_tracker.deadlines)

    response = client.get("/deadlines?days_ahead=500")
    assert response.status_code == 200
    data = response.json()
    assert data["tracked_count"] >= 1
    for item in data["deadlines"]:
        assert item.get("url")
        assert item.get("deadline_date")
        assert "factor.ca" in item["url"] or "canadacouncil.ca" in item["url"]

    ics = client.get("/deadlines/export.ics?days_ahead=500")
    assert ics.status_code == 200
    assert "text/calendar" in ics.headers.get("content-type", "")
    assert "BEGIN:VCALENDAR" in ics.text
    assert "BEGIN:VEVENT" in ics.text

    alerts = client.get("/deadlines/alerts?days_ahead=500").json()
    assert "alerts" in alerts

if __name__ == "__main__":
    test_root_endpoint()
    test_health_endpoint()
    test_grants_endpoint()
    test_health_with_repo_grant_data()
    test_match_endpoint()
    test_scrape_endpoint_reloads_grants()
    test_deadlines_endpoints_with_repo_data()

    # Also run grant_data + deadline tracker unit tests
    loader = unittest.TestLoader()
    for module_name in ("test_grant_data",):
        suite = loader.loadTestsFromName(module_name)
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        if not result.wasSuccessful():
            raise SystemExit(1)

    root = os.path.join(os.path.dirname(__file__), "..")
    sys.path.insert(0, root)
    suite = loader.loadTestsFromName("test_deadline_tracker")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)

    # Compose file structural check (no Docker daemon required)
    from pathlib import Path
    scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
    sys.path.insert(0, str(scripts_dir))
    from validate_compose import main as validate_compose_main
    if validate_compose_main() != 0:
        raise SystemExit(1)

    print("All tests passed!")
