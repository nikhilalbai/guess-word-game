import random
from utils import check_guess
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

from models import Game, Word, Guess
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

    return redirect(url_for("game.play_game"))
@game.route("/play", methods=["GET", "POST"])
@login_required
def play_game():

    game_id = session.get("game_id")

    if not game_id:
        flash("Please start a new game.", "warning")
        return redirect(url_for("game.dashboard"))

    current_game = Game.query.get(game_id)

    if current_game.completed:
        flash("This game has already finished.", "warning")
        return redirect(url_for("game.dashboard"))
    if not current_game:
        flash("Game not found.", "danger")
        return redirect(url_for("game.dashboard"))

    if request.method == "POST":

        guess_word = request.form["guess"].strip().upper()

        if len(guess_word) != 5 or not guess_word.isalpha():
            flash("Please enter exactly 5 letters.", "danger")
            return redirect(url_for("game.play_game"))

        if len(current_game.guesses) >= 5:
            flash("Maximum 5 guesses reached.", "danger")
            return redirect(url_for("game.dashboard"))
        new_guess = Guess(
            game_id=current_game.id,
            guess_word=guess_word,
            guess_number=len(current_game.guesses) + 1,
            correct=False
        )

        db.session.add(new_guess)
        db.session.commit()
        if guess_word == current_game.actual_word:

            new_guess.correct = True

            current_game.won = True

            current_game.completed = True

            db.session.commit()

            session.pop("game_id", None)

            flash("Congratulations! You guessed the word!", "success")

            return redirect(url_for("game.dashboard"))

            if len(current_game.guesses) >= 5:

                current_game.completed = True

                db.session.commit()

                session.pop("game_id", None)

                flash(
                    f"Better luck next time! The word was {current_game.actual_word}.",
                    "danger"
                )

                return redirect(url_for("game.dashboard"))

    guesses = Guess.query.filter_by(
    game_id=current_game.id
    ).order_by(Guess.guess_number).all()

    guess_results = []

    for guess in guesses:

        colors = check_guess(
            current_game.actual_word,
            guess.guess_word
        )

        guess_results.append({
            "word": guess.guess_word,
            "colors": colors,
            "number": guess.guess_number
        })

    return render_template(
        "game.html",
            guess_results=guess_results
)