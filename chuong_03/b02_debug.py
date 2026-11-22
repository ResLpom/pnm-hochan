from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "Xin chào Flask! Chương 3."


@app.get("/chia-nhom")
def chia_nhom():
    so_bai = 12
    so_nhom = 0
    # Cố ý gây lỗi để học cách đọc traceback (Bài 2).
    return f"Mỗi nhóm làm {so_bai / so_nhom} bài"
