class RiskService:
    def predict(self, score):
        if score >= 60:
            return "LOW_RISK"
        return "HIGH_RISK"

    def summary(self, students):
        total = len(students)
        high_risk = sum(student.is_high_risk() for student in students)
        return {
            "total": total,
            "high_risk": high_risk,
            "low_risk": total - high_risk,
        }
