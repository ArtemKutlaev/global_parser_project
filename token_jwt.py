import jwt
import datetime
from config import Sekret_Key

SECRET_KEY = Sekret_Key

# Функция для генерации JWT
def generate_token(user_id, endpoint):
     payload = {
        "user_id": user_id,
        "endpoint": endpoint,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        "iat": datetime.datetime.utcnow(),
    }
     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Функция для проверки JWT
def verify_token(token,  expected_endpoint):
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