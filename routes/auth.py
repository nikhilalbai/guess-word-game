from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_login import login_user, logout_user, login_required

from extensions import db

from models import User

from forms import RegisterForm
from forms import LoginForm

from validators import (
    is_valid_username,
    is_valid_password
)

auth = Blueprint("auth", __name__)
@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        if not is_valid_username(username):
            flash(
                "Username must contain uppercase and lowercase letters and be at least 5 characters.",
                "danger",
            )
            return render_template("register.html", form=form)

        if not is_valid_password(password):
            flash(
                "Password must contain one letter, one number and one special character.",
                "danger",
            )
            return render_template("register.html", form=form)

        if password != form.confirm_password.data:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", form=form)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.", "danger")
            return render_template("register.html", form=form)

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password=hashed_password,
            role="PLAYER",
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful!", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "register.html",
        form=form,
    )
@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data,
        ):

            login_user(user)

            flash("Login Successful!", "success")

            return redirect(url_for("game.dashboard"))

        flash(
            "Invalid Username or Password",
            "danger",
        )

    return render_template(
        "login.html",
        form=form,
    )
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out successfully.", "success")

    return redirect(url_for("auth.login"))
