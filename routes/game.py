import random

from datetime import date

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db

from models import Game, Word
from flask import Blueprint, render_template
from flask_login import login_required

game = Blueprint("game", __name__)

@game.route("/dashboard")
@login_required
def dashboard():

    today = date.today()

    games_today = Game.query.filter_by(
        user_id=current_user.id,
        game_date=today
    ).count()

    return render_template(
        "dashboard.html",
        games_today=games_today
    )
@game.route("/start-game")
@login_required
def start_game():

    today = date.today()

    games_today = Game.query.filter_by(
        user_id=current_user.id,
        game_date=today
    ).count()

    if games_today >= 3:

        flash(
            "You have reached today's limit of 3 games.",
            "danger"
        )

        return redirect(url_for("game.dashboard"))

    words = Word.query.all()

    secret_word = random.choice(words)

    new_game = Game(

        user_id=current_user.id,

        actual_word=secret_word.word
    )

    db.session.add(new_game)

    db.session.commit()
    session["game_id"] = new_game.id

    return render_template(
    "game.html",
    game_id=new_game.id
)