"""Public assessment API. No credentials or source code are accepted."""
from fastapi import FastAPI, HTTPException
from .models import AssessmentInput, AssessmentResult, ConsultationRequest, ConsultationReceipt
from .scoring import assess
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Castler SRP Exposure Check (Prototype)', version='0.1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://staging-my-site-15a2b62d.ploy.build",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

@app.get('/health')
def health():
    return {'status': 'ok', 'mode': 'demo'}

@app.get('/v1/assessment/questions')
def questions():
    return {'version': 'DEMO-ONLY-0.1', 'questions': [
        {'field': 'application_name', 'question': 'What is the application called?', 'type': 'text'},
        {'field': 'business_criticality', 'question': 'How critical is it to the business?', 'options': ['high','medium','low']},
        {'field': 'third_party_maintained', 'question': 'Is a third party responsible for maintaining it?', 'options': ['yes','no','unknown']},
        {'field': 'source_code_access', 'question': 'Could your organization access the source code if needed?', 'options': ['yes','no','unknown']},
        {'field': 'build_instructions_available', 'question': 'Are reproducible build instructions available?', 'options': ['yes','no','unknown']},
        {'field': 'dependencies_documented', 'question': 'Are required services and dependencies documented?', 'options': ['yes','no','unknown']},
        {'field': 'recovery_tested', 'question': 'Has application recovery been successfully tested?', 'options': ['yes','no','unknown']},
    ]}

@app.post('/v1/assessment', response_model=AssessmentResult)
def create_assessment(payload: AssessmentInput):
    return assess(payload)

@app.post('/v1/consultation', response_model=ConsultationReceipt)
def request_consultation(payload: ConsultationRequest):
    if not payload.consent_to_contact:
        raise HTTPException(status_code=400, detail='Explicit consent is required.')
    # Demo intentionally does not store or forward personal data.
    return ConsultationReceipt(status='demo_not_submitted', message='Consent validated; no lead was stored or sent. Connect an approved CRM before launch.')
