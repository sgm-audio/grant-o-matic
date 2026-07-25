# Canonical source registry

Agents may cite these URLs in documentation and UI only after a successful HTTP HEAD or GET in the current phase. To add a source: fetch it, record the verification date below, then use it.

Do **not** invent program names, amounts, or deadlines. Prefer primary government or administering-agency pages over secondary blogs.

## Federal / national arts and media

| Body | URL | Notes |
|------|-----|-------|
| Canada Council for the Arts | https://canadacouncil.ca/ | Primary arts funder |
| Canada Council — Funding / Grants | https://canadacouncil.ca/funding/grants | Grant program index |
| FACTOR | https://www.factor.ca/ | Sound recording / music industry (`factor.ca` redirects here) |
| Musicaction | https://musicaction.ca/ | Francophone music industry (use `.ca`; `.com` is not reliable) |
| Telefilm Canada | https://telefilm.ca/ | Film / audiovisual |
| Canada Media Fund (CMF) | https://cmf-fmc.ca/ | Media fund |
| SOCAN Foundation | https://www.socanfoundation.ca/ | Music creators |

## Provincial arts councils

| Body | URL | Notes |
|------|-----|-------|
| Ontario Arts Council | https://www.arts.on.ca/ | Ontario |
| BC Arts Council | https://www.bcartscouncil.ca/ | British Columbia |

## Tax incentives (CRA / government)

| Program area | URL | Notes |
|--------------|-----|-------|
| SR&ED tax incentive (CRA) | https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html | Federal SR&ED overview |
| CRA — Corporations | https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/corporations.html | Corporate tax context |

## Product / platform docs (automation)

| Topic | URL |
|-------|-----|
| Cursor Automations | https://cursor.com/docs/cloud-agent/automations.md |
| Cursor Cloud Agents API | https://cursor.com/docs/cloud-agent/api/endpoints.md |
| Cursor Cloud Agent best practices | https://cursor.com/docs/cloud-agent/best-practices.md |

## Verification log

Updated when the chain is authored and by audit phases. Prefer `curl -4` if HTTP/2 to `canada.ca` fails in the agent environment.

| URL | Status | HTTP | Verified (UTC) | Effective URL / notes |
|-----|--------|------|----------------|------------------------|
| https://canadacouncil.ca/ | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://canadacouncil.ca/funding/grants | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://www.factor.ca/ | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://musicaction.ca/ | ok | 200 | 2026-07-25T21:05:00Z | replaces musicaction.com |
| https://telefilm.ca/ | ok | 200 | 2026-07-25T21:05:00Z | www redirects to apex |
| https://cmf-fmc.ca/ | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://www.socanfoundation.ca/ | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://www.arts.on.ca/ | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://www.bcartscouncil.ca/ | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://www.canada.ca/en/revenue-agency/services/scientific-research-experimental-development-tax-incentive-program.html | ok | 200 | 2026-07-25T21:10:00Z | WebFetch (curl to Akamai often INTERNAL_ERROR; content confirmed SR&ED page) |
| https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/corporations.html | ok | 200 | 2026-07-25T21:05:00Z | WebFetch (curl flaky; content confirmed Corporations tax page) |
| https://cursor.com/docs/cloud-agent/automations.md | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://cursor.com/docs/cloud-agent/api/endpoints.md | ok | 200 | 2026-07-25T21:05:00Z | same |
| https://cursor.com/docs/cloud-agent/best-practices.md | ok | 200 | 2026-07-25T21:05:00Z | same |

## Rules for agents

1. User-facing copy about a program must include a working link from this registry (or a child page on the same official domain that was fetch-verified in the same PR).
2. If fetch fails, mark the claim `UNVERIFIED` in handoff and exclude it from README/UI.
3. Amounts and deadlines must come from the linked page or official PDF linked from that page—not from memory.
4. Secondary sources (news, blogs) are allowed only as supplemental context, never as the sole citation for eligibility or funding amounts.
