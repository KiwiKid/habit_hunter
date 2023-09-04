import datetime

class Task:
    def __init__(self, name, frequency, priority):
        self.name = name
        self.frequency = frequency
        self.priority = priority
        self.last_changed = None

    def complete(self):
        self.last_changed = datetime.now()
