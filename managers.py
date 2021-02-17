import sqlite3
from abc import ABC, abstractmethod


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
        pass

    def get(self, uid: int, cols: str='*') -> sqlite3.Cursor:
        '''Vrátí záznam s daným identifikátorem.'''

        return self.execute(
            f'SELECT {cols} FROM {self.table_name} WHERE id=?;',
            (uid,),
        )

    @abstractmethod
    def update(self, uid, **kwargs):
        '''Aktualizuje daný záznam.'''
        pass

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
