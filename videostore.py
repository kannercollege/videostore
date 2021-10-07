import json
import random

from flask import Flask, abort, render_template

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
    ]

    return render_template("products.html", products=products)


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
