from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
def get_db():
    conn = sqlite3.connect('library.db')
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT
        )
    """)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = get_db()
        conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)",
            (title, author)
        )
        conn.commit()
        conn.close()

        return redirect('/view')

    return render_template('add_book.html')

@app.route('/view')
def view_books():
    conn = get_db()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template('view_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
