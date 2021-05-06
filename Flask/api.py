import flask
from flask import redirect, url_for, request, jsonify, render_template
import sqlite3
import json


app = flask.Flask(__name__, template_folder='./')
app.config["DEBUG"] = True



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')

    conn.row_factory = dict_factory
    
    cur = conn.cursor()

    all_books = cur.execute('SELECT * FROM books;').fetchall()
    #return jsonify(all_books)
    return render_template("index.html",object = all_books)

@app.route('/books', methods=['POST'])
def add_books():
    conn = sqlite3.connect('books.db')

    sql = '''INSERT INTO books(id, published, author, title, first_sentence)
                VALUES(?,?,?,?,?) '''
                
    #book = (222, 2021, 'kevin ansard', 'cours Python', 'Bonne chance')
    cur = conn.cursor()

    bodyjson = request.get_json() #get body from post request

    bodydict = json.loads(json.dumps(body)) #get body into dict
    testb = (data['id'], data['published'], data['author'], data['title'], data['first_sentence'])

    #print(data['author'])
    #print(body)
    cur.execute(sql, testb)

    conn.commit()

    return redirect("http://127.0.0.1:5000/books/all")


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Page Coucou trouvée</p>", 404


@app.route('/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()