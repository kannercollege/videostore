import os

import flask_login
from flask import Flask

from .db import get_db, init_app
from .user import User


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "videostore.sqlite"),
        ADMIN_USERNAMES=["admin"],
        CURRENCY_SYMBOL="€",
    )

    login_manager = flask_login.LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Log in to access this page."
    login_manager.init_app(app)

    os.makedirs(app.instance_path, exist_ok=True)

    init_app(app)

    from . import auth, store

    app.register_blueprint(auth.bp)
    app.register_blueprint(store.bp)

    @app.login_manager.user_loader
    def user_loader(username):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            return
        else:
            is_admin = user["username"] in app.config["ADMIN_USERNAMES"]

        user = User(is_admin=is_admin)
        user.id = username
        return user

    @app.login_manager.request_loader
    def request_loader(request):
        username = request.form.get("username")

        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            return

        user = User()
        user.id = username
        return user

    return app
