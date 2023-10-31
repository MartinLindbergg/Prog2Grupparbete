from flask import Flask, render_template, redirect, request
import requests
import random


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home-ex.html")
'''
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
'''

@app.route("/favorites")
def favourites():
    return "This is the favorites site."


@app.route('/random')
def random_book():
    total_books = 10000  # någon som vet hur många böcker det finns det i vårt api?
    random_book_id = random.randint(1, total_books)
    book_data = get_book_data(random_book_id)

    if book_data:
        return render_template('random.html', book_data=book_data)
    else:
        return "Book not found."


#----------Maltes kod nedan-----------

# kommentera bort koden under för att få random att funka

@app.route('/search')
def search():
    query = request.args.get('query', '')
    books_result = search_books(query)
    authors_result = search_authors(query)

    return render_template('search_results.html', books_result=books_result, authors_result=authors_result)

def get_all_books():
    response = requests.get('https://gutendex.com/books')
    if response.status_code == 200:
        books_info = response.json()
        return [book['id'] for book in books_info['results']]
    else:
        return []

def get_book_data(book_id):
    response = requests.get(f"https://gutendex.com/books/{book_id}")
    if response.status_code == 200:
        book_info = response.json()
        format = book_info.get("format", {})
        return {
            "book_id": book_id,
            "title": book_info.get("title", ""),
            "authors": [author["name"] for author in book_info.get("authors", [])],
            "subjects": book_info.get("subjects", []),
            "languages": book_info.get("languages", []),
            "download_links": format,
        }
    else:
        return None

def search_books(query):
    response = requests.get(f"https://gutendex.com/books/?search={query}")
    if response.status_code == 200:
        books_data = response.json()['results']
        return books_data or []  # Returnera en tom lista om inga böcker hittades
    else:
        return []

def search_authors(query):
    response = requests.get(f"https://gutendex.com/books/?search={query}&type=author")
    if response.status_code == 200:
        authors_data = response.json()['results']
        return authors_data or []  # Returnera en tom lista om inga författare hittades
    else:
        return []

