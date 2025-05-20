from pydantic import BaseModel, Field

class registration_data(BaseModel):
    """
    Функция нужна для валидации логина и пароля пользователя
    Args:
        BaseModel : для валидации введенных данных
    """
    login: str= Field()
    password: str= Field()