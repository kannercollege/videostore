import flask_login
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from is_safe_url import is_safe_url
from werkzeug.security import check_password_hash, generate_password_hash

from videostore.db import get_db
from videostore.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash("Registered your account successfully.")

                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        if error is None:
            user = User()
            user.id = username
            flask_login.login_user(user)

            next = request.args.get("next")

            if next and not is_safe_url(next, {"127.0.0.1"}):
                return abort(400)

            flash("Logged in successfully.")
            return redirect(next or url_for("store.index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    flask_login.logout_user()

    flash("Logged out successfully.")

    return redirect(url_for("store.index"))


@bp.route("/delete", methods=("POST",))
def delete():
    db = get_db()
    db.execute(
        "DELETE FROM user WHERE username = ?", (flask_login.current_user.get_id(),)
    )

    flask_login.logout_user()

    flash("Deleted your account successfully.")

    return redirect(url_for("store.index"))
