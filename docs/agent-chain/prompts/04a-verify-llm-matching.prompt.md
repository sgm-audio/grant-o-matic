# Phase 04a: Verify LLM matching

## Goal

Verify optional LLM layer guardrails. **No new features.**

## Preconditions

- `phase-04-approved`.

## Steps

1. Confirm CI uses mocks (no live provider calls).
2. Confirm rule-only path works without keys.
3. Confirm LLM cannot introduce unknown grant IDs (test evidence).
4. Write `docs/agent-chain/audits/04a-audit.md`.

## Decision rules

- Hallucinated grants possible → FAIL.
- Pass → `phase-04-verified`.

## Done when

- [ ] Guardrail tests evidenced
- [ ] Fallback path evidenced

## Verify commands

```bash
python api/test_api.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```
