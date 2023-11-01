from flask import Flask, render_template, redirect, request, make_response
import requests
import random
import pandas as pd
import re


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
    total_books = 71993  # Det finns 71993 olika böcker i api:et
    random_book_id = random.randint(0, total_books)
    book_data = get_book_data(random_book_id)
    
    return render_template('random.html', book_data=book_data)


@app.route('/search')
def search():
    #Hämtar sökfrågan från URL och söker efter författare och böcker från den givna sökningen
    query = request.args.get('query', '')
    books_result = search_books(query)
    authors_result = search_authors(query)

    #Skapar dataframes från sökresultatet  
    books_df = pd.DataFrame(books_result)
    authors_df = pd.DataFrame(authors_result)

    #Tar bort kolumner som vi inte vill ha
    books_df = books_df.drop (['id', 'translators', 'bookshelves', 'copyright', 'media_type', 'formats', 'download_count'], axis=1)
    authors_df = authors_df.drop (['id', 'translators', 'bookshelves', 'copyright', 'media_type', 'formats', 'download_count'], axis=1)

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


def get_books_data(book_id):
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

