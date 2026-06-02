"""
Grant-O-Matic AI Matching Engine
"""
import json
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class GrantMatch:
    grant_id: str
    program_name: str
    administering_agency: str
    match_score: float
    eligibility_score: float
    project_type_score: float
    keyword_score: float
    complexity_score: float
    details: Dict[str, Any]
    matched_criteria: List[str]
    missing_criteria: List[str]

class GrantMatchingEngine:
    def __init__(self, grants_data: List[Dict] = None):
        self.grants = grants_data or []
        # Weights for different scoring components
        self.weights = {
            'eligibility': 0.4,
            'project_type': 0.3,
            'keywords': 0.2,
            'complexity': 0.1  # Lower complexity is better (higher score for simpler applications)
        }
        
        # Common keywords for different art forms (can be expanded)
        self.art_keywords = {
            'music': ['music', 'song', 'album', 'ep', 'lp', 'track', 'composition', 'melody', 'rhythm', 
                     'instrument', 'vocal', 'choir', 'band', 'orchestra', 'jazz', 'classical', 'rock', 
                     'pop', 'hip hop', 'electronic', 'folk', 'world music', 'experimental'],
            'visual_arts': ['painting', 'sculpture', 'photography', 'installation', 'video art', 
                           'digital art', 'printmaking', 'ceramics', 'textile', 'drawing'],
            'performing_arts': ['theatre', 'dance', 'performance', 'opera', 'ballet', 'circus', 
                               'spoken word', 'storytelling', 'puppetry'],
            'literary_arts': ['poetry', 'fiction', 'non-fiction', 'novel', 'short story', 
                             'playwriting', 'screenwriting', 'criticism'],
            'media_arts': ['film', 'video', 'animation', 'documentary', 'new media', 'interactive', 
                          'virtual reality', 'augmented reality', 'game design']
        }
    
    def load_grants_from_file(self, filepath: str):
        """Load grant data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                self.grants = json.load(f)
            logger.info(f"Loaded {len(self.grants)} grants from {filepath}")
        except Exception as e:
            logger.error(f"Error loading grants from {filepath}: {e}")
            self.grants = []
    
    def match_project_to_grants(self, project_description: str, 
                               artist_type: str = None,
                               residency: str = None,
                               genre: str = None,
                               project_type: str = None) -> List[GrantMatch]:
        """
        Match a project description to available grants
        
        Args:
            project_description: Description of the artistic project
            artist_type: Individual, group, organization, etc.
            residency: Canadian citizen, permanent resident, etc.
            genre: Music genre, art form, etc.
            project_type: Recording, touring, creation, performance, etc.
            
        Returns:
            List of GrantMatch objects sorted by match score (descending)
        """
        if not self.grants:
            logger.warning("No grants loaded for matching")
            return []
        
        matches = []
        
        for grant in self.grants:
            match = self._calculate_match_score(
                grant, project_description, artist_type, residency, genre, project_type
            )
            if match:
                matches.append(match)
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches
    
    def _calculate_match_score(self, grant: Dict, project_description: str,
                              artist_type: str, residency: str, genre: str, 
                              project_type: str) -> GrantMatch:
        """Calculate match score for a single grant"""
        
        # Initialize scores
        eligibility_score = self._calculate_eligibility_score(grant, artist_type, residency, genre, project_type)
        project_type_score = self._calculate_project_type_score(grant, project_type)
        keyword_score = self._calculate_keyword_score(grant, project_description)
        complexity_score = self._calculate_complexity_score(grant)
        
        # Calculate weighted score
        match_score = (
            self.weights['eligibility'] * eligibility_score +
            self.weights['project_type'] * project_type_score +
            self.weights['keywords'] * keyword_score +
            self.weights['complexity'] * complexity_score
        )
        
        # Identify matched and missing criteria
        matched_criteria, missing_criteria = self._analyze_criteria(
            grant, artist_type, residency, genre, project_type, project_description
        )
        
        return GrantMatch(
            grant_id=grant.get('id', 'unknown'),
            program_name=grant.get('program_name', 'Unknown Program'),
            administering_agency=grant.get('administering_agency', 'Unknown Agency'),
            match_score=match_score,
            eligibility_score=eligibility_score,
            project_type_score=project_type_score,
            keyword_score=keyword_score,
            complexity_score=complexity_score,
            details=grant,
            matched_criteria=matched_criteria,
            missing_criteria=missing_criteria
        )
    
    def _calculate_eligibility_score(self, grant: Dict, artist_type: str, 
                                   residency: str, genre: str, project_type: str) -> float:
        """Calculate eligibility match score (0-1)"""
        eligibility = grant.get('eligibility_criteria', {})
        score = 0.0
        total_checks = 0
        
        # Check artist type
        if artist_type:
            total_checks += 1
            allowed_types = eligibility.get('artist_type', [])
            if not allowed_types or 'any' in [t.lower() for t in allowed_types] or \
               any(artist_type.lower() in t.lower() for t in allowed_types):
                score += 1.0
        
        # Check residency
        if residency:
            total_checks += 1
            allowed_residency = eligibility.get('residency_requirements', [])
            if not allowed_residency or 'any' in [r.lower() for r in allowed_residency] or \
               any(residency.lower() in r.lower() for r in allowed_residency):
                score += 1.0
        
        # Check genre
        if genre:
            total_checks += 1
            allowed_genres = eligibility.get('genre_restrictions', [])
            if not allowed_genres or 'all genres' in [g.lower() for g in allowed_genres] or \
               any(genre.lower() in g.lower() for g in allowed_genres):
                score += 1.0
        
        # Check project type
        if project_type:
            total_checks += 1
            allowed_projects = eligibility.get('project_type', [])
            if not allowed_projects or 'any' in [p.lower() for p in allowed_projects] or \
               any(project_type.lower() in p.lower() for p in allowed_projects):
                score += 1.0
        
        return score / total_checks if total_checks > 0 else 0.5  # Neutral if no criteria specified
    
    def _calculate_project_type_score(self, grant: Dict, project_type: str) -> float:
        """Calculate project type match score"""
        if not project_type:
            return 0.5  # Neutral
        
        eligibility = grant.get('eligibility_criteria', {})
        allowed_projects = eligibility.get('project_type', [])
        
        if not allowed_projects or 'any' in [p.lower() for p in allowed_projects]:
            return 1.0
        
        # Check if project type matches any allowed types
        for allowed in allowed_projects:
            if project_type.lower() in allowed.lower() or allowed.lower() in project_type.lower():
                return 1.0
        
        return 0.0
    
    def _calculate_keyword_score(self, grant: Dict, project_description: str) -> float:
        """Calculate keyword match score based on project description"""
        if not project_description:
            return 0.5
        
        description = grant.get('description', '').lower()
        proj_desc = project_description.lower()
        
        # Extract potential art form from project description
        art_form_scores = {}
        for art_form, keywords in self.art_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in proj_desc:
                    score += 1
            art_form_scores[art_form] = score
        
        # Determine likely art form
        likely_art_form = max(art_form_scores, key=art_form_scores.get) if max(art_form_scores.values()) > 0 else None
        
        # Check if grant description contains keywords from the likely art form
        keyword_score = 0.0
        if likely_art_form and likely_art_form in self.art_keywords:
            keywords = self.art_keywords[likely_art_form]
            matches = sum(1 for keyword in keywords if keyword in description)
            keyword_score = min(matches / len(keywords), 1.0) if keywords else 0.0
        else:
            # Fallback: general keyword matching
            # Extract nouns and key terms from project description (simplified)
            words = set(re.findall(r'\b[a-z]{3,}\b', proj_desc))
            desc_words = set(re.findall(r'\b[a-z]{3,}\b', description))
            if words:
                overlap = len(words.intersection(desc_words))
                keyword_score = min(overlap / len(words), 1.0)
        
        return keyword_score
    
    def _calculate_complexity_score(self, grant: Dict) -> float:
        """
        Calculate complexity score (0-1), where 1 is least complex (simplest application)
        We invert this so simpler applications get higher scores
        """
        # Factors that increase complexity:
        # - Matching fund requirements
        # - Extensive application requirements
        # - Low success rate (if available)
        # - High budget requirements
        
        complexity_factors = []
        
        # Check for matching funds requirement
        funding = grant.get('funding_details', {})
        if funding.get('requires_matching_funds', False):
            complexity_factors.append(0.3)  # Adds complexity
        
        # Count application requirements
        reqs = grant.get('application_requirements', [])
        req_count = len(reqs)
        # Normalize: 0-5 requirements -> 0.0-0.3 complexity, 6+ -> 0.3
        req_complexity = min(req_count * 0.05, 0.3)
        complexity_factors.append(req_complexity)
        
        # Check funding amount (very high amounts might be more competitive)
        max_amount = funding.get('max_amount', 0)
        if max_amount > 100000:
            complexity_factors.append(0.2)
        elif max_amount > 50000:
            complexity_factors.append(0.1)
        
        # Total complexity (0-1 range, higher means more complex)
        total_complexity = sum(complexity_factors)
        # Clamp to 0-1
        total_complexity = min(max(total_complexity, 0.0), 1.0)
        
        # Return simplicity score (1 - complexity)
        return 1.0 - total_complexity
    
    def _analyze_criteria(self, grant: Dict, artist_type: str, residency: str, 
                         genre: str, project_type: str, project_description: str) -> Tuple[List[str], List[str]]:
        """Analyze which criteria are matched and missing"""
        matched = []
        missing = []
        eligibility = grant.get('eligibility_criteria', {})
        
        # Check artist type
        if artist_type:
            allowed_types = eligibility.get('artist_type', [])
            if not allowed_types or 'any' in [t.lower() for t in allowed_types] or \
               any(artist_type.lower() in t.lower() for t in allowed_types):
                matched.append(f"Artist type: {artist_type}")
            else:
                missing.append(f"Artist type: {artist_type} (allowed: {', '.join(allowed_types)})")
        
        # Check residency
        if residency:
            allowed_residency = eligibility.get('residency_requirements', [])
            if not allowed_residency or 'any' in [r.lower() for r in allowed_residency] or \
               any(residency.lower() in r.lower() for r in allowed_residency):
                matched.append(f"Residency: {residency}")
            else:
                missing.append(f"Residency: {residency} (allowed: {', '.join(allowed_residency)})")
        
        # Check genre
        if genre:
            allowed_genres = eligibility.get('genre_restrictions', [])
            if not allowed_genres or 'all genres' in [g.lower() for g in allowed_genres] or \
               any(genre.lower() in g.lower() for g in allowed_genres):
                matched.append(f"Genre: {genre}")
            else:
                missing.append(f"Genre: {genre} (allowed: {', '.join(allowed_genres)})")
        
        # Check project type
        if project_type:
            allowed_projects = eligibility.get('project_type', [])
            if not allowed_projects or 'any' in [p.lower() for p in allowed_projects] or \
               any(project_type.lower() in p.lower() for p in allowed_projects):
                matched.append(f"Project type: {project_type}")
            else:
                missing.append(f"Project type: {project_type} (allowed: {', '.join(allowed_projects)})")
        
        return matched, missing
    
    def get_top_matches(self, matches: List[GrantMatch], limit: int = 10) -> List[GrantMatch]:
        """Get top N matches"""
        return matches[:limit]
    
    def format_match_for_display(self, match: GrantMatch) -> Dict[str, Any]:
        """Format a match for display in the UI"""
        return {
            'id': match.grant_id,
            'program_name': match.program_name,
            'administering_agency': match.administering_agency,
            'match_score': round(match.match_score * 100, 1),  # Percentage
            'eligibility_score': round(match.eligibility_score * 100, 1),
            'project_type_score': round(match.project_type_score * 100, 1),
            'keyword_score': round(match.keyword_score * 100, 1),
            'complexity_score': round(match.complexity_score * 100, 1),
            'matched_criteria': match.matched_criteria,
            'missing_criteria': match.missing_criteria,
            'description': match.details.get('description', ''),
            'deadline_info': match.details.get('deadline_info', {}),
            'funding_details': match.details.get('funding_details', {}),
            'application_requirements': match.details.get('application_requirements', []),
            'url': match.details.get('url', '')
        }

# Example usage
if __name__ == "__main__":
    # This would normally load from the scraper output
    sample_grants = [
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
        }
    ]
    
    engine = GrantMatchingEngine(sample_grants)
    
    # Test matching
    project_desc = "I am an emerging electronic music producer based in Toronto working on my debut EP"
    matches = engine.match_project_to_grants(
        project_description=project_desc,
        artist_type="individual",
        residency="Canadian citizen",
        genre="electronic",
        project_type="Recording"
    )
    
    if matches:
        top_match = matches[0]
        print(f"Top match: {top_match.program_name}")
        print(f"Match score: {top_match.match_score:.2%}")
        print(f"Matched criteria: {top_match.matched_criteria}")
        print(f"Missing criteria: {top_match.missing_criteria}")
        
        # Format for display
        display = engine.format_match_for_display(top_match)
        print("\nFormatted for display:")
        print(json.dumps(display, indent=2))