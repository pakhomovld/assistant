from fastapi import Request, Form, File, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import SessionLocal, QueryHistory, User
from app.services.token_manager import ensure_valid_iam_token
from app.services.document_handler import retrieve_relevant_parts
from app.services.auth import is_authenticated
from app.config import settings
from langchain_community.llms import YandexGPT
from app.utils import verify_password

templates = Jinja2Templates(directory="app/templates")

current_document_content = ""
current_document_name = "Нет загруженного документа"
yandex_gpt = YandexGPT(iam_token=settings.IAM_TOKEN, folder_id=settings.FOLDER_ID)

def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and verify_password(password, user.password_hash):
        return user
    return None

def register_routes(app):
    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @app.post("/login")
    async def login(request: Request, username: str = Form(...), password: str = Form(...)):
        user = authenticate_user(username, password)
        if user:
            request.session["user"] = user.username
            return RedirectResponse(url="/", status_code=303)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})

    @app.get("/logout")
    async def logout(request: Request):
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        db = SessionLocal()
        history = db.query(QueryHistory).filter(QueryHistory.username == request.session["user"]).all()
        db.close()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "user": request.session.get("user"),
                "history": history,
                "current_document_name": current_document_name,
            }
        )

    @app.post("/ask")
    async def ask(request: Request, question: str = Form(...)):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        current_token = settings.IAM_TOKEN  # Текущий токен из конфигурации
        valid_token = ensure_valid_iam_token(current_token)
        settings.IAM_TOKEN = valid_token
        relevant_content = retrieve_relevant_parts(current_document_content, question)
        prompt = (
            f"Вот релевантный текст из документа: {relevant_content}\n"
            f"Вопрос пользователя: {question}\n"
            f"Ответь на вопрос с учётом текста."
        )

        try:
            response = yandex_gpt.invoke(prompt)
        except Exception as e:
            response = f"Ошибка при запросе: {e}"

        db = SessionLocal()
        new_entry = QueryHistory(username=request.session["user"], question=question, response=response)
        db.add(new_entry)
        db.commit()
        db.close()

        return RedirectResponse(url="/", status_code=303)

    @app.get("/clear-history", response_class=HTMLResponse)
    async def clear_history(request: Request):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        # Очистка истории для текущего пользователя в базе данных
        db = SessionLocal()
        db.query(QueryHistory).filter(QueryHistory.username == request.session["user"]).delete()
        db.commit()
        db.close()

        return RedirectResponse(url="/", status_code=303)

    @app.get("/upload", response_class=HTMLResponse)
    async def upload_page(request: Request):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)
        return templates.TemplateResponse("upload.html", {"request": request})

    @app.post("/upload")
    async def upload_document(request: Request, file: UploadFile = File(...)):
        global current_document_content, current_document_name

        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        # Чтение содержимого загруженного файла
        file_content = await file.read()
        current_document_content = file_content.decode("utf-8")
        current_document_name = file.filename  # Сохранение имени файла

        return RedirectResponse(url="/", status_code=303)

    @app.post("/users")
    async def create_user(username: str, password: str, is_admin: bool = False):
        db = SessionLocal()
        user = User(
            username=username,
            password_hash=hash_password(password),
            is_admin=is_admin
        )
        db.add(user)
        db.commit()
        db.close()
        return {"message": "User created"}
