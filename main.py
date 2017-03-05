from flask import Flask, render_template, request, redirect, url_for
from models.todo import Todo
from models.data_base import DataBase

app = Flask(__name__)


@app.route("/")
def list():
    """ Shows list of todo items stored in the database.
    """
    return render_template('index.html', list_all=Todo.get_all())


@app.route("/add", methods=['GET', 'POST'])
def add():
    """ Creates new todo item
    If the method was GET it should show new item form.
    If the method was POST it shold create and save new todo item.
    """
    if request.method == 'POST':
        Todo(None, request.form['title']).save()
        return redirect(url_for('list'))
    return render_template('form.html')


@app.route("/remove/<todo_id>")
def remove(todo_id):
    """ Removes todo item with selected id from the database """
    todo = Todo.get_by_id(todo_id)
    if todo:
        todo.delete()
    return redirect(url_for('list'))


@app.route("/edit/<todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    """ Edits todo item with selected id in the database
    If the method was GET it should show todo item form.
    If the method was POST it shold update todo item in database.
    """
    todo = Todo.get_by_id(todo_id)
    if request.method == 'POST':
        todo.name = request.form['title']
        todo.save()
        return redirect(url_for('list'))
    return render_template('form.html', todo=todo)


@app.route("/toggle/<todo_id>")
def toggle(todo_id):
    """ Toggles the state of todo item """
    todo = Todo.get_by_id(todo_id)
    if todo:
        todo.toggle()
        todo.save()
    return redirect(url_for('list'))

if __name__ == "__main__":
    DataBase.create_db()
    app.run()
