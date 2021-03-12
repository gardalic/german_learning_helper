from flask import render_template, request, url_for, current_app
from helper.vocabulary import bp
from helper.vocabulary.forms import TypeSelectors
from helper.models import Entry

type_set = {"phrase", "misc", "noun"}


@bp.route("/dictionary", methods=["POST", "GET"])
def dictionary():
    form = TypeSelectors()
    sorting = request.args.get("sorting", None, type=str)
    page = request.args.get("page", 1, type=int)

    if form.is_submitted():
        if not form.noun.data:
            type_set.discard("noun")
        else:
            type_set.add("noun")
        if not form.phrase.data:
            type_set.discard("phrase")
        else:
            type_set.add("phrase")
        if not form.misc.data:
            type_set.discard("misc")
        else:
            type_set.add("misc")
        sorting = form.sorting.data
    elif request.method == "GET":
        # Persist form values after next page GET request
        form.noun.data = True if "noun" in type_set else False
        form.phrase.data = True if "phrase" in type_set else False
        form.misc.data = True if "misc" in type_set else False
        form.sorting.data = sorting

    entries = Entry.get_entries(e_type=type_set, lst=False, sorting=sorting).paginate(
        page, current_app.config["DICT_ITEMS_PER_PAGE"], False
    )
    next_url = (
        url_for("vocab.dictionary", sorting=sorting, page=entries.next_num)
        if entries.has_next
        else None
    )
    prev_url = (
        url_for("vocab.dictionary", sorting=sorting, page=entries.prev_num)
        if entries.has_prev
        else None
    )
    first_url = url_for("vocab.dictionary", sorting=sorting, page=1)
    last_url = url_for("vocab.dictionary", sorting=sorting, page=entries.pages)

    form_entries = [e.format_entry() for e in entries.items]

    return render_template(
        "vocabulary/dictionary.html",
        title="Dictionary",
        entries=form_entries,
        next_url=next_url,
        prev_url=prev_url,
        first_url=first_url,
        last_url=last_url,
        form=form,
        sorting=sorting,
    )
