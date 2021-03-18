from flask import Blueprint

bp = Blueprint("dict", __name__)

from helper.dictionary import routes
