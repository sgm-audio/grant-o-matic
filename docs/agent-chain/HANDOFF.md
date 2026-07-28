# Agent chain handoff

Copy this file to `HANDOFF.md` on the first phase run and keep it updated.

## Current state

- **Last completed phase:** `01-grant-data-scrapers` (PR open; await review)
- **Last verify status:** `pass` (local verify commands)
- **Active branch / PR:** `cursor/phase-01-grant-data-scrapers-adf9` — https://github.com/SGM-Studios/grant-o-matic/pull/4
- **Blocked:** `none`
- **Note:** User asked to “begin phase 2”; chain phase `02-deadline-alerts` requires `01a` first, so this run implemented **phase 01**.

## Environment notes

- Python / Node versions verified: Python 3.12.3; Node (frontend toolchain as in CI)
- Secrets required next (names only, never values): none for 01a; phase 02 may need email provider env vars if email alerts are chosen
- Data path (`GRANT_DATA_PATH`): repo `data/` / Docker `/app/data`

## Data / product facts

- Grants loaded count: `9`
- Agencies present in data: `Canada Council for the Arts`, `FACTOR`
- Deadlines populated (yes/no + count): partial — **2** FACTOR programs have `next_deadline` (`2026-09-10` JSR Album; `2027-01-14` Video fiscal cutoff). CCA deadlines intentionally `null` (point to official deadlines page).
- Claims that must not appear in UI until data exists: Musicaction, OAC, BC Arts Council, Telefilm, CMF, SOCAN Foundation, municipal programs, federal/provincial tax credits

## Tests run (last phase)

```text
python3 scraper/test_scraper.py                  PASS
python3 api/test_api.py                          PASS (includes /scrape fixtures reload)
python3 .github/workflows/validate_data.py       PASS
cd frontend && npx tsc --noEmit && npm run lint && npm run build
                                                 (run before PR)
```

## Citations added or changed

| Claim | Source URL | Verified (date UTC) |
|-------|------------|---------------------|
| Canada Council grants programs in catalog | https://canadacouncil.ca/funding/grants | 2026-07-26 (HTTP 200 + program pages fetched for fixtures) |
| FACTOR artist programs / amounts / deadlines in catalog | https://www.factor.ca/ | 2026-07-26 (HTTP 200 + program pages fetched for fixtures) |

## Next phase instructions

- **Next phase id:** `01a-audit-grant-data`
- **Preconditions met:** after human review + `phase-01-approved`
- **Files the next agent should read first:**
  - `docs/agent-chain/prompts/01a-audit-grant-data.prompt.md`
  - `scraper/` + `scraper/fixtures/`
  - `data/all_grants.json`
  - `docs/agent-chain/HANDOFF.md`

## Open risks

- CCA funding amounts left `null` (not on scraped program overview pages); do not invent.
- FACTOR Video max uses first “project maximum” phrase ($20,000 Artist 2); Artist 3 $30,000 also on page.
- Live `POST /scrape` without fixtures hits the network; CI uses `use_fixtures=true`.
- Phase 02 still blocked until 01a verifies.
