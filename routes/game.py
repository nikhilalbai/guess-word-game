from flask import Blueprint, render_template

game = Blueprint("game", __name__)


@game.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")