# Phase 00a: Verify bootstrap

## Goal

Audit phase 00 against its Done-when checklist. **No new features.** Minimal fixes only if verification fails.

## Scope

- Verify compose, smoke tests, handoff, README accuracy for compose.
- Out of scope: scrapers, auth, LLM.

## Preconditions

- Phase 00 PR merged or labeled `phase-00-approved`.
- Read `docs/agent-chain/CHECKLIST.md` and phase 00 prompt.

## Steps

1. Diff against phase 00 Done-when items.
2. Re-run verify commands; record output in `docs/agent-chain/audits/00a-audit.md`.
3. Confirm `HANDOFF.md` exists and lists grant count.
4. Claims: README must not claim `docker compose up` unless compose file exists.
5. If fail → minimal fix PR; if pass → report-only update + recommend label `phase-00-verified`.

## Decision rules

- Do not start phase 01 work.
- Open PR only for audit report and/or minimal fixes.

## Done when

- [ ] `audits/00a-audit.md` with pass/fail evidence
- [ ] Verify commands re-run
- [ ] Label recommendation recorded in handoff

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
docker build -t grant-o-matic-api .
test -f docker-compose.yml || test -f compose.yaml
```
