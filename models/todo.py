from models.data_base import DataBase


class Todo:
    """ Class representing todo item."""

    def __init__(self, id, name, done=False):
        self.id = id
        self.name = name
        self.done = done

    def toggle(self):
        """ Toggles item's state """
        self.done = not self.done

    def save(self):
        """ Saves/updates todo item in database """
        if self.done:
            done = 1
        else:
            done = 0
        if not self.id:
            query = 'INSERT INTO todo (title, done) VALUES(?, ?)'
            DataBase.request(query, self.name, done)
        query = 'UPDATE todo SET title=?, done=? WHERE id=?'
        DataBase.request(query, self.name, done, self.id)

    def delete(self):
        """ Removes todo item from the database """
        query = 'DELETE FROM todo WHERE id=?'
        DataBase.request(query, self.id)

    @classmethod
    def get_all(cls):
        """ Retrieves all Todos form database and returns them as list.
        Returns:
            list(Todo): list of all todos
        """
        todo_list = []
        query = 'SELECT * FROM todo;'
        data = DataBase.request(query)
        if data:
            for row in data:
                todo_list.append(Todo(row[0], row[1], True if row[2] == 1 else False))
        return todo_list

    @classmethod
    def get_by_id(cls, id):
        """ Retrieves todo item with given id from database.
        Args:
            id(int): item id
        Returns:
            Todo: Todo object with a given id
        """
        query = 'SELECT * FROM todo WHERE id=?'
        data = DataBase.request(query, id)
        if data:
            for row in data:
                return Todo(row[0], row[1], True if row[2] == 1 else False)
        return None
