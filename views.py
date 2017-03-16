from app import app, db
from flask import Blueprint, request, flash, url_for, redirect, render_template
from models.todo import Todo
import datetime

todo = Blueprint('todo', __name__, template_folder='templates')


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
                    due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y").date()
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
    return render_template('form.html')


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
                        due_date = datetime.datetime.strptime(due_date, "%d-%m-%Y").date()
                    except ValueError:
                        flash('Please enter valid date')
                        return render_template('form.html', todo=todo)
                else:
                    due_date = None
                todo.name = title
                todo.due_date = due_date
                db.session.commit()
                return redirect(url_for('show_all'))
        return render_template('form.html', todo=todo)
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
