from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_gazprombank, get_rsb, get_all

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/gazprombank", response_class=HTMLResponse)
async def gazprombank(request: Request):
    gazprombank = get_gazprombank()
    return templates.TemplateResponse("gazprombank.html", {"request": request,"gazprombank": gazprombank})

@app.get("/rsb", response_class=HTMLResponse)
async def rsb(request: Request):
    rsb = get_rsb()
    return templates.TemplateResponse('rsb.html', {"request":request, "rsb": rsb})

@app.get("/all", response_class=HTMLResponse)
async def all(request: Request):
    all = get_all()
    return templates.TemplateResponse('all.html', {"request":request, "all": all})

@app.get('/', response_class=HTMLResponse)
async def entrance(request:Request):
    return templates.TemplateResponse('entrance.html',{"request":request})