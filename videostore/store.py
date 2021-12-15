import flask_login
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from videostore.db import get_db

bp = Blueprint("store", __name__)


@bp.route("/")
def index():
    db = get_db()
    products = db.execute(
        "SELECT * FROM product WHERE product_is_stock_left = 1 ORDER BY created DESC"
    ).fetchall()

    return render_template("store/index.html", products=products[:5])


@bp.route("/all")
def all():
    db = get_db()
    products = db.execute("SELECT * FROM product ORDER BY product_name").fetchall()

    return render_template("store/all.html", products=products)


def get_product(id):
    product = (
        get_db()
        .execute(
            "SELECT * FROM product WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if product is None:
        abort(404)

    return product


@bp.route("/<int:id>/view")
def view(id):
    product = get_product(id)

    db = get_db()
    genres = db.execute(
        """
        SELECT * FROM product_genre
        INNER JOIN genre ON genre.id = product_genre.genre_id
        WHERE product_id = ?
        ORDER BY genre.genre_name
        """,
        (product["id"],),
    ).fetchall()

    return render_template("store/view.html", product=product, genres=genres)


@bp.route("/<int:id>/buy", methods=("GET", "POST"))
@flask_login.login_required
def buy(id):
    if request.method == "POST":
        country = request.form["country"]
        city = request.form["city"]
        street = request.form["street"]
        house_number = request.form["house_number"]
        zip_code = request.form["zip_code"]

        email = request.form["email"]
        full_name = request.form["full_name"]
        phone_number = request.form["phone_number"]

        product_id = request.form["product_id"]

        username = flask_login.current_user.get_id()

        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO product_order (customer_id, product_id, country, city, street, house_number, zip_code, email, full_name, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    user["id"],
                    product_id,
                    country,
                    city,
                    street,
                    house_number,
                    zip_code,
                    email,
                    full_name,
                    phone_number,
                ),
            )
            db.commit()

            flash("Your order has been placed successfully.")
            return redirect(url_for("store.view", id=id))

    product = get_product(id)

    return render_template("store/buy.html", product=product)


@bp.route("/create", methods=("GET", "POST"))
@flask_login.login_required
def create():
    if not flask_login.current_user.is_admin:
        abort(403)

    if request.method == "POST":
        db = get_db()

        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        price = float(request.form["price"])
        product_imdb_id = request.form["imdb_id"]
        is_stock_left = int("is_stock_left" in request.form)

        genres = [
            db.execute("SELECT * FROM genre WHERE id = ?", (id,)).fetchone()
            for id in request.form.getlist("genres")
        ]

        error = None

        if not product_name:
            error = "Product name is required."

        if not product_imdb_id:
            error = "IMDb id is required."

        if None in genres:
            error = "Invalid genre entered."

        if error is None:
            try:
                cursor = db.execute(
                    "INSERT INTO product (product_name, product_description, product_imdb_id, product_is_stock_left, price) VALUES (?, ?, ?, ?, ?)",
                    (
                        product_name,
                        product_description,
                        product_imdb_id,
                        is_stock_left,
                        price,
                    ),
                )
                db.commit()

                for genre in genres:
                    db.execute(
                        "INSERT INTO product_genre (product_id, genre_id) VALUES (?, ?)",
                        (cursor.lastrowid, genre["id"]),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"Product {product_name} already exists, or there was some other error with adding this product."
            else:
                flash("Product created successfully.")
                return redirect(url_for("store.view", id=cursor.lastrowid))

        flash(error)

    db = get_db()
    genres = db.execute("SELECT * FROM genre ORDER BY genre_name").fetchall()

    return render_template("store/create.html", genres=genres)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@flask_login.login_required
def update(id):
    if not flask_login.current_user.is_admin:
        abort(403)

    product = get_product(id)

    if request.method == "POST":
        db = get_db()

        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        price = float(request.form["price"])
        product_imdb_id = request.form["imdb_id"]
        is_stock_left = int("is_stock_left" in request.form)

        genres = [
            db.execute("SELECT * FROM genre WHERE id = ?", (id,)).fetchone()
            for id in request.form.getlist("genres")
        ]

        error = None

        if not product_name:
            error = "Product name is required."

        if not product_imdb_id:
            error = "IMDb id is required."

        if None in genres:
            error = "Invalid genre entered."

        if error is None:
            try:
                db.execute(
                    "UPDATE product SET product_name = ?, product_description = ?, product_imdb_id = ?, product_is_stock_left = ?, price = ? WHERE id = ?",
                    (
                        product_name,
                        product_description,
                        product_imdb_id,
                        is_stock_left,
                        price,
                        id,
                    ),
                )
                db.commit()

                db.execute(
                    "DELETE FROM product_genre WHERE product_id = ?",
                    (id,),
                )

                for genre in genres:
                    db.execute(
                        "INSERT INTO product_genre (product_id, genre_id) VALUES (?, ?)",
                        (id, genre["id"]),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"Product {product_name} already exists, or there was some other error with adding this product."
            else:
                flash("Product updated successfully.")
                return redirect(url_for("store.view", id=id))

        flash(error)

    db = get_db()
    genres = db.execute("SELECT * FROM genre ORDER BY genre_name").fetchall()

    current_genres = [
        genre["id"]
        for genre in db.execute(
            """
            SELECT genre.id
            FROM product_genre
            INNER JOIN genre ON genre.id = product_genre.genre_id
            WHERE product_genre.product_id = ?
            """,
            (id,),
        ).fetchall()
    ]

    return render_template(
        "store/update.html",
        product=product,
        genres=genres,
        current_genres=current_genres,
    )


@bp.route("/<int:id>/delete", methods=("POST",))
@flask_login.login_required
def delete(id):
    if not flask_login.current_user.is_admin:
        abort(403)

    get_product(id)
    db = get_db()
    db.execute("DELETE FROM product WHERE id = ?", (id,))
    db.commit()

    flash("Product deleted successfully.")
    return redirect(url_for("store.index"))


@bp.route("/profile")
@flask_login.login_required
def profile():
    username = flask_login.current_user.get_id()

    db = get_db()
    user = db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()

    orders = db.execute(
        """
        SELECT product.id AS product_id, product.product_name, strftime('%s', product_order.created) AS created
        FROM product_order
        INNER JOIN product ON product.id = product_order.product_id
        WHERE product_order.customer_id = ?
        ORDER BY product_order.created DESC
        """,
        (user["id"],),
    ).fetchall()

    return render_template("store/profile.html", user=user, orders=orders)


@bp.route("/search")
def search():
    search_term = request.args.get("q").lower()

    db = get_db()

    products = db.execute(
        """
        SELECT * FROM product
        WHERE product_name LIKE ?
        ORDER BY created DESC
        """,
        (f"%{search_term}%",),
    ).fetchall()

    return render_template(
        "store/search.html", products=products, search_term=search_term
    )
