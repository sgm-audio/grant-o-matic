# Agent chain handoff

Copy this file to `HANDOFF.md` on the first phase run and keep it updated.

## Current state

- **Last completed phase:** `00-bootstrap`
- **Last verify status:** `pass`
- **Active branch / PR:** `cursor/phase-00-bootstrap-adf9`
- **Blocked:** `none`

## Environment notes

- Python / Node versions verified: Python 3.12.3; Node v22.14.0; npm 10.9.7
- Secrets required next (names only, never values): none for phase 01 (scrapers use fixtures in CI)
- Data path (`GRANT_DATA_PATH`): defaults to repo `data/`; Docker compose sets `/app/data` and mounts `./data`

## Data / product facts

- Grants loaded count: `6`
- Agencies present in data: `Canada Council for the Arts`
- Deadlines populated (yes/no + count): no concrete `next_deadline` values (all `null`; frequency text only)
- Claims that must not appear in UI until data exists: FACTOR, Musicaction, OAC, BC Arts Council, Telefilm, CMF, SOCAN Foundation, municipal programs, federal/provincial tax credits

## Tests run (last phase)

```text
python3 api/test_api.py                          PASS (smoke /, /health, /grants + grant_data + compose validate)
python3 .github/workflows/validate_data.py       PASS
cd frontend && npx tsc --noEmit                  PASS
cd frontend && npm run lint                      PASS (3 pre-existing unused-var warnings)
cd frontend && npm run build                     PASS
docker compose config                            PASS
docker build -t grant-o-matic-api .              PASS (vfs storage driver required in this agent VM)
docker run smoke: GET /health grants_loaded=6    PASS
```

## Citations added or changed

| Claim | Source URL | Verified (date UTC) |
|-------|------------|---------------------|
| Canada Council funding/grants index linked from README + About | https://canadacouncil.ca/funding/grants | 2026-07-25 (HTTP 200 HEAD + WebFetch; Grants index page) |

## Next phase instructions

- **Next phase id:** `00a-verify-bootstrap`
- **Preconditions met:** yes (implement phase complete; await human `phase-00-approved` before verify automation)
- **Files the next agent should read first:**
  - `docs/agent-chain/prompts/00a-verify-bootstrap.prompt.md`
  - `docker-compose.yml`
  - `api/grant_data.py`
  - `docs/agent-chain/HANDOFF.md`

## Open risks

- Agent VM Docker may need `--storage-driver=vfs`; GitHub Actions should use default overlay2.
- Frontend offline mock in `GrantMatcher.tsx` still synthesizes match scores when API is down; agencies limited to Canada Council only.
- Sample FACTOR grants remain in `api/test_api.py` fixtures only (not user-facing catalog claims).
