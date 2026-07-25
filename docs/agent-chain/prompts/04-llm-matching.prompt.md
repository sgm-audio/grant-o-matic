# Phase 04: Multi-LLM matching

## Goal

Add optional LLM re-ranking / explanation (Groq and/or Anthropic) on top of the existing keyword scoring engine—not a replacement that invents grants.

## Scope

- In scope: provider adapters behind env flags, merge LLM rationale with `EnhancedGrantMatchingEngine` scores, API field for explanations, tests with mocked providers.
- Out of scope: training custom models, changing grant corpus, bilingual UI.

## Preconditions

- Phase `03a-verify-accounts` verified.
- Read `ai_model/enhanced_matching_engine.py`.

## Steps

1. Design interface: rule score first; optional LLM explain/re-rank top-N only from **existing** grant IDs.
2. Implement Groq and Anthropic clients selected by `LLM_PROVIDER` env; disable when keys absent.
3. Mocked unit/API tests (no live LLM calls in CI).
4. Document cost/privacy and that LLM must not invent programs.
5. Frontend: show explanation when present.

## Full test coverage bar

- Mock provider tests for success, timeout, and invalid JSON.
- Assert LLM cannot introduce grant IDs not in the candidate set.
- Rule-only path still works with no API keys.

## Documentation + citations

- When naming agencies in examples, cite `SOURCES.md`.
- Document that eligibility facts come from grant records / official sites, not model memory.

## Decision rules

- If LLM can invent grants → fail; do not ship.
- PR: `phase-04: optional LLM matching layer`, label `phase-04`.

## Tools

- PR creation enabled. Keys only in secrets.

## Done when

- [ ] Optional LLM layer with mocks in CI
- [ ] Guardrail: only existing grant IDs
- [ ] Rule-only fallback works
- [ ] `HANDOFF.md` updated

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
