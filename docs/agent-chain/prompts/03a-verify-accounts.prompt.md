# Phase 03a: Verify accounts

## Goal

Verify auth and saved matches. **No new features.**

## Preconditions

- `phase-03-approved`.

## Steps

1. Diff phase 03 Done-when.
2. Re-run API tests including 401/403 cases.
3. Confirm passwords hashed; no secrets in repo.
4. Frontend auth + save flow builds.
5. Write `docs/agent-chain/audits/03a-audit.md`.

## Decision rules

- Plaintext passwords or missing authz tests → FAIL.
- Pass → `phase-03-verified`.

## Done when

- [ ] Audit report written
- [ ] Authz cases evidenced

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
