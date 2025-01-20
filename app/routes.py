from fastapi import Request, Form, File, UploadFile, FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import SessionLocal, QueryHistory, User, UploadedDocument
from app.services.document_handler import retrieve_relevant_parts
from app.services.auth import is_authenticated
from app.config import settings
from langchain_community.llms import YandexGPT
from app.utils import verify_password, hash_password

"""
Routes module for defining API endpoints and application logic.
"""

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

def authenticate_user(username: str, password: str):
    """
    Authenticate a user based on username and password.

    Args:
        username (str): Username provided by the user.
        password (str): Password provided by the user.

    Returns:
        User or None: Authenticated user object or None if authentication fails.
    """
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and verify_password(password, user.password_hash):
        return user
    return None

def register_routes(app: FastAPI):
    """
    Register routes to the FastAPI application instance.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @app.post("/login")
    async def login(request: Request, username: str = Form(...), password: str = Form(...)):
        user = authenticate_user(username, password)
        if user:
            request.session["user"] = user.username
            return RedirectResponse(url="/", status_code=303)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

    @app.get("/logout")
    async def logout(request: Request):
        request.session.clear()
        return RedirectResponse(url="/login", status_code=303)

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        db = SessionLocal()
        history = db.query(QueryHistory).filter(QueryHistory.username == request.session.get("user", "")).all()
        current_document = db.query(UploadedDocument).filter(UploadedDocument.username == request.session.get("user", "Anonymous")).first()
        db.close()

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "user": request.session.get("user"),
                "history": history,
                "current_document_name": current_document.file_name if current_document else "Нет загруженного документа",
                "current_document_content": current_document.content if current_document else "",
            }
        )

    @app.post("/ask")
    async def ask(request: Request, question: str = Form(...)):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        yandex_gpt = YandexGPT(iam_token=settings.IAM_TOKEN, folder_id=settings.FOLDER_ID)
        prompt = f"User's question: {question}\n"

        try:
            response = yandex_gpt.invoke(prompt)
        except Exception as e:
            response = f"Error during request: {e}"

        db = SessionLocal()
        new_entry = QueryHistory(username=request.session.get("user", "Anonymous"), question=question, response=response)
        db.add(new_entry)
        db.commit()
        db.close()

        return RedirectResponse(url="/", status_code=303)

    @app.get("/clear-history", response_class=HTMLResponse)
    async def clear_history(request: Request):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        db = SessionLocal()
        db.query(QueryHistory).filter(QueryHistory.username == request.session.get("user", "")).delete()
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
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        file_content = await file.read()
        db = SessionLocal()
        new_document = UploadedDocument(
            username=request.session.get("user", "Anonymous"),
            file_name=file.filename,
            content=file_content.decode("utf-8")
        )
        db.add(new_document)
        db.commit()
        db.close()

        return RedirectResponse(url="/", status_code=303)

    @app.post("/delete")
    async def delete_document(request: Request):
        if not is_authenticated(request):
            return RedirectResponse(url="/login", status_code=303)

        db = SessionLocal()
        db.query(UploadedDocument).filter(UploadedDocument.username == request.session.get("user", "Anonymous")).delete()
        db.commit()
        db.close()

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
