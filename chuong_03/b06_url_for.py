from flask import Flask, request, url_for
from markupsafe import escape

app = Flask(__name__)


@app.get("/")
def index():
    return f'<h1>Trang chủ</h1><a href="{url_for("menu")}">Menu</a>'


@app.get("/about")
def about():
    return "Giới thiệu"


@app.get("/post/<int:post_id>")
def post_detail(post_id):
    return f"Bài viết số {post_id}"


@app.get("/user/<username>")
def user_profile(username):
    return f"Người dùng: {escape(username)}"


@app.get("/search")
def search():
    return f"Tìm kiếm: {escape(request.args.get('q', ''))}"


@app.get("/menu")
def menu():
    links = [
        ("Trang chủ", url_for("index")),
        ("Giới thiệu", url_for("about")),
        ("Bài viết 7", url_for("post_detail", post_id=7, lang="vi")),
        ("Nguyễn An", url_for("user_profile", username="Nguyễn An")),
        ("Tìm kiếm", url_for("search", q="flask & python")),
    ]
    return "<h1>Menu</h1><ul>" + "".join(
        f'<li><a href="{escape(url)}">{escape(label)}</a></li>'
        for label, url in links
    ) + "</ul>"
