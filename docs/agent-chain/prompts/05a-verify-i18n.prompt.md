# Phase 05a: Verify i18n

## Goal

Verify FR/EN parity and switcher. **No new features.**

## Preconditions

- `phase-05-approved`.

## Steps

1. Diff phase 05 Done-when.
2. Assert EN/FR key parity via tests or script.
3. Confirm funder links still cite `SOURCES.md`.
4. Write `docs/agent-chain/audits/05a-audit.md`.

## Decision rules

- Missing FR keys on primary routes → FAIL.
- Pass → `phase-05-verified`.

## Done when

- [ ] Key parity evidenced
- [ ] Build green

## Verify commands

```bash
cd frontend && npx tsc --noEmit && npm run lint && npm run build
python api/test_api.py
```
