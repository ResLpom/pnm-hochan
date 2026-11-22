from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.get("/hello/", defaults={"name": "bạn"})
@app.get("/hello/<name>")
def hello(name):
    return f"Xin chào, {escape(name)}!"
