# MiniBlog v0.1

Lab 3 — Flask căn bản. Dữ liệu list POSTS, 3 bài viết mẫu. Dùng layout(),
escape(), url_for() và không cần database, đúng phạm vi chương 3.

Từ thư mục miniblog, với môi trường đã cài Flask:

```powershell
python -m pip install -r requirements.txt
python -m flask --app app run --debug --port 8000
```

| URL | HTTP | Kết quả |
| --- | --- | --- |
| / | 200 | 3 liên kết bài viết |
| /about | 200 | Giới thiệu |
| /post/2 | 200 | Định tuyến trong Flask, tác giả binh |
| /user/an | 200 | 2 bài |
| /user/zz | 200 | Chưa có bài viết |
| /search?q=flask | 200 | 3 kết quả |
| /search?q=BSD | 200 | 1 kết quả |
| /search?q=%3Cb%3Ex%3C%2Fb%3E | 200 | Văn bản nguyên dạng đã escape |
| /post/99, /post/abc, /abc, /about/ | 404 | Trang 404 tùy biến |
| /blog | 301 | Location: / |
| /api/posts | 200 | JSON 3 bài viết |
| POST / | 405 | Method not allowed |

Lưu ý slide 62 đặt cả ba tiêu đề có chữ Flask, trong khi bảng kiểm tra
ở slide 68 ghi 2 kết quả. Bản này giữ nguyên ba tiêu đề theo slide 62,
nên tìm theo tiêu đề flask trả 3 kết quả đúng với dữ liệu, không cố tình bỏ sót.

```powershell
curl.exe -i http://127.0.0.1:8000/blog
curl.exe -i http://127.0.0.1:8000/api/posts
curl.exe -i -X POST http://127.0.0.1:8000/
python -m flask --app app routes
```

Kiểm thử từ thư mục cha: python -m unittest -v test_chuong_03.

Git: mã nguồn có thể đưa vào repository miniblog, commit feat: MiniBlog v0.1
và tag v0.1. Xem README_CHUONG_03.md tại thư mục nhom1 để dùng Git bundle.
