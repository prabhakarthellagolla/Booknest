from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books')
def books():
    search_query = request.args.get('search', '').lower()
    book_list = []

    with open('books.csv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (search_query in row['Title'].lower()) or (search_query in row['Author'].lower()):
                book_list.append(row)

    return render_template('books.html', books=book_list)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        cover = request.form['cover']

        with open('books.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([title, author, genre, cover])

        return redirect('/books')
    return render_template('add_book.html')

@app.route('/delete', methods=['POST'])
def delete_book():
    title = request.form['title']
    author = request.form['author']
    genre = request.form['genre']
    cover = request.form['cover']

    books = []
    with open('books.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            books.append(row)

    header = books[0]
    books = books[1:]

    books = [book for book in books if book != [title, author, genre, cover]]

    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(books)

    return redirect('/books')

@app.route('/edit', methods=['GET', 'POST'])
def edit_book():
    if request.method == 'GET':
        # get book data from URL parameters
        title = request.args.get('title')
        author = request.args.get('author')
        genre = request.args.get('genre')
        cover = request.args.get('cover')
        return render_template('edit_book.html', title=title, author=author, genre=genre, cover=cover)

    # POST: save edited data
    old_title = request.form['old_title']
    old_author = request.form['old_author']
    old_genre = request.form['old_genre']
    old_cover = request.form['old_cover']

    new_title = request.form['title']
    new_author = request.form['author']
    new_genre = request.form['genre']
    new_cover = request.form['cover']

    books = []
    with open('books.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            books.append(row)

    header = books[0]
    books = books[1:]

    # update the matching book
    updated_books = []
    for book in books:
        if book == [old_title, old_author, old_genre, old_cover]:
            updated_books.append([new_title, new_author, new_genre, new_cover])
        else:
            updated_books.append(book)

    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(updated_books)

    return redirect('/books')

if __name__ == '__main__':
    app.run(debug=True)
