from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json() == {'ok': True}

def test_targets_mock_shape():
    params = {'lat': 47.6, 'lon': -122.3, 'date': '2025-08-21', 'min_alt': 30}
    resp = client.get('/api/targets', params=params)
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list) and len(data) >= 1
    
    resp_dict = data[0]
    for key in [
        'name', 'ra_deg', 'dec_deg', 'vmag', 
        'peak_altitude_deg', 'best_window', 'series']:
        assert key in resp_dict
    
    assert 'start' in resp_dict['best_window']
    assert 'end' in resp_dict['best_window']
    assert isinstance(resp_dict['series'], list) and len(resp_dict['series']) >= 3
