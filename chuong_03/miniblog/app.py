from flask import Flask, abort, redirect, request, url_for
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False

POSTS = [
    {"id": 1, "title": "Chào Flask", "author": "an",
     "content": "Flask là một micro-framework Python để xây dựng ứng dụng web.",
     "created": "2026-09-01"},
    {"id": 2, "title": "Định tuyến trong Flask", "author": "binh",
     "content": "Route ánh xạ URL tới view function. Dùng url_for để sinh URL.",
     "created": "2026-09-02"},
    {"id": 3, "title": "Giấy phép BSD của Flask", "author": "an",
     "content": "Giấy phép BSD cho phép sử dụng và phân phối phần mềm nếu tuân thủ các điều kiện.",
     "created": "2026-09-03"},
]


def find_post(post_id):
    return next((post for post in POSTS if post["id"] == post_id), None)


def layout(title, body):
    return f"""<!doctype html>
<html lang="vi">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} - MiniBlog</title>
<link rel="stylesheet" href="{url_for('static', filename='style.css')}"></head>
<body>
<header><nav>
    <strong>MiniBlog</strong>
    <a href="{url_for('index')}">Trang chủ</a>
    <a href="{url_for('about')}">Giới thiệu</a>
    <a href="{url_for('search')}">Tìm kiếm</a>
    <a href="{url_for('api_posts')}">API JSON</a>
</nav></header>
<main>{body}</main>
<footer>MiniBlog v0.1 · Flask căn bản</footer>
</body></html>"""


def post_list(posts):
    if not posts:
        return "<p>Chưa có bài viết.</p>"
    items = "".join(
        f'<li><a href="{url_for("post_detail", post_id=p["id"])}">{escape(p["title"])}</a>'
        f'<span>{escape(p["created"])} · <a href="{url_for("user_profile", username=p["author"])}">'
        f'{escape(p["author"])}</a></span></li>'
        for p in posts
    )
    return f'<ul class="posts">{items}</ul>'


@app.get("/")
def index():
    return layout("Trang chủ", "<h1>MiniBlog</h1><p>Khám phá các bài viết về Flask.</p>" + post_list(POSTS))


@app.get("/about")
def about():
    return layout("Giới thiệu", "<h1>Giới thiệu</h1><p>Blog minh họa học phần Phần mềm mã nguồn mở.</p>")


@app.get("/post/<int:post_id>")
def post_detail(post_id):
    post = find_post(post_id)
    if post is None:
        abort(404)
    author_link = url_for("user_profile", username=post["author"])
    body = f"""<h1>{escape(post['title'])}</h1>
    <p><em>Tác giả: <a href="{author_link}">{escape(post['author'])}</a>
    — {escape(post['created'])}</em></p><p>{escape(post['content'])}</p>
    <a href="{url_for('index')}">Quay lại trang chủ</a>"""
    return layout(post["title"], body)


@app.get("/user/<username>")
def user_profile(username):
    posts = [p for p in POSTS if p["author"] == username]
    return layout(username, f"<h1>Bài viết của {escape(username)}</h1>" + post_list(posts))


@app.get("/search")
def search():
    q = request.args.get("q", "").strip()
    form = f"""<h1>Tìm kiếm</h1><form method="get" action="{url_for('search')}">
    <input name="q" value="{escape(q)}" placeholder="Nhập tiêu đề bài viết">
    <button>Tìm</button></form>"""
    if not q:
        return layout("Tìm kiếm", form)
    results = [p for p in POSTS if q.casefold() in p["title"].casefold()]
    return layout("Tìm kiếm", form + f"<p>Có {len(results)} kết quả cho “{escape(q)}”.</p>" + post_list(results))


@app.get("/blog")
def old_blog():
    return redirect(url_for("index"), code=301)


@app.get("/api/posts")
def api_posts():
    return POSTS


@app.errorhandler(404)
def page_not_found(error):
    return layout("Không tìm thấy", "<h1>404 – Không tìm thấy trang</h1>"
                  f'<p><a href="{url_for("index")}">Về trang chủ</a></p>'), 404
