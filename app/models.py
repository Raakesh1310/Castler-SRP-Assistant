from typing import Literal
from pydantic import BaseModel, Field, EmailStr

Answer = Literal['yes', 'no', 'unknown']

class AssessmentInput(BaseModel):
    application_name: str = Field(min_length=1, max_length=120)
    business_criticality: Literal['high', 'medium', 'low']
    third_party_maintained: Answer
    source_code_access: Answer
    build_instructions_available: Answer
    dependencies_documented: Answer
    recovery_tested: Answer

class Finding(BaseModel):
    code: str
    title: str
    explanation: str
    recommendation: str
    points: int

class AssessmentResult(BaseModel):
    assessment_id: str
    application_name: str
    exposure: Literal['low', 'moderate', 'high', 'undetermined']
    illustrative_score: int | None
    maximum_score: int = 10
    findings: list[Finding]
    unknown_fields: list[str]
    limitations: list[str]
    next_step: str
    scoring_version: str = 'DEMO-ONLY-0.1'

class ConsultationRequest(BaseModel):
    assessment_id: str = Field(min_length=1, max_length=100)
    contact_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    consent_to_contact: bool

class ConsultationReceipt(BaseModel):
    status: str
    message: str
