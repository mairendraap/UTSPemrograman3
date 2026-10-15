"""Repository: seluruh akses DB students terpusat di sini (refactoring app.py)."""
from db import get_connection
from models.student import Student


class StudentRepository:
    def get_all(self):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name, score, risk FROM students ORDER BY id;")
            rows = cur.fetchall()
            cur.close()
        finally:
            conn.close()
        return [Student.from_row(r) for r in rows]

    def search(self, keyword="", risk="ALL"):
        conn = get_connection()
        try:
            cur = conn.cursor()
            query = "SELECT id, name, score, risk FROM students WHERE 1=1"
            params = []
            if keyword:
                query += " AND name ILIKE %s"
                params.append(f"%{keyword}%")
            if risk in Student.VALID_RISKS:
                query += " AND risk = %s"
                params.append(risk)
            query += " ORDER BY id;"
            cur.execute(query, params)
            rows = cur.fetchall()
            cur.close()
        finally:
            conn.close()
        return [Student.from_row(r) for r in rows]

    def add(self, name, score, risk):
        student = Student(None, name, score, risk)  # validasi di model
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO students (name, score, risk) VALUES (%s, %s, %s) RETURNING id;",
                (student.name, student.score, student.risk),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        finally:
            conn.close()
        student.student_id = new_id
        return student

    def delete(self, student_id):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE id = %s;", (student_id,))
            deleted = cur.rowcount
            conn.commit()
            cur.close()
        finally:
            conn.close()
        return deleted > 0
