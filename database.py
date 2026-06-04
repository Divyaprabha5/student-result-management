from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(10))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    roll_number = db.Column(db.String(20), unique=True)
    tamil = db.Column(db.Float)
    english = db.Column(db.Float)
    maths = db.Column(db.Float)
    science = db.Column(db.Float)
    social = db.Column(db.Float)

    def total(self):
        return self.tamil + self.english + self.maths + self.science + self.social

    def average(self):
        return self.total() / 5

    def grade(self):
        avg = self.average()
        if avg >= 90: return 'O'
        elif avg >= 80: return 'A+'
        elif avg >= 70: return 'A'
        elif avg >= 60: return 'B+'
        elif avg >= 50: return 'B'
        else: return 'Fail'

    def status(self):
        marks = [self.tamil, self.english, self.maths, self.science, self.social]
        return 'Pass' if all(m >= 35 for m in marks) else 'Fail'