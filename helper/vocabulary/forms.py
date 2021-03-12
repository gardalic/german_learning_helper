from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class TypeSelectors(FlaskForm):
    """ Form for the noun/phrase/other selectors for the dictionary page. """
    noun = BooleanField("nouns", default=True, false_values="n")
    phrase = BooleanField("phrases", default=True, false_values="n")
    misc = BooleanField("adj/verb/other", default=True, false_values="n")
    submit = SubmitField("Refresh")
