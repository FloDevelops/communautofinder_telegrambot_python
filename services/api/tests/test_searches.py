from fastapi.testclient import TestClient
import pytest

from back_reservauto.main import app


client = TestClient(app)

@pytest.fixture
def search():
    return dict(
        user_id='16EA6DC54CE2454AB399B9AEAFCADD1D',
        search_type='station',
        city_id='59',
        area_min_lat=11.11,
        area_max_lat=11.11,
        area_min_lon=11.11,
        area_max_lon=11.11,
        start_date='2023-12-03T05:26:34.932Z',
        end_date='2023-12-03T05:26:34.932Z',
    )

def test_create_search(search):
    response = client.post('/api/search', json=search)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json()['search_id'] is not None

def test_get_searches(search):
    response = client.get(f'/api/searches?telegram_user_id={search["user_id"]}')
    assert response.status_code == 200
    assert type(response.json()) == list

def test_get_search(search):
    search['search_id'] = client.get('/api/searches').json()[0]['search_id']
    response = client.get(f'/api/search/{search["search_id"]}')
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_update_search(search):
    search['search_id'] = client.get('/api/searches').json()[0]['search_id']
    response = client.put(f'/api/search/{search["search_id"]}', json=user)
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_delete_search(search):
    search['search_id'] = client.get('/api/searches').json()[0]['search_id']
    response = client.delete(f'/api/search/{search["search_id"]}')
    assert response.status_code == 200
    assert response.text == 'true'
