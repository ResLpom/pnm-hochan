from flask import Flask, render_template, abort

app = Flask(__name__)


POSTS = [
    {
        "id": 1,
        "title": "Học Flask cơ bản",
        "content": "Tìm hiểu route, request và response trong Flask.",
        "tags": ["Python", "Flask"]
    },

    {
        "id": 2,
        "title": "Template với Jinja2",
        "content": "Tìm hiểu extends, include, block và macro.",
        "tags": ["Jinja2", "HTML"]
    },

    {
        "id": 3,
        "title": "Macro trong Jinja2",
        "content": "Macro giúp tạo các thành phần HTML có thể tái sử dụng.",
        "tags": ["Macro", "Jinja2", "Flask"]
    }
]


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/hello/<name>")
def hello(name):
    return render_template(
        "hello.html",
        name=name,
        skills=["Python", "Flask"]
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        posts=POSTS
    )
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def post_detail(post_id):

    post = next(
        (
            post
            for post in POSTS
            if post["id"] == post_id
        ),
        None
    )

    if post is None:
        abort(404)

    return f"""
        <h1>{post["title"]}</h1>
        <p>{post["content"]}</p>
        <a href="/about">Quay lại</a>
    """


if __name__ == "__main__":
    app.run(
        debug=True,
        port=1000
    )