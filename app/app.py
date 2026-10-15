from flask import Flask, render_template, request
from db import get_connection
from models.student import Student
from services.risk_service import RiskService

app = Flask(__name__)
risk_service = RiskService()

def get_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, score, risk FROM students ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Student(row[0], row[1], row[2], row[3])
        for row in rows
    ]

@app.route("/")
def index():
    students = get_students()
    summary = risk_service.summary(students)
    return render_template("index.html", students=students, summary=summary)

@app.route("/students")
def students_page():
    risk = request.args.get("risk", "ALL")
    students = get_students()

    if risk in {"HIGH_RISK", "LOW_RISK"}:
        students = [s for s in students if s.risk == risk]

    return render_template(
        "students.html",
        students=students,
        selected_risk=risk,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
