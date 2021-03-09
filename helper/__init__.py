from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)

    from helper.main import bp as main_bp
    app.register_blueprint(main_bp)

    from helper.vocabulary import bp as vocabulary_bp
    app.register_blueprint(vocabulary_bp, url_prefix="/vocab")

    return app
