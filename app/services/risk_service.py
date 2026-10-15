"""Layanan prediksi & analisis risiko student."""


class RiskService:
    HIGH_THRESHOLD = 55
    LOW_THRESHOLD = 75

    def predict(self, score):
        """Prediksi 3-tier: LOW (>=75), MEDIUM (>=55), HIGH (<55)."""
        try:
            score = float(score)
        except (TypeError, ValueError):
            raise ValueError("Score harus berupa angka.")
        if not 0 <= score <= 100:
            raise ValueError("Score harus antara 0-100.")
        if score >= self.LOW_THRESHOLD:
            return "LOW_RISK"
        if score >= self.HIGH_THRESHOLD:
            return "MEDIUM_RISK"
        return "HIGH_RISK"

    def summary(self, students):
        total = len(students)
        high = sum(s.is_high_risk() for s in students)
        medium = sum(s.is_medium_risk() for s in students)
        low = total - high - medium
        scores = [s.score for s in students]
        avg = round(sum(scores) / total, 2) if total else 0
        return {
            "total": total,
            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low,
            "high_pct": round(high / total * 100, 1) if total else 0,
            "medium_pct": round(medium / total * 100, 1) if total else 0,
            "low_pct": round(low / total * 100, 1) if total else 0,
            "avg_score": avg,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
        }

    def needs_attention(self, students, limit=5):
        """Fitur analisis baru: daftar student paling butuh perhatian (score terendah)."""
        return sorted(students, key=lambda s: s.score)[:limit]
