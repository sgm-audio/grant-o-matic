# Phase 99: Full system audit

## Goal

End-to-end audit of the product after phases 00–08: tests, citations, security hygiene, and claims vs reality. **No new features.**

## Scope

- In scope: run full checklist in `docs/agent-chain/CHECKLIST.md`, re-fetch sources, produce `docs/agent-chain/audits/99-full-system-audit.md`, minimal fixes only for audit failures.
- Out of scope: roadmap features not yet implemented.

## Preconditions

- Phase `08a-verify-ops` verified (`phase-08-verified`).

## Steps

1. Run all verify commands from phases 00–08 that still apply.
2. Spot-check `SOURCES.md` URLs (HTTP GET/HEAD; use `curl -4` for canada.ca if needed).
3. Claims audit: README, Home, About vs grant data and implemented endpoints.
4. Security: secrets, CORS, authz on saved matches, scraper User-Agent.
5. Write audit report with pass/fail evidence.
6. Open findings PR **only** for minimal fixes required to pass audit; otherwise report-only.

## Full test coverage bar

- Confirm CI-equivalent commands pass locally.
- List any modules lacking tests as FAIL items.

## Documentation + citations

- Every failing citation must be fixed or removed from user-facing copy.
- Official references: Canada Council https://canadacouncil.ca/funding/grants , FACTOR https://www.factor.ca/ , CRA SR&ED https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html

## Decision rules

- Feature work disguised as audit → reject.
- If audit fails → PR with fixes + report; if pass → PR with report only or attach report on existing branch.
- Label `chain-complete` only when audit passes.

## Tools

- PR creation enabled for fixes/report.

## Done when

- [ ] `audits/99-full-system-audit.md` written
- [ ] All checklist sections addressed
- [ ] Sources re-verified
- [ ] `HANDOFF.md` marks chain complete or lists residual risks

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
docker build -t grant-o-matic-api .
```
