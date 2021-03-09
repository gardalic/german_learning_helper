from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from helper.main import bp as main_bp
    app.register_blueprint(main_bp)

    from helper.vocabulary import bp as vocabulary_bp
    app.register_blueprint(vocabulary_bp, url_prefix="/vocab")

    return app
