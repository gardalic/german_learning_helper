from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField
from wtforms.fields.core import SelectField


class TypeSelectors(FlaskForm):
    """ Form for the noun/phrase/other selectors for the dictionary page. """

    noun = BooleanField("nouns", default=True)
    phrase = BooleanField("phrases", default=True)
    misc = BooleanField("adj/verb/other", default=True)
    sorting = SelectField(
        "Sorting",
        choices=[
            (None, None),
            ("entry asc", "entry asc"),
            ("entry desc", "entry desc"),
        ],
    )
    submit = SubmitField("Refresh")
