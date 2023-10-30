from flask import Flask, render_template, redirect
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/books')
def index():
    return render_template('home.html')
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
        return render_template('books.html', book_data=book_data)
    else:
        return "Book not found."






















'''

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")






@app.route('/books')
def index():
    return render_template('books.html')
def get_book_data(book_id):

    response = requests.get(f"https://gutendex.com/books/%7Bbook_id%7D")
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/books/<int:book_id>')
def book_details(book_id):
    book_data = get_book_data(book_id)

    if book_data:
        return render_template('bokdetaljer.html', book_data=book_data)
    else:
        return "Book not found."




@app.route("/books")
def books():
    # Exempel på att hämta data från Gutendex API
    response = requests.get('https://gutendex.com/books')
    data = response.json() 
    # Hantera och behandla svaret enligt behov

    return render_template("books.html", data=data)  # Skicka data till HTML-filen


@app.route("/redirect/<category>")
def redirect_to_category(category):
    if category == "children":
        return redirect("https://gutendex.com/books?topic=children")
    elif category == "adventure":
        return redirect("https://gutendex.com/books?topic=adventure")

    else:
        # Om kategorin inte matchar någon av de fördefinierade kategorierna, omdirigera till startsidan
        return redirect("/")
    
    
'''

