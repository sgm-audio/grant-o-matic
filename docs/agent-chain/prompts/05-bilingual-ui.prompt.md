# Phase 05: Bilingual (FR/EN) UI

## Goal

Ship French and English UI strings for all user-facing frontend copy, with a language switcher and persistent preference.

## Scope

- In scope: i18n framework, EN/FR catalogs for Home, Matcher, About, deadlines/auth screens that exist, `lang` routing or toggle, tests for missing keys.
- Out of scope: translating scraped grant JSON (unless trivial); backend locale negotiation beyond `Accept-Language` optional support.

## Preconditions

- Phase `04a-verify-llm-matching` verified.
- Read `frontend/src/pages/*` and `App.tsx`.

## Steps

1. Add i18n library already compatible with the stack (or lightweight custom dictionaries).
2. Extract all user-visible strings; provide FR + EN.
3. Language switcher in nav; persist preference (localStorage).
4. Ensure grant content from API remains in source language with clear labeling if untranslated.
5. Test: no missing key in either locale for rendered routes.

## Full test coverage bar

- Unit test that EN and FR catalogs contain the same keys.
- Build + lint + tsc pass.
- Smoke: both locales render matcher form labels.

## Documentation + citations

- About page funder links must use `SOURCES.md` (e.g. https://canadacouncil.ca/, https://www.factor.ca/, https://musicaction.ca/).
- Do not invent French program names; use official names from agency sites.

## Decision rules

- Incomplete FR catalog → no PR.
- PR: `phase-05: bilingual FR/EN UI`, label `phase-05`.

## Tools

- PR creation enabled.

## Done when

- [ ] Language switcher works
- [ ] Key parity EN/FR
- [ ] Tests/build green
- [ ] `HANDOFF.md` updated

## Verify commands

```bash
cd frontend && npx tsc --noEmit && npm run lint && npm run build
python api/test_api.py
```
