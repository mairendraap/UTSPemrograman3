# Starter Pack UTS — Student Risk Prediction Web

Starter project UTS Pemrograman III. Project sudah dapat dijalankan; pengembangan dilakukan pada project ini, bukan membuat project baru.

## Jalankan
```bash
docker compose up -d --build
docker compose ps
```
Buka: http://localhost:8080

Stop:
```bash
docker compose down
```

Hapus volume/database:
```bash
docker compose down -v
```

## Struktur
```text
student-risk-web/
├── app/
│   ├── app.py
│   ├── db.py
│   ├── requirements.txt
│   ├── models/student.py
│   ├── services/risk_service.py
│   ├── templates/base.html
│   ├── templates/index.html
│   ├── templates/students.html
│   └── static/style.css
├── db/init.sql
├── Dockerfile
├── compose.yaml
└── .gitignore
```

Detail task UTS diberikan oleh dosen.
