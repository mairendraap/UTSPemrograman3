#!/bin/bash
# Cek UTS — jalankan: ./cek_uts.sh

echo "=== 1. git status: memastikan tidak ada file yang belum di-commit ==="
git status

echo ""
echo "=== 2. git branch: memastikan posisi di branch uts-work ==="
git branch

echo ""
echo "=== 3. git log: menunjukkan commit bertahap yang dapat ditelusuri ==="
git log --oneline -n 7

echo ""
echo "=== 4. docker compose ps: memastikan Web + Database berjalan ==="
docker compose ps

echo ""
echo "=== 5. health check: memastikan Web bisa konek ke Database ==="
curl -s http://localhost:8080/health
echo ""

echo ""
echo "=== 6. api stats: bukti fitur analisis/prediksi berjalan ==="
curl -s http://localhost:8080/api/stats | head -c 400
echo ""

echo ""
echo "=== 7. cek route: memastikan semua halaman bisa diakses (200 = OK) ==="
for p in "/" "/students" "/students/add" "/api/stats" "/health"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080$p")
  echo "$p -> $code"
done

echo ""
echo "=== Selesai. Buka http://localhost:8080 untuk demo ==="
