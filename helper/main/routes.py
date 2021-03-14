from flask import render_template
from helper.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    # Placeholder
    return render_template("index.html")
