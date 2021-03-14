from flask import render_template, request, url_for, current_app, redirect
from helper.vocabulary import bp
from helper.vocabulary.forms import TypeSelectors
from helper.models import Entry


@bp.route("/dictionary", methods=["POST", "GET"])
def dictionary():
    form = TypeSelectors()
    args = request.args
    sorting = args.get("sorting", type=str)
    page = args.get("page", 1, type=int)

    noun = args.get("noun", type=str)
    phrase = args.get("phrase", type=str)
    misc = args.get("misc", type=str)

    type_set = []

    if noun == "y":
        type_set.append("noun")
    else:
        noun = "n"
        form.noun.data = False
    if phrase == "y":
        type_set.append("phrase")
    else:
        phrase = "n"
        form.phrase.data = False
    if misc == "y":
        type_set.append("misc")
    else:
        misc = "n"
        form.misc.data = False

    entries = Entry.get_entries(e_type=type_set, lst=False, sorting=sorting).paginate(
        page, current_app.config["DICT_ITEMS_PER_PAGE"], False
    )
    next_url = (
        url_for(
            "vocab.dictionary",
            noun=noun,
            phrase=phrase,
            misc=misc,
            sorting=sorting,
            page=entries.next_num,
        )
        if entries.has_next
        else None
    )
    prev_url = (
        url_for(
            "vocab.dictionary",
            noun=noun,
            phrase=phrase,
            misc=misc,
            sorting=sorting,
            page=entries.prev_num,
        )
        if entries.has_prev
        else None
    )
    first_url = url_for(
        "vocab.dictionary", noun=noun, phrase=phrase, misc=misc, sorting=sorting, page=1
    )
    last_url = url_for(
        "vocab.dictionary",
        noun=noun,
        phrase=phrase,
        misc=misc,
        sorting=sorting,
        page=entries.pages,
    )

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
        noun=noun,
        phrase=phrase,
        misc=misc,
    )
