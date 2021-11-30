import flask_login
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from videostore.db import get_db

bp = Blueprint("genres", __name__, url_prefix="/genres")


def get_genre(id):
    genre = (
        get_db()
        .execute(
            "SELECT * FROM genre WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if genre is None:
        abort(404)

    return genre


@bp.route("/")
def index():
    db = get_db()
    genres = db.execute("SELECT * FROM genre ORDER BY created DESC").fetchall()

    return render_template("store/genre/index.html", genres=genres)


@bp.route("/create", methods=("GET", "POST"))
@flask_login.login_required
def create():
    if not flask_login.current_user.is_admin:
        abort(403)

    if request.method == "POST":
        genre_name = request.form["genre_name"]

        error = None

        if not genre_name:
            error = "Genre name is required."

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO genre (genre_name) VALUES (?)",
                    (genre_name,),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Genre {genre_name} already exists."
            else:
                flash("Genre created successfully.")

                return redirect(url_for("genres.index"))

        flash(error)

    return render_template("store/genre/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@flask_login.login_required
def update(id):
    if not flask_login.current_user.is_admin:
        abort(403)

    genre = get_genre(id)

    if request.method == "POST":
        genre_name = request.form["genre_name"]

        error = None

        if not genre_name:
            error = "Genre name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE genre SET genre_name = ? WHERE id = ?",
                (genre_name, id),
            )
            db.commit()

            flash("Genre updated successfully.")
            return redirect(url_for("genres.index"))

    return render_template("store/genre/update.html", genre=genre)


@bp.route("/<int:id>/view")
def view(id):
    genre = get_genre(id)

    db = get_db()
    products = db.execute(
        """
        SELECT * FROM product_genre
        INNER JOIN product ON product.id = product_genre.product_id
        WHERE genre_id = ?
        ORDER BY product.product_name
        """,
        (genre["id"],),
    ).fetchall()

    return render_template("store/genre/view.html", genre=genre, products=products)


@bp.route("/<int:id>/delete", methods=("POST",))
@flask_login.login_required
def delete(id):
    if not flask_login.current_user.is_admin:
        abort(403)

    get_genre(id)
    db = get_db()
    db.execute("DELETE FROM genre WHERE id = ?", (id,))
    db.commit()

    flash("Genre deleted successfully.")
    return redirect(url_for("genres.index"))
