# LibraryMS v0.1

Bài tập dự án Chương 3 – Flask căn bản, học phần Phần mềm mã nguồn mở.

Ứng dụng quản lý danh mục sách đơn giản. Dữ liệu gồm sáu cuốn sách mẫu
trong list `BOOKS`, không cần SQLite hoặc cơ sở dữ liệu.
HTML được tạo bằng hàm `layout()` dùng chung, đúng phạm vi Chương 3.

## 1. Cài đặt và chạy (PowerShell)

Mở terminal trong thư mục `libraryms`. Nếu chưa có môi trường ảo:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --debug --port 8000
```

Hoặc nếu thư mục cha đã có `.venv`, sử dụng luôn môi trường đó:

```powershell
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m flask --app app run --debug --port 8000
```

Mở http://127.0.0.1:8000/ trong trình duyệt.

## 2. Cấu trúc

| File | Chức năng |
| --- | --- |
| `app.py` | Dữ liệu BOOKS, hàm dùng chung, 5 route, xử lý lỗi 404 |
| `static/style.css` | Giao diện chung |
| `test_app.py` | Kiểm thử tự động với unittest và Flask test client |
| `requirements.txt` | Thư viện cần cài |
| `.gitignore` | Loại môi trường ảo và file tạm khỏi Git |

## 3. Các route

| Method | URL | Kết quả |
| --- | --- | --- |
| GET | / | Tổng 6 đầu sách, 4 sẵn sàng, 2 đang được mượn |
| GET | /books | Bảng danh sách và bộ lọc thể loại |
| GET | /books/1 | Chi tiết sách Python cơ bản |
| GET | /api/books | JSON danh sách 6 cuốn sách |
| GET | /api/books/1 | JSON chi tiết sách |

Flask còn tự đăng ký route static để phục vụ CSS.

## 4. Kiểm thử bằng URL / curl

Khởi động Flask ở port 8000 trước khi chạy curl. Trên PowerShell dùng
`curl.exe` thay cho `curl` nếu curl là alias của Invoke-WebRequest.

| URL kiểm thử | HTTP | Kết quả mong đợi |
| --- | --- | --- |
| http://127.0.0.1:8000/ | 200 | Tổng 6 sách, 4 sẵn sàng |
| http://127.0.0.1:8000/books | 200 | Đủ 6 dòng dữ liệu |
| http://127.0.0.1:8000/books?category=L%E1%BA%ADp%20tr%C3%ACnh | 200 | Chỉ 2 sách Lập trình |
| http://127.0.0.1:8000/books?category=xyz | 200 | Không có sách phù hợp |
| http://127.0.0.1:8000/books/1 | 200 | Chi tiết sách |
| http://127.0.0.1:8000/books/999 | 404 | Không có sách với ID = 999 |
| http://127.0.0.1:8000/books/abc | 404 | Trang 404 tiếng Việt |
| http://127.0.0.1:8000/abc | 404 | Trang 404 có menu chung |
| http://127.0.0.1:8000/api/books | 200 | JSON array |
| http://127.0.0.1:8000/api/books/1 | 200 | JSON object |
| http://127.0.0.1:8000/api/books/999 | 404 | JSON có trường error |
| http://127.0.0.1:8000/api/books/abc | 404 | JSON có trường error |
| http://127.0.0.1:8000/books?category=%3Cscript%3Ealert(1)%3C%2Fscript%3E | 200 | Chuỗi script được escape |

```powershell
curl.exe -i http://127.0.0.1:8000/
curl.exe -i http://127.0.0.1:8000/books
curl.exe -i -G --data-urlencode "category=Lập trình" http://127.0.0.1:8000/books
curl.exe -i http://127.0.0.1:8000/books/999
curl.exe -i http://127.0.0.1:8000/api/books/999
curl.exe -i -X POST http://127.0.0.1:8000/books
```

Kiểm thử tự động (dùng Python trong môi trường đã cài Flask):

```powershell
python -m unittest -v
python -m flask --app app routes
```

Kết quả đã kiểm thử bằng Flask 3.1.3: 16/16 bài kiểm thử thành công.
Lệnh routes hiển thị đủ 5 route nghiệp vụ và 1 route static.

## 5. Đối chiếu yêu cầu

- [x] BOOKS có ít nhất 4 sách với đủ 6 trường.
- [x] Đủ 5 route, GET.
- [x] Danh sách dạng bảng, có liên kết tới chi tiết và lọc thể loại.
- [x] Lỗi 404 HTML tiếng Việt với menu chung; lỗi API trả JSON và HTTP 404.
- [x] Mọi liên kết trong HTML sinh bằng url_for().
- [x] Dữ liệu động đưa vào HTML được escape() bằng MarkupSafe.
- [x] Tái sử dụng layout(), get_book(), status_badge(), not_found_message().
- [x] .gitignore, README hướng dẫn kiểm thử.

## 6. Nộp GitHub

Tên repository: `libraryms`. Tag theo đề: `v0.1`.

Nếu dùng gói ZIP có sẵn thư mục Git, không cần git init hoặc commit lại.
Kiểm tra:

```powershell
git status
git log -1 --oneline
git tag
```

Tạo repository trống tên libraryms trong tài khoản GitHub của bạn, sau đó
thay TEN_GITHUB bằng username thực tế:

```powershell
git remote add origin https://github.com/TEN_GITHUB/libraryms.git
git push -u origin main
git push origin v0.1
```

Nếu origin đã tồn tại, kiểm tra bằng git remote -v và chỉ cập nhật URL nếu
đó là repository bạn định nộp. Xác thực GitHub khi được yêu cầu.
