# Prompt chain verification report

**Date (UTC):** 2026-07-25  
**Branch intent:** author-and-verify prompt chain only (no feature phase execution)  
**Auditor:** META criteria from `prompts/META-verify-prompt-chain.prompt.md`

## Summary

| Check | Result |
|-------|--------|
| phases.json ↔ prompt files bijection | **PASS** |
| Implement/verify pairing (00–08) + 99 + META | **PASS** |
| Implement prompt contract sections | **PASS** |
| Verify/audit no-new-features + audit report | **PASS** |
| Roadmap → phase mapping | **PASS** |
| Source URL verification | **PASS** (see notes) |
| Automation wiring paths | **PASS** |
| Forbidden “skip tests” / invent-data instructions | **PASS** (negations only) |

**Overall: PASS**

## Completeness

- Phase count in `phases.json`: **20**
- Missing `prompt_path` files: **none**
- Unlisted `prompts/*.prompt.md` files: **none**
- Pairs present: 00/00a … 08/08a, `99-full-system-audit`, `META-verify-prompt-chain`
- Dependency edges: all `depends_on` ids resolve

## Roadmap mapping

| README roadmap item | Phase |
|---------------------|-------|
| Live integrated scraping (CCA / FACTOR) | 01 (+ 01a) |
| Deadline alert system | 02 (+ 02a) |
| Multi-LLM matching | 04 (+ 04a) |
| User accounts and saved matches | 03 (+ 03a) |
| Bilingual FR/EN UI | 05 (+ 05a) |
| SR&ED tax credit eligibility checker | 06 (+ 06a) |

Additional high-value phases: 00 bootstrap, 07 application assistant, 08 ops/CI, 99 full audit.

## Contract lint (implement phases)

Required headings present in all implement prompts:

- Goal, Scope, Preconditions, Steps, Full test coverage bar, Documentation + citations, Decision rules, Done when, Verify commands

## Verify/audit lint

All verify/audit prompts instruct no new features (or META: do not implement product features) and require an audit/report artifact (`audits/*` or `CHAIN-VERIFICATION.md`).

## Source lint

Canonical URLs from `SOURCES.md` (14 unique):

| URL | Method | HTTP / evidence |
|-----|--------|-----------------|
| https://canadacouncil.ca/ | curl -4 | 200 |
| https://canadacouncil.ca/funding/grants | curl -4 | 200 |
| https://www.factor.ca/ | curl -4 | 200 |
| https://musicaction.ca/ | curl -4 | 200 (`.com` rejected; not listed) |
| https://telefilm.ca/ | curl -4 | 200 |
| https://cmf-fmc.ca/ | curl -4 | 200 |
| https://www.socanfoundation.ca/ | curl -4 | 200 |
| https://www.arts.on.ca/ | curl -4 | 200 |
| https://www.bcartscouncil.ca/ | curl -4 | 200 |
| https://www.canada.ca/.../scientific-research-experimental-development-tax-incentive-program.html | WebFetch | 200 content (SR&ED page; curl often fails on Akamai HTTP/2) |
| https://www.canada.ca/.../corporations.html | WebFetch | 200 content (Corporations page) |
| https://cursor.com/docs/cloud-agent/automations.md | curl -4 | 200 |
| https://cursor.com/docs/cloud-agent/api/endpoints.md | curl -4 | 200 |
| https://cursor.com/docs/cloud-agent/best-practices.md | curl -4 | 200 |

## Automation wiring

- `WIRING.md` lists Automations for every phase id with matching prompt paths
- `automation/launch-phase.example.sh` resolves paths via `phases.json`
- `automation/README.md` documents API sequencing and human gates

## Explicit non-execution

This verification **did not**:

- Run scrapers or mutate `data/all_grants.json`
- Change matching engine, API product behavior, or frontend features
- Create Cursor dashboard Automations
- Call Cloud Agents API to build product phases

## Residual notes for operators

1. Prefer `curl -4` or WebFetch when re-checking `canada.ca` from Cloud Agent VMs.
2. Create GitHub labels listed in `WIRING.md` before enabling label triggers.
3. Align `launch-phase.example.sh` JSON body with the latest Cloud Agents API schema before production use.
4. Start execution with phase **00-bootstrap** only after merging this authoring PR.
