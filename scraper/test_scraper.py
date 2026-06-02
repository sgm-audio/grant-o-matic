"""
Simple test for the Canada Council scraper
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from canada_council import CanadaCouncilScraper

def test_scraper_initialization():
    """Test that the scraper initializes correctly"""
    scraper = CanadaCouncilScraper()
    assert scraper.base_url == "https://canadacouncil.ca"
    assert scraper.grants_url == "https://canadacouncil.ca/funding/grants"

def test_id_generation():
    """Test ID generation"""
    scraper = CanadaCouncilScraper()
    test_url = "https://canadacouncil.ca/funding/grants/test-grant"
    grant_id = scraper._generate_id(test_url)
    assert len(grant_id) == 8  # MD5 hash truncated to 8 chars
    assert grant_id.isalnum()  # Should be alphanumeric

if __name__ == "__main__":
    test_scraper_initialization()
    test_id_generation()
    print("All scraper tests passed!")