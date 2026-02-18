from flask import Flask, request, jsonify, render_template
import os
from waitress import serve

app = Flask(__name__)

books = [{"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
         {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
         {"id": 3, "title": "Problems in General Physsics", "author": "I.E Irodov"}
         ]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/all', methods=['GET'])
def all():
    return jsonify(books)


@app.route('/single_book', methods=['GET', 'POST'])
def single_book():
    if request.method == 'POST':
        search_id = request.form['id']
        for x in books:
            if int(search_id) == x['id']:
                return jsonify(x)
        return jsonify({'Error': 'Book Not Found'})
    else:
        return render_template('single_book.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_id = request.form['id']
        new_tit = request.form['tit']
        new_aut = request.form['aut']

        new_book = {'id': int(new_id), 'title': new_tit, 'author': new_aut}

        if new_id == '' or new_tit == '' or new_aut == '':
            return jsonify({'Error': 'Blank Input'})

        for x in books:
            if int(new_id) == x['id']:
                return jsonify({'Error': 'ID Already Exist'})

        books.append(new_book)
        return jsonify({'Success': 'New Book Added'})
    return render_template('addition.html')


@app.route('/delete_book', methods=['POST', 'GET'])
def delete_book():
    global books
    if request.method == 'POST':
        id = request.form['id']
        new_book_list = [x for x in books if int(id) != x['id']]
        books = new_book_list
        return jsonify(books)
    return render_template('deletion.html')


@app.route('/update_book', methods=['POST', 'GET'])
def update_book():
    if request.method == 'POST':
        count = 0
        id = request.form['id']
        category = request.form['category']
        new_value = request.form['new_value']

        if category == 'title':
            for x in books:
                if int(id) == x['id']:
                    count += 1
                    x['title'] = new_value
        elif category == 'author':
            for x in books:
                if int(id) == x['id']:
                    count += 1
                    x['author'] = new_value

        if count > 0:
            return jsonify(books)
        else:
            return jsonify({'Error': 'No Records Found'})
    return render_template('updation.html')


if __name__ == '__main__':
    # app.run(debug=True)
    # Render sets PORT, fallback for local dev
    port = int(os.environ.get('PORT', 8080))
    serve(app, host='0.0.0.0', port=port)
