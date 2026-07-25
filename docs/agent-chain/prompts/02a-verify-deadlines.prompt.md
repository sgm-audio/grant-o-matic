# Phase 02a: Verify deadlines

## Goal

Verify deadline API/UI/alerts from phase 02. **No new features.**

## Preconditions

- `phase-02-approved`.

## Steps

1. Diff Done-when for phase 02.
2. Re-run tests; hit deadline endpoints.
3. Confirm DeadlineTracker is used (not unused import).
4. Ensure displayed deadlines are not fabricated; missing data documented.
5. Write `docs/agent-chain/audits/02a-audit.md`.

## Decision rules

- Invented deadlines → FAIL and remove.
- Pass → `phase-02-verified`.

## Done when

- [ ] Audit report with endpoint evidence
- [ ] ICS/email path verified or explicitly deferred with handoff note

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
