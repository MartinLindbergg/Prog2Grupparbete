from flask import Flask, jsonify, render_template, request, make_response, url_for, redirect
import requests
import random
import pandas as pd
import re


app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.errorhandler(AttributeError)
def handle_attribute_error(e):
    error_message = "AttributeError: Ett attribut eller en metod finns inte eller kan inte nås."
    return jsonify({"error": error_message}), 500  # 500 är HTTP-statusen för interna fel


def get_book_data(book_id):
    response = requests.get(f"https://gutendex.com/books/{book_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/")
def home():
    return render_template("home-ex.html")

@app.route('/books')
def index():
    total_books = 71993  # Totalt antal tillgängliga böcker, anpassa efter ditt API
    random_book_id = random.randint(1, total_books)
    book_data = get_book_data(random_book_id)

    if book_data:
        return render_template('books-ex.html', book_data=book_data)  # Skicka book_data till mallen
    else:
        return "Book data not found."

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book_data = get_book_data(book_id)

    if book_data:
        return render_template('books-ex.html', book_data=book_data)
    else:
        return "Book not found."



@app.route('/favorites')
def add_favorite():
    """ Den hämtar 'saved_id' från användarens cookies
    och använder sedan 'get_book_data' för att hämta bokdata baserat på 'saved_id' """
# Kontrollera om 'saved_id' finns i cookies
    saved_id = request.cookies.get('saved_id')
    book_data = get_book_data(saved_id)

    if saved_id:
        # Hantera när 'saved_id' finns
        return render_template("books-ex.html", book_data=book_data)
    else:
        # Hantera när 'saved_id' inte finns
        return render_template("books-ex.html", book_data=None) 
        


@app.route('/random', methods=["GET", "POST"])
def random_book():
    total_books = 71993
    random_book_id = random.randint(1, total_books)
    book_data = get_book_data(random_book_id)
    """ För POST-förfrågningar hämtas 'saved_id' från formuläret och sparar det som en cookie (Saved_id sparar
    alltså användarens favorit bok (dess id)). Sedan returneras en HTML-sida med bokdata, 
    och den slumpmässigt valda boken"""
    if request.method == "POST":
        global saved_id
        saved_id = request.form['saved_id']

        response = make_response(render_template('random.html', book_data=book_data))
        response.set_cookie("saved_id", saved_id)
        return response
    return render_template('random.html', book_data=book_data)




@app.route('/search', methods =['GET','POST'])
def search():
    if request.method == 'POST':
     saved_id=request.form.get('saved_id')
     return redirect(url_for('search', query=request.form.get('query')))
    
    #Hämtar sökfrågan från URL och söker efter författare och böcker från den givna sökningen
    query = request.args.get('query', '')
    books_result = search_books(query)
    authors_result = search_authors(query)

    #Skapar dataframes från sökresultatet  
    books_df = pd.DataFrame(books_result)
    authors_df = pd.DataFrame(authors_result)

    

    #Tar bort kolumner som vi inte vill ha
    books_df = books_df.drop (['translators', 'bookshelves', 'copyright', 'media_type', 'formats', 'download_count'], axis=1)
    authors_df = authors_df.drop (['translators', 'bookshelves', 'copyright', 'media_type', 'formats', 'download_count'], axis=1)

    #Skapar HTML tabeller från dataframes
    books_table = books_df.to_html(classes="table table-bordered table-hover", index=False, justify="left")
    authors_table = authors_df.to_html(classes="table table-bordered table-hover", index=False, justify="left")

    #gör om kolumner till stor bokstav(men då bli varje ords första bokstav stor)
    '''
    books_table = re.sub(r'(?<=<td>)(.*?)(?=<\/td>)',lambda x:x.group(0).title(), books_table)
    authors_table = re.sub(r'(?<=<td>)(.*?)(?=<\/td>)',lambda x:x.group(0).title(), authors_table)
    '''
    #gör om titlar till stor bokstav
    books_table = re.sub(r'(?<=<th>)(.*?)(?=<\/th>)', lambda x: x.group(0).title(), books_table)
    authors_table = re.sub(r'(?<=<th>)(.*?)(?=<\/th>)', lambda x: x.group(0).title(), authors_table)

    return render_template('search_results.html', books_table=books_table, authors_table=authors_table)



def get_all_books():
    #Hämtar info om alla tillgänliga böcker från API
    response = requests.get('https://gutendex.com/books')
    if response.status_code == 200:
        books_info = response.json()
        return [book['id'] for book in books_info['results']]
    else:
        return []


def get_books_datas(book_id):
    #Hämtar info om en specifik bok via dess ID
    response = requests.get(f"https://gutendex.com/books/%7Bbook_id%7D")
    if response.status_code == 200:
        book_info = response.json()
        formats = book_info.get("formats", {})
        return {
            "Title": book_info.get("Title", ""),
            "Authors": [{'Name': author["name"].title(), 'Birth Year': author.get('birth_year', ''), 'Death Year': author.get('death_year', '')} for author in book_info.get("authors", [])],
            "Subjects": book_info.get("Subjects", []),
            "Languages": book_info.get("Languages", []),
            
        }
    else:
        return None

def search_books(query):
    #Söker efter böcker från den givna sökningen
    response = requests.get(f"https://gutendex.com/books/?search={query}")
    if response.status_code == 200:
        books_data = response.json()['results']
        books_df = pd.DataFrame(books_data)
        books_df = clean_dataframe(books_df)
        return books_df.to_dict(orient='records') or []
    else:
        return []

def search_authors(query):
    #Söker efter författare från den givna sökningen
    response = requests.get(f"https://gutendex.com/books/?search={query}&type=author")
    if response.status_code == 200:
        authors_data = response.json()['results']
        authors_df = pd.DataFrame(authors_data)
        authors_df = clean_dataframe(authors_df)
        return authors_df.to_dict(orient='records') or []
    else:
        return []

def clean_dataframe(df):
    # Använd applymap för att ersätta alla (){}[] med en tom sträng i varje cell
    df = df.applymap(lambda x: re.sub(r'[(){}[\]\'\']', '', str(x)))
    #ersätt _ med mellan slag
    df= df.applymap(lambda x: x.replace('_',' '))
    return df