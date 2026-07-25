# Cloud Agents API orchestration

Use this when you want a scripted sequence instead of (or in addition to) dashboard Automations.

Docs: [Cloud Agents API endpoints](https://cursor.com/docs/cloud-agent/api/endpoints.md)

## Flow

```text
for phase in phases.json (respecting depends_on):
  read prompt_path text
  POST /v1/agents  (prompt, repository, autoCreatePR, startingRef)
  poll GET .../runs/{runId} until FINISHED or ERROR
  if implement: wait for human label / merge
  if verify failed: stop
```

Constraints from docs:

- Only **one active run** per agent (`409 agent_busy` if overlapping)
- Prefer a **new agent** (or follow-up run after finish) per phase
- Do not store API keys in the repo; export `CURSOR_API_KEY` in your shell

## Machine-readable graph

[`../phases.json`](../phases.json) fields used by launchers:

| Field | Meaning |
|-------|---------|
| `id` | Phase id |
| `type` | `implement` \| `verify` \| `audit` |
| `prompt_path` | Repo-relative prompt to send |
| `depends_on` | Prior phase ids that must be verified/complete |
| `suggested_trigger` | Dashboard wiring hint |

## Example launcher

See [`launch-phase.example.sh`](launch-phase.example.sh). It launches **one** phase by id. It does not auto-run the full chain (human gates remain).

## Webhook Automations

1. Create an Automation with webhook trigger; copy URL + API key from the Automation after save.
2. From CI or your orchestrator, POST to start the next phase when labels/CI allow.
3. Keep the Automation prompt identical to the `.prompt.md` file (or instruct the agent to read that path from the repo—prefer pasting so the Automation is self-contained).

## Safety

- Do not point an unattended loop at implement phases without human review between merges.
- Verify/audit phases should not enable Memories on public PR triggers.
