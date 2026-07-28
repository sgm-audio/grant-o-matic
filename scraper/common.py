"""
Shared helpers for grant scrapers.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

USER_AGENT = "Grant-O-Matic/1.0 (+https://github.com/SGM-Studios/grant-o-matic; educational)"
DEFAULT_TIMEOUT = 15
DEFAULT_RATE_LIMIT_SECONDS = 1.0

MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)


def generate_grant_id(url: str) -> str:
    """Stable 8-char id derived from the program URL."""
    return hashlib.md5(url.encode("utf-8")).hexdigest()[:8]


def absolute_url(base: str, href: str) -> str:
    return urljoin(base if base.endswith("/") else base + "/", href)


def normalize_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def today_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def parse_money_amounts(text: str) -> List[float]:
    amounts: List[float] = []
    for match in re.findall(r"\$[\d,]+(?:\.\d{2})?", text or ""):
        try:
            amounts.append(float(match.replace("$", "").replace(",", "")))
        except ValueError:
            continue
    return amounts


def parse_iso_dates_from_text(text: str) -> List[str]:
    """
    Extract calendar dates and return them as YYYY-MM-DD when parseable.
    Supports 'Month D, YYYY' and 'D Month YYYY'.
    """
    found: List[str] = []
    patterns = [
        re.compile(
            r"\b("
            + "|".join(MONTHS)
            + r")\s+(\d{1,2}),?\s+(\d{4})\b",
            re.I,
        ),
        re.compile(
            r"\b(\d{1,2})\s+("
            + "|".join(MONTHS)
            + r")\s+(\d{4})\b",
            re.I,
        ),
    ]
    for pattern in patterns:
        for match in pattern.finditer(text or ""):
            groups = match.groups()
            try:
                if groups[0].isdigit():
                    day = int(groups[0])
                    month = MONTHS.index(groups[1].lower()) + 1
                    year = int(groups[2])
                else:
                    month = MONTHS.index(groups[0].lower()) + 1
                    day = int(groups[1])
                    year = int(groups[2])
                found.append(f"{year:04d}-{month:02d}-{day:02d}")
            except (ValueError, IndexError):
                continue
    # de-dupe preserving order
    return list(dict.fromkeys(found))


def empty_funding_details() -> Dict[str, Any]:
    return {
        "min_amount": None,
        "max_amount": None,
        "average_award": None,
        "funding_type": "Grant",
        "requires_matching_funds": None,
        "matching_requirements": None,
    }


def funding_from_amounts(
    amounts: List[float],
    *,
    requires_matching: Optional[bool] = None,
    matching_requirements: Optional[str] = None,
) -> Dict[str, Any]:
    details = empty_funding_details()
    if amounts:
        details["min_amount"] = min(amounts)
        details["max_amount"] = max(amounts)
        details["average_award"] = round(sum(amounts) / len(amounts), 2)
    details["requires_matching_funds"] = requires_matching
    details["matching_requirements"] = matching_requirements
    return details


def default_deadline_info(
    *,
    frequency: Optional[str] = None,
    next_deadline: Optional[str] = None,
    application_window: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "frequency": frequency,
        "next_deadline": next_deadline,
        "application_window": application_window,
    }


def same_registered_domain(url: str, allowed_hosts: List[str]) -> bool:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    return any(host == h.removeprefix("www.") or host.endswith("." + h.removeprefix("www.")) for h in allowed_hosts)
