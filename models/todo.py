from app import db


class Todo(db.Model):
    """ Class representing todo item."""
    id = db.Column('todo_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Integer)

    def __init__(self, name, done=0):
        self.name = name
        self.done = bool(done)

    def toggle(self):
        """ Toggles item's state """
        self.done = not self.done
