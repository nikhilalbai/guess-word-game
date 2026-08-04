from datetime import date

from flask import request

from flask import (
    Blueprint,
    render_template
)

from decorators import admin_required

from models import (
    User,
    Game
)

admin = Blueprint("admin", __name__)


@admin.route("/admin")
@admin_required
def dashboard():

    total_users = User.query.count()

    total_games = Game.query.count()

    games_today = Game.query.filter_by(
        game_date=date.today()
    ).count()

    total_wins = Game.query.filter_by(
        won=True
    ).count()

    total_losses = Game.query.filter_by(
        completed=True,
        won=False
    ).count()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_games=total_games,
        games_today=games_today,
        total_wins=total_wins,
        total_losses=total_losses
    )
@admin.route("/admin/users")
@admin_required
def users():

    search = request.args.get("search", "").strip()

    if search:

        users = User.query.filter(
            User.username.ilike(f"%{search}%")
        ).order_by(User.id).all()

    else:

        users = User.query.order_by(
            User.id
        ).all()

    return render_template(
        "admin_users.html",
        users=users,
        search=search
    )
@admin.route("/admin/games")
@admin_required
def games():

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "")

    query = Game.query

    # Search by username
    if search:

        query = query.join(User).filter(
            User.username.ilike(f"%{search}%")
        )

    # Filter by status
    if status == "completed":

        query = query.filter(
            Game.completed == True
        )

    elif status == "active":

        query = query.filter(
            Game.completed == False
        )

    games = query.order_by(
        Game.game_date.desc(),
        Game.id.desc()
    ).all()

    return render_template(
        "admin_games.html",
        games=games,
        search=search,
        status=status
    )