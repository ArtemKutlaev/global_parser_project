from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_gazprombank, get_rsb, get_all
from model import registration_data
from cipher import authenticate_user
from token_jwt import generate_token, verify_token
import jwt

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/gazprombank", response_class=HTMLResponse)
async def gazprombank(request: Request, token : Optional[str] = None):
    """
    Обрабатывает GET запрос к эндпоинту /gazprombank.

    Args:
        request (Request): Объект Request от FastAPI.
        token (Optional[str]): JWT токен для проверки, может отсутствовать.

    Returns:
        HTMLResponse: HTML ответ с данными Газпромбанка или страницей входа.
    """
    if verify_token(token, '/gazprombank') == 3:    
        gazprombank = get_gazprombank()
        return templates.TemplateResponse("gazprombank.html", {"request": request,"gazprombank": gazprombank})
    else:
        return templates.TemplateResponse('entrance.html', {"request":request}) 

@app.get("/rsb", response_class=HTMLResponse)
async def rsb(request: Request, token : Optional[str] = None):
    """
    Обрабатывает GET запрос к эндпоинту /rsb.

    Args:
        request (Request): Объект Request от FastAPI.
        token (Optional[str]): JWT токен для проверки, может отсутствовать.

    Returns:
        HTMLResponse: HTML ответ с данными РСБ или страницей входа.
    """
    if verify_token(token, '/rsb') == 2:
        rsb = get_rsb()
        return templates.TemplateResponse('rsb.html', {"request":request, "rsb": rsb})
    else:
        return templates.TemplateResponse('entrance.html', {"request":request})
    

@app.get("/all", response_class=HTMLResponse)
async def all(request: Request, token : Optional[str] = None):
    """
    Обрабатывает GET запрос к эндпоинту /all.

    Args:
        request (Request): Объект Request от FastAPI.
        token (Optional[str]): JWT токен для проверки, может отсутствовать.

    Returns:
        HTMLResponse: HTML ответ со всеми данными или страницей входа.
    """
    if verify_token(token, '/all') == 1:
        all = get_all()
        return templates.TemplateResponse('all.html', {"request":request, "all": all})
    else:
        return templates.TemplateResponse('entrance.html', {"request":request})

@app.get('/', response_class=HTMLResponse)
async def entrance_post(request:Request):
    """
    Обрабатывает GET запрос к эндпоинту /.

    Args:
        request (Request): Объект Request от FastAPI.

    Returns:
        HTMLResponse: HTML ответ со страницей входа.
    """
    return templates.TemplateResponse('entrance.html',{"request":request})

@app.post('/', response_class=HTMLResponse)
async def entrance_post(request:Request):
    """
    Обрабатывает POST запрос к эндпоинту /.

    Args:
        request (Request): Объект Request от FastAPI.

    Returns:
        HTMLResponse: HTML ответ со страницей входа.
    """
    return templates.TemplateResponse('entrance.html',{"request":request})

@app.post('/register')
async def registration(reg: registration_data):
    """
    Обрабатывает POST запрос к эндпоинту /register для регистрации пользователя.

    Args:
        reg (registration_data): Объект registration_data, содержащий данные для регистрации (логин и пароль).

    Returns:
        dict: Словарь с URL для перенаправления пользователя и JWT токеном, или None, если регистрация не удалась.
    """
    login = reg.login
    password = reg.password
    user_id = authenticate_user(login, password)
    if user_id == 1:
        url = '/all'
        token = generate_token(user_id, "/all")
    elif user_id == 2:
        url = '/rsb'
        token = generate_token(user_id, "/rsb")
    elif user_id == 3:
        url = '/gazprombank'
        token = generate_token(user_id, "/gazprombank")
    else:
        return {'redirect_url': None}
    return {"redirect_url": f"{url}?token={token}"}

@app.post('/parser')
async def change(request : Request):
    """
    Обрабатывает POST запрос к эндпоинту /parser для изменения данных.

    Args:
        request (Request): Объект Request от FastAPI.

    Returns:
        TemplateResponse: HTML ответ с обновленными данными в зависимости от значения параметра 'value'.
    """
    data = await request.json()
    value = data["value"]
    if value == "rsb":
        rsb = get_rsb()
        return templates.TemplateResponse('rsb.html',{ 'request' : request, "rsb": rsb})
    elif value == 'gazprombank':
        gazprombank = get_gazprombank()
        return templates.TemplateResponse("gazprombank.html", {"request": request,"gazprombank": gazprombank})
    else:
        all_banks = get_all()
        return templates.TemplateResponse('all.html', {"request":request, "all": all_banks})
           
    
    

        

    