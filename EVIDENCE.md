# Evidence UTS — Student Risk Prediction

Branch: `uts-work`

## 1. Menjalankan starter + Web + DB (5%)
```bash
docker compose up -d --build
docker compose ps
# NAME               STATUS
# student-risk-web   Up (0.0.0.0:8080->5000/tcp)
# student-risk-db    Up (5432/tcp)
curl http://localhost:8080/health
# {"status":"ok","db":"up"}
```
Buka: http://localhost:8080, http://localhost:8080/students, http://localhost:8080/api/stats

## 2. Fitur tambahan halaman Web (10%) + multi-bagian (10%) + multi-layer (5%)
- `GET /students/add` form tambah student (templates/add_student.html)
- `POST /students/add` simpan ke DB via program
- `POST /students/<id>/delete` hapus student
- Search nama `?q=` + filter risk `ALL/HIGH/MEDIUM/LOW` di `/students`
- Dashboard `/` : kartu Total/High/Medium/Low/Avg + tabel "Butuh Perhatian"
- `GET /api/stats` JSON (route -> repository -> service -> JSON)
- `GET /health` cek DB untuk Docker

## 3. Class/Method + OOP (5%+5%)
- `Student` (app/models/student.py): konstanta HIGH/MEDIUM/LOW, validasi nama & score 0-100, `from_row`, `is_*_risk`, `risk_label`, `to_dict`
- `RiskService` (app/services/risk_service.py): `predict` 3-tier (LOW>=75, MEDIUM>=55, HIGH<55), `summary` (total, distribusi, %, avg/min/max), `needs_attention`
- `StudentRepository` (app/repositories/student_repository.py): `get_all`, `search`, `add`, `delete` — sentralisasi SQL

## 4. Refactoring (5%)
Sebelum: `app.py:get_students()` campur koneksi DB + mapping + query.
Sesudah: `app.py` hanya orkestrasi; SQL di `StudentRepository`, prediksi di `RiskService`, validasi di `Student`.

## 5. Validasi/error handling (5%)
- Form: nama wajib, score angka 0-100 (400 + flash jika gagal)
- `RiskService.predict` & `Student.__init__` raise ValueError
- `try/except psycopg2.Error` -> halaman error.html 500; handler 404/500
- Filter risk tak dikenal -> flash warning + fallback ALL
- Delete ID tak ada -> flash warning

## 6. Add/update via program (5%)
`repo.add(name, score, risk)` dengan `risk = risk_service.predict(score)`; delete via tombol di tabel.

## 7. Analisis/prediksi baru (10%)
Prediksi 3-tier + `summary` (avg/min/max, %) + `needs_attention` (5 score terendah) + `/api/stats`.

## 8. Git branch + commit (5%+5%)
```bash
git branch          # uts-work
git log --oneline   # 5+ commit bertahap
git status
docker compose ps
```

## 9. Pemeriksaan cepat
```bash
git status; git branch; git log --oneline; docker compose ps
curl -s localhost:8080/health
curl -s localhost:8080/api/stats | head -c 300
```
