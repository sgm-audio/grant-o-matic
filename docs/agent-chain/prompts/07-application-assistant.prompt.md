# Phase 07: Application assistant

## Goal

Expand beyond budget templates into a broader application assistant: requirement checklists, project description helpers, and structured drafts grounded in grant `application_requirements` / `assessment_criteria`.

## Scope

- In scope: extend `budget_generator.py` or sibling modules; API endpoints; frontend assistant panel; tests; no hallucinated requirements.
- Out of scope: submitting applications to funders, autofill of third-party portals.

## Preconditions

- Phase `06a-verify-tax-credits` verified.
- Read `ai_model/budget_generator.py` and match response shape.

## Steps

1. Checklist generator from grant `application_requirements`.
2. Draft helpers (project summary, artistic need) that take user inputs + grant fields only.
3. Keep budget justification path; add tests for each generator.
4. Frontend UX on match detail.
5. If LLM used, same guardrails as phase 04 (mock in CI; no invented requirements).

## Full test coverage bar

- Unit tests for checklist completeness and budget categories.
- API tests for assistant endpoints.
- Snapshot or string tests ensuring output references only provided grant fields.

## Documentation + citations

- Assistant copy linking to programs must use grant `url` and `SOURCES.md` agencies.
- State clearly that applicants must confirm requirements on the official page.

## Decision rules

- Invented requirements → fail.
- PR: `phase-07: application assistant`, label `phase-07`.

## Tools

- PR creation enabled.

## Done when

- [ ] Checklist + draft helpers shipped
- [ ] Budget path still works
- [ ] Tests green; `HANDOFF.md` updated

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
