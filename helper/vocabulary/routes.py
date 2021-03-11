from flask import render_template, request, url_for, current_app
from helper.vocabulary import bp
from helper.models import Entry


@bp.route("/dictionary")
def dictionary():
    page = request.args.get("page", 1, type=int)
    entries = Entry.get_entries(lst=False).paginate(
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
    )
