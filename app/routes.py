from fastapi import Request, Form, File, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import SessionLocal, QueryHistory
from app.services.token_manager import ensure_valid_iam_token
from app.services.document_handler import retrieve_relevant_parts
from app.config import settings
from langchain_community.llms import YandexGPT

templates = Jinja2Templates(directory="app/templates")

current_document_content = ""
current_document_name = "Нет загруженного документа"
yandex_gpt = YandexGPT(iam_token=settings.IAM_TOKEN, folder_id=settings.FOLDER_ID)

def register_routes(app):
    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @app.post("/login")
    async def login(request: Request, username: str = Form(...), password: str = Form(...)):
        # Логика авторизации
        ...

    @app.post("/ask")
    async def ask(request: Request, question: str = Form(...)):
        # Логика обработки вопроса
        ...

