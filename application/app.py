
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
    