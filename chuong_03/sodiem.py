from flask import Flask, jsonify, request, url_for, abort, redirect, Response
import csv, io

app = Flask(__name__)
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001":{"name":"Nguyễn Văn An","lop":"K47A","scores":{"PMMNM":8.5,"CSDL":7.0,"MMT":9.0}},
    "23T1020002":{"name":"Trần Thị Bình","lop":"K47A","scores":{"PMMNM":6.0,"CSDL":5.5,"MMT":7.0}},
    "23T1020003":{"name":"Lê Hoàng Cường","lop":"K47B","scores":{"PMMNM":9.5,"CSDL":9.0}},
    "23T1020004":{"name":"Phạm Minh Dũng","lop":"K47B","scores":{"PMMNM":4.0,"CSDL":3.5,"MMT":5.0}},
    "23T1020005":{"name":"Hoàng Thu Hà","lop":"K47A","scores":{}},
    "23T1020006":{"name":"Võ Quốc Khánh","lop":"K47C","scores":{"PMMNM":7.5,"MMT":8.0}}
}

def diem_tb(scores):
    return sum(scores.values()) / len(scores) if scores else None

def xep_loai(tb):
    if tb is None: return "Chưa có điểm"
    if tb >= 8: return "Giỏi"
    if tb >= 6.5: return "Khá"
    if tb >= 5: return "Trung bình"
    return "Yếu"

@app.route("/")
def home():
    return f"""
    <h1>SỔ ĐIỂM SINH VIÊN</h1>
    <p>Tổng số sinh viên: <b>{len(STUDENTS)}</b></p>
    <p>Tổng số lớp: <b>{len({sv['lop'] for sv in STUDENTS.values()})}</b></p>
    <p><a href="{url_for('students')}">Xem danh sách sinh viên</a></p>
    <p><a href="{url_for('api_students')}">Xem API sinh viên</a></p>
    """

@app.route("/students")
def students():
    lop = request.args.get("lop", "")
    q = request.args.get("q", "").strip()

    ds = {
        mssv: sv for mssv, sv in STUDENTS.items()
        if (not lop or sv["lop"].lower() == lop.lower())
        and (not q or q.casefold() in sv["name"].casefold()
             or q.casefold() in mssv.casefold())
    }

    loc = f'<a href="{url_for("students", q=q)}">Tất cả</a>'
    for l in sorted({sv["lop"] for sv in STUDENTS.values()}):
        loc += f' | <a href="{url_for("students", lop=l, q=q)}">{l}</a>'

    rows = ""
    for mssv, sv in ds.items():
        tb = diem_tb(sv["scores"])
        rows += f"""
        <tr>
            <td><a href="{url_for('detail', mssv=mssv)}">{mssv}</a></td>
            <td>{sv["name"]}</td>
            <td>{sv["lop"]}</td>
            <td>{"—" if tb is None else f"{tb:.2f}"}</td>
            <td>{xep_loai(tb)}</td>
        </tr>
        """

    if not rows:
        rows = '<tr><td colspan="5">Không có sinh viên phù hợp.</td></tr>'

    ketqua = ""
    if q:
        links = "".join(
            f'<li><a href="{url_for("detail", mssv=m)}">{m} - {sv["name"]}</a></li>'
            for m, sv in ds.items()
        )
        ketqua = f'<p>Tìm thấy <b>{len(ds)}</b> kết quả "{q}"</p><ul>{links}</ul>'

    hidden = f'<input type="hidden" name="lop" value="{lop}">' if lop else ""

    return f"""
    <h1>Danh sách sinh viên</h1>

    <form method="GET">
        {hidden}
        <input name="q" value="{q}" placeholder="Nhập họ tên hoặc MSSV">
        <button>Tìm kiếm</button>
    </form>

    {ketqua}

    <p>Lọc theo lớp: {loc}</p>

    <table border="1" cellpadding="8" cellspacing="0">
        <tr>
            <th>MSSV</th><th>Họ tên</th><th>Lớp</th>
            <th>Điểm TB</th><th>Xếp loại</th>
        </tr>
        {rows}
    </table>

    <br><a href="{url_for('home')}">Về trang chủ</a>
    """

@app.route("/students/<mssv>")
def detail(mssv):
    sv = STUDENTS.get(mssv)
    if not sv:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

    tb = diem_tb(sv["scores"])

    rows = "".join(
        f"<tr><td>{mon}</td><td>{diem}</td></tr>"
        for mon, diem in sv["scores"].items()
    ) or '<tr><td colspan="2">Chưa có điểm</td></tr>'

    return f"""
    <h1>Chi tiết sinh viên</h1>

    <p><b>MSSV:</b> {mssv}</p>
    <p><b>Họ tên:</b> {sv["name"]}</p>
    <p><b>Lớp:</b>
        <a href="{url_for('students', lop=sv['lop'])}">{sv["lop"]}</a>
    </p>
    <p><b>Điểm TB:</b> {"Chưa có điểm" if tb is None else f"{tb:.2f}"}</p>
    <p><b>Xếp loại:</b> {xep_loai(tb)}</p>

    <h3>Bảng điểm học phần</h3>

    <table border="1" cellpadding="8" cellspacing="0">
        <tr><th>Học phần</th><th>Điểm</th></tr>
        {rows}
    </table>

    <br>
    <a href="{url_for('download_csv', mssv=mssv)}">Tải bảng điểm CSV</a>

    <p>
        Link rút gọn:
        <a href="{url_for('short_link', mssv=mssv)}">/sv/{mssv}</a>
    </p>

    <a href="{url_for('students')}">Quay lại danh sách</a>
    """

@app.route("/students/<mssv>/csv")
def download_csv(mssv):
    sv = STUDENTS.get(mssv)
    if not sv:
        abort(404)

    f = io.StringIO()
    w = csv.writer(f)

    w.writerow(["MSSV", mssv])
    w.writerow(["Họ tên", sv["name"]])
    w.writerow(["Lớp", sv["lop"]])
    w.writerow([])
    w.writerow(["Học phần", "Điểm"])

    for mon, diem in sv["scores"].items():
        w.writerow([mon, diem])

    tb = diem_tb(sv["scores"])
    w.writerow([])
    w.writerow(["Điểm TB", "" if tb is None else f"{tb:.2f}"])
    w.writerow(["Xếp loại", xep_loai(tb)])

    return Response(
        "\ufeff" + f.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=bang_diem_{mssv}.csv"}
    )

@app.route("/sv/<mssv>")
def short_link(mssv):
    return redirect(url_for("detail", mssv=mssv), code=301)

@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)

if __name__ == "__main__":
    app.run(debug=True, port=8000)