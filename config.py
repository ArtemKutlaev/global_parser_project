import os
from dotenv import load_dotenv

load_dotenv()
#Получаем Sekret_key для jwt token из файла .env
Sekret_Key = os.getenv("Sekret_Key")