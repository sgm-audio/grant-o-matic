"""
Canada Council for the Arts grant scraper.

Supports live HTTP fetches and offline fixture HTML (preferred in CI).
Does not invent funding amounts or deadlines; unknown fields are null.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

try:
    from scraper.common import (
        DEFAULT_RATE_LIMIT_SECONDS,
        DEFAULT_TIMEOUT,
        USER_AGENT,
        absolute_url,
        default_deadline_info,
        empty_funding_details,
        generate_grant_id,
        normalize_whitespace,
        today_iso,
    )
except ImportError:  # pragma: no cover
    from common import (
        DEFAULT_RATE_LIMIT_SECONDS,
        DEFAULT_TIMEOUT,
        USER_AGENT,
        absolute_url,
        default_deadline_info,
        empty_funding_details,
        generate_grant_id,
        normalize_whitespace,
        today_iso,
    )

logger = logging.getLogger(__name__)

PROGRAM_PATH_PREFIX = "/funding/grants/"
KNOWN_PROGRAM_SLUGS = {
    "explore-and-create",
    "engage-and-sustain",
    "creating-knowing-sharing",
    "supporting-artistic-practice",
    "arts-across-canada-and-abroad",
}


class CanadaCouncilScraper:
    def __init__(
        self,
        *,
        rate_limit_seconds: float = DEFAULT_RATE_LIMIT_SECONDS,
        session: Optional[requests.Session] = None,
    ):
        self.base_url = "https://canadacouncil.ca"
        self.grants_url = f"{self.base_url}/funding/grants"
        self.rate_limit_seconds = rate_limit_seconds
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def fetch_html(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            logger.error("Error fetching %s: %s", url, exc)
            return None

    def parse_program_links(self, html: str) -> List[Dict[str, str]]:
        """Extract program URLs from the grants index HTML."""
        soup = BeautifulSoup(html, "html.parser")
        found: Dict[str, str] = {}
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full = absolute_url(self.base_url, href)
            path = urlparse(full).path.rstrip("/")
            if not path.startswith(PROGRAM_PATH_PREFIX.rstrip("/")):
                continue
            slug = path.split("/")[-1]
            if slug in {"grants", "deadlines"}:
                continue
            if slug not in KNOWN_PROGRAM_SLUGS and "/funding/grants/" not in full:
                continue
            # Prefer known program pages; still accept other grant program paths
            if slug == "grants":
                continue
            text = normalize_whitespace(link.get_text(" ", strip=True))
            if full not in found or (text and text.lower() != "learn more about this program"):
                if slug in KNOWN_PROGRAM_SLUGS or path.count("/") >= 3:
                    if slug in KNOWN_PROGRAM_SLUGS:
                        found[full] = text or slug
        # Ensure known programs appear even if link text was generic
        for slug in KNOWN_PROGRAM_SLUGS:
            url = f"{self.base_url}/funding/grants/{slug}"
            found.setdefault(url, slug.replace("-", " ").title())
        return [{"url": url, "link_text": name} for url, name in sorted(found.items())]

    def parse_program_page(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, "html.parser")
        program_name = self._extract_program_name(soup)
        description = self._extract_description(soup)
        return {
            "id": generate_grant_id(url),
            "program_name": program_name,
            "administering_agency": "Canada Council for the Arts",
            "description": description,
            "eligibility_criteria": self._extract_eligibility(soup),
            "deadline_info": default_deadline_info(
                frequency="See Canada Council deadlines page",
                next_deadline=None,
                application_window="https://canadacouncil.ca/funding/grants/deadlines",
            ),
            "funding_details": empty_funding_details(),
            "application_requirements": self._extract_listish(
                soup,
                keywords=("application", "require", "submit"),
                fallback=[
                    "See program guidelines on the Canada Council website",
                    "Application via Canada Council portal",
                ],
            ),
            "assessment_criteria": self._extract_listish(
                soup,
                keywords=("assessment", "criteria", "evaluation"),
                fallback=["See program assessment criteria on the Canada Council website"],
            ),
            "url": url,
            "last_updated": today_iso(),
            "status": "Active",
        }

    def scrape_all_grants(
        self,
        *,
        fixture_dir: Optional[str | Path] = None,
        max_programs: Optional[int] = None,
    ) -> List[Dict]:
        """
        Scrape grants from live site or local fixtures.

        When fixture_dir is set, no network calls are made.
        Expected fixture layout:
          grants_index.html
          <program-slug>.html
        """
        fixture_path = Path(fixture_dir) if fixture_dir else None
        if fixture_path:
            index_html = (fixture_path / "grants_index.html").read_text(encoding="utf-8")
        else:
            index_html = self.fetch_html(self.grants_url)
            if not index_html:
                return []

        programs = self.parse_program_links(index_html)
        if max_programs is not None:
            programs = programs[:max_programs]

        grants: List[Dict] = []
        for item in programs:
            url = item["url"]
            slug = urlparse(url).path.rstrip("/").split("/")[-1]
            if fixture_path:
                page_file = fixture_path / f"{slug}.html"
                if not page_file.is_file():
                    logger.warning("Missing fixture for %s", slug)
                    continue
                html = page_file.read_text(encoding="utf-8")
            else:
                html = self.fetch_html(url)
                if not html:
                    continue
                time.sleep(self.rate_limit_seconds)
            grants.append(self.parse_program_page(html, url))
        return grants

    def _extract_program_name(self, soup: BeautifulSoup) -> str:
        for selector in ("h1", "h2", ".grant-title", ".program-name"):
            element = soup.select_one(selector)
            if element:
                text = normalize_whitespace(element.get_text(" ", strip=True))
                if text:
                    return text
        return "Unknown Program"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        main = soup.find("main") or soup.body or soup
        for p in main.find_all("p"):
            text = normalize_whitespace(p.get_text(" ", strip=True))
            if len(text) >= 60:
                return text[:800]
        return "Description not available on parsed page"

    def _extract_eligibility(self, soup: BeautifulSoup) -> Dict:
        text = soup.get_text(" ", strip=True).lower()
        artist_type: List[str] = []
        if "individual" in text:
            artist_type.append("individual")
        if "group" in text or "collective" in text:
            artist_type.append("group")
        if "organization" in text:
            artist_type.append("organization")
        if not artist_type:
            artist_type = ["individual", "group", "organization"]
        return {
            "artist_type": artist_type,
            "residency_requirements": ["See program guidelines"],
            "genre_restrictions": ["See program guidelines"],
            "career_stage": ["See program guidelines"],
            "project_type": ["See program guidelines"],
        }

    def _extract_listish(
        self,
        soup: BeautifulSoup,
        *,
        keywords: tuple[str, ...],
        fallback: List[str],
    ) -> List[str]:
        items: List[str] = []
        for li in soup.find_all("li"):
            text = normalize_whitespace(li.get_text(" ", strip=True))
            low = text.lower()
            if any(k in low for k in keywords) and 20 <= len(text) <= 240:
                items.append(text)
            if len(items) >= 6:
                break
        return items or list(fallback)
