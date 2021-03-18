import json
from helper import db
from helper.models import Lesson, Entry

""" 
One time loading script, could turn it into a feature later. Files are generated 
with github.com/gardalic/dw_vocabulary_scraper script that scrapes DW A1 course.
"""


class LoadLessons:
    def __init__(self, file):
        self.file = file
        self.lessons = []

    def read_lessons(self):
        """ Reads lessons from file and selects the fields that match the model columns. """
        with open(self.file, "r", encoding="utf8") as f:
            lessons_f = json.load(f)
            # print(lessons_f)
            for lesson in lessons_f:
                # print(lesson)
                l = Lesson(
                    sequence_id=lesson["sequence_id"],
                    lesson_id=lesson["lesson_id"],
                    link=lesson["link"],
                    title=lesson["title"],
                    subtitle=lesson["subtitle"],
                    description=lesson["description"],
                )
                self.lessons.append(l)

    def insert_lessons(self):
        db.session.add_all(self.lessons)
        db.session.commit()


class LoadEntries:
    def __init__(self, *file):
        self.files = list(file)
        self.entries = []

    def read_entries(self):
        for file in self.files:
            with open(file, "r", encoding="utf8") as f:
                entries = json.load(f)

                for entry in entries:
                    e = Entry(
                        entry=entry["entry"],
                        translation=entry["translation"],
                        lesson_id=entry["lesson_id"],
                        e_type=entry["e_type"],
                    )
                    if entry["e_type"] == "noun":
                        e.article = entry["article"]
                        e.plural = entry["plural"]
                    self.entries.append(e)

    def insert_entries(self):
        db.session.add_all(self.entries)
        db.session.commit()


if __name__ == "main":
    pass
    # flask shell commands to load scraped files

    # from helper import db
    # from helper.vocabulary.load_from_file import LoadLessons, LoadEntries
    # l = LoadLessons("./helper/vocabulary/initial_load/lessons.json")
    # l.read_lessons()
    # l.insert_lessons()
    # e = LoadEntries("./helper/vocabulary/initial_load/nouns.json", "./helper/vocabulary/initial_load/phrases. json")
    # e.read_entries()
    # e.insert_entries()