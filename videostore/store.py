import flask_login
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from videostore.db import get_db

bp = Blueprint("store", __name__)


@bp.route("/")
def index():
    db = get_db()
    products = db.execute(
        """
        SELECT id, created, product_name, product_description, price
        FROM product
        ORDER BY created DESC
        """
    ).fetchall()

    return render_template("store/index.html", products=products)


@bp.route("/test")
@flask_login.login_required
def test():
    return "test"


def get_product(id):
    product = (
        get_db()
        .execute(
            "SELECT id, created, product_name, product_description, price"
            " FROM product"
            " WHERE id = ?",
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

    return render_template("store/view.html", product=product)


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
                "INSERT INTO product_order (customer_id, country, city, street, house_number, zip_code, email, full_name, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    user["id"],
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

            return redirect(url_for("store.view", id=id))

    product = get_product(id)

    return render_template("store/buy.html", product=product)


@bp.route("/create", methods=("GET", "POST"))
@flask_login.login_required
def create():
    if not flask_login.current_user.is_admin:
        abort(403)

    if request.method == "POST":
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        price = float(request.form["price"])

        error = None

        if not product_name:
            error = "Product name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.execute(
                "INSERT INTO product (product_name, product_description, price) VALUES (?, ?, ?)",
                (product_name, product_description, price),
            )
            db.commit()

            return redirect(url_for("store.view", id=cursor.lastrowid))

    return render_template("store/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@flask_login.login_required
def update(id):
    if not flask_login.current_user.is_admin:
        abort(403)

    product = get_product(id)

    if request.method == "POST":
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        price = float(request.form["price"])

        error = None

        if not product_name:
            error = "Product name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE product SET product_name = ?, product_description = ?, price = ? WHERE id = ?",
                (product_name, product_description, price, id),
            )
            db.commit()
            return redirect(url_for("store.index"))

    return render_template("store/update.html", product=product)


@bp.route("/<int:id>/delete", methods=("POST",))
@flask_login.login_required
def delete(id):
    if not flask_login.current_user.is_admin:
        abort(403)

    get_product(id)
    db = get_db()
    db.execute("DELETE FROM product WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("store.index"))
