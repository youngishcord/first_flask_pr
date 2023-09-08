import sqlite3

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.exceptions import abort

# TODO: https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-ru#
#  делать с этого момента

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM posts WHERE id = ?',
                          (post_id,)).fetchone()
    conn.close()
    if result is None:
        abort(404)
    return result


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    result = get_post(post_id)
    return render_template('post.html', post=result)


@app.route('/create', methods=("GET", "POST"))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title and content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
