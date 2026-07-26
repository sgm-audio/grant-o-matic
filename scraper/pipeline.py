"""
Scrape pipeline: run agency scrapers, merge, persist to GRANT_DATA_PATH.
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from scraper.canada_council import CanadaCouncilScraper
    from scraper.factor import FactorScraper
except ImportError:  # pragma: no cover
    from canada_council import CanadaCouncilScraper
    from factor import FactorScraper

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures"


def merge_grants(*grant_lists: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge grants by id; later lists override earlier on id collision."""
    by_id: Dict[str, Dict[str, Any]] = {}
    for grants in grant_lists:
        for grant in grants:
            grant_id = grant.get("id")
            if not grant_id:
                continue
            by_id[grant_id] = grant
    return sorted(by_id.values(), key=lambda g: (g.get("administering_agency") or "", g.get("program_name") or ""))


def resolve_data_dir(data_dir: Optional[str | Path] = None) -> Path:
    if data_dir is not None:
        return Path(data_dir)
    env = os.environ.get("GRANT_DATA_PATH")
    if env:
        return Path(env)
    return REPO_ROOT / "data"


def run_scrapers(
    *,
    use_fixtures: bool = False,
    fixture_root: Optional[str | Path] = None,
) -> List[Dict[str, Any]]:
    root = Path(fixture_root) if fixture_root else DEFAULT_FIXTURE_ROOT
    cca = CanadaCouncilScraper()
    factor = FactorScraper()

    if use_fixtures:
        cca_grants = cca.scrape_all_grants(fixture_dir=root / "canada_council")
        factor_grants = factor.scrape_all_grants(fixture_dir=root / "factor")
    else:
        cca_grants = cca.scrape_all_grants()
        factor_grants = factor.scrape_all_grants()

    merged = merge_grants(cca_grants, factor_grants)
    logger.info(
        "Scraped %s Canada Council + %s FACTOR = %s merged grants",
        len(cca_grants),
        len(factor_grants),
        len(merged),
    )
    return merged


def persist_grants(
    grants: List[Dict[str, Any]],
    *,
    data_dir: Optional[str | Path] = None,
    filename: str = "all_grants.json",
) -> Path:
    directory = resolve_data_dir(data_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / filename
    path.write_text(json.dumps(grants, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def run_scrape_and_persist(
    *,
    use_fixtures: bool = False,
    fixture_root: Optional[str | Path] = None,
    data_dir: Optional[str | Path] = None,
) -> Dict[str, Any]:
    grants = run_scrapers(use_fixtures=use_fixtures, fixture_root=fixture_root)
    path = persist_grants(grants, data_dir=data_dir)
    agencies = sorted({g.get("administering_agency") for g in grants if g.get("administering_agency")})
    return {
        "path": str(path),
        "count": len(grants),
        "agencies": agencies,
        "grants": grants,
    }
