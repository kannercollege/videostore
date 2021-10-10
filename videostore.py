import json
import random

from flask import Flask, abort, jsonify, render_template, request

from database_utils import PRODUCTS_DATABASE_FILENAME, setup_databases
from product import Product
from utils import setup_logging

logger = setup_logging()

setup_databases()

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    with PRODUCTS_DATABASE_FILENAME.open("r") as f:
        data = json.load(f)

    highlighted_products = random.sample(
        data["products"], min(2, len(data["products"]))
    )

    return render_template("index.html", highlighted_products=highlighted_products)


@app.route("/products")
def products():
    list_all = (
        "search" not in request.args
        or request.args.get("search", "").replace(" ", "") == ""
    )
    search_term = ""
    if not list_all:
        search_term = request.args["search"].strip()

    with PRODUCTS_DATABASE_FILENAME.open("r") as f:
        data = json.load(f)

    products = [
        Product(
            product["id"],
            product["name"],
            product["price"],
            product["image_filename"],
        )
        for product in data["products"]
        if list_all or search_term.lower() in product["name"].lower()
    ]

    return render_template(
        "products.html",
        products=products,
        is_search=not list_all,
        search_term=search_term,
    )


@app.route("/products/<int:product_id>")
def view_product(product_id):
    with PRODUCTS_DATABASE_FILENAME.open("r") as f:
        data = json.load(f)

    product = next(
        (product for product in data["products"] if product["id"] == product_id), None
    )

    if product is None:
        abort(404)

    return render_template("view_product.html", product=product)


@app.route("/products/<int:product_id>/buy")
def buy_product(product_id):
    abort(501)


@app.route("/api/products")
def api_products():
    with PRODUCTS_DATABASE_FILENAME.open("r") as f:
        data = json.load(f)

    resp_data = {"data": []}

    for product in data["products"]:
        product = Product(
            product["id"],
            product["name"],
            product["price"],
            product["image_filename"],
        )

        resp_data["data"].append(
            {"id": product.id, "name": product.name, "price": product.price}
        )

    return jsonify(resp_data)


@app.route("/api/product")
def api_individual_product():
    if "id" in request.args:
        try:
            product_id = int(request.args["id"])
        except ValueError:
            code = 400
            resp_data = {
                "error": {"code": code, "message": "product id must be an integer"}
            }
            return jsonify(resp_data), code
    else:
        code = 400
        resp_data = {
            "error": {
                "code": code,
                "message": "no product id was specified as parameter",
            }
        }
        return jsonify(resp_data), code

    with PRODUCTS_DATABASE_FILENAME.open("r") as f:
        data = json.load(f)

    match = next(
        (product for product in data["products"] if product["id"] == product_id), None
    )

    resp_data = {"data": []}

    if match:
        product = Product(
            match["id"],
            match["name"],
            match["price"],
            match["image_filename"],
        )

        resp_data["data"].append(
            {"id": product.id, "name": product.name, "price": product.price}
        )

    return jsonify(resp_data)
