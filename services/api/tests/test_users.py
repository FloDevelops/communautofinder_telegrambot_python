from fastapi.testclient import TestClient
import pytest

from back_reservauto.main import app


client = TestClient(app)

@pytest.fixture
def user():
    return dict(
        telegram_user_id='123456789',
        telegram_username='BarackObama',
        telegram_first_name='Barack',
        telegram_last_name='Obama',
        telegram_language_code='fr',
        telegram_chat_id='123456789',
        has_accepted_communications=False,
        preferred_city_id='59',
    )

def test_create_user(user):
    response = client.post('/api/users', json=user)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json()['telegram_user_id'] == user['telegram_user_id']

def test_get_user(user):
    response = client.get(f'/api/users/{user["telegram_user_id"]}')
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json()['telegram_user_id'] == user['telegram_user_id']

def test_get_users():
    response = client.get('/api/users')
    assert response.status_code == 200
    assert type(response.json()) == list

def test_update_user(user):
    user['user_id'] = client.get(f'/api/users/{user["telegram_user_id"]}').json()['user_id']
    user['telegram_user_id'] = '123456789'
    user['telegram_username'] = 'MichelleObama'
    user['telegram_first_name'] = 'Michelle'
    user['telegram_last_name'] = 'Obama'
    user['telegram_language_code'] = 'en'
    user['telegram_chat_id'] = '987654321'
    user['has_accepted_communications'] = True
    user['is_enabled'] = True
    user['preferred_city_id'] = '60'

    response = client.put(f'/api/users/{user["telegram_user_id"]}', json=user)
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json()['has_accepted_communications'] == user['has_accepted_communications']
    assert response.json()['is_enabled'] == user['is_enabled']
    assert response.json()['preferred_city_id'] == user['preferred_city_id']
    assert response.json()['telegram_username'] == user['telegram_username']
    assert response.json()['telegram_first_name'] == user['telegram_first_name']
    assert response.json()['telegram_last_name'] == user['telegram_last_name']

def test_delete_user(user):
    response = client.delete(f'/api/users/{user["telegram_user_id"]}')
    assert response.status_code == 200
    assert response.text == 'true'
