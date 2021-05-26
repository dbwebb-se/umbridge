
"""
Contains Databse model classes
"""

from app import db

class Submission(db.Model):
    """
    Represents an submission
    """
    id = db.Column(db.Integer, primary_key=True)

    # Student information
    user_id = db.Column(db.Integer, index=True)
    user_acronym = db.Column(db.String(6), index=True)

    # Assignment information
    kmom = db.Column(db.String(6), index=True)
    assignment_id = db.Column(db.Integer, index=True)

    # Course information
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship(
        'Course',
        primaryjoin="Course.id == Submission.course_id",
        backref=db.backref('courses', uselist=False))

    # PG | Ux
    grade = db.Column(db.String(2), default=None)
    feedback = db.Column(db.Text, default=None)

    # submitted | pending_review | graded -> Follows CanvasAPI standards
    workflow_state = db.Column(db.String(15), default='submitted')


    def __repr__(self):
        return '<Assignment {}, {}, {}>'.format(self.user_acronym, self.kmom, self.course.name)


class Course(db.Model):
    """
    Represents a course
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25))
    active = db.Column(db.Integer, index=True, default=1)

    def __repr__(self):
        return '<Course {}, {}, {}>'.format(self.id, self.name, self.active == 1)
