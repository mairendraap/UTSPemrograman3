#!/bin/bash
# Demo 2 web + 1 db — jalankan: ./demo_dua_web.sh
# web1 :8080 dan web2 :8081 memakai database yang SAMA (service db).

run() {
  echo "$ $*"
  "$@"
}

echo "=== 1. Nyalakan 2 web + 1 db: dua aplikasi, satu database ==="
run docker compose up -d --build

echo ""
echo "=== 2. Bukti 3 container jalan ==="
run docker compose ps

echo ""
echo "=== 3. Bukti dua-duanya konek ke db yang sama ==="
echo "$ sleep 5 (tunggu web2 selesai start)"
sleep 5
for i in 1 2 3; do
  curl -s --max-time 5 http://localhost:8081/health | grep -q '"db":"up"' && break
  sleep 3
done
run curl -s http://localhost:8080/health
echo ""
run curl -s http://localhost:8081/health
echo ""

echo ""
echo "=== 4. Bukti db-nya sama: tulis via web1, baca via web2 ==="
echo "$ curl -s -X POST -d \"name=Demo2&score=90\" http://localhost:8080/students/add -o /dev/null -w \"%{http_code}\""
curl -s -X POST -d "name=Demo2&score=90" http://localhost:8080/students/add -o /dev/null -w "%{http_code}\n"
echo "$ curl -s \"http://localhost:8081/students?q=Demo2\" | grep -o \"Demo2\" (baca di web2)"
curl -s "http://localhost:8081/students?q=Demo2" | grep -o "Demo2" | head -n 1
echo "$ bandingkan total di dua web (harus sama):"
echo -n "web1 total: "
curl -s http://localhost:8080/api/stats | python3 -c "import json,sys; print(json.load(sys.stdin)['total'])"
echo -n "web2 total: "
curl -s http://localhost:8081/api/stats | python3 -c "import json,sys; print(json.load(sys.stdin)['total'])"

echo ""
echo "=== 5. Bersihkan data demo (hapus via web2, cek hilang di web1) ==="
ID=$(curl -s http://localhost:8081/api/stats | python3 -c "import json,sys; print([s['id'] for s in json.load(sys.stdin)['students'] if s['name']=='Demo2'][0])")
echo "$ curl -s -X POST http://localhost:8081/students/$ID/delete"
curl -s -X POST "http://localhost:8081/students/$ID/delete" -o /dev/null -w "HTTP:%{http_code}\n"
echo -n "web1 total sekarang: "
curl -s http://localhost:8080/api/stats | python3 -c "import json,sys; print(json.load(sys.stdin)['total'])"

echo ""
echo "=== Selesai. web1 http://localhost:8080 | web2 http://localhost:8081 | db: 1 buah ==="
