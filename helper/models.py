from helper import db
from sqlalchemy import func, desc


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

    @classmethod
    def get_entries(  # looks bad, black formatter sugesstion
        cls,
        lesson_start=None,
        lesson_end=None,
        e_type=["phrase", "misc", "noun"],
        lst=True,
        sorting=None,
    ) -> list:
        """ Returns a list of entries, or query object, not sorted. Can be limited by session or type. """

        beginning = (
            lesson_start
            if lesson_start
            else db.session.query(func.min(Lesson.sequence_id)).first()[0]
        )
        end = (
            lesson_end
            if lesson_end
            else db.session.query(func.max(Lesson.sequence_id)).first()[0]
        )

        # offloaded logic to DB, test if it is better to do it in flask
        entry_obj = cls.query.filter(
            cls.lesson_id >= beginning,
            cls.lesson_id <= end,
            cls.e_type.in_(e_type),
        )
        
        if sorting == "entry asc":
            entry_obj = entry_obj.order_by(cls.entry)
        elif sorting == "entry desc":
            entry_obj = entry_obj.order_by(desc(cls.entry))
        return entry_obj.all() if lst else entry_obj

    def format_entry(self) -> dict:
        """ Returns dict that is entry formatted for display in the dictionary. """
        if self.e_type == "noun":
            return {
                "id": self.id,
                "entry": f"{self.article} {self.entry}, die {self.plural}",
                "translation": self.translation,
                "base": self.entry,
            }
        return {
            "id": self.id,
            "entry": self,
            "translation": self.translation,
            "base": None,
        }
