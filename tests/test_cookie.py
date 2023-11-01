from application import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_save_name(client):
    response = client.post('/save_name', data=dict(name='TestName'))
    assert b"We will now remember your name" in response.data

def test_delete_cookie(client):
    response = client.get('/delete_cookie')
    assert b"We will no longer remember your name" in response.data
