import sqlite3
from datetime import datetime

class DataBase():
    def __init__(self):
        self._db = sqlite3.connect("items.db")
        self._cursor = self._db.cursor()

        try:
            self._cursor.execute('SELECT * FROM config')
        except:
            self._init_db()

    def _init_db(self):
        self._cursor.execute("CREATE TABLE config (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(50), value VARCHAR(50));")
        self._db.commit()
        self._cursor.execute("CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(50), time_create DATE);")
        self._db.commit()
        self._cursor.execute("CREATE TABLE items_fields (id INTEGER PRIMARY KEY AUTOINCREMENT, id_item INTEGER, title VARCHAR(50), type VARCHAR(50), value VARCHAR(50));")
        self._db.commit()
        self._cursor.execute("CREATE TABLE reports (id INTEGER PRIMARY KEY AUTOINCREMENT, id_item INTEGER, value VARCHAR(50));")
        self._db.commit()
        self._cursor.execute("CREATE TABLE selects (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(50))")
        self._db.commit()
        self._cursor.execute("CREATE TABLE selects_fields (id INTEGER PRIMARY KEY AUTOINCREMENT, id_type INTEGER, value VARCHAR(50));")
        self._db.commit()
        self._cursor.execute("INSERT INTO config (title, value) VALUES ('version', '0.1');")
        self._db.commit()

    
    def get_all_items(self):
        res = []
        query = self._cursor.execute('SELECT * FROM items')
        for item in query:
            res.append(item)
        return res

    def insert_item(self, title, fields):

        self._cursor.execute("INSERT INTO items (title, time_create) VALUES (?, ?)",
                                (title, datetime.now()))
        self._db.commit()
        
        id_item = self._cursor.lastrowid

        for field in fields:
            self._cursor.execute(
                "INSERT INTO items_fields (id_item, title, type, value) VALUES (?, ?, ?, ?)",
                (id_item, field['title'], field['type'], field['val'])
            )
        self._db.commit()
    
    def get_item_by_id(self, id_item):
        query = self._cursor.execute(
            'SELECT id, title FROM items WHERE id=%s' % (id_item)
        )
        item = query.fetchall()[0]

        query = self._cursor.execute(
            'SELECT id, title, type, value FROM items_fields WHERE id_item=%s' % (id_item)
        )

        item_fields = query.fetchall()

        return (item, item_fields)

    def update_item(self, id_item, title, fields):
        self._cursor.execute(
            "UPDATE items SET title='%s' WHERE id=%s" % (title, id_item)
        )

        for field in fields:
            if field['id'] != None:
                self._cursor.execute(
                    "UPDATE items_fields SET title='%s', value='%s', type='%s' WHERE id=%s" \
                        % (field['title'], field['val'], field['type'], field['id'])
                )
            else:
                self._cursor.execute(
                    "INSERT INTO items_fields (id_item, title, type, value) VALUES (?, ?, ?, ?)",
                    (id_item, field['title'], field['type'], field['val'])
                )

        self._db.commit()

    def delete_item(self, id_item):
        self._cursor.execute(
            "DELETE FROM items WHERE id=%s" % (id_item)
        )
        self._cursor.execute(
            "DELETE FROM items_fields WHERE id_item=%s" % (id_item)
        )

        self._db.commit()
