class Student:
    def __init__(self, student_id, name, score, risk):
        self.student_id = student_id
        self.name = name
        self.score = float(score)
        self.risk = risk

    def is_high_risk(self):
        return self.risk == "HIGH_RISK"
