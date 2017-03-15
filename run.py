from app import app, db
from views import todo

app.register_blueprint(todo)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
