"""Model Student dengan validasi dan OOP yang lebih baik."""


class Student:
    HIGH_RISK = "HIGH_RISK"
    MEDIUM_RISK = "MEDIUM_RISK"
    LOW_RISK = "LOW_RISK"
    VALID_RISKS = {HIGH_RISK, MEDIUM_RISK, LOW_RISK}

    def __init__(self, student_id, name, score, risk):
        name = (name or "").strip()
        if not name:
            raise ValueError("Nama tidak boleh kosong.")
        if len(name) > 100:
            raise ValueError("Nama maksimal 100 karakter.")
        try:
            score = float(score)
        except (TypeError, ValueError):
            raise ValueError("Score harus berupa angka.")
        if not 0 <= score <= 100:
            raise ValueError("Score harus antara 0-100.")
        if risk not in self.VALID_RISKS:
            raise ValueError(f"Risk tidak valid: {risk}")

        self.student_id = student_id
        self.name = name
        self.score = score
        self.risk = risk

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2], row[3])

    def is_high_risk(self):
        return self.risk == self.HIGH_RISK

    def is_medium_risk(self):
        return self.risk == self.MEDIUM_RISK

    def is_low_risk(self):
        return self.risk == self.LOW_RISK

    def risk_label(self):
        return {
            self.HIGH_RISK: "High",
            self.MEDIUM_RISK: "Medium",
            self.LOW_RISK: "Low",
        }.get(self.risk, self.risk)

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "score": self.score,
            "risk": self.risk,
        }

    def __repr__(self):
        return f"Student(id={self.student_id}, name={self.name!r}, score={self.score}, risk={self.risk})"
