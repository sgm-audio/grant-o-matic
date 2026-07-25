# Phase 01a: Audit grant data + scrapers

## Goal

Audit phase 01 data quality, scraper tests, citations, and claims vs reality. **No new features** except minimal fixes.

## Preconditions

- Phase 01 labeled `phase-01-approved`.

## Steps

1. Diff against phase 01 Done-when.
2. Re-run API, validate_data, scraper fixture tests.
3. Fetch-verify every distinct agency `url` domain against `SOURCES.md` (add only after successful fetch).
4. Confirm `POST /scrape` is not a print-only stub.
5. Claims audit: README/UI agencies ⊆ data agencies.
6. Write `docs/agent-chain/audits/01a-audit.md`.

## Documentation + citations

- Spot-check: https://canadacouncil.ca/funding/grants and https://www.factor.ca/
- Reject invented amounts/deadlines.

## Decision rules

- Live-net required in CI → FAIL.
- Stub scrape remains → FAIL.
- Pass → recommend `phase-01-verified`.

## Done when

- [ ] Audit report written
- [ ] Source spot-checks recorded
- [ ] Handoff updated with agencies + grant count

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
python -m pytest scraper/ -q || python scraper/test_scraper.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
