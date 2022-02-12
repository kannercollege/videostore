import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(CURRENCY_SYMBOL="€")

    os.makedirs(app.instance_path, exist_ok=True)

    from . import store

    app.register_blueprint(store.bp)

    return app
