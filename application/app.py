from flask import Flask, render_template, redirect, request, make_response
import requests
import random
import pandas as pd


app = Flask(__name__)

@app.route("/")
def first_page():
    saved_name = request.cookies.get("saved_name")
    return render_template("first_page.html", saved_name=saved_name)

@app.route("/save_name", methods=["POST"])
def save_name():
    name = request.form['name']

    response = make_response(f"We will now remember your name, {name}!")
    response.set_cookie("saved_name", name)
    return response

@app.route("/delete_cookie")
def delete_cookie():
    response = make_response("We will no longer remember your name!")
    response.set_cookie("saved_name", "", expires=0)
    return response



@app.route("/home")
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

    books_df = pd.DataFrame(books_result)
    authors_df = pd.DataFrame(authors_result)

    books_df = books_df.drop (['id', 'translators', 'bookshelves', 'copyright', 'media_type', 'formats', 'download_count'], axis=1)
    authors_df = authors_df.drop (['id', 'translators', 'bookshelves', 'copyright', 'media_type', 'formats', 'download_count'], axis=1)

    books_table = books_df.to_html(classes="table table-bordered table-hover", index=False, justify="left")
    authors_table = authors_df.to_html(classes="table table-bordered table-hover", index=False, justify="left")

    return render_template('search_results.html', books_table=books_table, authors_table=authors_table)


def get_all_books():
    response = requests.get('https://gutendex.com/books')
    if response.status_code == 200:
        books_info = response.json()
        return [book['id'] for book in books_info['results']]
    else:
        return []

def get_book_datas(book_id):
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

