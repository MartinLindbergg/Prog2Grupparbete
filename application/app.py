from flask import Flask, render_template, redirect, request
import requests as req
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/books')
def index():
    all_books = get_all_books()
    books_data = [get_book_data(book_id) for book_id in all_books]
    return render_template('books.html', data=books_data)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book_data = get_book_data(book_id)

    if book_data:
        return render_template('books.html', book_data=book_data)
    else:
        return "Book not found."

@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route('/search')
def search():
    query = request.args.get('query', '')
    books_result = search_books(query)
    authors_result = search_authors(query)

    return render_template('search_results.html', books_result=books_result, authors_result=authors_result)

def get_all_books():
    response = req.get('https://gutendex.com/books')
    if response.status_code == 200:
        books_info = response.json()
        return [book['id'] for book in books_info['results']]
    else:
        return []

def get_book_data(book_id):
    response = req.get(f"https://gutendex.com/books/{book_id}")
    if response.status_code == 200:
        book_info = response.json()
        formats = book_info.get("formats", {})
        return {
            "book_id": book_id,
            "title": book_info.get("title", ""),
            "authors": [author["name"] for author in book_info.get("authors", [])],
            "subjects": book_info.get("subjects", []),
            "languages": book_info.get("languages", []),
            "download_links": formats,
        }
    else:
        return None

def search_books(query):
    response = req.get(f"https://gutendex.com/books/?search={query}")
    if response.status_code == 200:
        books_data = response.json()['results']
        return books_data or []  # Returnera en tom lista om inga böcker hittades
    else:
        return []

def search_authors(query):
    response = req.get(f"https://gutendex.com/books/?search={query}&type=author")
    if response.status_code == 200:
        authors_data = response.json()['results']
        return authors_data or []  # Returnera en tom lista om inga författare hittades
    else:
        return []

































'''
from flask import Flask, render_template, redirect
import requests
import random


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home-ex.html")

@app.route('/books')
def index():
    return render_template('home-ex.html')
def get_book_data(book_id):

    response = requests.get(f"https://gutendex.com/books/{book_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book_data = get_book_data(book_id)

    if book_data:
        return render_template('books-ex.html', book_data=book_data)
    else:
        return "Book not found."


@app.route('/random')
def random_book():
    total_books = 50000  # någon som vet hur många böcker det finns det i vårt api?
    random_book_id = random.randint(1, total_books)
    book_data = get_book_data(random_book_id)

    if book_data:
        return render_template('books-ex.html', book_data=book_data)
    else:
        return "Book not found."
'''