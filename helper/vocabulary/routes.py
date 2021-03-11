from flask import render_template, request
from helper.vocabulary import bp
from helper.models import Entry


@bp.route("/dictionary")
def dictionary():
    entries = [e.format_entry() for e in Entry.query.all()]
    
    return render_template("vocabulary/dictionary.html", title="Dictionary", entries=entries)
