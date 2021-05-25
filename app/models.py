
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
    grade = db.Column(db.String(2), default=None)
    status = db.Column(db.String(20), default='PENDING')
    feedback = db.Column(db.Text, default=None)

    kmom = db.Column(db.String(6), index=True)
    course = db.Column(db.String(25), index=True)

    # stud_id = db.Column(db.Integer, index=True)
    # kmom = db.Column(db.Integer, index=True)
    # course = db.Column(db.Integer, index=True)


    def __repr__(self):
        return '<Assignment {}, {}, {}>'.format(self.acronym, self.kmom, self.course)


    def update_status_grade_feedback(self, status, grade, feedback):
        self.status = status
        self.grade = grade
        self.feedback = feedback