from helper import db
from sqlalchemy import func


class Lesson(db.Model):
    """ Represents the lesson from which the entry came. """

    sequence_id = db.Column(db.Integer)
    # this could be an int, see later
    lesson_id = db.Column(db.String(16), primary_key=True)
    link = db.Column(db.String(128))
    title = db.Column(db.String(128))
    subtitle = db.Column(db.String(128))
    description = db.Column(db.String(512))

    entries = db.relationship("Entry", backref="entries", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Lesson '{self.title}'>"


class Entry(db.Model):
    """ Represents a vocabulary entry (phrase, noun, other). """

    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(512), index=True)
    translation = db.Column(db.String(512))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.lesson_id"))
    e_type = db.Column(db.String(12), index=True)

    # noun specific
    article = db.Column(db.String(3), index=True, default=None)
    plural = db.Column(db.String(128), default=None)

    def __repr__(self) -> str:
        return f"<Entry {self.entry}>"

    def __str__(self) -> str:
        return f"{self.entry}"

    def get_entries( # looks bad, black formatter sugesstion
        self,
        lesson_start=None,
        lesson_end=None,
        e_type=["phrase", "misc", "noun"],
        rand=False,
    ) -> list:  
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
        ).all()
        return entry_list

    def format_entry(self, entry) -> dict:
        """ Returns formatted entry for display. Input should be an Entry object. """
        if isinstance(entry, Entry):
            if entry.e_type == "noun":
                return {
                    "entry": f"{entry.article} {entry.entry}, die {entry.plural}",
                    "translation": entry.translation,
                }
            return {"entry": entry, "translation": entry.translation}
        raise TypeError("Not an <Entry> object")
