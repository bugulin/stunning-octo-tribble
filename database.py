import sqlite3
from gi.repository import GObject


class Database(GObject.GObject):
    '''Třída implementující komunikaci s SQLite databází'''

    _managers = []

    saved = GObject.Property(type=bool, default=True)

    def __init__(self, db_path: str):
        super().__init__()
        self._conn = sqlite3.connect(db_path)

    def create_schemes(self):
        for manager in self._managers:
            self._conn.executescript(
                f'CREATE TABLE {manager.scheme};'
            )

    def register(self, klass):
        manager = klass(self, self._conn.cursor())
        setattr(self, manager.table_name, manager)
        self._managers.append(manager)

    def rollback(self):
        self._conn.rollback()
        self.saved = True

    def save(self):
        self._conn.commit()
        self.saved = True

    def quit(self):
        self._conn.close()
