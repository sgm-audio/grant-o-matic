# Wiring Cursor Automations for the Grant-O-Matic chain

Cursor Automations are configured in the dashboard ([cursor.com/automations](https://cursor.com/automations)), not as committed YAML. This file tells you exactly how to create each Automation from the repo prompts.

References:

- [Automations](https://cursor.com/docs/cloud-agent/automations.md)
- [Cloud Agents API](https://cursor.com/docs/cloud-agent/api/endpoints.md)
- [Best practices](https://cursor.com/docs/cloud-agent/best-practices.md)

## Recommended orchestration (human-gated labels)

```text
Implement Automation (manual/webhook)
  → opens PR with label phase-N
Human reviews
  → adds label phase-N-approved
Verify Automation (trigger: PR label changed)
  → writes audits/NNa-audit.md; recommends phase-N-verified
Human adds phase-N-verified
  → next Implement Automation (trigger: label phase-N-verified) OR manual start
```

Create GitHub labels before wiring: `phase-00` … `phase-08`, `phase-00-approved` … `phase-08-approved`, `phase-00-verified` … `phase-08-verified`, `chain-complete`.

## Shared Automation settings

| Setting | Recommendation |
|---------|----------------|
| Repo | This Grant-O-Matic repository |
| Environment | Same Cloud environment with Python 3.12 + Node 20 |
| Model | Team default / high-reasoning for implement; faster OK for verify |
| Tools | Pull requests **on**; Memories **off** for untrusted triggers |
| Scope | Private (or Team Visible); avoid Team Owned unless intended |
| Instructions | Paste **entire** corresponding `.prompt.md` body |

Also ensure the environment / agent can read `AGENTS.md` and `.cursor/rules/grant-o-matic-agents.mdc`.

## Per-phase wiring table

| Automation name | Prompt file | Trigger | On success |
|-----------------|-------------|---------|------------|
| GOM 00 Bootstrap | `docs/agent-chain/prompts/00-bootstrap.prompt.md` | Manual or webhook | PR + label `phase-00` |
| GOM 00a Verify Bootstrap | `.../00a-verify-bootstrap.prompt.md` | PR label `phase-00-approved` | Recommend `phase-00-verified` |
| GOM 01 Grant Data | `.../01-grant-data-scrapers.prompt.md` | Label `phase-00-verified` or manual | PR + `phase-01` |
| GOM 01a Audit Data | `.../01a-audit-grant-data.prompt.md` | Label `phase-01-approved` | Recommend `phase-01-verified` |
| GOM 02 Deadlines | `.../02-deadline-alerts.prompt.md` | Label `phase-01-verified` or manual | PR + `phase-02` |
| GOM 02a Verify Deadlines | `.../02a-verify-deadlines.prompt.md` | Label `phase-02-approved` | Recommend `phase-02-verified` |
| GOM 03 Accounts | `.../03-accounts-saved-matches.prompt.md` | Label `phase-02-verified` or manual | PR + `phase-03` |
| GOM 03a Verify Accounts | `.../03a-verify-accounts.prompt.md` | Label `phase-03-approved` | Recommend `phase-03-verified` |
| GOM 04 LLM Matching | `.../04-llm-matching.prompt.md` | Label `phase-03-verified` or manual | PR + `phase-04` |
| GOM 04a Verify LLM | `.../04a-verify-llm-matching.prompt.md` | Label `phase-04-approved` | Recommend `phase-04-verified` |
| GOM 05 Bilingual | `.../05-bilingual-ui.prompt.md` | Label `phase-04-verified` or manual | PR + `phase-05` |
| GOM 05a Verify i18n | `.../05a-verify-i18n.prompt.md` | Label `phase-05-approved` | Recommend `phase-05-verified` |
| GOM 06 Tax/SR&ED | `.../06-tax-credits-sred.prompt.md` | Label `phase-05-verified` or manual | PR + `phase-06` |
| GOM 06a Verify Tax | `.../06a-verify-tax-credits.prompt.md` | Label `phase-06-approved` | Recommend `phase-06-verified` |
| GOM 07 App Assistant | `.../07-application-assistant.prompt.md` | Label `phase-06-verified` or manual | PR + `phase-07` |
| GOM 07a Verify Assistant | `.../07a-verify-application-assistant.prompt.md` | Label `phase-07-approved` | Recommend `phase-07-verified` |
| GOM 08 Ops CI | `.../08-ops-compose-ci.prompt.md` | Label `phase-07-verified` or manual | PR + `phase-08` |
| GOM 08a Verify Ops | `.../08a-verify-ops.prompt.md` | Label `phase-08-approved` | Recommend `phase-08-verified` |
| GOM 99 Full Audit | `.../99-full-system-audit.prompt.md` | Label `phase-08-verified` or manual | Recommend `chain-complete` |
| GOM META Chain Audit | `.../META-verify-prompt-chain.prompt.md` | Manual (after authoring chain) | Updates `CHAIN-VERIFICATION.md` |

If GitHub label triggers are unavailable on your plan, use **webhook** triggers and the script in [`automation/launch-phase.example.sh`](automation/launch-phase.example.sh), or start each phase manually from the Agents UI by pasting the prompt.

## CI-gated alternative

After an implement PR merges, trigger the verify Automation on **CI completed** / **workflow run completed** (GitHub). Put in the verify prompt: “If CI is red, do nothing except report.”

## Secrets to configure in the Cloud environment (later phases)

| Secret | Phases |
|--------|--------|
| `GROQ_API_KEY` / `ANTHROPIC_API_KEY` | 04 |
| `DATABASE_URL` | 03 |
| Email provider keys | 02 |

Never commit these values.

## API orchestration alternative

See [`automation/README.md`](automation/README.md) for `POST /v1/agents` sequencing using `phases.json`.
