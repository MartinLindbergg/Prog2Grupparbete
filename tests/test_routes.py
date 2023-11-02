import pytest
from application.app import app


@pytest.fixture
def client():
    app.app_context().push()  # Skapa applikationskontext
    app.config['TESTING'] = True  # Sätt app.config['TESTING'] till True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200


def test_books_route(client):
    response = client.get('/books')
    assert response.status_code == 200


def test_favorites_route(client):
    response = client.get('/favorites')
    assert response.status_code == 200


def test_random_route(client):
    response = client.get('/random')
    assert response.status_code == 200


def test_search_route(client):
    response = client.get('/search')
    assert response.status_code == 200


def test_book_details_route(client):
    response = client.get('/book/1')  # Anpassa ID här enligt dina behov
    assert response.status_code == 200
