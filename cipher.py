import hashlib
from database import c, db

def hash_password(password):
    """
    Функция хэширует пароль

    Args:
        password (str): Пароль который нужно захэшировать

    Returns:
        str: Возвращает захэшированный пароль
    """
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

def create_user(login, password):
    """
    Функция добавляет в базу данных логин и захэшированный пароль для увеличения количества уровней доступа
    Args:
        login (str): Логин
        password (str): Захэшированный пароль
    """
    hashed_password = hash_password(password)
    c.execute("INSERT INTO reg_db(login, password) VALUES(?, ?)", (login, hashed_password))
    db.commit()
    
def authenticate_user(login, password):
    """
    Функция проверяет есть ли такой логин и пароль в базе данных

    Args:
        login (str): Логин
        password (str):  Захэшированный пароль

    Returns:
        Функция возвращает ID из базы данных если находит такой логин и пароль, либо возвращает None
    """
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





   

