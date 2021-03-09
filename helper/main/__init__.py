from flask import Blueprint

bp = Blueprint("main", __name__)

from helper.main import routes
