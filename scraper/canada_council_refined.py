"""
Refined Canada Council for the Arts Grant Scraper
"""
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from typing import List, Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)

class CanadaCouncilScraper:
    def __init__(self):
        self.base_url = "https://canadacouncil.ca"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Grant-O-Matic/1.0 (Educational Tool for Canadian Artists)'
        })
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page and return BeautifulSoup object"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_grant_programs(self) -> List[Dict]:
        """Extract all grant programs from Canada Council"""
        logger.info("Starting Canada Council grant programs extraction...")
        
        # Start from the grants page
        grants_url = f"{self.base_url}/funding/grants"
        soup = self.get_page(grants_url)
        if not soup:
            logger.error("Failed to fetch grants page")
            return []
        
        # Find the main content area
        main_content = soup.select_one('[role="main"]')
        if not main_content:
            logger.error("Could not find main content area")
            return []
        
        # Extract program information from the page
        programs = self._extract_programs_from_page(main_content)
        logger.info(f"Extracted {len(programs)} top-level programs")
        
        # For each program, try to get more specific grant opportunities
        all_grants = []
        for program_name, program_description in programs:
            logger.info(f"Processing program: {program_name}")
            
            # Try to find a specific URL for this program
            program_url = self._find_program_url(soup, program_name)
            if program_url:
                logger.info(f"Found specific URL for {program_name}: {program_url}")
                program_soup = self.get_page(program_url)
                if program_soup:
                    # Extract specific grants from this program page
                    specific_grants = self._extract_specific_grants(program_soup, program_name, program_description)
                    all_grants.extend(specific_grants)
                else:
                    logger.warning(f"Could not fetch specific page for {program_name}")
                    # Add the program as a general grant opportunity
                    all_grants.append(self._create_grant_object(program_name, program_description, grants_url))
            else:
                logger.warning(f"Could not find specific URL for {program_name}, using general page")
                # Add the program as a general grant opportunity
                all_grants.append(self._create_grant_object(program_name, program_description, grants_url))
            
            # Be respectful with rate limiting
            time.sleep(1)
        
        logger.info(f"Successfully extracted {len(all_grants)} grant opportunities")
        return all_grants
    
    def _extract_programs_from_page(self, soup: BeautifulSoup) -> List[tuple]:
        """Extract top-level programs from the grants page"""
        programs = []
        text = soup.get_text()
        
        # Known top-level programs from our earlier analysis
        known_programs = [
            'Explore and Create',
            'Engage and Sustain', 
            'Creating, Knowing and Sharing: The Arts and Cultures of First Nations, Inuit and Métis Peoples',
            'Supporting Artistic Practice',
            'Arts Across Canada and Abroad'
        ]
        
        for program in known_programs:
            if program in text:
                # Extract a reasonable description around the program name
                # This is simplified - in reality we'd want to extract the actual description
                description = f"Supports {program.lower()} initiatives across the Canadian arts sector."
                programs.append((program, description))
        
        return programs
    
    def _find_program_url(self, soup: BeautifulSoup, program_name: str) -> Optional[str]:
        """Try to find a specific URL for a program"""
        # Clean the program name for URL matching
        clean_name = program_name.lower()
        clean_name = re.sub(r'[^a-z0-9\s]', '', clean_name)
        clean_name = re.sub(r'\s+', '-', clean_name.strip())
        
        # Try common URL patterns
        possible_urls = [
            f"{self.base_url}/funding/grants/{clean_name}",
            f"{self.base_url}/funding/grants/{clean_name.lower()}",
            f"{self.base_url}/funding/grants/explore-and-create/{clean_name}" if 'explore' in clean_name else None,
        ]
        
        # Remove None values
        possible_urls = [url for url in possible_urls if url is not None]
        
        # For now, we'll return the first one and let the scraping handle 404s
        # In a production version, we'd check each URL
        if possible_urls:
            return possible_urls[0]
        return None
    
    def _extract_specific_grants(self, soup: BeautifulSoup, program_name: str, program_description: str) -> List[Dict]:
        """Extract specific grant opportunities from a program page"""
        grants = []
        
        # Look for known specific programs under Explore and Create
        if 'explore' in program_name.lower():
            specific_programs = [
                'Research and Creation',
                'Concept to Realization', 
                'Artists and Community Collaboration',
                'Indigenous Individuals and Organizations',
                'Official Language Minority Communities',
                'Deaf and Disability Arts Projects',
                'Cultural Spaces',
                'Public Art'
            ]
            
            for specific_program in specific_programs:
                if specific_program.lower() in soup.get_text().lower():
                    # Create a more specific description
                    description = f"{specific_program} grant under the {program_name} program. {program_description}"
                    grants.append(self._create_grant_object(specific_program, description, soup.find('link', {'rel': 'canonical'})['href'] if soup.find('link', {'rel': 'canonical'}) else f"{self.base_url}/funding/grants/explore-and-create"))
        
        # If we didn't find specific grants, return the general program
        if not grants:
            grants.append(self._create_grant_object(program_name, program_description, soup.find('link', {'rel': 'canonical'})['href'] if soup.find('link', {'rel': 'canonical'}) else f"{self.base_url}/funding/grants"))
        
        return grants
    
    def _create_grant_object(self, program_name: str, description: str, url: str) -> Dict:
        """Create a standardized grant object"""
        # Generate a simple ID from the program name and URL
        import hashlib
        id_string = f"{program_name}_{url}"
        grant_id = hashlib.md5(id_string.encode()).hexdigest()[:8]
        
        # Determine if it's likely to require matching funds based on program name
        requires_matching = any(keyword in program_name.lower() for keyword in ['engage', 'sustain', 'supporting', 'arts across'])
        
        # Set typical funding ranges (these would be refined with actual data)
        if 'explore' in program_name.lower():
            min_amount, max_amount = 1000, 25000
        elif 'engage' in program_name.lower():
            min_amount, max_amount = 5000, 100000
        elif 'indigenous' in program_name.lower() or 'first nations' in program_name.lower():
            min_amount, max_amount = 5000, 50000
        else:
            min_amount, max_amount = 1000, 50000
        
        return {
            "id": grant_id,
            "program_name": program_name,
            "administering_agency": "Canada Council for the Arts",
            "description": description,
            "eligibility_criteria": {
                "artist_type": ["individual", "group", "organization"],
                "residency_requirements": ["Canadian citizen", "Permanent resident"],
                "genre_restrictions": ["All genres"],
                "career_stage": ["Emerging", "Established", "Any"],
                "project_type": ["Creation", "Production", "Research", "Touring"]
            },
            "deadline_info": {
                "frequency": "Varies by program",
                "next_deadline": None,  # Would need to be scraped from specific program pages
                "application_window": "Check specific program for deadlines"
            },
            "funding_details": {
                "min_amount": min_amount,
                "max_amount": max_amount,
                "average_award": (min_amount + max_amount) // 2,
                "funding_type": "Grant",
                "requires_matching_funds": requires_matching,
                "matching_requirements": "Varies by specific program" if requires_matching else None
            },
            "application_requirements": [
                "Project description",
                "Budget",
                "Work samples",
                "Artist bio/CV",
                "Supporting materials"
            ],
            "assessment_criteria": [
                "Artistic merit",
                "Project feasibility", 
                "Impact and significance",
                "Viability"
            ],
            "url": url,
            "last_updated": time.strftime('%Y-%m-%d'),
            "status": "Active"
        }

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = CanadaCouncilScraper()
    grants = scraper.extract_grant_programs()
    
    # Save to JSON file
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'canada_council_grants_refined.json')
    with open(out_path, 'w') as f:
        json.dump(grants, f, indent=2)
    
    print(f"Extracted {len(grants)} grant opportunities from Canada Council for the Arts")
    
    # Show a sample
    if grants:
        print("\\nSample grant:")
        print(json.dumps(grants[0], indent=2))