import aiohttp
from flask import Blueprint, abort, render_template, request

bp = Blueprint("store", __name__)


@bp.route("/")
async def index():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://apex.oracle.com/pls/apex/lkc-ct14/store/movies/"
        ) as response:
            data = await response.json()

    products = data["items"]

    return render_template("store/index.html", products=products[:5])


@bp.route("/all")
async def all():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://apex.oracle.com/pls/apex/lkc-ct14/store/movies/"
        ) as response:
            data = await response.json()

    products = data["items"]

    return render_template("store/all.html", products=products)


async def get_product(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://apex.oracle.com/pls/apex/lkc-ct14/store/movies/"
        ) as response:
            data = await response.json()

    products = data["items"]

    for product in products:
        if product["imdb"] == id:
            return product
    abort(404)


@bp.route("/<id>/view")
async def view(id):
    product = await get_product(id)
    genres = product["genres"].split(",")

    return render_template("store/view.html", product=product, genres=genres)


@bp.route("/search")
async def search():
    search_term = request.args.get("q").lower()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://apex.oracle.com/pls/apex/lkc-ct14/store/movies/"
        ) as response:
            data = await response.json()

    products = data["items"]

    search_results = [
        product for product in products if search_term in product["title"].lower()
    ]

    return render_template(
        "store/search.html", products=search_results, search_term=search_term
    )
