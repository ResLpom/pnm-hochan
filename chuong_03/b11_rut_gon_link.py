from flask import Flask, abort, redirect, url_for
from markupsafe import escape

app = Flask(__name__)
LINKS = {
    "flask": "https://flask.palletsprojects.com/",
    "python": "https://www.python.org/",
    "github": "https://github.com/",
    "osi": "https://opensource.org/",
}


@app.get("/links")
def links():
    items = "".join(
        f'<li><a href="{url_for("go", code=code)}">{escape(code)}</a> — {escape(url)}</li>'
        for code, url in LINKS.items()
    )
    return f"<h1>Danh sách liên kết</h1><ul>{items}</ul>"


@app.get("/go/<code>")
def go(code):
    target = LINKS.get(code.lower())
    if target is None:
        abort(404, description=f"Không có mã {code}.")
    return redirect(target, code=302)


@app.errorhandler(404)
def not_found(error):
    return (f"<h1>404 – Không tìm thấy</h1><p>{escape(error.description)}</p>"
            f'<a href="{url_for("links")}">Về danh sách liên kết</a>'), 404
