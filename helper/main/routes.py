from flask import current_app, render_template, url_for
from helper.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    # Placeholder
    return render_template("index.html")
