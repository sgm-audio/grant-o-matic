# META: Verify the prompt chain package

## Goal

Audit the **prompt chain itself** (completeness, contracts, sources, wiring). **Do not execute feature-building phases. Do not implement product features.**

## Scope

- In scope: `docs/agent-chain/**`, `AGENTS.md`, `.cursor/rules/grant-o-matic-agents.mdc`, root README pointer.
- Out of scope: changing scrapers, API, frontend product code (except README link to the chain).

## Preconditions

- Prompt chain files have been authored on the branch.

## Steps

1. **Completeness:** Every phase in `phases.json` has a file at `prompt_path`. Every implement phase 00–08 has a paired verify phase. Phase 99 and META exist.
2. **Roadmap map:** Root README roadmap items map to phases:
   - Live scraping → 01
   - Deadline alerts → 02
   - Multi-LLM → 04
   - User accounts → 03
   - Bilingual → 05
   - SR&ED checker → 06
   High-value extras: bootstrap 00, application assistant 07, ops 08, full audit 99.
3. **Contract lint:** Every `implement` prompt contains sections: Goal, Scope, Preconditions, Steps, Full test coverage bar, Documentation + citations, Decision rules, Done when, Verify commands.
4. **Verify lint:** Every verify/audit prompt forbids new features and writes an audit report path.
5. **Source lint:** Re-check all URLs in `SOURCES.md` (use `curl -4` / WebFetch for canada.ca as needed). Failures must be fixed or removed.
6. **Automation lint:** `WIRING.md` and `automation/` reference real prompt paths; `phases.json` `suggested_trigger` values consistent with WIRING.
7. Write results to `docs/agent-chain/CHAIN-VERIFICATION.md`.

## Decision rules

- Missing prompt file or missing mandatory section → FAIL.
- Dead source URL left as `ok` → FAIL.
- Do not launch Cloud Agents for phases 00–99 as part of this META run unless the operator explicitly asks later.

## Done when

- [ ] `CHAIN-VERIFICATION.md` complete with pass/fail
- [ ] `phases.json` ↔ files bijection confirmed
- [ ] Sources verified
- [ ] No feature code changes required (docs-only fixes OK)

## Verify commands

```bash
# File bijection
python - <<'PY'
import json, pathlib
root = pathlib.Path('docs/agent-chain')
phases = json.loads((root/'phases.json').read_text())['phases']
missing = [p['id'] for p in phases if not (pathlib.Path(p['prompt_path'])).exists()]
print('missing', missing or 'none')
files = {p.name for p in (root/'prompts').glob('*.prompt.md')}
listed = {pathlib.Path(p['prompt_path']).name for p in phases}
print('unlisted files', sorted(files-listed) or 'none')
print('listed missing files', sorted(listed-files) or 'none')
PY
```
