import json
from pathlib import Path

DATABASES_DIRECTORY = Path("databases/")
PRODUCTS_DATABASE_FILENAME = DATABASES_DIRECTORY / "db_products.json"


def create_products_database(file: Path):
    data = {"products": []}

    with file.open("x") as f:
        json.dump(data, f, indent=4)


def check_products_database(file: Path):
    with file.open("r") as f:
        data = json.load(f)

    assert type(data) == dict
    assert "products" in data
    assert type(data["products"]) == list

    for item in data["products"]:
        assert "id" in item
        assert "name" in item
        assert "price" in item
        assert "image_filename" in item


def create_databases():
    create_products_database(PRODUCTS_DATABASE_FILENAME)


def check_databases():
    check_products_database(PRODUCTS_DATABASE_FILENAME)


def _check():
    check_databases()


def setup_databases():
    try:
        DATABASES_DIRECTORY.mkdir(parents=True)

        create_databases()

        _check()
    except FileExistsError:
        pass
