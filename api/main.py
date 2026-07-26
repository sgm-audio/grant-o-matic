"""
Grant-O-Matic API Main Module
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys
from datetime import datetime

# Import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai_model.enhanced_matching_engine import EnhancedGrantMatchingEngine, GrantMatch
from deadline_tracker import DeadlineTracker
try:
    from api.grant_data import load_grants, resolve_grants_file
except ImportError:  # pragma: no cover - script-style imports (python api/test_api.py)
    from grant_data import load_grants, resolve_grants_file
# We'll import the scraper when we implement it fully

app = FastAPI(
    title="Grant-O-Matic API",
    description="AI-powered grant matching system for Canadian artists",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ProjectRequest(BaseModel):
    project_description: str
    artist_type: Optional[str] = None
    residency: Optional[str] = None
    genre: Optional[str] = None
    project_type: Optional[str] = None
    budget_amount: Optional[float] = None
    limit: Optional[int] = 10

class GrantMatchResponse(BaseModel):
    id: str
    program_name: str
    administering_agency: str
    match_score: float
    match_grade: str
    eligibility_score: float
    project_type_score: float
    keyword_score: float
    complexity_score: float
    matched_criteria: List[str]
    missing_criteria: List[str]
    description: str
    deadline_info: Dict[str, Any]
    funding_details: Dict[str, Any]
    application_requirements: List[str]
    assessment_criteria: List[str]
    url: str
    budget_suggestion: Optional[Dict[str, Any]] = None

class GrantListResponse(BaseModel):
    grants: List[GrantMatchResponse]
    total_count: int
    timestamp: str

# Global variable to hold our matching engine
matching_engine = None
scrape_status: Dict[str, Any] = {
    "status": "idle",
    "last_run": None,
    "last_error": None,
    "grants_count": 0,
    "agencies": [],
}


def reload_matching_engine_from_disk() -> int:
    """Reload grants from GRANT_DATA_PATH into the matching engine."""
    global matching_engine
    if matching_engine is None:
        matching_engine = EnhancedGrantMatchingEngine()
    grants = load_grants()
    matching_engine.grants = grants
    return len(grants)


@app.on_event("startup")
async def startup_event():
    """Initialize the matching engine on startup"""
    global matching_engine
    matching_engine = EnhancedGrantMatchingEngine()

    grants_file = resolve_grants_file()
    count = reload_matching_engine_from_disk()
    if count:
        print(f"Loaded {count} grants from {grants_file}")
    else:
        print(f"No grant data found at {grants_file}. Please run the scraper first.")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Grant-O-Matic API",
        "version": "1.0.0",
        "description": "AI-powered grant matching system for Canadian artists",
        "docs": "/docs"
    }

@app.post("/match", response_model=GrantListResponse)
async def match_grants(request: ProjectRequest):
    """
    Match a project description to available grants
    """
    if not matching_engine:
        raise HTTPException(status_code=503, detail="Matching engine not initialized")
    
    try:
        matches = matching_engine.match_project_to_grants(
            project_description=request.project_description,
            artist_type=request.artist_type,
            residency=request.residency,
            genre=request.genre,
            project_type=request.project_type,
            budget_amount=request.budget_amount
        )
        
        # Limit results
        limited_matches = matching_engine.get_top_matches(matches, request.limit)
        
        # Format for response
        formatted_matches = [
            matching_engine.format_match_for_display(match)
            for match in limited_matches
        ]
        
        return GrantListResponse(
            grants=formatted_matches,
            total_count=len(matches),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/grants")
async def get_all_grants(skip: int = 0, limit: int = 100):
    """
    Get all grants in the database
    """
    if not matching_engine or not matching_engine.grants:
        raise HTTPException(status_code=404, detail="No grant data available")
    
    # Return a slice of grants
    grants_slice = matching_engine.grants[skip:skip+limit]
    
    # Format for response (simplified)
    formatted_grants = []
    for grant in grants_slice:
        formatted_grants.append({
            "id": grant.get("id"),
            "program_name": grant.get("program_name"),
            "administering_agency": grant.get("administering_agency"),
            "description": grant.get("description")[:200] + "..." if len(grant.get("description", "")) > 200 else grant.get("description"),
            "deadline_info": grant.get("deadline_info"),
            "funding_details": grant.get("funding_details")
        })
    
    return {
        "grants": formatted_grants,
        "total_count": len(matching_engine.grants),
        "skip": skip,
        "limit": limit
    }

@app.get("/grants/{grant_id}")
async def get_grant(grant_id: str):
    """
    Get a specific grant by ID
    """
    if not matching_engine or not matching_engine.grants:
        raise HTTPException(status_code=404, detail="No grant data available")
    
    # Find grant by ID
    grant = None
    for g in matching_engine.grants:
        if g.get("id") == grant_id:
            grant = g
            break
    
    if not grant:
        raise HTTPException(status_code=404, detail=f"Grant with ID {grant_id} not found")
    
    return grant

@app.post("/scrape")
async def trigger_scrape(
    background_tasks: BackgroundTasks,
    use_fixtures: bool = False,
):
    """
    Trigger a background scrape of grant databases and reload the matching engine.

    Set ``use_fixtures=true`` for offline/CI runs (no live network).
    """
    if scrape_status.get("status") == "running":
        return {
            "message": "Scrape already in progress",
            "status": "running",
            "scrape": scrape_status,
        }

    scrape_status["status"] = "queued"
    scrape_status["last_error"] = None
    background_tasks.add_task(run_scraper_background, use_fixtures)
    return {
        "message": "Scraping triggered in background",
        "status": "started",
        "use_fixtures": use_fixtures,
    }


@app.get("/scrape/status")
async def get_scrape_status():
    """Return the latest scrape job status."""
    return scrape_status


async def run_scraper_background(use_fixtures: bool = False):
    """Background task to run scrapers, persist JSON, and reload the engine."""
    from scraper.pipeline import run_scrape_and_persist

    scrape_status["status"] = "running"
    scrape_status["last_run"] = datetime.now().isoformat()
    try:
        result = run_scrape_and_persist(use_fixtures=use_fixtures)
        count = reload_matching_engine_from_disk()
        scrape_status.update(
            {
                "status": "completed",
                "last_error": None,
                "grants_count": count,
                "agencies": result.get("agencies", []),
                "path": result.get("path"),
            }
        )
        print(
            f"Scrape completed: {count} grants from {', '.join(result.get('agencies', []))}"
        )
    except Exception as exc:  # pragma: no cover - exercised via API tests with fixtures
        scrape_status["status"] = "failed"
        scrape_status["last_error"] = str(exc)
        print(f"Scrape failed: {exc}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    agencies = sorted(
        {
            g.get("administering_agency")
            for g in (matching_engine.grants if matching_engine and matching_engine.grants else [])
            if g.get("administering_agency")
        }
    )
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "grants_loaded": len(matching_engine.grants) if matching_engine and matching_engine.grants else 0,
        "agencies": agencies,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)