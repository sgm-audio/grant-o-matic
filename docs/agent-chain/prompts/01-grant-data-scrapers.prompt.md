# Phase 01: Grant data + scrapers

## Goal

Replace stub scraping with real Canada Council + FACTOR ingestion, expand `data/all_grants.json` beyond the current six Canada Council rows, and wire `POST /scrape` to run scrapers and reload the matching engine.

## Scope

- In scope: scrapers under `scraper/`, API scrape endpoint in `api/main.py`, fixture-based scraper tests, data schema validation, README/data docs with citations.
- Out of scope: user accounts, LLM matching, deadline alert delivery, tax credits.

## Preconditions

- Phase `00a-verify-bootstrap` verified (`phase-00-verified` or equivalent in `HANDOFF.md`).
- Read existing `scraper/canada_council*.py`, `data/all_grants.json`, `docs/grant-databases-research.md`.

## Steps

1. Implement/repair Canada Council scraper; add FACTOR scraper against https://www.factor.ca/ (fixture-tested).
2. Persist normalized grants into `data/all_grants.json` (or merge pipeline) matching the schema in research docs.
3. Wire `POST /scrape` to run scrapers in background and reload `EnhancedGrantMatchingEngine`.
4. Add fixture HTML under `scraper/fixtures/`; CI must not require live network.
5. Update user-facing source lists to match **actual** agencies in data, citing `SOURCES.md` URLs.
6. Run verify commands; open PR only if green.

## Full test coverage bar

- Unit tests for parse/normalize helpers.
- Fixture-based scraper tests (no live-net in CI).
- API tests for `/scrape` status and post-reload `/grants` / `/match`.
- `validate_data.py` passes on committed JSON.

## Documentation + citations

Required links when mentioning bodies:

- Canada Council grants: https://canadacouncil.ca/funding/grants
- FACTOR: https://www.factor.ca/

Do not invent program names, max amounts, or deadlines. If a field is unknown, use `null` and document.

## Decision rules

- If tests fail or sources cannot be verified → no PR; blockers in `HANDOFF.md`.
- If pass → PR `phase-01: live CCA + FACTOR grant data` with label `phase-01`.
- Never commit scraped PII or credentials.

## Tools

- PR creation enabled. Rate-limit scrapers; identify User-Agent as Grant-O-Matic.

## Done when

- [ ] `POST /scrape` is not a stub
- [ ] Data includes Canada Council and FACTOR programs with cited URLs
- [ ] Fixture tests + API tests + validate_data pass
- [ ] README/UI claims match data
- [ ] `HANDOFF.md` updated (grant count, agencies)

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
# scraper fixture tests (path as implemented, e.g.):
python -m pytest scraper/ -q || python scraper/test_scraper.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
