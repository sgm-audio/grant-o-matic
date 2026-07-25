# Phase 00: Bootstrap

## Goal

Establish a reliable baseline for later phases: docker compose for API + frontend, hardened data loading, smoke tests, and an initial `HANDOFF.md`.

## Scope

- In scope: `docker-compose.yml` (API + frontend as documented in root README), smoke/health tests, ensure `GRANT_DATA_PATH` works, copy `HANDOFF.template.md` → `HANDOFF.md`, fix README compose instructions if needed.
- Out of scope: new scrapers, auth, LLM, i18n, tax credits, deadline UI.

## Preconditions

- Read `AGENTS.md`, `docs/agent-chain/SOURCES.md`, `docs/agent-chain/HANDOFF.template.md`.
- Starting from `main` (or latest verified chain branch).

## Steps

1. Add `docker-compose.yml` that builds/runs the FastAPI image and serves/runs the Vite frontend per README claims.
2. Confirm `GET /health` reports `grants_loaded` from `data/all_grants.json`.
3. Add or extend backend smoke tests covering `/`, `/health`, `/grants`.
4. Run verify commands below; fix failures before PR.
5. Create `docs/agent-chain/HANDOFF.md` from the template with current grant count and agencies.

## Full test coverage bar

- Every new public helper or compose-related script has a test or CI check.
- Existing `python api/test_api.py` and `python .github/workflows/validate_data.py` must pass.
- Frontend: `cd frontend && npx tsc --noEmit && npm run lint && npm run build`.

## Documentation + citations

- Do not expand “Supported grant sources” beyond agencies present in loaded data.
- Link Canada Council only if citing it: https://canadacouncil.ca/funding/grants

## Decision rules

- If tests fail → do not open PR; record blockers in `HANDOFF.md`.
- If pass → open PR titled `phase-00: bootstrap compose and smoke tests` with label `phase-00`.
- If already done → update handoff and do nothing else.

## Tools

- PR creation enabled. No secrets in repo. No destructive git.

## Done when

- [ ] `docker-compose.yml` present and documented
- [ ] Health/smoke tests pass
- [ ] `HANDOFF.md` created
- [ ] Verify commands green
- [ ] PR opened (or ready) with label `phase-00`

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
docker build -t grant-o-matic-api .
```
