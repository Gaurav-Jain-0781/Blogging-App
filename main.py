from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

posts_data = {
    0: {
        'post_id': 1,
        'title': 'My First Blog',
        'content': 'Hello , world !!',
    },
}


def create_blog_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS blog (post_id integer, title text, content text)')

    connection.commit()
    connection.close()


def add_blog(data):
    post_id = data['post_id']
    title = data['title'].capitalize()
    content = data['content']

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO blog VALUES ("{post_id}", "{title}", "{content}")')

    connection.commit()
    connection.close()


def retrive_data():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT post_id, title, content FROM blog')
    blog = [{'post_id': row[0],
             'title': row[1],
             'content': row[2]}
            for row in cursor.fetchall()]

    connection.close()

    for b in blog:
        post_id = len(posts_data)
        new_post = {
            'post_id': b['post_id'],
            'title': b['title'],
            'content': b['content']
        }
        posts_data[post_id] = new_post


@app.route('/')
def home_page():
    return render_template('home.html', post=posts_data)


@app.route('/post/<int:post_id>')
def returning_post(post_id):
    posts = posts_data.get(post_id)
    if not posts:   # if not post => true
        return render_template('error.html', message=f'post with id {post_id} was not found . ')
    return render_template('post_html.html', post=posts)


@app.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('Title').capitalize()
        content = request.form.get('content')
        new_post_id = len(posts_data)
        new_post = {
            'post_id': new_post_id,
            'title': title,
            'content': content
        }
        posts_data[new_post_id] = new_post
        add_blog(new_post)
        return redirect(url_for('returning_post', post_id=new_post_id))
    return render_template('form.html', message='Form for Creating Post')


retrive_data()

if __name__ == '__main__':
    create_blog_table()
    app.run(debug=True)
