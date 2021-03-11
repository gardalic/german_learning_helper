from flask import render_template
from helper.main import bp


sections = [
    {"title": "Dictionary", "for_url": "vocab.dictionary"},
]


@bp.route("/")
@bp.route("/index")
def index():
    # Placeholder
    return render_template("index.html", sections=sections)
