from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )
    games = db.relationship(
    "Game",
    backref="player",
    lazy=True,
    )
class Word(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    word = db.Column(
        db.String(5),
        unique=True,
        nullable=False
    )
class Game(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
    db.Integer,
    db.ForeignKey("user.id"),
    nullable=False
    )

    actual_word = db.Column(
        db.String(5),
        nullable=False
    )

    guess_word = db.Column(
        db.String(5),
        nullable=False
    )

    guess_number = db.Column(
        db.Integer,
        nullable=False
    )

    correct = db.Column(
        db.Boolean,
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )