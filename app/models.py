
"""
Contains Databse model classes
"""

from app import db

class Assignment(db.Model):
    """
    Represents an assignment
    """
    id = db.Column(db.Integer, primary_key=True)
    acronym = db.Column(db.String(6), index=True)
    kmom = db.Column(db.String(6), index=True)
    course = db.Column(db.String(25), index=True)
    grade = db.Column(db.String(2), default=None)
    status = db.Column(db.String(20), default='PENDING')
    feedback = db.Column(db.Text, default='')

    def __repr__(self):
        return '<Assignment {}, {}, {}>'.format(self.acronym, self.kmom, self.course)

    def set_status(self, status):
        self.status = status

    def set_grade(self, grade):
        self.grade = grade

    def set_feedback(self, feedback):
        self.feedback = feedback