from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/info", methods=["GET", "POST"])
def info():
    values = [
        ("Phương thức", request.method),
        ("Đường dẫn", request.path),
        ("Đường dẫn kèm query", request.full_path),
        ("URL đầy đủ", request.url),
        ("Địa chỉ IP", request.remote_addr),
        ("User-Agent", request.headers.get("User-Agent", "")),
        ("Các tham số query", dict(request.args.lists())),
    ]
    rows = "".join(
        f"<tr><th>{escape(label)}</th><td>{escape(value)}</td></tr>"
        for label, value in values
    )
    return f'<h1>Thông tin request</h1><table border="1" cellpadding="8">{rows}</table>'
