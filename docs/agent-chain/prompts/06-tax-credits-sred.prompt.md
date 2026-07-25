# Phase 06: Tax credits + SR&ED eligibility checker

## Goal

Add an eligibility checker for relevant Canadian tax incentives (starting with CRA SR&ED overview guidance and clearly scoped provincial/audio tax-credit pointers), with every rule cited to government sources.

## Scope

- In scope: questionnaire API + UI, rule engine that outputs eligible / maybe / not eligible with citations, links to CRA SR&ED page, disclaimers that this is not tax advice.
- Out of scope: filing taxes, CRA API integration, inventing credit percentages.

## Preconditions

- Phase `05a-verify-i18n` verified.
- Read `docs/agent-chain/SOURCES.md` CRA entries and `docs/grant-databases-research.md` tax section.

## Steps

1. Define a minimal question set (business type, R&D activity, jurisdiction) grounded in CRA SR&ED public guidance.
2. Implement checker returning status + cited URLs + next official steps.
3. Frontend flow with strong disclaimer.
4. Tests for rule branches; citation URLs must be in `SOURCES.md` or fetch-verified government domains added there.
5. Re-verify CRA URLs (`curl -4` or WebFetch) in the PR evidence.

## Full test coverage bar

- Unit tests for each eligibility branch.
- API tests for the checker endpoint.
- Assertion that every response includes at least one citation URL.

## Documentation + citations (required)

- SR&ED: https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html
- Corporations context: https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/corporations.html
- Provincial credits: only add when verified on official `.gov` / provincial domains; update `SOURCES.md`.

## Decision rules

- Any rule without a live citation → do not ship that rule.
- This is guidance UX, not legal advice—disclaimer required.
- PR: `phase-06: tax credit and SR&ED checker`, label `phase-06`.

## Tools

- PR creation enabled.

## Done when

- [ ] Checker API + UI with citations
- [ ] Disclaimer present
- [ ] CRA URLs re-verified in audit notes
- [ ] Tests green; `HANDOFF.md` updated

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
# Re-check CRA URLs (prefer IPv4):
curl -4 -sL -o /dev/null -w "%{http_code}\n" "https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html" || true
```
