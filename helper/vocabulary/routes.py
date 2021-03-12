from flask import render_template, request, url_for, current_app
from flask.helpers import flash
from werkzeug.utils import redirect
from helper.vocabulary import bp
from helper.vocabulary.forms import TypeSelectors
from helper.models import Entry

type_list = {"phrase", "misc", "noun"}

@bp.route("/dictionary", methods=["POST", "GET"])
def dictionary():
    form = TypeSelectors() #request.form

    page = request.args.get("page", 1, type=int)

    if form.is_submitted():
        if not form.noun.data:
            type_list.discard("noun")
        else: 
            type_list.add("noun")
        if not form.phrase.data:
            type_list.discard("phrase")
        else: 
            type_list.add("phrase")
        if not form.misc.data:
            type_list.discard("misc")
        else: 
            type_list.add("misc")
    # elif request.method == "GET":
    #     form.noun.data = "y" if "noun" in type_list else "n"
    #     form.phrase.data = "y" if "phrase" in type_list else "n"
    #     form.misc.data = "y" if "misc" in type_list else "n"
    
    entries = Entry.get_entries(e_type=type_list,lst=False).paginate(
        page, current_app.config["DICT_ITEMS_PER_PAGE"], False
    )
    next_url = (
        url_for("vocab.dictionary", page=entries.next_num) if entries.has_next else None
    )
    prev_url = (
        url_for("vocab.dictionary", page=entries.prev_num) if entries.has_prev else None
    )
    first_url = url_for("vocab.dictionary", page=1)
    last_url = url_for("vocab.dictionary", page=entries.pages)

    form_entries = [e.format_entry() for e in entries.items]

    return render_template(
        "vocabulary/dictionary.html",
        title="Dictionary",
        entries=form_entries,
        next_url=next_url,
        prev_url=prev_url,
        first_url=first_url,
        last_url=last_url,
        form=form
    )
