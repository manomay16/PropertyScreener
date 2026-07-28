import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from database import get_db
from schemas import PropertyCreate, PropertyUpdate, PropertyOut
import models
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/properties", response_model=PropertyOut)
def create_property(property_data: PropertyCreate, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    new_property = models.Property(session_id=session_id, **property_data.model_dump())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property


@app.get("/properties", response_model=list[PropertyOut])
def list_properties(request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    return db.query(models.Property).filter(models.Property.session_id == session_id).all()


@app.get("/properties/{property_id}", response_model=PropertyOut)
def get_property(property_id: int, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    prop = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.session_id == session_id
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


@app.put("/properties/{property_id}", response_model=PropertyOut)
def update_property(property_id: int, updates: PropertyUpdate, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    prop = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.session_id == session_id
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)

    db.commit()
    db.refresh(prop)
    return prop


@app.delete("/properties/{property_id}")
def delete_property(property_id: int, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    prop = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.session_id == session_id
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    db.delete(prop)
    db.commit()
    return {"detail": "Property deleted"}
