from flask import Flask, abort, jsonify, request, url_for
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False

BOOKS = [
    {"id": 1, "title": "Python cơ bản", "author": "Nguyễn Văn An",
     "year": 2024, "category": "Lập trình", "available": True},
    {"id": 2, "title": "Flask từ cơ bản đến ứng dụng", "author": "Trần Minh Anh",
     "year": 2025, "category": "Lập trình", "available": True},
    {"id": 3, "title": "Cơ sở dữ liệu", "author": "Lê Hoàng Nam",
     "year": 2023, "category": "Công nghệ thông tin", "available": False},
    {"id": 4, "title": "Mạng máy tính", "author": "Phạm Quốc Huy",
     "year": 2024, "category": "Công nghệ thông tin", "available": True},
    {"id": 5, "title": "Dế Mèn phiêu lưu ký", "author": "Tô Hoài",
     "year": 1941, "category": "Văn học", "available": True},
    {"id": 6, "title": "Lão Hạc", "author": "Nam Cao",
     "year": 1943, "category": "Văn học", "available": False},
]


def layout(title, body):
    """Bố cục chung; body chỉ nhận HTML đã escape dữ liệu."""
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} | LibraryMS</title>
    <link rel="stylesheet" href="{escape(url_for('static', filename='style.css'))}">
</head>
<body>
    <header>
        <nav class="container nav">
            <a class="brand" href="{escape(url_for('index'))}">Library<span>MS</span></a>
            <div class="nav-links">
                <a href="{escape(url_for('index'))}">Trang chủ</a>
                <a href="{escape(url_for('books'))}">Danh sách sách</a>
                <a href="{escape(url_for('api_books'))}">API JSON</a>
            </div>
        </nav>
    </header>
    <main class="container">{body}</main>
    <footer class="container">LibraryMS v0.1 · Học phần Phần mềm mã nguồn mở</footer>
</body>
</html>"""


def get_book(book_id):
    return next((book for book in BOOKS if book["id"] == book_id), None)


def not_found_message(book_id):
    return f"Không có sách với ID = {book_id}"


def status_badge(book):
    if book["available"]:
        return '<span class="badge available">Sẵn sàng cho mượn</span>'
    return '<span class="badge borrowed">Đang được mượn</span>'


@app.get("/")
def index():
    total = len(BOOKS)
    available = sum(book["available"] for book in BOOKS)
    body = f"""
    <section class="hero">
        <p class="eyebrow">THƯ VIỆN TRỰC TUYẾN · V0.1</p>
        <h1>Khám phá kho sách của bạn.</h1>
        <p>Tra cứu sách, xem thông tin và tình trạng sẵn sàng cho mượn.</p>
        <a class="button" href="{escape(url_for('books'))}">Khám phá danh sách sách</a>
    </section>
    <section class="stats" aria-label="Thống kê thư viện">
        <article><p>Tổng số đầu sách</p><strong>{escape(total)}</strong></article>
        <article><p>Sẵn sàng cho mượn</p><strong>{escape(available)}</strong></article>
        <article><p>Đang được mượn</p><strong>{escape(total - available)}</strong></article>
    </section>
    """
    return layout("Trang chủ", body)


@app.get("/books")
def books():
    category = request.args.get("category", "").strip()
    categories = sorted({book["category"] for book in BOOKS})
    results = [
        book for book in BOOKS
        if not category or book["category"].casefold() == category.casefold()
    ]
    all_class = "chip active" if not category else "chip"
    filters = [f'<a class="{all_class}" href="{escape(url_for("books"))}">Tất cả</a>']
    for item in categories:
        css = "chip active" if item.casefold() == category.casefold() else "chip"
        filters.append(
            f'<a class="{css}" href="{escape(url_for("books", category=item))}">'
            f'{escape(item)}</a>'
        )

    rows = []
    for book in results:
        rows.append(f"""
        <tr>
            <td>{escape(book["id"])}</td>
            <td><a class="book-link" href="{escape(url_for('book_detail', book_id=book['id']))}">
                {escape(book["title"])}</a></td>
            <td>{escape(book["author"])}</td>
            <td>{escape(book["year"])}</td>
            <td>{escape(book["category"])}</td>
            <td>{status_badge(book)}</td>
        </tr>""")
    table_rows = "".join(rows) or '<tr><td colspan="6" class="empty">Không có sách phù hợp.</td></tr>'
    body = f"""
    <p class="eyebrow">DANH MỤC THƯ VIỆN</p>
    <h1>Danh sách sách</h1>
    <p class="muted">Chọn thể loại để lọc sách hoặc nhấn tên sách để xem chi tiết.</p>
    <div class="filters" aria-label="Lọc theo thể loại">{"".join(filters)}</div>
    <p class="muted">Hiển thị {escape(len(results))} / {escape(len(BOOKS))} đầu sách
        · Thể loại: {escape(category or "Tất cả")}</p>
    <div class="table-wrap">
        <table>
            <thead><tr><th>ID</th><th>Tên sách</th><th>Tác giả</th><th>Năm</th>
            <th>Thể loại</th><th>Tình trạng</th></tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>
    """
    return layout("Danh sách sách", body)


@app.get("/books/<int:book_id>")
def book_detail(book_id):
    book = get_book(book_id)
    if book is None:
        abort(404, description=not_found_message(book_id))
    body = f"""
    <a class="back" href="{escape(url_for('books'))}">← Danh sách sách</a>
    <section class="detail">
        <p class="eyebrow">THÔNG TIN SÁCH · #{escape(book["id"])}</p>
        <h1>{escape(book["title"])}</h1>
        {status_badge(book)}
        <dl>
            <dt>ID</dt><dd>{escape(book["id"])}</dd>
            <dt>Tác giả</dt><dd>{escape(book["author"])}</dd>
            <dt>Năm xuất bản</dt><dd>{escape(book["year"])}</dd>
            <dt>Thể loại</dt><dd><a href="{escape(url_for('books', category=book['category']))}">
                {escape(book["category"])}</a></dd>
        </dl>
        <a class="button" href="{escape(url_for('api_book_detail', book_id=book_id))}">Xem JSON</a>
    </section>
    """
    return layout(book["title"], body)


@app.get("/api/books")
def api_books():
    return jsonify(BOOKS)


@app.get("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = get_book(book_id)
    if book is None:
        return jsonify(error=not_found_message(book_id)), 404
    return jsonify(book)


@app.errorhandler(404)
def page_not_found(error):
    message = error.description
    # Dùng JSON cho cả URL API không khớp converter hoặc không tồn tại.
    if request.path.startswith("/api/") or request.path == "/api":
        return jsonify(error="Không tìm thấy tài nguyên."), 404
    if not message.startswith("Không có sách với ID = "):
        message = "Trang bạn tìm kiếm không tồn tại."
    body = f"""
    <section class="error-page">
        <p class="error-code">404</p>
        <h1>Không tìm thấy trang</h1>
        <p>{escape(message)}</p>
        <a class="button" href="{escape(url_for('index'))}">Về trang chủ</a>
    </section>"""
    return layout("404 - Không tìm thấy trang", body), 404


if __name__ == "__main__":
    app.run(port=8000)
