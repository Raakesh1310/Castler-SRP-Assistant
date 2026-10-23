from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)
BASE = dict(application_name='Payment Service', business_criticality='high',
            third_party_maintained='yes', source_code_access='yes',
            build_instructions_available='yes', dependencies_documented='yes',
            recovery_tested='yes')

def test_health():
    assert client.get('/health').json()['status'] == 'ok'

def test_questions():
    assert len(client.get('/v1/assessment/questions').json()['questions']) == 7

def test_low_exposure():
    data = client.post('/v1/assessment', json=BASE).json()
    assert data['exposure'] == 'low' and data['illustrative_score'] == 0

def test_high_exposure():
    data = client.post('/v1/assessment', json={**BASE, 'source_code_access': 'no', 'recovery_tested': 'no'}).json()
    assert data['exposure'] == 'high' and data['illustrative_score'] == 6
    assert len(data['findings']) == 2

def test_unknown_not_false_certainty():
    data = client.post('/v1/assessment', json={**BASE, 'source_code_access': 'unknown', 'recovery_tested': 'unknown'}).json()
    assert data['exposure'] == 'undetermined' and data['illustrative_score'] is None

def test_invalid_answer_rejected():
    assert client.post('/v1/assessment', json={**BASE, 'source_code_access': 'maybe'}).status_code == 422

def test_consent_required():
    req = {'assessment_id': 'a', 'contact_name': 'Example', 'email': 'test@example.org', 'consent_to_contact': False}
    assert client.post('/v1/consultation', json=req).status_code == 400
    req['consent_to_contact'] = True
    assert client.post('/v1/consultation', json=req).json()['status'] == 'demo_not_submitted'
