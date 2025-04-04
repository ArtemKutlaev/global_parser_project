import sqlite3
import time

db = sqlite3.connect('base.db')
c = db.cursor()

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
db.commit()

def clear_database():
    #Функция для очистки базы данных.
    c.execute('DELETE FROM parser_db') 
    c.execute('DELETE FROM sqlite_sequence WHERE name="parser_db"')
    db.commit()
    
def get_gazprombank():
    db = sqlite3.connect('base.db')
    c = db.cursor()
    c.execute('SELECT * FROM parser_db WHERE bank="Газпромбанк"')
    time.sleep(2)
    gazprombank = c.fetchall()
    time.sleep(2)
    return gazprombank

def get_rsb():
    db = sqlite3.connect('base.db')
    c = db.cursor()
    c.execute('SELECT * FROM parser_db WHERE bank="Банк Русский Стандарт"')
    time.sleep(2)
    rsb = c.fetchall()
    time.sleep(2)
    return rsb

def get_all():
    db = sqlite3.connect('base.db')
    c = db.cursor()
    c.execute('SELECT * FROM parser_db')
    time.sleep(2)
    all = c.fetchall()
    time.sleep(2)
    return all