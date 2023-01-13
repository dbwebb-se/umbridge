
"""
Contains Databse model classes
"""

import uuid as uid
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app import db
from app.errors.custom.database import DBCreationError


def rollback_and_log(error):
    """
    Rollback the database and loggs the error.
    Can be used when overriding http-status 500.
    """
    current_app.logger.error(error)
    db.session.rollback()

def format_dict(dic):
    """
    SqlAlchemy (on Linux) can't
    handle string arguments on type int.
    """
    if not dic:
        return {}

    formated_dic = {}
    for k, v in dic.items():
        formated_dic[k] = int(v) if v.isdigit() else v

    return formated_dic

def get_uuid4():
    """ Returns a unique if for feedback view """
    return str(uid.uuid4())


class Submission(db.Model):
    """
    Represents an submission
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(45), default=get_uuid4)

    user_id = db.Column(db.Integer, nullable=False, index=True)
    user_acronym = db.Column(db.String(6), nullable=False)

    assignment_name = db.Column(db.String(9), nullable=False)
    assignment_id = db.Column(db.Integer, nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship(
        'Course',
        primaryjoin="Course.id == Submission.course_id",
        backref=db.backref('courses', uselist=False))

    attempt_nr = db.Column(db.Integer, nullable=False)


    grade = db.Column(db.String(2), default=None)
    feedback = db.Column(db.Text, default=None)
    workflow_state = db.Column(db.String(15), default='new') # new/tested/graded/
    zip_file_path = db.Column(db.String(255), default=None)


    def __repr__(self):
        return '<Assignment {}, {}, {}>'.format(
            self.user_acronym, self.assignment_name, self.course.name)



class Course(db.Model):
    """
    Represents a course
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    active = db.Column(db.Integer, default=1)

    @property
    def serialize(self):
        """ Returns the course as an object """
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
        }

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a course and
        adds it to the database.
        """
        if cls.query.filter_by(id=kwargs.get('id')).first() is not None:
            raise DBCreationError(f'ID {kwargs.get("id")} already exists.')

        course = cls(**kwargs)
        db.session.add(course)
        db.session.commit()
        return course

    def update(self, data):
        """
        Updates a course and
        commits changes to the database.
        """
        self.active = data.get('active') or self.active
        self.name = data.get('name') or self.name
        db.session.commit()
        return self

    def delete(self):
        """
        Deletes a course and
        commits changes to the database.
        """
        db.session.delete(self)
        db.session.commit()
        return self


    def __repr__(self):
        return '<Course {}, {}, Active: {}>'.format(self.id, self.name, self.active == 1)


class User(db.Model):
    """ Represents a system user """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        """ Getter for password """
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        """ Setter for password """
        self.password_hash = generate_password_hash(password)

    def compare_password(self, password):
        """ Compares given password to the hashed password """ 
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)
