import sqlite3
from abc import ABC, abstractmethod


class SQL_Table(ABC):
    '''Abstraktní třída na správu SQL tabulky'''

    def __init__(self, db):
        self.execute = db.c.execute

    @abstractmethod
    def all(self):
        '''Vrátí všechny záznamy v tabulce.'''
        pass

    @abstractmethod
    def create(self, *args):
        '''Vytvoří nový záznam v tabulce.'''
        pass

    @abstractmethod
    def get(self, uid):
        '''Vrátí záznam s daným identifikátorem.'''
        pass

    @abstractmethod
    def update(self, uid, *args):
        '''Aktualizuje záznam s daným identifikátorem.'''
        pass

    @abstractmethod
    def remove(self, uid):
        '''Smaže daný záznam z tabulky.'''
        pass


class EmployeeManager(SQL_Table):
    '''Třída na správu zaměstnanců v SQL databázi'''

    scheme = '''users (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(255),
        last_name  VARCHAR(255) NOT NULL
    )'''

    def all(self) -> sqlite3.Cursor:
        return self.execute('''
            SELECT id, first_name, last_name FROM users;
        ''')

    def create(self, first_name: str, last_name: str):
        self.execute('''
            INSERT INTO users (first_name,last_name)
            VALUES (?,?);
        ''', (first_name, last_name))

    def get(self, uid: int) -> sqlite3.Cursor:
        return self.execute('''
            SELECT * FROM users WHERE id=?;
        ''', (uid,))

    def update(self, uid: int, first_name: str, last_name: str):
        self.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?
            WHERE id=?
        ''', (first_name, last_name, uid))

    def remove(self, uid: int):
        self.execute('''
            DELETE FROM users WHERE ID=?
        ''', (uid,))


class Database:
    '''Třída implementující komunikaci s SQLite databází'''

    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

        self.employees = EmployeeManager(self)

    def create_schema(self):
        # TODO: create index
        self.c.executescript(f'''
            CREATE TABLE {self.employees.scheme};
        ''')

    def save(self):
        self.conn.commit()

    def quit(self):
        self.save()
        self.conn.close()

    def __del__(self):
        self.quit()
