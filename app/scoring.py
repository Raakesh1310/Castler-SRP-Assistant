"""Demo scoring adapter. REPLACE with Castler's approved scoring API.

No scores in this module are presented as actual Castler policy.
"""
from uuid import uuid4
from .models import AssessmentInput, AssessmentResult, Finding

RULES = [
    ('source_code_access', 'CODE_ACCESS', 'Source code access not confirmed',
     'Without accessible source code, rebuilding the application may be difficult.',
     'Review source-code escrow and recovery access arrangements.', 3),
    ('build_instructions_available', 'BUILD_GUIDE', 'Build instructions unavailable',
     'A recovery team may not know how to reproduce the application.',
     'Document and validate reproducible build instructions.', 2),
    ('dependencies_documented', 'DEPENDENCIES', 'Dependencies not documented',
     'Undocumented infrastructure and service dependencies can slow recovery.',
     'Inventory and validate service and infrastructure dependencies.', 2),
    ('recovery_tested', 'RECOVERY_TEST', 'Recovery not tested',
     'A plan without a recovery test may not work when needed.',
     'Conduct an authorized recovery rehearsal and capture results.', 3),
]

def assess(payload: AssessmentInput) -> AssessmentResult:
    findings: list[Finding] = []
    unknown: list[str] = []
    score = 0
    for field, code, title, explanation, recommendation, points in RULES:
        answer = getattr(payload, field)
        if answer == 'unknown':
            unknown.append(field)
        elif answer == 'no':
            score += points
            findings.append(Finding(code=code, title=title, explanation=explanation,
                                    recommendation=recommendation, points=points))
    if payload.third_party_maintained == 'unknown':
        unknown.append('third_party_maintained')
    # Criticality informs narrative; no invented weight for criticality.
    if len(unknown) >= 2:
        exposure = 'undetermined'
        display_score = None
    else:
        exposure = 'high' if score >= 6 else 'moderate' if score >= 3 else 'low'
        display_score = score
    next_step = ('Confirm missing information before making a coverage recommendation.'
                 if exposure == 'undetermined' else
                 'Discuss an appropriate SRP review with Castler.' if exposure == 'high' else
                 'Review the identified gaps and confirm suitable recovery coverage.')
    return AssessmentResult(
        assessment_id=str(uuid4()), application_name=payload.application_name,
        exposure=exposure, illustrative_score=display_score, findings=findings,
        unknown_fields=unknown,
        limitations=[
            'Illustrative demo rules only; not approved Castler scoring.',
            'Based solely on self-reported answers; no technical recovery was verified.',
            'No guarantees of recoverability, RTO, or SRP eligibility.',
        ], next_step=next_step)
