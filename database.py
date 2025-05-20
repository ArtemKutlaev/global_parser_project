import sqlite3
import time

db = sqlite3.connect('base.db')
c = db.cursor()

def db_init():
    """
    Функция создает таблицы в базе данных. 
    parser_db для хранения новостей.
    reg_db для хранения логинов и паролей для уровней доступа.
    """
    c.execute('''
        CREATE TABLE IF NOT EXISTS parser_db(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank TEXT,
            title TEXT,
            news TEXT,
            data TEXT,
            data_parsing TEXT, 
            time_parsing TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reg_db(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT,
            password TEXT
        )
    ''')
    db.commit()

def clear_database():
    """
    Функция для очистки базы данных parser_db
    """
    c.execute('DELETE FROM parser_db') 
    c.execute('DELETE FROM sqlite_sequence WHERE name="parser_db"')
    db.commit()

def clear_database_reg():
    """
    Функция для очистки базы данных reg_db
    """
    c.execute('DELETE FROM reg_db') 
    c.execute('DELETE FROM sqlite_sequence WHERE name="reg_db"')
    db.commit()
    
def get_gazprombank():
    """
    Функция достает из таблицы parser_db все записи с bank="Газпромбанк"

    Returns:
        Функция возвращает все записи с bank="Газпромбанк"
    """
    db = sqlite3.connect('base.db')
    c = db.cursor()
    c.execute('SELECT * FROM parser_db WHERE bank="Газпромбанк"')
    gazprombank = c.fetchall()
    return gazprombank

def get_rsb():
    """
    Функция достает из таблицы parser_db все записи с bank="Банк Русский Стандарт"

    Returns:
        Функция возвращает все записи с bank="Банк Русский Стандарт"
    """
    db = sqlite3.connect('base.db')
    c = db.cursor()
    c.execute('SELECT * FROM parser_db WHERE bank="Банк Русский Стандарт"')
    rsb = c.fetchall()
    return rsb

def get_all():
    """
    Функция достает из таблицы parser_db все записи

    Returns:
        Функция возвращает все записи
    """
    db = sqlite3.connect('base.db')
    c = db.cursor()
    c.execute('SELECT * FROM parser_db')
    all = c.fetchall()
    return all

    