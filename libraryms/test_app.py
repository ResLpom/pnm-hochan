import unittest
from unittest.mock import patch

from app import BOOKS, app


class LibraryMSTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_book_data(self):
        self.assertGreaterEqual(len(BOOKS), 4)
        self.assertEqual(len({book["id"] for book in BOOKS}), len(BOOKS))
        for book in BOOKS:
            self.assertEqual(set(book), {"id", "title", "author", "year", "category", "available"})
            self.assertIsInstance(book["available"], bool)

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Tổng số đầu sách", html)
        self.assertIn(f"<strong>{len(BOOKS)}</strong>", html)
        self.assertIn(f'<strong>{sum(b["available"] for b in BOOKS)}</strong>', html)

    def test_books(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for book in BOOKS:
            self.assertIn(book["title"], html)
            self.assertIn(f'href="/books/{book["id"]}"', html)
        self.assertIn("Tất cả", html)

    def test_category(self):
        response = self.client.get("/books", query_string={"category": "Lập trình"})
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for book in BOOKS:
            if book["category"] == "Lập trình":
                self.assertIn(book["title"], html)
            else:
                self.assertNotIn(book["title"], html)

    def test_unknown_category(self):
        response = self.client.get("/books", query_string={"category": "Không tồn tại"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Không có sách phù hợp", response.get_data(as_text=True))

    def test_book_detail(self):
        response = self.client.get("/books/1")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for key in ("title", "author", "year", "category"):
            self.assertIn(str(BOOKS[0][key]), html)
        self.assertIn('href="/api/books/1"', html)

    def test_missing_book_html(self):
        response = self.client.get("/books/999")
        self.assertEqual(response.status_code, 404)
        html = response.get_data(as_text=True)
        self.assertIn("Không có sách với ID = 999", html)
        self.assertIn('href="/books"', html)

    def test_unknown_html_route(self):
        for url in ("/abc", "/books/abc"):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.assertIn("Không tìm thấy trang", response.get_data(as_text=True))

    def test_api_list(self):
        response = self.client.get("/api/books")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(response.get_json(), BOOKS)

    def test_api_detail(self):
        response = self.client.get("/api/books/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), BOOKS[0])

    def test_api_missing(self):
        response = self.client.get("/api/books/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Không có sách với ID = 999"})

    def test_api_invalid_route(self):
        for url in ("/api/books/abc", "/api/abc"):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
                self.assertIn("error", response.get_json())

    def test_escape_query(self):
        response = self.client.get("/books", query_string={"category": "<script>alert(1)</script>"})
        html = response.get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)

    def test_escape_book_data(self):
        # Giả lập dữ liệu có HTML độc hại ở tên sách, tác giả và thể loại.
        sample = {"id": 42, "title": "<b>Test</b>", "author": "<img src=x>",
                  "year": 2026, "category": "<script>test</script>", "available": True}
        with patch("app.BOOKS", [sample]):
            for url in ("/books", "/books/42"):
                html = self.client.get(url).get_data(as_text=True)
                for key in ("title", "author", "category"):
                    self.assertNotIn(sample[key], html)
                self.assertIn("&lt;b&gt;Test&lt;/b&gt;", html)

    def test_css(self):
        response = self.client.get("/static/style.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.content_type)
        response.close()

    def test_get_only(self):
        self.assertEqual(self.client.post("/books").status_code, 405)


if __name__ == "__main__":
    unittest.main()
