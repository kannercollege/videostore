from flask import Flask, render_template

from database_utils import setup_databases
from utils import setup_logging

logger = setup_logging()

setup_databases()

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/products")
def products():
    return render_template("products.html")
