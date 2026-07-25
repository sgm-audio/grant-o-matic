# Phase 03: User accounts and saved matches

## Goal

Add authenticated user accounts and persistence for saved grant matches.

## Scope

- In scope: auth (secure password or magic-link; document choice), user store, save/list/delete matches APIs, frontend save UX, tests.
- Out of scope: OAuth social providers beyond one method, LLM, tax credits, i18n.

## Preconditions

- Phase `02a-verify-deadlines` verified.
- Persistence choice: SQLite or Postgres via env `DATABASE_URL` (default SQLite for local).

## Steps

1. Add persistence layer and migrations.
2. Implement register/login/logout (or magic-link) with hashed credentials / signed tokens.
3. Endpoints: save match, list saved, delete saved (auth required).
4. Frontend: auth screens + save button on match results.
5. Full API tests including unauthorized access cases.
6. Document env vars; never commit secrets.

## Full test coverage bar

- Unit tests for auth helpers and password hashing.
- API tests for auth and saved-match CRUD, including 401/403 cases.
- No plaintext passwords in logs or fixtures.

## Documentation + citations

- Product docs may link arts funders when describing saved grants; use `SOURCES.md` only.
- Security notes in README or `docs/`.

## Decision rules

- If auth is incomplete → no PR.
- PR: `phase-03: accounts and saved matches`, label `phase-03`.

## Tools

- PR creation enabled.

## Done when

- [ ] Users can register/login
- [ ] Matches can be saved and listed
- [ ] Tests cover authz failures
- [ ] `HANDOFF.md` updated

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
