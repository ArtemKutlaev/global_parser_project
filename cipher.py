import hashlib
from database import c, db

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

def create_user(login, password):
    #Функция для добавления логинов и хэшированных паролей в базу данных для увеличения количество уровней доступа
    hashed_password = hash_password(password)
    c.execute("INSERT INTO reg_db(login, password) VALUES(?, ?)", (login, hashed_password))
    db.commit()
    
def authenticate_user(login, password):
    login = str(login)
    password = str(password)
    c.execute("SELECT id, password FROM reg_db WHERE login = ?", (login,))
    result = c.fetchone()
    if result:
        user_id = result[0]
        hashed_password_from_db = result[1]
        hashed_password_attempt = hash_password(password)  # Хешируем введенный пароль
        if hashed_password_attempt == hashed_password_from_db:
            return user_id  # Возвращаем ID пользователя
        else:
            return None  # Пароль неверный
    return None #логин неверный





   

