import jwt
import datetime
from config import Sekret_Key

SECRET_KEY = Sekret_Key


def generate_token(user_id, endpoint):
    """
    Функция для генерации JWT токена.

    Args:
        user_id (int): ID пользователя, который будет включен в токен.
        endpoint (str): Эндпоинт, для которого предназначен токен.

    Returns:
        str: JWT токен.
    """
    payload = {
        "user_id": user_id,        
        "endpoint": endpoint,      
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        "iat": datetime.datetime.utcnow(), 
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token,  expected_endpoint):
    """
    Функция для проверки JWT токена.

    Args:
        token (str): JWT токен для проверки.
        expected_endpoint (str): Ожидаемый эндпоинт, для которого предназначен токен.

    Returns:
        int: ID пользователя, если токен действителен, иначе None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["endpoint"] != expected_endpoint:
            return None
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        return None 