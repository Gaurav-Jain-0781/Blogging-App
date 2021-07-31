from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import database

app = Flask(__name__)

posts_data = {
    0: {
        'post_id': 1,
        'title': 'My First Blog',
        'content': 'Hello , world !!',
        'author': 'gaurav jain'
    },
}


def home_page_update(title, content, author):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    data = cursor.execute("SELECT post_id, title from blog")

    for d in data:
        if d[1] == title:
            post_id = d[0]
            title_to_be_updated = title
            content_to_be_updated = content
            author_to_be_updated = author
            posts_data[post_id]['title'] = title_to_be_updated
            posts_data[post_id]['content'] = content_to_be_updated
            posts_data[post_id]['author'] = author_to_be_updated

    connection.close()


def adding_data():
    blog = database.retrive_data()

    for b in blog:
        post_id = len(posts_data)
        new_post = {
            'post_id': b['post_id'],
            'title': b['title'],
            'content': b['content'],
            'author': b['author']
        }
        posts_data[post_id] = new_post


@app.route('/')
def home_page():
    return render_template('home.html', post=posts_data)


@app.route('/post/<int:post_id>')
def returning_post(post_id):
    posts = posts_data.get(post_id)
    if not posts:   # if not post => true
        return render_template('error.html', message=f'Post with id {post_id} was not found . ')
    return render_template('post_html.html', post=posts)


@app.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('Title')
        content = request.form.get('content')
        author = request.form.get('author')

        new_post_id = len(posts_data)
        new_post = {
            'post_id': new_post_id,
            'title': title,
            'content': content,
            'author': author
        }
        posts_data[new_post_id] = new_post
        database.add_blog(new_post)
        return redirect(url_for('returning_post', post_id=new_post_id))
    return render_template('form.html', message='Form for Creating Post')


@app.route('/update')
def update():
    return render_template('update.html', message='Form to Update an Existing Post')


@app.route('/post/update_post', methods=['GET', 'POST'])
def update_post():
    if request.method == 'POST':
        title = request.form.get('Title')
        updated_title = request.form.get('Updated Title')
        updated_content = request.form.get('Updated Content')
        author = request.form.get('author')

        database.post_update(title, updated_title, updated_content, author)

        post = {
            'title': updated_title,
            'content': updated_content,
            'author': author,
        }

        home_page_update(updated_title, updated_content, author)
        return render_template('post_html.html', post=post)
    return render_template('error.html')


if __name__ == '__main__':
    database.create_blog_table()
    database.retrive_data()
    adding_data()
    app.run(debug=True)
