from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts_data = {
    0: {
        'post_id': 1,
        'title': 'my first blog',
        'content': 'hello , world !!',
    },
}


def update_post_data():
    with open('data.txt', 'r') as file:
        lines = [line.strip().split(',') for line in file.readlines()]

    for line in lines:
        post_id = len(posts_data)
        new_post = {
            'post_id': line[0],
            'title': line[1],
            'content': line[2],
        }
        posts_data[post_id] = new_post


def add_blog(data):
    post_id = data['post_id']
    title = data['title']
    content = data['content']
    with open('data.txt', 'a') as file:
        file.write(f'{post_id},{title},{content}\n')


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
        title = request.form.get('Title')
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
    return render_template('form.html', message='form for creating post .')


update_post_data()


if __name__ == '__main__':
    app.run(debug=True)

