import uuid
from datetime import datetime

class Habit:
    def __init__(self, name, time, category_id, description, user_id):
        self.name = str(name)
        self.time = time
        self.category_id = category_id
        self.description = description
        self.user_id = user_id
        