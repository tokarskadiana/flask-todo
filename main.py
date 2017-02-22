from flask import Flask
from models.todo import Todo


app = Flask(__name__)


@app.route("/")
def list():
    """ Shows list of todo items stored in the database.
    """
    return "Hello World!"


@app.route("/add")
def add():
    """ Creates new todo item
    If the method was GET it should show new item form.
    If the method was POST it shold create and save new todo item.
    """
    return "Add todo"


@app.route("/remove/<todo_id>")
def remove(todo_id):
    """ Removes todo item with selected id from the database """
    return "Remove " + todo_id


@app.route("/toggle/<todo_id>")
def toggle(todo_id):
    """ Toggles the state of todo item """
    return "Toggle " + todo_id

if __name__ == "__main__":
    app.run()