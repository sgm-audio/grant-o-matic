"""
Simple test for the Grant-O-Matic API
"""
from fastapi.testclient import TestClient
import sys
import os
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
    """Test the health endpoint"""
    test_app = create_test_app()
    client = TestClient(test_app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

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

if __name__ == "__main__":
    test_root_endpoint()
    test_health_endpoint()
    test_match_endpoint()
    print("All tests passed!")