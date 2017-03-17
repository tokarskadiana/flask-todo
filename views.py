from app import app, db
from flask import Blueprint, request, flash, url_for, redirect, render_template
from models.todo import Todo
import datetime

todo = Blueprint('todo', __name__, template_folder='templates')


def date_format():
    """
    Detect if browser supports date type of input.
    Returns: str
    """
    browser = request.user_agent.browser
    version = request.user_agent.version and int(
        request.user_agent.version.split('.')[0])
    if browser and version:
        if (browser == 'msie') \
                or (browser == 'firefox') \
                or (browser == 'chrome' and version < 5.0) \
                or (browser == 'opera' and version < 10.62):
                print('dupa')
                return "%d-%m-%Y"
        return "%Y-%m-%d"
    return "%d-%m-%Y"


@app.route("/")
def show_all():
    """ Shows list of todo items stored in the database.
    """
    return render_template('index.html', list_all=Todo.query.order_by(Todo.due_date).all())


@app.route("/new", methods=['GET', 'POST'])
def new():
    """ Creates new todo item
    If the method was GET it should show new item form.
    If the method was POST it shold create and save new todo item.
    """
    if request.method == 'POST':
        title, due_date = request.form['title'], request.form['due_date']
        if not title:
            flash('Please enter the title')
        else:
            if due_date:
                try:
                    due_date = datetime.datetime.strptime(
                        due_date, date_format()).date()
                except ValueError:
                    flash('Please enter valid date')
                    return render_template('form.html')
            else:
                due_date = None
            todo = Todo(title, due_date)
            db.session.add(todo)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('form.html', date_format=date_format())


@app.route("/delete/<todo_id>")
def delete(todo_id):
    """ Removes todo item with selected id from the database """
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Record was successfully deleted')
    else:
        flash('No such todo item')
    return redirect(url_for('show_all'))


@app.route("/edit/<todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    """ Edits todo item with selected id in the database
    If the method was GET it should show todo item form.
    If the method was POST it shold update todo item in database.
    """
    todo = Todo.query.get(todo_id)
    if todo:
        if request.method == 'POST':
            title, due_date = request.form['title'], request.form['due_date']
            if not title:
                flash('Please enter the title')
            else:
                if due_date:
                    try:
                        due_date = datetime.datetime.strptime(
                            due_date, date_format()).date()
                    except ValueError:
                        flash('Please enter valid date')
                        return render_template('form.html', todo=todo)
                else:
                    due_date = None
                todo.name = title
                todo.due_date = due_date
                db.session.commit()
                return redirect(url_for('show_all'))
        return render_template('form.html', todo=todo, date_format=date_format())
    else:
        flash('No such todo item')
        return redirect(url_for('show_all'))


@app.route("/toggle/<todo_id>")
def toggle(todo_id):
    """ Toggles the state of todo item """
    todo = Todo.query.get(todo_id)
    if todo:
        todo.toggle()
        db.session.commit()
    else:
        flash('No such todo item')
    return redirect(url_for('show_all'))
