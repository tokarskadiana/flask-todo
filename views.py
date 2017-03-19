from app import app, db
from flask import Blueprint, request, flash, url_for, redirect, render_template, make_response, abort
from models.todo import Todo
import datetime
import json

todo = Blueprint('todo', __name__, template_folder='templates')


@app.errorhandler(404)
def abort(e):
    return render_template('404.html'), 404


def get_saved_data(name, reset=False):
    try:
        data = json.loads(request.cookies.get(name))
    except TypeError:
        data = {}
    if reset:
        data = {}
    return data


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
    todo_query = Todo.query.filter(Todo.deleted.is_(False)).order_by(Todo.due_date)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        list_all = todo_query.filter(Todo.due_date.between(start_date, end_date))
        saves = get_saved_data('filter')
    else:
        list_all = todo_query.all()
        saves = get_saved_data('filter', reset=True)
    return render_template('index.html', list_all=list_all, saves=saves)


@app.route('/', methods=['POST'])
def filter():
    try:
        start_date = datetime.datetime.strptime(request.form['start_date'], date_format()).date()
        end_date = datetime.datetime.strptime(request.form['end_date'], date_format()).date()
    except ValueError:
        flash(u'Please enter valid dates', 'error')
        return redirect(url_for('show_all'))
    response = make_response(redirect(url_for('show_all', start_date=start_date, end_date=end_date)))
    data = get_saved_data('filter')
    data.update(dict(request.form.items()))
    response.set_cookie(b'filter', json.dumps(data))
    return response


@app.route("/new", methods=['GET', 'POST'])
def new():
    """ Creates new todo item
    If the method was GET it should show new item form.
    If the method was POST it shold create and save new todo item.
    """
    if request.method == 'POST':
        error = False
        title, due_date = request.form['title'], request.form['due_date']
        if not title:
            flash(u'Please enter the title', 'error')
            error = True
        if due_date:
            try:
                due_date = datetime.datetime.strptime(
                    due_date, date_format()).date()
            except ValueError:
                flash(u'Please enter valid date', 'error')
                error = True
        else:
            due_date = None
        if not error:
            todo = Todo(name=title, due_date=due_date)
            db.session.add(todo)
            db.session.commit()
            flash(u'Record was successfully added', 'success')
            return redirect(url_for('show_all'))
    return render_template('form.html', date_format=date_format())


@app.route("/delete/<todo_id>")
def delete(todo_id):
    """ Removes todo item with selected id from the database """
    todo = Todo.query.get_or_404(todo_id)
    if todo.deleted:
        abort(404)
    todo.deleted = True
    db.session.commit()
    flash(u'Record was successfully deleted', 'success')
    return redirect(url_for('show_all'))


@app.route("/edit/<todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    """ Edits todo item with selected id in the database
    If the method was GET it should show todo item form.
    If the method was POST it shold update todo item in database.
    """
    todo = Todo.query.get_or_404(todo_id)
    if todo.deleted:
        abort(404)
    if request.method == 'POST':
        title, due_date = request.form['title'], request.form['due_date']
        if not title:
            flash(u'Please enter the title', 'error')
        else:
            if due_date:
                try:
                    due_date = datetime.datetime.strptime(
                        due_date, date_format()).date()
                except ValueError:
                    flash(u'Please enter valid date', 'error')
                    return render_template('form.html', todo=todo)
            else:
                due_date = None
            todo.name = title
            todo.due_date = due_date
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('form.html', todo=todo, date_format=date_format())


@app.route("/toggle/<todo_id>")
def toggle(todo_id):
    """ Toggles the state of todo item """
    todo = Todo.query.get_or_404(todo_id)
    if todo.deleted:
        abort(404)
    todo.toggle()
    db.session.commit()
    return redirect(url_for('show_all'))
