# Chương 3 — Flask căn bản

Học phần Phần mềm mã nguồn mở. Bám sát tài liệu chương 3, bài 1–14 (trang 9, 16, 24–25, 28, 32, 37, 46–48, 52, 56–57), Lab 3 và dự án (trang 59–74).

## Cài đặt và chạy

Từ thư mục nhom1 trên Windows PowerShell:

```powershell
# Chỉ tạo môi trường ảo nếu chưa có .venv
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r chuong_03\requirements.txt
cd chuong_03
..\.venv\Scripts\python.exe -m flask --app b03_loi_chao run --debug --port 8000
```

Nếu đã có .venv thì bỏ qua lệnh py -m venv. Mỗi bài có ứng dụng Flask riêng.
Nhấn Ctrl+C để dừng ứng dụng trước khi chạy bài tiếp theo. Đổi tên module
b03_loi_chao thành tên file cần chạy (bỏ đuôi .py). Khi dùng PowerShell,
dùng curl.exe thay vì curl. Không cần SQLite cho các bài mới.

| Bài | File hoặc mục | URL kiểm thử chính |
| --- | --- | --- |
| 1 | README: khảo sát phụ thuộc | pip show |
| 2 | b02_debug.py | /, /chia-nhom |
| 3 | b03_loi_chao.py | /hello/, /hello/An |
| 4 | b04_binh_phuong.py | /square/12, /square/-3 |
| 5 | b05_converter.py | /sum/1,2,3 |
| 6 | b06_url_for.py | /menu |
| 7 | b07_login.py | /login |
| 8 | b08_request.py | /info?x=1&y=2 |
| 9 | b09_may_tinh.py | /calc?a=5&b=3 |
| 10 | b10_api_tien_ich.py | /api/time, /api/random |
| 11 | b11_rut_gon_link.py | /links, /go/flask |
| 12 | b12_counter.py | /counter |
| 13 | README: context | flask shell, dùng Bài 6 |
| 14 | b14_co_loi.py | /, /about, /post/1, /grade/3, /contact |
| Lab 3 | miniblog/app.py | /, /search, /api/posts |
| Dự án | ../libraryms/app.py | /, /books, /api/books |

## Bài 1 — Khảo sát các gói phụ thuộc

Lệnh đã chạy trong môi trường kiểm thử:

```powershell
python -m pip show flask
python -m pip show Werkzeug Jinja2 click blinker itsdangerous MarkupSafe
python -m pip show -v Jinja2 blinker itsdangerous
```

Flask 3.1.3, Requires: blinker, click, itsdangerous, jinja2, markupsafe, werkzeug.

| Gói | Phiên bản ghi nhận | Giấy phép | Vai trò |
| --- | --- | --- | --- |
| Flask | 3.1.3 | BSD-3-Clause | Framework web |
| Werkzeug | 3.1.9 | BSD-3-Clause | WSGI, routing, request/response |
| Jinja2 | 3.1.6 | BSD-3-Clause | Template HTML |
| click | 8.5.1 | BSD-3-Clause | Lệnh CLI flask |
| blinker | 1.9.0 | MIT | Tín hiệu, sự kiện |
| itsdangerous | 2.2.0 | BSD-3-Clause | Ký dữ liệu, xác thực tính toàn vẹn |
| MarkupSafe | 3.0.4 | BSD-3-Clause | Escape ký tự HTML |

Khi License trống, xem LICENSE.txt trong thư mục *.dist-info hoặc thư mục
licenses/ bên trong *.dist-info (đã đọc giấy phép cài đặt của Jinja2, blinker,
itsdangerous để đối chiếu). Phiên bản trên máy khác có thể khác.

BSD và MIT là giấy phép mã nguồn mở cho phép sử dụng trong phần mềm thương mại
đóng mã nguồn, không bắt buộc phát hành toàn bộ mã nguồn ứng dụng theo cùng
giấy phép, nhưng phải tuân thủ thông báo bản quyền, giấy phép và điều kiện
phân phối tương ứng. Không dùng tên tác giả để quảng bá khi không được phép.

## Bài 2 — Debug và traceback

```powershell
python -m flask --app b02_debug run --debug --port 8000
```

- Ban đầu đặt câu chào ở index là Hello, World!, sửa thành Xin chào Flask! Chương 3.
  Khi lưu file ở chế độ debug/reloader, Flask phát hiện thay đổi và khởi động
  lại; thông báo dạng Detected change ... reloading / Restarting with stat.
  File nộp là bản sau khi sửa câu chào.
- / trả 200, /chia-nhom trả 500 với ZeroDivisionError: division by zero,
  file b02_debug.py, dòng 16, hàm chia_nhom (đã kiểm tra bằng HTTP).
- Dừng server rồi chạy không có --debug:

```powershell
python -m flask --app b02_debug run --port 8000
curl.exe -i http://127.0.0.1:8000/chia-nhom
```

HTTP 500 trong cả hai chế độ. Debug hiển thị trang Werkzeug Debugger; không
debug chỉ trả trang Internal Server Error. Terminal vẫn ghi traceback.
Không bật debug khi triển khai vì có thể lộ thông tin nội bộ và debugger
có khả năng thực thi mã. Lỗi chia 0 được chủ ý giữ lại đúng đề.

## Bài 3–5 — Routing

Chạy từng module tương ứng và thử các URL sau với tiền tố http://127.0.0.1:8000.

| Bài | URL | Kết quả đã kiểm tra |
| --- | --- | --- |
| 3 | /hello/ | Xin chào, bạn! |
| 3 | /hello/An | Xin chào, An! |
| 3 | /hello/%3Cscript%3E | Hiển thị chữ script trong dấu ngoặc góc, HTML đã escape |
| 4 | /square/12 | 144 |
| 4 | /square/abc | 404 |
| 4 | /square/2.5 | 404 |
| 4 | /square/-3 | Trước: 404; sau signed=True: 9 |
| 5 | /sum/1,2,3 | numbers=[1,2,3], sum=6 |
| 5 | /sum/5 | numbers=[5], sum=5 |
| 5 | /sum/-1,4,10 | numbers=[-1,4,10], sum=13 |
| 5 | /sum/1,,2, /sum/a,b | 404 |

Bài 3 dùng cùng một view và defaults. Escape làm cho đầu vào từ URL trở
thành văn bản, không phải thẻ HTML. Bài 4 converter int mặc định chỉ khớp
số không âm; signed=True mở rộng cho số âm. Bài 5:

```python
with app.test_request_context():
    print(url_for("sum_numbers", numbers=[4, 5, 6]))
# /sum/4,5,6
```

## Bài 6 — url_for

```powershell
python -m flask --app b06_url_for shell
```

```python
from flask import url_for
ctx = app.test_request_context()
ctx.push()
url_for("about")
url_for("post_detail", post_id=7)
url_for("post_detail", post_id=7, lang="vi")
url_for("user_profile", username="Nguyễn An")
url_for("search", q="flask & python")
url_for("post_detail")
url_for("post_detail", post_id="abc")
ctx.pop()
```

| Lệnh | Dự đoán | Kết quả kiểm tra |
| --- | --- | --- |
| about | /about | /about |
| post_detail, 7 | /post/7 | /post/7 |
| post_detail, 7, lang=vi | /post/7?lang=vi | /post/7?lang=vi |
| user_profile, Nguyễn An | URL Unicode được mã hóa | /user/Nguy%E1%BB%85n%20An |
| search, flask & python | Query được mã hóa | /search?q=flask+%26+python |
| post_detail, thiếu ID | BuildError | BuildError: Did you forget to specify values ['post_id']? |
| post_detail, abc | ValueError | ValueError: invalid literal for int() with base 10: 'abc' |

/menu có 5 liên kết sinh bằng url_for.

## Bài 7 — GET và POST

```powershell
curl.exe -i http://127.0.0.1:8000/login
curl.exe -i -X POST http://127.0.0.1:8000/login
curl.exe -i -X PUT http://127.0.0.1:8000/login
```

GET 200: form; POST 200: Đã nhận yêu cầu đăng nhập (POST).
PUT 405, Allow gồm GET, HEAD, POST, OPTIONS (thứ tự có thể thay đổi).
Đã kiểm tra HTTP trực tiếp. Có thể mở DevTools → Network, vào /login và
nhấn Đăng nhập để quan sát GET và POST. Đây là bài phương thức HTTP, không
thay thế trang đăng nhập thực tế của dự án nhom1.

## Bài 8 — Request

```powershell
curl.exe -i "http://127.0.0.1:8000/info?x=1&y=2"
curl.exe -i -X POST "http://127.0.0.1:8000/info?x=1&y=2"
curl.exe -i -A "<script>" http://127.0.0.1:8000/info
```

GET và POST đều 200. Bảng có method, path, full_path, url, remote_addr,
User-Agent, query. Path là /info; full_path là /info?x=1&y=2;
query là x=1, y=2. Khi chạy curl và trình duyệt, User-Agent thường khác
(curl/<version> so với Mozilla/5.0... tùy trình duyệt). Kiểm thử tự động xác
nhận User-Agent chứa dấu ngoặc góc được escape.

## Bài 9 — Máy tính JSON

| URL | HTTP | Kết quả |
| --- | --- | --- |
| /calc?a=5&b=3 | 200 | a=5.0, b=3.0, op=add, expression="5 + 3", result=8.0 |
| /calc?a=5&b=3&op=sub | 200 | 2.0 |
| /calc?a=5&b=3&op=mul | 200 | 15.0 |
| /calc?a=6&b=3&op=div | 200 | 2.0 |
| /calc?a=5 | 400 | JSON error |
| /calc?a=abc&b=3 | 400 | JSON error |
| /calc?a=1&b=0&op=div | 400 | JSON error |
| /calc?a=1&b=2&op=bad | 400 | JSON error |

## Bài 10 — API tiện ích

```powershell
curl.exe -i http://127.0.0.1:8000/api/time
curl.exe -i "http://127.0.0.1:8000/api/random?min=1&max=100&count=3"
curl.exe -i "http://127.0.0.1:8000/api/random?min=10&max=1"
curl.exe -i "http://127.0.0.1:8000/api/random?count=101"
```

/api/time trả iso, date, time, weekday (giờ Việt Nam UTC+7). Random mặc
định min=1, max=100, count=1. Count phải 1–100, min không quá max,
tham số phải nguyên; sai trả 400 JSON. Tiếng Việt có dấu.

## Bài 11 — Rút gọn link

- /links: 4 link flask, python, github, osi (200).
- /go/flask và /go/FLASK: 302, cùng Location.
- /go/xyz: 404 tiếng Việt, có liên kết về /links.
- Dùng 302 vì đích của link rút gọn có thể thay đổi; 301 thích hợp cho URL
  chuyển vĩnh viễn và có thể bị cache.

## Bài 12 — Counter

```powershell
curl.exe -i http://127.0.0.1:8000/counter
curl.exe -i -X POST http://127.0.0.1:8000/counter
curl.exe -i -X POST "http://127.0.0.1:8000/counter?step=5"
curl.exe -i -X DELETE http://127.0.0.1:8000/counter
curl.exe -i -X PUT http://127.0.0.1:8000/counter
```

Kết quả HTTP thực tế: GET 200 counter=0; POST 200 counter=1, message
Đã tăng 1; POST step=5 200 counter=6, message Đã tăng 5; DELETE 204,
body rỗng; PUT 405. GET sau reset trả counter=0.

Biến toàn cục mất khi tiến trình khởi động lại, không đồng bộ giữa nhiều
worker, có nguy cơ cập nhật cạnh tranh, không phân biệt người dùng. Ứng dụng
thật cần nơi lưu trạng thái dùng chung và cập nhật nguyên tử, như cơ sở dữ liệu.

## Bài 13 — Context trong Flask shell

```powershell
python -m flask --app b06_url_for shell
```

```python
from flask import request, url_for
request.path
# RuntimeError: Working outside of request context.
url_for("about")
# RuntimeError: Unable to build URLs outside an active request without 'SERVER_NAME' configured.

with app.test_request_context("/search?q=flask&page=2", method="POST"):
    print(request.method)
    print(request.path)
    print(request.args.get("page", type=int))
    print(url_for("about"))

# POST
# /search
# 2
# /about
```

Đã chạy và ghi kết quả. Shell có application context, nhưng không có request
context; request cần HTTP request và url_for cần thông tin URL (hoặc cấu
hình SERVER_NAME). test_request_context cung cấp môi trường request mô phỏng,
vì vậy cả hai hoạt động.

## Bài 14 — Sửa 5 lỗi

Đã tái hiện từng nguyên nhân và đối chiếu với bản sửa b14_co_loi.py.

| Lỗi | URL/thời điểm | Thông báo | Nguyên nhân | Sửa |
| --- | --- | --- | --- | --- |
| 1 | Khởi động | AssertionError: View function mapping is overwriting an existing endpoint function: index | 2 hàm index | Đổi hàm thứ hai thành about |
| 2 | / | BuildError: Could not build url for endpoint 'home' | Không có endpoint home | url_for("index") |
| 3 | /post/1 | TypeError: unexpected keyword argument 'id' | Route id khác tham số post_id | Route dùng post_id |
| 4 | /grade/3 | TypeError: view function did not return a valid response | Không return khi score < 5 | return "Không đạt" |
| 5 | POST /contact | 405 Method Not Allowed | Chỉ cho GET | methods=["GET", "POST"] |

```powershell
python -m flask --app b14_co_loi routes
python -m flask --app b14_co_loi run --debug --port 8000
curl.exe -i -X POST http://127.0.0.1:8000/contact
```

Các URL /, /about, /post/1, /grade/3, /contact GET đều 200; POST /contact
200 với Đã gửi liên hệ.

## Lab 3: MiniBlog

Mở từ chuong_03: python -m flask --app miniblog.app run --debug --port 8000.
File miniblog/README.md giải thích chi tiết. Giữ nguyên app.py, sodiem.py,
templates và static cũ; không dùng các template đăng nhập cũ cho MiniBlog mới.

## Kiểm thử tự động

Từ chuong_03:

```powershell
..\.venv\Scripts\python.exe -m unittest -v test_chuong_03
```

Kết quả thực tế: 16 nhóm kiểm thử, tất cả OK (gồm Bài 2–14 trừ Bài 1
khảo sát thủ công, kiểm thử context Bài 13 và 3 nhóm MiniBlog).
Dự án LibraryMS có test riêng.
