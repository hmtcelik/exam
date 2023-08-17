from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    answer = db.Column(db.String(100))
    choice1 = db.Column(db.String(100))
    choice2 = db.Column(db.String(100))
    choice3 = db.Column(db.String(100))
    choice4 = db.Column(db.String(100))

    def __repr__(self):
        return "<Question %r>" % self.question


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Exam %r>" % self.name
