import sqlite3


class DataBase:

    @classmethod
    def request(cls, query, *args):
        """Makea request to database
           Returns:
                  list(data): list of data for specific query
        """
        conn = sqlite3.connect('data.sqlite')
        cursor = conn.cursor()
        cursor.execute(query, args)
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data

    @classmethod
    def create_db(cls):
        """Creates database table if doesn't exists.
        """
        table = """
        CREATE TABLE IF NOT EXISTS todo
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER
        );
        """
        conn = sqlite3.connect('data.sqlite')
        cursor = conn.cursor()
        cursor.execute(table)
        cursor.close()
