from flask import Flask

app = Flask(__name__)


@app.get("/square/<int(signed=True):n>")
def square(n):
    return str(n ** 2)
