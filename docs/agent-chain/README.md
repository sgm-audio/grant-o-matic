# Grant-O-Matic Cloud Agent Prompt Chain

Automation-ready prompt files for building every high-value addition through the full product roadmap. **This package is for launching Cursor Cloud Agents / Automations later.** Authoring the chain does not execute feature phases.

## How chaining works

Cursor Automations have no native DAG. This repo packages:

1. Per-phase `.prompt.md` files (paste into an Automation or send via Cloud Agents API)
2. [`phases.json`](phases.json) — machine-readable dependency graph
3. [`WIRING.md`](WIRING.md) — how to create each Automation and gate the next phase
4. Human-gated labels: implement → review → `phase-N-approved` → verify → `phase-N-verified` → next implement

Docs: [Cursor Automations](https://cursor.com/docs/cloud-agent/automations.md) · [Cloud Agents API](https://cursor.com/docs/cloud-agent/api/endpoints.md) · [Best practices](https://cursor.com/docs/cloud-agent/best-practices.md)

## Phase map

```text
00 bootstrap → 00a verify
01 grant data/scrapers → 01a audit
02 deadline alerts → 02a verify
03 accounts + saved matches → 03a verify
04 LLM matching → 04a verify
05 bilingual UI → 05a verify
06 tax credits / SR&ED → 06a verify
07 application assistant → 07a verify
08 ops / compose / CI → 08a verify
99 full system audit
META verify prompt chain (run after authoring the chain itself)
```

| Phase | Type | Prompt |
|-------|------|--------|
| 00 | implement | [`prompts/00-bootstrap.prompt.md`](prompts/00-bootstrap.prompt.md) |
| 00a | verify | [`prompts/00a-verify-bootstrap.prompt.md`](prompts/00a-verify-bootstrap.prompt.md) |
| 01 | implement | [`prompts/01-grant-data-scrapers.prompt.md`](prompts/01-grant-data-scrapers.prompt.md) |
| 01a | verify | [`prompts/01a-audit-grant-data.prompt.md`](prompts/01a-audit-grant-data.prompt.md) |
| 02 | implement | [`prompts/02-deadline-alerts.prompt.md`](prompts/02-deadline-alerts.prompt.md) |
| 02a | verify | [`prompts/02a-verify-deadlines.prompt.md`](prompts/02a-verify-deadlines.prompt.md) |
| 03 | implement | [`prompts/03-accounts-saved-matches.prompt.md`](prompts/03-accounts-saved-matches.prompt.md) |
| 03a | verify | [`prompts/03a-verify-accounts.prompt.md`](prompts/03a-verify-accounts.prompt.md) |
| 04 | implement | [`prompts/04-llm-matching.prompt.md`](prompts/04-llm-matching.prompt.md) |
| 04a | verify | [`prompts/04a-verify-llm-matching.prompt.md`](prompts/04a-verify-llm-matching.prompt.md) |
| 05 | implement | [`prompts/05-bilingual-ui.prompt.md`](prompts/05-bilingual-ui.prompt.md) |
| 05a | verify | [`prompts/05a-verify-i18n.prompt.md`](prompts/05a-verify-i18n.prompt.md) |
| 06 | implement | [`prompts/06-tax-credits-sred.prompt.md`](prompts/06-tax-credits-sred.prompt.md) |
| 06a | verify | [`prompts/06a-verify-tax-credits.prompt.md`](prompts/06a-verify-tax-credits.prompt.md) |
| 07 | implement | [`prompts/07-application-assistant.prompt.md`](prompts/07-application-assistant.prompt.md) |
| 07a | verify | [`prompts/07a-verify-application-assistant.prompt.md`](prompts/07a-verify-application-assistant.prompt.md) |
| 08 | implement | [`prompts/08-ops-compose-ci.prompt.md`](prompts/08-ops-compose-ci.prompt.md) |
| 08a | verify | [`prompts/08a-verify-ops.prompt.md`](prompts/08a-verify-ops.prompt.md) |
| 99 | audit | [`prompts/99-full-system-audit.prompt.md`](prompts/99-full-system-audit.prompt.md) |
| META | audit | [`prompts/META-verify-prompt-chain.prompt.md`](prompts/META-verify-prompt-chain.prompt.md) |

## Operator quick start

1. Read [`AGENTS.md`](../../AGENTS.md) and [`SOURCES.md`](SOURCES.md).
2. Wire Automations using [`WIRING.md`](WIRING.md) (or API launcher under [`automation/`](automation/)).
3. Start with **00-bootstrap** (manual/webhook).
4. After each implement PR: human review → add `phase-N-approved` → verify Automation runs → on pass add `phase-N-verified`.
5. Never skip verify phases.

## Mandatory quality bar (all implement phases)

- Full tests for new modules and routes
- Citations from [`SOURCES.md`](SOURCES.md) for every funding-body claim
- PR only if verify commands pass
- Update [`HANDOFF.template.md`](HANDOFF.template.md) → `HANDOFF.md`

## Related

- Audit criteria: [`CHECKLIST.md`](CHECKLIST.md)
- Chain self-verification results: [`CHAIN-VERIFICATION.md`](CHAIN-VERIFICATION.md) (written when the chain is authored)
- Research notes: [`../grant-databases-research.md`](../grant-databases-research.md)
