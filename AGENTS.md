# Grant-O-Matic — Cursor Cloud Agent Instructions

This repository uses a **phased Cloud Agent prompt chain**. Do not invent grant programs, deadlines, funding amounts, or eligibility rules. Every user-facing claim about a funding body must cite a live URL from [`docs/agent-chain/SOURCES.md`](docs/agent-chain/SOURCES.md).

## Before any work

1. Read [`docs/agent-chain/README.md`](docs/agent-chain/README.md) and the active phase prompt under `docs/agent-chain/prompts/`.
2. Read [`docs/agent-chain/HANDOFF.md`](docs/agent-chain/HANDOFF.md) if it exists (copy from `HANDOFF.template.md` on first run).
3. Confirm preconditions for your phase (`depends_on` in [`docs/agent-chain/phases.json`](docs/agent-chain/phases.json)).

## Hard rules

- **No feature work outside your phase scope.** Verify/audit phases only report or apply minimal fixes.
- **Full test coverage for new code.** Public functions and API routes need tests. Scrapers use fixture HTML; do not hit live networks in CI.
- **Citations required.** If a source cannot be verified with HTTP GET/HEAD, mark `UNVERIFIED` and keep it out of user-facing copy.
- **No secrets in the repo.** Use environment variables / Cursor secrets only.
- **Decision rule:** open or update a PR only when the phase’s verify commands pass; otherwise write blockers to `HANDOFF.md` and stop.
- **Claims audit:** README and UI must not advertise agencies or programs absent from loaded grant data.

## Standard verify commands

```bash
# Backend
python api/test_api.py
python .github/workflows/validate_data.py

# Frontend
cd frontend && npx tsc --noEmit && npm run lint && npm run build

# Docker (when compose exists)
docker build -t grant-o-matic-api .
```

Phase prompts may add more commands; those are authoritative for that phase.

## Handoff

At the end of every phase, update `docs/agent-chain/HANDOFF.md` using the template fields so the next agent can continue without rediscovering state.

## Prompt chain location

| Artifact | Path |
|----------|------|
| Chain map | `docs/agent-chain/README.md` |
| Phase prompts | `docs/agent-chain/prompts/*.prompt.md` |
| Automation wiring | `docs/agent-chain/WIRING.md` |
| Source registry | `docs/agent-chain/SOURCES.md` |
| Phase graph | `docs/agent-chain/phases.json` |
