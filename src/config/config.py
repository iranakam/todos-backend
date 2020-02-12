from sqlalchemy.engine.url import URL
import os

config = {
    'development': 'config/development.json',
    'testing': 'config/testing.json',
    'production': 'config/production.json',
}


def configure_app(app):
    name = os.getenv('FLASK_CONFIGURATION', 'development')
    app.config.from_json(config[name])
    app.config.from_pyfile('instance/application.cfg', silent=False)

