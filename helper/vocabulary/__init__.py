from flask import Blueprint

bp = Blueprint("vocab", __name__)

from helper.vocabulary import routes
