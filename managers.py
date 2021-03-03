import sqlite3
from abc import ABC, abstractmethod
from enum import IntEnum


class Manager(ABC):
    '''Abstraktní třída na správu SQL tabulky'''

    table_name = None
    scheme = ''

    def __init__(self, db, cursor):
        def execute(sql, params=(), safe=True):
            if not safe:
                db.saved = False

            return cursor.execute(sql, params)

        self.execute = execute

    def all(self, cols='*') -> sqlite3.Cursor:
        '''Vrátí všechny záznamy v tabulce.'''

        return self.execute('SELECT {} FROM {};'.format(
            cols,
            self.table_name,
        ))

    @abstractmethod
    def create(self, **kwargs):
        '''Vytvoří nový záznam v tabulce.'''

    def get(self, uid: int, cols: str='*') -> sqlite3.Cursor:
        '''Vrátí záznam s daným identifikátorem.'''

        return self.execute(
            f'SELECT {cols} FROM {self.table_name} WHERE id=?;',
            (uid,),
        )

    @abstractmethod
    def update(self, uid, **kwargs):
        '''Aktualizuje daný záznam.'''

    def remove(self, uid: int):
        '''Smaže daný záznam z tabulky.'''

        self.execute(
            f'DELETE FROM {self.table_name} WHERE ID=?',
            (uid,),
            safe=False,
        )


class WorkerManager(Manager):
    '''Třída na správu zaměstnanců v SQL databázi'''

    table_name = 'workers'
    scheme = (
        'workers (\n'
        '    id         INTEGER PRIMARY KEY AUTOINCREMENT,\n'
        '    first_name VARCHAR(255),\n'
        '    last_name  VARCHAR(255) NOT NULL\n'
        ')'
    )

    def create(self, first_name: str, last_name: str) -> int:
        cursor = self.execute(
            'INSERT INTO workers (first_name,last_name) '
            'VALUES (?,?);',
            (first_name, last_name),
            safe=False,
        )

        return cursor.lastrowid

    def update(self, uid: int, first_name: str, last_name: str):
        self.execute(
            'UPDATE workers '
            'SET first_name=?, last_name=? '
            'WHERE id=?',
            (first_name, last_name, uid),
            safe=False,
        )


class EventManager(Manager):
    '''Třída na správu událostí v SQL databázi'''

    table_name = 'events'
    scheme = (
        'events (\n'
        '    id         INTEGER PRIMARY KEY AUTOINCREMENT,\n'
        '    type       INTEGER NOT NULL,\n'
        '    start      DATETIME NOT NULL,\n'
        '    duration   INTEGER NOT NULL,\n'
        '    worker_id  INTEGER NOT NULL,\n'
        '    FOREIGN KEY (worker_id)\n'
        '        REFERENCES workers (id)\n'
        '        ON UPDATE CASCADE\n'
        '        ON DELETE CASCADE\n'
        ')'
    )

    class EventTypes(IntEnum):
        WORK = 1
        VACATION = 2
        SICKNESS = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Kontrola podpory 'foreign_keys' v sqlite (od verze 3.6.19)
        if self.execute('PRAGMA foreign_keys;').fetchone()[0] == 0:
            self.execute('PRAGMA foreign_keys = ON;')
            assert self.execute('PRAGMA foreign_keys;').fetchone()[0] == 1, \
                'nepodporovaná verze SQLite'

    def create(self, typ: EventTypes, start: str, duration: int, worker_id: int) -> int:
        cursor = self.execute(
            'INSERT INTO events (type,start,duration,worker_id) '
            'VALUES (?,?,?,?);',
            (typ, start, duration, worker_id),
            safe=False,
        )

        return cursor.lastrowid

    def update(self, uid: int, typ: int, start: str, duration: int):
        self.execute(
            'UPDATE events '
            'SET type=?, start=?, duration=?'
            'WHERE id=?',
            (typ, start, duration, uid),
            safe=False,
        )

    def select(self, year: int, month: int, cols: str='*') -> sqlite3.Cursor:
        '''Vrátí všechny události v daný měsíc.'''
        year = '{:04d}'.format(year)
        month = '{:02d}'.format(month)

        return self.execute(
            f'SELECT {cols} FROM events '
            'WHERE strftime(\'%Y\', start)=? AND strftime(\'%m\', start)=?;',
            (year, month),
        )
