from flask import render_template, request, url_for, current_app
from helper.dictionary import bp
from helper.models import Entry


@bp.route("/dictionary")
def dictionary():
    args = request.args
    sorting = args.get("srt", type=str)
    page = args.get("page", 1, type=int)

    noun = args.get("noun", type=str)
    phrase = args.get("phrase", type=str)
    misc = args.get("misc", type=str)

    type_set = []

    if noun == "true":
        type_set.append("noun")
    if phrase == "true":
        type_set.append("phrase")
    if misc == "true":
        type_set.append("misc")

    entries = Entry.get_entries(e_type=type_set, lst=False, sorting=sorting).paginate(
        page, current_app.config["DICT_ITEMS_PER_PAGE"], False
    )
    next_url = (
        url_for(
            "dict.dictionary",
            noun=noun,
            phrase=phrase,
            misc=misc,
            srt=sorting,
            page=entries.next_num,
        )
        if entries.has_next
        else None
    )
    prev_url = (
        url_for(
            "dict.dictionary",
            noun=noun,
            phrase=phrase,
            misc=misc,
            srt=sorting,
            page=entries.prev_num,
        )
        if entries.has_prev
        else None
    )
    first_url = url_for(
        "dict.dictionary", noun=noun, phrase=phrase, misc=misc, srt=sorting, page=1
    )
    last_url = url_for(
        "dict.dictionary",
        noun=noun,
        phrase=phrase,
        misc=misc,
        srt=sorting,
        page=entries.pages,
    )

    form_entries = [e.format_entry() for e in entries.items]

    return render_template(
        "dict/dictionary.html",
        title="Dictionary",
        entries=form_entries,
        next_url=next_url,
        prev_url=prev_url,
        first_url=first_url,
        last_url=last_url,
        noun=noun,
        phrase=phrase,
        misc=misc,
        srt=sorting,
    )
