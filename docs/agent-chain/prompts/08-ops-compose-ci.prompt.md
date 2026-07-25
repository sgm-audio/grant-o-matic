# Phase 08: Ops, compose, CI coverage gates

## Goal

Harden operations: ensure docker compose, CI coverage gates, deploy docs, and claims in README match reality after prior phases.

## Scope

- In scope: `.github/workflows/ci.yml` coverage/reporting, compose polish, deploy notes (Render/Fly/static), README accuracy, remove or label stubs.
- Out of scope: new product features.

## Preconditions

- Phase `07a-verify-application-assistant` verified.

## Steps

1. Add coverage measurement for Python (e.g. coverage.py) and fail CI under agreed threshold for touched packages (document threshold in workflow).
2. Ensure frontend lint/tsc/build remain required.
3. Align README architecture, endpoints, and roadmap checkboxes with implemented features.
4. Document deploy env vars; cite Cursor/ops docs only if relevant.
5. Claims audit against `data/all_grants.json` agencies.

## Full test coverage bar

- CI enforces tests + coverage gate.
- Data validation job remains.
- Docker build job remains or improves via compose.

## Documentation + citations

- Funder lists must match data + `SOURCES.md`.
- Roadmap items done should be checked off only if truly shipped.

## Decision rules

- Marketing ahead of data → fix copy before PR merge.
- PR: `phase-08: ops CI and docs accuracy`, label `phase-08`.

## Tools

- PR creation enabled.

## Done when

- [ ] Coverage gate in CI
- [ ] README claims accurate
- [ ] Compose + deploy docs usable
- [ ] `HANDOFF.md` updated

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
docker build -t grant-o-matic-api .
```
