from flask import Blueprint, jsonify, request

from videostore.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api/v1")


@bp.route("/products")
def products():
    param_name = None
    if "name" in request.args:
        param_name = request.args.get("name")

    db = get_db()

    if param_name is not None:
        products = db.execute(
            "SELECT * FROM product WHERE product_name LIKE ? ORDER BY id",
            (f"%{param_name}%",),
        ).fetchall()
    else:
        products = db.execute("SELECT * FROM product ORDER BY id").fetchall()

    data = {"products": []}

    for product in products:
        data["products"].append(
            {
                "id": product["id"],
                "name": product["product_name"],
                "description": product["product_description"],
                "price": product["price"],
            }
        )

    return jsonify(data=data)


@bp.route("/products/<product_id>")
def product(product_id):
    db = get_db()

    the_product = db.execute(
        "SELECT * FROM product WHERE id = ? ORDER BY id",
        (product_id,),
    ).fetchone()

    if the_product is None:
        data = {"status": 404, "message": f"Product with id {product_id} not found."}

        return jsonify(data=data)

    data = {
        "id": the_product["id"],
        "name": the_product["product_name"],
        "description": the_product["product_description"],
        "price": the_product["price"],
    }

    return jsonify(data=data)
