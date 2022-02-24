import aiohttp
from flask import Blueprint, abort, render_template, request

bp = Blueprint("store", __name__)


async def get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                # oracle returns an html page if the id is invalid
                return None
    return data


MOVIES_URL = "https://apex.oracle.com/pls/apex/lkc-ct14/store/movies"


def MOVIE_IMAGE_URL(id):
    return f"https://apex.oracle.com/pls/apex/lkc-ct14/store/images/{id}"


@bp.route("/")
async def index():
    data = await get_data(MOVIES_URL)

    products = data["items"]

    return render_template("store/index.html", products=products[:5])


@bp.route("/all")
async def all():
    data = await get_data(MOVIES_URL)

    products = data["items"]

    return render_template("store/all.html", products=products)


async def get_product(id):
    data = await get_data(MOVIES_URL)

    for product in data["items"]:
        if product["title_id"] == id:
            return product
    abort(404)


async def get_product_image(id):
    data = await get_data(MOVIE_IMAGE_URL(id))

    # returns None if there's no image
    return data.get("image")


@bp.route("/<int:id>/view")
async def view(id):
    product = await get_product(id)
    genres = product["genres"].split(",")

    image_b64 = await get_product_image(id)

    return render_template(
        "store/view.html", product=product, genres=genres, image_b64=image_b64
    )


@bp.route("/search")
async def search():
    search_term = request.args.get("q").lower()

    data = await get_data(MOVIES_URL)

    products = data["items"]

    search_results = [
        product for product in products if search_term in product["title"].lower()
    ]

    return render_template(
        "store/search.html", products=search_results, search_term=search_term
    )
