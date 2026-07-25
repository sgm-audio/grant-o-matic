# Phase 07a: Verify application assistant

## Goal

Verify assistant outputs stick to grant fields. **No new features.**

## Preconditions

- `phase-07-approved`.

## Steps

1. Diff phase 07 Done-when.
2. Re-run tests; sample outputs for invented requirements.
3. Confirm budget path still works with `budget_amount`.
4. Write `docs/agent-chain/audits/07a-audit.md`.

## Decision rules

- Invented requirements → FAIL.
- Pass → `phase-07-verified`.

## Done when

- [ ] Audit report written
- [ ] Budget + checklist evidenced

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
