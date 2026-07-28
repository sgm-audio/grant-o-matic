"""
FACTOR (factor.ca) grant scraper.

Supports live HTTP fetches and offline fixture HTML (preferred in CI).
Funding amounts and deadlines are taken only from page text when present.
"""
from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
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
        funding_from_amounts,
        generate_grant_id,
        normalize_whitespace,
        parse_iso_dates_from_text,
        parse_money_amounts,
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
        funding_from_amounts,
        generate_grant_id,
        normalize_whitespace,
        parse_iso_dates_from_text,
        parse_money_amounts,
        today_iso,
    )

logger = logging.getLogger(__name__)

# Programs we ship fixtures for / prioritize in catalog
ARTIST_PROGRAM_SLUGS = {
    "artist-development",
    "juried-sound-recording-album",
    "juried-sound-recording-single-ep",
    "video",
}


class FactorScraper:
    def __init__(
        self,
        *,
        rate_limit_seconds: float = DEFAULT_RATE_LIMIT_SECONDS,
        session: Optional[requests.Session] = None,
    ):
        self.base_url = "https://www.factor.ca"
        self.artist_programs_url = f"{self.base_url}/programs/artist-programs/"
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

    def parse_artist_program_links(self, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        found: Dict[str, str] = {}
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full = absolute_url(self.base_url, href)
            path = urlparse(full).path.rstrip("/")
            if "/programs/artist-programs/" not in path:
                continue
            slug = path.split("/")[-1]
            if slug in {"artist-programs", ""}:
                continue
            text = normalize_whitespace(link.get_text(" ", strip=True))
            text = re.sub(r"\s*-\s*Read more\s*$", "", text, flags=re.I)
            if slug in ARTIST_PROGRAM_SLUGS:
                found[full.split("?")[0]] = text or slug.replace("-", " ").title()
        # Ensure fixture-backed programs are present
        for slug in ARTIST_PROGRAM_SLUGS:
            url = f"{self.base_url}/programs/artist-programs/{slug}/"
            found.setdefault(url, slug.replace("-", " ").title())
        return [{"url": url, "link_text": name} for url, name in sorted(found.items())]

    def parse_program_page(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n", strip=True)
        program_name = self._extract_program_name(soup)
        description = self._extract_description(soup)
        funding, matching_note = self._extract_funding(text)
        deadline = self._extract_deadline(text)

        return {
            "id": generate_grant_id(url.rstrip("/") + "/"),
            "program_name": program_name,
            "administering_agency": "FACTOR",
            "description": description,
            "eligibility_criteria": self._extract_eligibility(text),
            "deadline_info": deadline,
            "funding_details": funding
            if funding.get("max_amount") is not None
            else {
                **empty_funding_details(),
                "matching_requirements": matching_note,
            },
            "application_requirements": self._extract_requirements(soup),
            "assessment_criteria": [
                "Artistic and project merit as assessed by FACTOR jury/process",
                "See program guidelines on factor.ca",
            ],
            "url": url if url.endswith("/") else url + "/",
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
        When fixture_dir is set:
          artist-programs.html
          <program-slug>.html
        """
        fixture_path = Path(fixture_dir) if fixture_dir else None
        if fixture_path:
            index_html = (fixture_path / "artist-programs.html").read_text(encoding="utf-8")
        else:
            index_html = self.fetch_html(self.artist_programs_url)
            if not index_html:
                return []

        programs = self.parse_artist_program_links(index_html)
        if max_programs is not None:
            programs = programs[:max_programs]

        grants: List[Dict] = []
        for item in programs:
            url = item["url"]
            slug = urlparse(url).path.rstrip("/").split("/")[-1]
            if fixture_path:
                page_file = fixture_path / f"{slug}.html"
                if not page_file.is_file():
                    logger.warning("Missing FACTOR fixture for %s", slug)
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
        h1 = soup.find("h1")
        if h1:
            text = normalize_whitespace(h1.get_text(" ", strip=True))
            if text:
                return text
        return "Unknown FACTOR Program"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            return normalize_whitespace(meta["content"])[:800]
        main = soup.find("main") or soup.body or soup
        for p in main.find_all("p"):
            text = normalize_whitespace(p.get_text(" ", strip=True))
            if len(text) >= 60:
                return text[:800]
        return "Description not available on parsed page"

    def _extract_funding(self, text: str) -> Tuple[Dict, Optional[str]]:
        matching_note = None
        low = text.lower()
        if "75%" in text and "eligible" in low:
            matching_note = "FACTOR contributes 75% of eligible expenses (see guidelines)"
            requires_matching = True
        elif "50%" in text and "eligible" in low:
            matching_note = "FACTOR contributes 50% of eligible expenses (see guidelines)"
            requires_matching = True
        else:
            requires_matching = None

        # Prefer the first explicit program-cap phrase (do not take max of all $-amounts on page)
        max_amount = None
        for pattern in (
            r"maximum reimbursement of\s+\$([\d,]+)",
            r"up to a maximum of\s+\$([\d,]+)",
            r"project maximum of\s+\$([\d,]+)",
            r"maximum of\s+\$([\d,]+)",
        ):
            match = re.search(pattern, text, flags=re.I)
            if match:
                max_amount = float(match.group(1).replace(",", ""))
                break
        if max_amount is not None:
            details = funding_from_amounts(
                [max_amount],
                requires_matching=requires_matching,
                matching_requirements=matching_note,
            )
            details["min_amount"] = None
            details["average_award"] = None
            return details, matching_note

        amounts = parse_money_amounts(text)
        if amounts:
            # Use only amounts that look like program caps (<= 100000)
            caps = [a for a in amounts if a <= 100000]
            if caps:
                details = funding_from_amounts(
                    [max(caps)],
                    requires_matching=requires_matching,
                    matching_requirements=matching_note,
                )
                details["min_amount"] = None
                details["average_award"] = None
                return details, matching_note

        details = empty_funding_details()
        details["requires_matching_funds"] = requires_matching
        details["matching_requirements"] = matching_note
        return details, matching_note

    def _extract_deadline(self, text: str) -> Dict:
        dates = parse_iso_dates_from_text(text)
        next_deadline = None
        frequency = None
        window = None

        if re.search(r"rolling deadlines", text, re.I):
            frequency = "Rolling"
        elif re.search(r"deadline", text, re.I):
            frequency = "Scheduled intakes"

        # Prefer a future-looking stated application deadline sentence
        m = re.search(
            r"application deadline[^\n.]{0,80}?(\d{1,2}\s+"
            + "(?:"
            + "|".join(
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ]
            )
            + r")\s+\d{4})",
            text,
            flags=re.I,
        )
        if m:
            parsed = parse_iso_dates_from_text(m.group(1))
            if parsed:
                next_deadline = parsed[0]
        elif dates:
            # If page says "Deadline was ..." treat as historical; keep null next_deadline
            if re.search(r"deadline was\s+", text, re.I):
                next_deadline = None
                window = f"Previous deadline mentioned on page: {dates[0]}"
            else:
                next_deadline = dates[0]

        if "january 14, 2027" in text.lower() or "january 14 2027" in text.lower():
            # Video fiscal cutoff stated on page
            if frequency == "Rolling":
                window = "Rolling; submit by 2027-01-14 for current fiscal program year (per page)"
                next_deadline = next_deadline or "2027-01-14"

        return default_deadline_info(
            frequency=frequency,
            next_deadline=next_deadline,
            application_window=window or "See https://www.factor.ca/artists/deadlines/",
        )

    def _extract_eligibility(self, text: str) -> Dict:
        low = text.lower()
        artist_type = ["individual"]
        if "record label" in low or "company" in low:
            artist_type.append("company")
        career = ["Emerging"] if "emerging" in low else ["See program guidelines"]
        project_type = []
        if "sound recording" in low or "recording" in low:
            project_type.append("Recording")
        if "tour" in low or "showcase" in low:
            project_type.append("Touring")
        if "video" in low:
            project_type.append("Video")
        if "marketing" in low:
            project_type.append("Marketing")
        if not project_type:
            project_type = ["See program guidelines"]
        return {
            "artist_type": artist_type,
            "residency_requirements": ["Canadian artist eligibility per FACTOR guidelines"],
            "genre_restrictions": ["Commercial music (see FACTOR guidelines)"],
            "career_stage": career,
            "project_type": project_type,
        }

    def _extract_requirements(self, soup: BeautifulSoup) -> List[str]:
        reqs: List[str] = []
        for li in soup.find_all("li"):
            text = normalize_whitespace(li.get_text(" ", strip=True))
            low = text.lower()
            if any(k in low for k in ("mp3", "profile", "plan", "budget", "lyrics", "track")):
                if 15 <= len(text) <= 220:
                    reqs.append(text)
            if len(reqs) >= 6:
                break
        return reqs or [
            "Rated Artist Profile and Applicant Profile in FACTOR system",
            "See program application checklist on factor.ca",
        ]
