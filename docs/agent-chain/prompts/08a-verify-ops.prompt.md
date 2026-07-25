# Phase 08a: Verify ops / CI

## Goal

Verify CI coverage gates and README accuracy. **No new features.**

## Preconditions

- `phase-08-approved`.

## Steps

1. Diff phase 08 Done-when.
2. Confirm coverage gate exists and fails on drop (read workflow).
3. Claims audit README vs data vs implemented endpoints.
4. Write `docs/agent-chain/audits/08a-audit.md`.

## Decision rules

- README advertises unimplemented features as live → FAIL.
- Pass → `phase-08-verified`.

## Done when

- [ ] Coverage gate evidenced
- [ ] Claims audit pass
- [ ] Verify commands green

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
docker build -t grant-o-matic-api .
```
