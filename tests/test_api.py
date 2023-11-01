from application import app, get_book_data, search_books, search_authors
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_book_data():
    assert get_book_data(42) is not None

def test_search_books():
    assert search_books('A Matter of Ethics') is not None

def test_search_authors():
    assert search_authors('William') is not None
