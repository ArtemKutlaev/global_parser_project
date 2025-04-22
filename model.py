from pydantic import BaseModel, Field

class registration_data(BaseModel):
    login: str= Field()
    password: str= Field()