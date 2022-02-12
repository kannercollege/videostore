import aiohttp
from flask import Blueprint, abort, render_template, request

bp = Blueprint("store", __name__)


async def get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    return data


@bp.route("/")
async def index():
    data = await get_data("https://apex.oracle.com/pls/apex/lkc-ct14/store/movies")

    products = data["items"]

    return render_template("store/index.html", products=products[:5])


@bp.route("/all")
async def all():
    data = await get_data("https://apex.oracle.com/pls/apex/lkc-ct14/store/movies")

    products = data["items"]

    return render_template("store/all.html", products=products)


async def get_product(id):
    data = await get_data(f"https://apex.oracle.com/pls/apex/lkc-ct14/store/movies")

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

    data = await get_data("https://apex.oracle.com/pls/apex/lkc-ct14/store/movies")

    products = data["items"]

    search_results = [
        product for product in products if search_term in product["title"].lower()
    ]

    return render_template(
        "store/search.html", products=search_results, search_term=search_term
    )
