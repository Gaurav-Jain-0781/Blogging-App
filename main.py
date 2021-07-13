from flask import Flask

app = Flask(__name__)

posts = {
    0: {'title': "my first blog",
        'content': 'hello , world !!'
        }
}


@app.route('/')
def home_page():
    return "my first flask app ."


@app.route('/posts/<int:post_id>')
def returning_post(post_id):
    post = posts.get(post_id)
    return f"post title : {post['title']}, content : {post['content']}"


if __name__ == '__main__':
    app.run(debug=True)
