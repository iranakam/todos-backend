import os

from flask import Flask
from flask_cors import CORS

from src.config.config import configure_app
from src.view.api import bp
from src.database import init_db


def create_app():
    app = Flask(__name__)
    CORS(app)
    configure_app(app)
    init_db(app)
    return app


app = create_app()
app.register_blueprint(bp)
