from functools import wraps

from flask import (
    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user,
    login_required
)


def admin_required(view):

    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):

        if current_user.role != "ADMIN":

            flash(
                "You are not authorized to access this page.",
                "danger"
            )

            return redirect(
                url_for("game.dashboard")
            )

        return view(*args, **kwargs)

    return wrapped_view