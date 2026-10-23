"""ChatGPT MCP interface. Start with: python -m app.mcp_server

The FastMCP dependency is declared in requirements.txt.
Set CASTLER_API_URL to your reachable assessment API base URL.
"""
import os
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

#mcp = FastMCP('Castler SRP Exposure Check', stateless_http=True, json_response=True, host='127.0.0.1', port=8001)

mcp = FastMCP(
    'Castler SRP Exposure Check',
    stateless_http=True,
    json_response=True,
    host='127.0.0.1',
    port=8002,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            '127.0.0.1:*',
            'localhost:*',
            'oppose-siren-divinely.ngrok-free.dev',
        ],
        allowed_origins=[
            'http://127.0.0.1:*',
            'http://localhost:*',
            'https://oppose-siren-divinely.ngrok-free.dev',
        ],
    ),
)

API_URL = os.getenv('CASTLER_API_URL', 'http://127.0.0.1:8000').rstrip('/')

async def call_api(method: str, path: str, payload: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.request(method, f'{API_URL}{path}', json=payload)
        response.raise_for_status()
        return response.json()

@mcp.tool()
async def get_assessment_questions() -> dict:
    """Get the approved question list for a preliminary application recoverability exposure check. Never ask for secrets, source code, or account access."""
    return await call_api('GET', '/v1/assessment/questions')

@mcp.tool()
async def assess_recoverability_exposure(
    application_name: str,
    business_criticality: str,
    third_party_maintained: str,
    source_code_access: str,
    build_instructions_available: str,
    dependencies_documented: str,
    recovery_tested: str,
) -> dict:
    
    """Assess an application's recoverability exposure.

    Allowed business criticality: high/medium/low.
    Allowed other answers: yes/no/unknown.

    Return the actual assessment findings without inventing scores.

    IMPORTANT DEMO WORKFLOW:
    After presenting the complete assessment findings and
    recommendations, always offer an optional consultation:

    "Would you like to connect with the Castler SRP team
    to discuss your application's recoverability exposure?"

    Do not ask for contact details until the user agrees.

    If the user agrees, ask for:
    1. Full name
    2. Work email
    3. Company name (optional)
    4. Job title (optional)
    5. Explicit consent to be contacted

    Once the user provides the required information and
    consent, call request_srp_consultation.

    This is a demonstration only. No lead is submitted,
    emailed, stored, or forwarded, and no call is booked.

    The assessment must remain fully available even if
    the user declines the consultation.
    """

    return await call_api('POST', '/v1/assessment', {
        'application_name': application_name,
        'business_criticality': business_criticality,
        'third_party_maintained': third_party_maintained,
        'source_code_access': source_code_access,
        'build_instructions_available': build_instructions_available,
        'dependencies_documented': dependencies_documented,
        'recovery_tested': recovery_tested,
    })


@mcp.tool()
async def request_srp_consultation(
    assessment_id: str,
    contact_name: str,
    email: str,
    consent_to_contact: bool,
    company_name: str = "",
    job_title: str = "",
) -> dict:
    """Demonstrate an optional Castler SRP consultation request.

    Only call after showing the recoverability assessment and
    the user explicitly agrees to request a consultation.

    Collect:
    - Full name
    - Work email
    - Company name (optional)
    - Job title (optional)
    - Explicit consent to be contacted

    Never call if consent is false. Do not submit, store, email,
    or forward any contact details. This is a demo only.
    """
    if not consent_to_contact:
        return {
            "status": "consent_required",
            "message": "No consultation requested.",
            "demo_only": True,
        }

    if not contact_name.strip() or not email.strip():
        return {
            "status": "missing_details",
            "message": "Full name and email are required.",
            "demo_only": True,
        }

    
    return {
        "status": "demo_preview_ready",
        "demo_only": True,
        "title": "Consultation Request Ready",
        "message": (
            "Thank you for your interest in Castler SRP! "
            "Your consultation request has been prepared successfully."
        ),
        "assessment_id": assessment_id,
        "request_type": "SRP Consultation",
        "next_step": (
            "In the live service, the Castler SRP team "
            "would review the request and contact the user "
            "using their provided details."
        ),
        "display_instructions": (
            "Present a professional consultation confirmation "
            "with the heading 'Consultation Request Ready'. "
            "Show the assessment reference and next steps. "
            "Display a small 'Demo Preview' indicator. "
            "Do not claim that a request was actually submitted, "
            "received, stored, or that a meeting was booked."
        ),
        "submission_performed": False,
        "data_stored": False,
        "meeting_booked": False,
    }



if __name__ == '__main__':
    mcp.run(transport='streamable-http')
