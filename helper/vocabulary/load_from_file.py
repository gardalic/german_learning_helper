import json
from helper import db
from helper.models import Lesson, Entry

""" One time loading script, could turn it into a feature later. """
class LoadLessons():
    def __init__(self, file):
        self.file = file
        self.lessons = []
    
    def read_lessons(self):
        """ Reads lessons from file and selects the fields that match the model columns. """
        with open(self.file, "r") as f:
            lessons_f = json.load(f)

            print(lessons_f)
            
            # for lesson in lessons_f:
            #     self.lessons.append({
            #         "sequence_id": lessons_f["sequence_id"],
            #         "lesson_id": lessons_f["lesson_id"],
            #         "title": lessons_f["title"],
            #         "link": lessons_f["link"],
            #         "subtitle": lessons_f["title"],
            #         "link": lessons_f["link"],
            #     })

    def insert_lessons(self):
        db.execute(Lesson.insert(), self.lessons)