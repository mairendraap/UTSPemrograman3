import os
import psycopg2
from flask import Flask, jsonify, redirect, render_template, request, url_for, flash
from models.student import Student
from repositories.student_repository import StudentRepository
from services.risk_service import RiskService

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "uts-secret-key")

risk_service = RiskService()
repo = StudentRepository()


def handle_db_error(e):
    app.logger.exception("Database error: %s", e)
    return render_template("error.html", message=f"Database error: {e}"), 500


@app.route("/")
def index():
    try:
        students = repo.get_all()
    except psycopg2.Error as e:
        return handle_db_error(e)
    summary = risk_service.summary(students)
    attention = risk_service.needs_attention(students)
    return render_template("index.html", students=students, summary=summary, attention=attention)


@app.route("/students")
def students_page():
    risk = request.args.get("risk", "ALL")
    keyword = request.args.get("q", "").strip()
    if risk not in Student.VALID_RISKS and risk != "ALL":
        flash(f"Filter risk tidak dikenal: {risk}. Menampilkan semua.", "warning")
        risk = "ALL"
    try:
        students = repo.search(keyword=keyword, risk=risk)
    except psycopg2.Error as e:
        return handle_db_error(e)
    return render_template(
        "students.html",
        students=students,
        selected_risk=risk,
        keyword=keyword,
    )


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        score_raw = request.form.get("score", "").strip()
        if not name:
            flash("Nama tidak boleh kosong.", "error")
            return render_template("add_student.html", name=name, score=score_raw), 400
        try:
            score = float(score_raw)
        except ValueError:
            flash("Score harus berupa angka 0-100.", "error")
            return render_template("add_student.html", name=name, score=score_raw), 400
        try:
            risk = risk_service.predict(score)
            repo.add(name, score, risk)
        except ValueError as e:
            flash(str(e), "error")
            return render_template("add_student.html", name=name, score=score_raw), 400
        except psycopg2.Error as e:
            return handle_db_error(e)
        flash(f"Student '{name}' ditambahkan dengan prediksi {risk}.", "success")
        return redirect(url_for("students_page"))
    return render_template("add_student.html", name="", score="")


@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    try:
        ok = repo.delete(student_id)
    except psycopg2.Error as e:
        return handle_db_error(e)
    if ok:
        flash(f"Student ID {student_id} dihapus.", "success")
    else:
        flash(f"Student ID {student_id} tidak ditemukan.", "warning")
    return redirect(url_for("students_page"))


@app.route("/api/stats")
def api_stats():
    """Integrasi JSON multi-layer: route -> repository -> service -> JSON."""
    try:
        students = repo.get_all()
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500
    summary = risk_service.summary(students)
    return jsonify({
        **summary,
        "students": [s.to_dict() for s in students],
    })


@app.route("/health")
def health():
    try:
        repo.get_all()
        db = "up"
    except Exception as e:  # noqa: BLE001
        db = f"down: {e}"
    return jsonify({"status": "ok", "db": db})


@app.errorhandler(404)
def not_found(_e):
    return render_template("error.html", message="Halaman tidak ditemukan (404)."), 404


@app.errorhandler(500)
def internal_error(_e):
    return render_template("error.html", message="Terjadi kesalahan server (500)."), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
