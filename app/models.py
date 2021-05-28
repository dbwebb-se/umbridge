
"""
Contains Databse model classes
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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


class User(db.Model):
    """ Represents a system user """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        """ Setter for password """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ Compares given password to the hashed password """ 
        return check_password_hash(self.password_hash, password)



    def __repr__(self):
        return '<User {}, {}>'.format(self.id, self.username)
