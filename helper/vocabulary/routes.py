from flask import render_template
from helper.vocabulary import bp


@bp.route("/dictionary")
def dictionary():
    return render_template("vocabulary/dictionary.html", title="Dictionary")
