from helper import db
from sqlalchemy import func


class Lesson(db.Model):
    """
    Represents the lesson from which the entry came. None type sequence_id and
    lesson_id in case of manual entries.
    """

    sequence_id = db.Column(db.Integer, default=0)
    # this could be an int, see later
    lesson_id = db.Column(db.String(16), primary_key=True)
    title = db.Column(db.String(128))
    link = db.Column(db.String(128))
    subtitle = db.Column(db.String(128))
    description = db.Column(db.String(512))

    entries = db.relationship("Entry", backref="lesson_id", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Lesson '{self.title}'>"


class Entry(db.Model):
    """ Represents a vocabulary entry (phrase, verb, adjective, other). """

    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(512), index=True)
    translation = db.Column(db.String(512))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))
    e_type = db.Column(db.String(12), index=True)

    # noun specific
    article = db.Column(db.String(3), index=True, default=None)
    plural = db.Column(db.String(128), default=None)

    def __repr__(self) -> str:
        return f"<Entry {self.entry}>"

    def get_entries(
        self,
        lesson_start=None,
        lesson_end=None,
        e_type=["phrase", "misc", "noun"],
        rand=False,
    ):  # looks bad, black formatter sugesstion
        """ Returns a list of entries, not sorted. Can be limited by session or type. """

        beginning = (
            lesson_start if lesson_start else Lesson.query(func.max(Lesson.sequence_id))
        )
        end = lesson_end if lesson_end else Lesson.query(func.max(Lesson.sequence_id))

        # offloaded logic to DB, test if it is better to do it in flask
        entry_list = self.query.filter(
            self.lesson_id >= beginning,
            self.lesson_id <= end,
            self.e_type.in_(e_type),
        )
