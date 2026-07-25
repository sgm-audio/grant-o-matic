#!/usr/bin/env bash
# Example: launch a single Grant-O-Matic chain phase via Cursor Cloud Agents API.
# Docs: https://cursor.com/docs/cloud-agent/api/endpoints.md
#
# Usage:
#   export CURSOR_API_KEY=...          # do not commit
#   export CURSOR_API_BASE=https://api.cursor.com   # adjust if your docs specify otherwise
#   export REPO_URL=https://github.com/YOUR_ORG/grant-o-matic
#   export REF=main
#   ./docs/agent-chain/automation/launch-phase.example.sh 00-bootstrap
#
# This script does NOT run the full chain and does NOT bypass human gates.

set -euo pipefail

PHASE_ID="${1:-}"
if [[ -z "$PHASE_ID" ]]; then
  echo "Usage: $0 <phase-id>" >&2
  echo "Phase ids are listed in docs/agent-chain/phases.json" >&2
  exit 1
fi

: "${CURSOR_API_KEY:?Set CURSOR_API_KEY}"
: "${REPO_URL:?Set REPO_URL to the GitHub repo HTTPS URL}"
API_BASE="${CURSOR_API_BASE:-https://api.cursor.com}"
REF="${REF:-main}"

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
PHASES_JSON="$ROOT/docs/agent-chain/phases.json"

PROMPT_PATH=$(python3 - <<PY
import json, sys
phases = json.load(open("$PHASES_JSON"))["phases"]
pid = "$PHASE_ID"
for p in phases:
    if p["id"] == pid:
        print(p["prompt_path"])
        sys.exit(0)
sys.exit("Unknown phase id: " + pid)
PY
)

PROMPT_FILE="$ROOT/$PROMPT_PATH"
if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Missing prompt file: $PROMPT_FILE" >&2
  exit 1
fi

# JSON-escape prompt body
PROMPT_JSON=$(python3 - <<PY
import json
print(json.dumps(open("$PROMPT_FILE").read()))
PY
)

NAME="gom-${PHASE_ID}"
NAME="${NAME:0:100}"

echo "Launching phase $PHASE_ID from $PROMPT_PATH on $REPO_URL@$REF"

# NOTE: Request shape may evolve; align fields with current Cloud Agents API docs
# before production use: https://cursor.com/docs/cloud-agent/api/endpoints.md
curl -sS -X POST "${API_BASE}/v1/agents" \
  -H "Authorization: Bearer ${CURSOR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "name": "${NAME}",
  "prompt": ${PROMPT_JSON},
  "source": {
    "repository": "${REPO_URL}",
    "ref": "${REF}"
  },
  "target": {
    "autoCreatePr": true
  }
}
EOF

echo
echo "Poll the returned agent/run ids until FINISHED before starting the next phase."
echo "For implement phases, wait for human review + labels before verify phases."
