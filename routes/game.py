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
from models import Game, Word, Guess
from utils import check_guess

game = Blueprint("game", __name__)


# ==========================
# Dashboard
# ==========================

@game.route("/dashboard")
@login_required
def dashboard():

    games_today = Game.query.filter_by(
        user_id=current_user.id,
        game_date=date.today()
    ).count()

    total_games = Game.query.filter_by(
        user_id=current_user.id
    ).count()

    total_wins = Game.query.filter_by(
        user_id=current_user.id,
        won=True
    ).count()

    active_game = Game.query.filter_by(
        user_id=current_user.id,
        completed=False,
        game_date=date.today()
    ).first()

    if active_game:
        status = "🟡 Game In Progress"
        button_text = "Continue Game"
    else:
        status = "🟢 Ready To Play"
        button_text = "Start New Game"

    return render_template(
        "dashboard.html",
        games_today=games_today,
        total_games=total_games,
        total_wins=total_wins,
        status=status,
        button_text=button_text
    )


# ==========================
# Start New Game
# ==========================

@game.route("/start-game")
@login_required
def start_game():

    # Continue today's unfinished game
    active_game = Game.query.filter_by(
        user_id=current_user.id,
        completed=False,
        game_date=date.today()
    ).first()

    if active_game:
        session["game_id"] = active_game.id
        return redirect(url_for("game.play_game"))

    # Daily limit
    games_today = Game.query.filter_by(
        user_id=current_user.id,
        game_date=date.today()
    ).count()

    if games_today >= 3:

        flash(
            "You have reached today's limit of 3 games.",
            "danger"
        )

        return redirect(url_for("game.dashboard"))

    # Pick random word
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


# ==========================
# Play Game
# ==========================

@game.route("/play", methods=["GET", "POST"])
@login_required
def play_game():

    game_id = session.get("game_id")

    if not game_id:

        flash(
            "Please start a game first.",
            "warning"
        )

        return redirect(url_for("game.dashboard"))

    current_game = Game.query.get(game_id)

    if current_game is None:

        session.pop("game_id", None)

        flash(
            "Game not found.",
            "danger"
        )

        return redirect(url_for("game.dashboard"))

    if current_game.completed:

        session.pop("game_id", None)

        flash(
            "This game has already finished.",
            "warning"
        )

        return redirect(url_for("game.dashboard"))

    if request.method == "POST":

        guess_word = request.form["guess"].strip().upper()

        # Validate input
        if len(guess_word) != 5 or not guess_word.isalpha():

            flash(
                "Enter a valid 5-letter word.",
                "danger"
            )

            return redirect(url_for("game.play_game"))

        # Validate dictionary
        valid_word = Word.query.filter_by(
            word=guess_word
        ).first()

        if not valid_word:

            flash(
                "This word is not in our dictionary.",
                "danger"
            )

            return redirect(url_for("game.play_game"))

        # Maximum guesses reached
        if len(current_game.guesses) >= 5:

            flash(
                "Maximum 5 guesses reached.",
                "danger"
            )

            return redirect(url_for("game.dashboard"))

        guess_number = len(current_game.guesses) + 1

        guess = Guess(
            game_id=current_game.id,
            guess_word=guess_word,
            guess_number=guess_number,
            correct=False
        )

        db.session.add(guess)
        db.session.commit()

        # Correct Guess
        if guess_word == current_game.actual_word:

            guess.correct = True
            current_game.won = True
            current_game.completed = True

            db.session.commit()

            session.pop("game_id", None)

            flash(
                "🎉 Congratulations! You guessed the word.",
                "success"
            )

            return redirect(url_for("game.dashboard"))

        # Fifth wrong guess
        if guess_number == 5:

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
    ).order_by(
        Guess.guess_number
    ).all()

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