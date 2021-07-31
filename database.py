import sqlite3


def create_blog_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS blog (post_id integer, title text, content text, author text)')

    connection.commit()
    connection.close()


def add_blog(data):
    post_id = data['post_id']
    title = data['title']
    content = data['content']
    author = data['author']

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO blog VALUES ("{post_id}", "{title}", "{content}", "{author}")')

    connection.commit()
    connection.close()


def post_update(title, updated_title, updated_content, author):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT post_id, title, content, author FROM blog')

    blog = [{'post_id': row[0],
             'title': row[1],
             'content': row[2],
             'author': row[3]}
            for row in cursor.fetchall()]

    titles = []

    for b in blog:
        titles.append(b['title'])

    for t in titles:
        if t == title:
            cursor.execute('UPDATE blog SET title=? WHERE title=?', (updated_title, title))
            cursor.execute('UPDATE blog SET content=? WHERE title=?', (updated_content, updated_title))
            cursor.execute('UPDATE blog SET author=? WHERE title=?', (author, updated_title))

    connection.commit()
    connection.close()


def retrive_data():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT post_id, title, content, author FROM blog')

    blog = [{'post_id': row[0],
             'title': row[1],
             'content': row[2],
             'author': row[3]}
            for row in cursor.fetchall()]

    connection.close()
    return blog
