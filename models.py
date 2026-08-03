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
    cascade="all, delete-orphan",
    lazy=True,
    )
class Word(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    word = db.Column(
        db.String(5),
        unique=True,
        nullable=False
    )
from datetime import date

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

    game_date = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    won = db.Column(
        db.Boolean,
        default=False
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    guesses = db.relationship(
        "Guess",
        backref="game",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Game {self.id} - {self.actual_word}>"
from datetime import datetime

class Guess(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("game.id"),
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
        default=False
    )

    guessed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Guess {self.guess_word}>"