import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


def get_session_id(request: Request) -> str:
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())
    return request.session["session_id"]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/whoami")
def whoami(request: Request):
    session_id = get_session_id(request)
    return {"session_id": session_id}
