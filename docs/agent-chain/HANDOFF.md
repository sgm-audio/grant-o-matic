# Agent chain handoff

Copy this file to `HANDOFF.md` on the first phase run and keep it updated.

## Current state

- **Last completed phase:** `02-deadline-alerts` (PR open)
- **Last verify status:** `pass`
- **Active branch / PR:** `cursor/phase-02-deadline-alerts-adf9`
- **Blocked:** `none`
- **01a gate:** PASS — `docs/agent-chain/audits/01a-audit.md`; `phase-01-verified` applied on PR #4

## Environment notes

- Python / Node versions verified: Python 3.12.x; Node 20+/22
- Secrets required next (names only, never values): none for ICS path; future email alerts would need provider keys (not committed)
- Data path (`GRANT_DATA_PATH`): repo `data/` / Docker `/app/data`

## Data / product facts

- Grants loaded count: `9`
- Agencies present in data: `Canada Council for the Arts`, `FACTOR`
- Deadlines populated (yes/no + count): **yes, partial — 2** grants with `next_deadline` (FACTOR JSR Album `2026-09-10`, FACTOR Video `2027-01-14`). CCA programs still `null` (link to official deadlines page).
- Documented minimum note: system implemented despite sparse coverage; **do not invent dates**.
- Alert channel: **ICS download** (`GET /deadlines/export.ics`) — primary. Email not configured.
- Claims that must not appear in UI until data exists: Musicaction, OAC, BC Arts Council, Telefilm, CMF, SOCAN Foundation, municipal programs, tax credits

## Tests run (last phase)

```text
python3 test_deadline_tracker.py
python3 api/test_api.py
python3 .github/workflows/validate_data.py
cd frontend && npx tsc --noEmit && npm run lint && npm run build
```

## Citations added or changed

| Claim | Source URL | Verified (date UTC) |
|-------|------------|---------------------|
| FACTOR deadlines hub linked from UI | https://www.factor.ca/artists/deadlines/ | 2026-07-28 (domain already in SOURCES; page linked as official) |
| Canada Council deadlines hub linked from UI | https://canadacouncil.ca/funding/grants/deadlines | 2026-07-28 |

## Next phase instructions

- **Next phase id:** `02a-verify-deadlines`
- **Preconditions met:** after human `phase-02-approved`
- **Files the next agent should read first:**
  - `docs/agent-chain/prompts/02a-verify-deadlines.prompt.md`
  - `deadline_tracker.py`
  - `frontend/src/pages/Deadlines.tsx`
  - `docs/agent-chain/HANDOFF.md`

## Open risks / UI checklist (no frontend test runner)

- [ ] Open `/deadlines` with API running — list shows dated FACTOR rows
- [ ] Download ICS — imports into calendar client
- [ ] Official program URL opens agency page
- Sparse CCA deadline coverage remains a data gap for later scraper enrichment
