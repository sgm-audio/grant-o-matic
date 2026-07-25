# Agent chain handoff

Copy this file to `HANDOFF.md` on the first phase run and keep it updated.

## Current state

- **Last completed phase:** `00a-verify-bootstrap`
- **Last verify status:** `pass`
- **Active branch / PR:** `cursor/phase-00a-verify-bootstrap-adf9` — https://github.com/SGM-Studios/grant-o-matic/pull/3 (audit); subject https://github.com/SGM-Studios/grant-o-matic/pull/2
- **Blocked:** `none`
- **Label recommendation:** add `phase-00-verified` on PR #2 / main after merging bootstrap + this audit

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
# 00a re-run 2026-07-25
python3 api/test_api.py                          PASS
python3 .github/workflows/validate_data.py       PASS
cd frontend && npx tsc --noEmit                  PASS
cd frontend && npm run lint                      PASS (3 unused-var warnings)
cd frontend && npm run build                     PASS
docker build -t grant-o-matic-api .              PASS
test -f docker-compose.yml                       PASS
```

Evidence: `docs/agent-chain/audits/00a-audit.md`

## Citations added or changed

| Claim | Source URL | Verified (date UTC) |
|-------|------------|---------------------|
| Canada Council funding/grants index linked from README + About | https://canadacouncil.ca/funding/grants | 2026-07-25 (phase 00; not re-fetched in 00a) |

## Next phase instructions

- **Next phase id:** `01-grant-data-scrapers`
- **Preconditions met:** pending human label `phase-00-verified` (00a audit PASS; bootstrap approved)
- **Files the next agent should read first:**
  - `docs/agent-chain/prompts/01-grant-data-scrapers.prompt.md`
  - `docs/agent-chain/audits/00a-audit.md`
  - `docs/agent-chain/SOURCES.md`
  - `docs/agent-chain/HANDOFF.md`
  - `scraper/` and `data/all_grants.json`

## Open risks

- Agent VM Docker may need `--storage-driver=vfs`; GitHub Actions should use default overlay2.
- Home page still advertises stub roadmap features (deadlines / application assistant) — cleanup deferred beyond 00a.
- Frontend offline mock synthesizes scores when API is down; agencies limited to Canada Council only.
- Sample FACTOR grants remain in `api/test_api.py` fixtures only (not user-facing catalog claims).
