# Castler SRP Recoverability Exposure Check — runnable prototype

**Status: DEMO. Not an official Castler scoring system or production-ready integration.**

This repository implements a public self-report assessment API and an MCP interface for ChatGPT. It deliberately uses a local demo scoring adapter because Castler's actual scoring rules, SRP API contracts, and credentials have not been supplied. It does **not** request source code, passwords, secrets, contracts, or access to infrastructure.

## Architecture

ChatGPT (MCP client) → MCP server (`app/mcp_server.py`) → assessment API (`app/api.py`) → scoring adapter (`app/scoring.py`).

The website can also call the assessment API directly. Replace the scoring adapter with the actual Castler API when approved contracts are available.

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for the interactive API explorer. In a **second** terminal (with the virtual environment active):

```bash
export CASTLER_API_URL=http://127.0.0.1:8000  # PowerShell: $env:CASTLER_API_URL='http://127.0.0.1:8000'
python -m app.mcp_server
```

The MCP server uses Streamable HTTP at `http://127.0.0.1:8001/mcp`, separate from the API on port 8000.

ChatGPT requires a reachable HTTPS MCP endpoint; localhost alone is not accessible from ChatGPT. Deploy behind TLS and appropriate access controls, then configure the ChatGPT app/developer connection to the public `/mcp` URL. Publication and review are separate steps.

## Example assessment

```bash
curl -X POST http://127.0.0.1:8000/v1/assessment \
  -H 'Content-Type: application/json' \
  -d '{"application_name":"Payment Service","business_criticality":"high","third_party_maintained":"yes","source_code_access":"no","build_instructions_available":"no","dependencies_documented":"unknown","recovery_tested":"no"}'
```

## Test

```bash
pytest -q
```

## Before production

1. Replace `DEMO-ONLY-0.1` and all illustrative weights/thresholds with the approved Castler rules or scoring API.
2. Confirm questionnaire, SRP coverage mapping, API auth, and response schemas with Castler.
3. Implement production authentication/authorization, request limits, abuse protection, privacy notices, audit logs with redaction, retention/deletion controls, and monitoring.
4. Connect consultation requests to an approved CRM only with explicit consent; the demo **does not store or send** leads.
5. Secure the MCP endpoint with HTTPS and an appropriate authorization model; validate tool metadata and app UX in ChatGPT developer mode.
6. Conduct end-to-end tests and security review before any public listing.

## ChatGPT tool behavior

- `get_assessment_questions`: retrieve the public questionnaire.
- `assess_recoverability_exposure`: send answers, return structured findings.
- `request_srp_consultation`: validate consent and return a demo-only receipt.

The assistant must not invent missing scores, claim verified recoverability, or say a consultation was submitted when the demo response says otherwise.
