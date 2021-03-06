from app import db


class Todo(db.Model):
    """ Class representing todo item."""
    id = db.Column('todo_id', db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    due_date = db.Column(db.Date, nullable=True)
    done = db.Column(db.Boolean(), default=False)
    deleted = db.Column(db.Boolean(), default=False)

    def toggle(self):
        """ Toggles item's state """
        self.done = not self.done
