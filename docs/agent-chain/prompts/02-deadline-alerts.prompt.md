# Phase 02: Deadline alerts

## Goal

Expose `DeadlineTracker` via API and UI, populate deadlines from grant data, and add email and/or calendar (ICS) alert pathways.

## Scope

- In scope: wire `deadline_tracker.py` into `api/main.py`, endpoints for upcoming deadlines, frontend deadlines view, ICS export and/or email alert stub with config via env secrets.
- Out of scope: LLM matching, accounts (beyond optional email address in alert signup if needed—prefer no auth yet), tax credits.

## Preconditions

- Phase `01a-audit-grant-data` verified; grants preferably include real `next_deadline` values.
- Read `deadline_tracker.py` and current API imports.

## Steps

1. Add API routes: list upcoming deadlines, load from grants, export ICS.
2. Integrate tracker on startup from loaded grants.
3. Frontend page or section listing deadlines with links to official program URLs.
4. Alert channel: env-configured email provider **or** downloadable ICS (document which).
5. Tests for tracker logic + API; no secrets in repo.
6. Update handoff with deadline coverage stats.

## Full test coverage bar

- Unit tests for date parsing, upcoming/passed status, ICS generation.
- API tests for new endpoints.
- UI builds; add component tests if the repo has a frontend test runner—otherwise manual checklist in handoff.

## Documentation + citations

- Deadlines shown must come from grant records whose `url` points to an official agency page in `SOURCES.md` domains.
- Do not fabricate deadline dates.

## Decision rules

- If fewer than a documented minimum of grants have deadlines, implement the system but mark data gap in handoff; do not invent dates.
- PR only if tests green: `phase-02: deadline tracking and alerts`, label `phase-02`.

## Tools

- PR creation enabled. Email API keys via Cursor/host secrets only.

## Done when

- [ ] DeadlineTracker used by API (not unused import)
- [ ] UI surfaces upcoming deadlines
- [ ] ICS and/or email path documented and tested
- [ ] Tests green; `HANDOFF.md` updated

## Verify commands

```bash
python api/test_api.py
python .github/workflows/validate_data.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
