from helper import db


class Lesson(db.Model):
    """
    Represents the lesson from which the entry came. None type sequence_id and
    lesson_id in case of manual entries.
    """

    sequence_id = db.Column(db.Integer, default=None)
    # this could be an int, see later
    lesson_id = db.Column(db.String(16), primary_key=True)
    title = db.Column(db.String(128))
    link = db.Column(db.String(128))
    subtitle = db.Column(db.String(128))
    description = db.Column(db.String(512))

    def __repr__(self) -> str:
        return f"<Lesson '{self.title}'>"


class Entry(db.Model):
    """ Represents a vocabulary entry (noun, phrase, other). """

    pass
    # entry = db.Column(db.String(256), )