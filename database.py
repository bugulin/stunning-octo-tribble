import sqlite3
from gi.repository import GObject


class Database(GObject.GObject):
    '''Třída implementující komunikaci s SQLite databází'''

    _managers = []

    saved = GObject.Property(type=bool, default=True)

    def __init__(self, db_path: str):
        super().__init__()
        self._conn = sqlite3.connect(db_path)
        self._conn.set_trace_callback(self.debug)

    def debug(self, statement):
        print('\x1b[1m[s]\x1b[0m', statement)

    def create_schemes(self):
        # TODO: create index
        for manager in self._managers:
            self._conn.executescript(
                f'CREATE TABLE {manager.scheme};'
            )

    def register(self, klass):
        manager = klass(self, self._conn.cursor())
        setattr(self, manager.table_name, manager)
        self._managers.append(manager)

    def save(self):
        self._conn.commit()
        self.saved = True

    def quit(self):
        print('\x1b[1m[d]\x1b[0m', 'Closing db connection')
        self._conn.close()
