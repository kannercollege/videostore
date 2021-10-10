import json
from pathlib import Path

from jsonschema import validate

DATABASES_DIRECTORY = Path("databases/")
PRODUCTS_DATABASE_FILENAME = DATABASES_DIRECTORY / "db_products.json"
PRODUCTS_DATABASE_SCHEMA_FILENAME = DATABASES_DIRECTORY / "db_products_schema.json"


def get_schema(file: Path):
    with file.open("r") as f:
        schema = json.load(f)

    return schema


def validate_json(data, schema_path: Path):
    schema = get_schema(schema_path)

    validate(instance=data, schema=schema)


def create_products_database(file: Path):
    data = {"products": []}

    with file.open("x") as f:
        json.dump(data, f, indent=4)


def check_products_database(file: Path):
    with file.open("r") as f:
        data = json.load(f)

    validate_json(data, PRODUCTS_DATABASE_SCHEMA_FILENAME)


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

    except FileExistsError:
        pass

    _check()
