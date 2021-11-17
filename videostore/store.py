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


def get_product(id, check_admin=True):
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
        abort(404, f"Product id {id} doesn't exist.")

    if check_admin and not flask_login.current_user.is_admin:
        abort(403)

    return product


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
            db.execute(
                "INSERT INTO product (product_name, product_description, price) VALUES (?, ?, ?)",
                (product_name, product_description, price),
            )
            db.commit()
            return redirect(url_for("store.index"))

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
