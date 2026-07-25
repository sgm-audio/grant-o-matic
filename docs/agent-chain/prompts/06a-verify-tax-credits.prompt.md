# Phase 06a: Verify tax credits / SR&ED

## Goal

Verify checker citations and disclaimers. **No new features.**

## Preconditions

- `phase-06-approved`.

## Steps

1. Diff phase 06 Done-when.
2. Re-run tests; ensure every response includes citations.
3. Re-fetch CRA URLs (WebFetch or `curl -4`); update `SOURCES.md` verification log.
4. Confirm “not tax advice” disclaimer in UI.
5. Write `docs/agent-chain/audits/06a-audit.md`.

## Documentation + citations

- https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html
- https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/corporations.html

## Decision rules

- Uncited rules → FAIL.
- Pass → `phase-06-verified`.

## Done when

- [ ] CRA URLs re-verified in audit
- [ ] Disclaimer evidenced
- [ ] Tests green

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
