"""
Canada Council for the Arts Grant Scraper
"""
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CanadaCouncilScraper:
    def __init__(self):
        self.base_url = "https://canadacouncil.ca"
        self.grants_url = f"{self.base_url}/funding/grants"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Grant-O-Matic/1.0 (Educational Tool for Canadian Artists)'
        })
    
    def fetch_grants_page(self) -> Optional[BeautifulSoup]:
        """Fetch the main grants page"""
        try:
            response = self.session.get(self.grants_url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching grants page: {e}")
            return None
    
    def extract_grant_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract links to individual grant pages"""
        grant_links = []
        # Look for links to grant programs
        # This selector will need adjustment based on actual site structure
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            # Filter for grant-related links
            if '/funding/grants/' in href and href not in grant_links:
                full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                grant_links.append(full_url)
        return grant_links
    
    def scrape_grant_details(self, grant_url: str) -> Optional[Dict]:
        """Scrape details from an individual grant page"""
        try:
            response = self.session.get(grant_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract grant information - selectors will need adjustment
            grant_data = {
                'id': self._generate_id(grant_url),
                'program_name': self._extract_program_name(soup),
                'administering_agency': 'Canada Council for the Arts',
                'description': self._extract_description(soup),
                'eligibility_criteria': self._extract_eligibility(soup),
                'deadline_info': self._extract_deadline_info(soup),
                'funding_details': self._extract_funding_details(soup),
                'application_requirements': self._extract_application_requirements(soup),
                'assessment_criteria': self._extract_assessment_criteria(soup),
                'url': grant_url,
                'last_updated': time.strftime('%Y-%m-%d'),
                'status': 'Active'
            }
            
            return grant_data
        except Exception as e:
            logger.error(f"Error scraping grant details from {grant_url}: {e}")
            return None
    
    def _generate_id(self, url: str) -> str:
        """Generate a unique ID for the grant"""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()[:8]
    
    def _extract_program_name(self, soup: BeautifulSoup) -> str:
        """Extract program name from page"""
        # Try common selectors for program title
        selectors = ['h1', 'h2', '.grant-title', '.program-name']
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
        return "Unknown Program"
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract program description"""
        # Look for description in common locations
        selectors = [
            '.grant-description',
            '.program-description',
            'div[property="description"]',
            '.field-name-body',
            'main p'
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)[:500]  # Limit length
        return "Description not available"
    
    def _extract_eligibility(self, soup: BeautifulSoup) -> Dict:
        """Extract eligibility criteria"""
        eligibility = {}
        # This would need to be customized based on actual page structure
        # Look for sections containing eligibility information
        eligibility_sections = soup.find_all(text=lambda text: text and 'eligibility' in text.lower())
        # For now, return placeholder structure
        eligibility = {
            'artist_type': ['individual', 'group'],
            'residency_requirements': ['Canadian citizen', 'Permanent resident'],
            'genre_restrictions': ['All genres'],
            'career_stage': ['Any'],
            'project_type': ['Various']
        }
        return eligibility
    
    def _extract_deadline_info(self, soup: BeautifulSoup) -> Dict:
        """Extract deadline information"""
        deadline_info = {
            'frequency': 'Varies',
            'next_deadline': None,
            'application_window': None
        }
        # Look for date information
        date_elements = soup.find_all(text=lambda text: text and any(
            month in text.lower() for month in 
            ['january', 'february', 'march', 'april', 'may', 'june',
             'july', 'august', 'september', 'october', 'november', 'december']
        ))
        # Placeholder implementation
        return deadline_info
    
    def _extract_funding_details(self, soup: BeautifulSoup) -> Dict:
        """Extract funding details"""
        funding_details = {
            'min_amount': 0,
            'max_amount': 0,
            'average_award': 0,
            'funding_type': 'Grant',
            'requires_matching_funds': False,
            'matching_requirements': None
        }
        # Look for money amounts in text
        import re
        text = soup.get_text()
        money_matches = re.findall(r'\$[\d,]+(?:\.\d{2})?', text)
        if money_matches:
            amounts = []
            for match in money_matches:
                try:
                    amount = float(match.replace('$', '').replace(',', ''))
                    amounts.append(amount)
                except ValueError:
                    continue
            if amounts:
                funding_details['min_amount'] = min(amounts)
                funding_details['max_amount'] = max(amounts)
                funding_details['average_award'] = sum(amounts) / len(amounts)
        return funding_details
    
    def _extract_application_requirements(self, soup: BeautifulSoup) -> List[str]:
        """Extract application requirements"""
        requirements = []
        # Look for lists or sections about requirements
        req_sections = soup.find_all(text=lambda text: text and (
            'application' in text.lower() and 
            ('require' in text.lower() or 'need' in text.lower())
        ))
        # Placeholder - would need more sophisticated extraction
        common_requirements = [
            'Project description',
            'Budget',
            'Work samples',
            'Artist CV/bio'
        ]
        return common_requirements
    
    def _extract_assessment_criteria(self, soup: BeautifulSoup) -> List[str]:
        """Extract assessment criteria"""
        criteria = []
        # Look for assessment/judging criteria
        criteria_sections = soup.find_all(text=lambda text: text and (
            'assessment' in text.lower() or 
            'criteria' in text.lower() or
            'judging' in text.lower()
        ))
        # Placeholder
        common_criteria = [
            'Artistic merit',
            'Viability',
            'Impact',
            'Feasibility'
        ]
        return common_criteria
    
    def scrape_all_grants(self) -> List[Dict]:
        """Main method to scrape all grants"""
        logger.info("Starting Canada Council for the Arts grant scraping...")
        
        # Fetch main grants page
        soup = self.fetch_grants_page()
        if not soup:
            logger.error("Failed to fetch grants page")
            return []
        
        # Extract grant links
        grant_links = self.extract_grant_links(soup)
        logger.info(f"Found {len(grant_links)} potential grant links")
        
        # Scrape each grant
        grants = []
        for i, link in enumerate(grant_links[:10]):  # Limit for testing
            logger.info(f"Scraping grant {i+1}/{min(len(grant_links), 10)}: {link}")
            grant_data = self.scrape_grant_details(link)
            if grant_data:
                grants.append(grant_data)
            # Be respectful with rate limiting
            time.sleep(1)
        
        logger.info(f"Successfully scraped {len(grants)} grants")
        return grants

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = CanadaCouncilScraper()
    grants = scraper.scrape_all_grants()
    
    # Save to JSON file
    with open('/var/home/SGM/dev/the-canada-creator-cog/grant-o-matic/data/canada_council_grants.json', 'w') as f:
        json.dump(grants, f, indent=2)
    
    print(f"Scraped {len(grants)} grants from Canada Council for the Arts")