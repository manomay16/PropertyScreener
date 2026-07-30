import os
import uuid
from dotenv import load_dotenv
from schemas import ScoreOut
from calculators import calculate_all_metrics
from risk_scoring import calculate_leverage_risk, calculate_cash_flow_risk, calculate_composite_risk_score
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from database import get_db
from geocoding import geocode_address
from schemas import PropertyCreate, PropertyUpdate, PropertyOut, PropertyWithMetrics
import models
from fastapi.middleware.cors import CORSMiddleware
from calculators import calculate_all_metrics
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

    try:
        geocode_result = geocode_address(property_data.address)
    except Exception:
        raise HTTPException(status_code=502, detail="Could not reach the geocoding service. Please try again.")

    if geocode_result is None:
        raise HTTPException(status_code=400, detail="Could not verify this address. Please check it and try again.")

    new_property = models.Property(
        session_id=session_id,
        census_tract=geocode_result["census_tract"],
        **property_data.model_dump(),
    )
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property


@app.get("/properties", response_model=list[PropertyWithMetrics])
def list_properties(request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    props = db.query(models.Property).filter(models.Property.session_id == session_id).all()
    result = []
    for p in props:
        metrics = calculate_all_metrics(p)
        result.append(PropertyWithMetrics(**PropertyOut.model_validate(p).model_dump(), metrics=metrics))
    return result


@app.get("/properties/{property_id}", response_model=PropertyWithMetrics)
def get_property(property_id: int, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    prop = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.session_id == session_id
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    metrics = calculate_all_metrics(prop)
    return PropertyWithMetrics(**PropertyOut.model_validate(prop).model_dump(), metrics=metrics)


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

@app.post("/properties/{property_id}/score", response_model=ScoreOut)
def create_score(property_id: int, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    prop = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.session_id == session_id
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    fema_data = db.query(models.FemaRisk).filter(
        models.FemaRisk.census_tract == prop.census_tract
    ).first()
    disaster_risk_score = fema_data.risk_score if fema_data else None

    metrics = calculate_all_metrics(prop)
    leverage_risk = calculate_leverage_risk(prop.down_payment, prop.purchase_price)
    cash_flow_risk = calculate_cash_flow_risk(metrics["monthly_cash_flow"], prop.monthly_rental_income)
    composite_score = calculate_composite_risk_score(
        disaster_risk_score,
        metrics["break_even_ratio"],
        leverage_risk,
        cash_flow_risk,
    )

    new_score = models.Score(
        property_id=property_id,
        disaster_risk_score=disaster_risk_score,
        ml_risk_score=composite_score,
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score

@app.get("/properties/{property_id}/scores", response_model=list[ScoreOut])
def list_scores(property_id: int, request: Request, db: Session = Depends(get_db)):
    session_id = get_session_id(request)
    prop = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.session_id == session_id
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    return db.query(models.Score).filter(models.Score.property_id == property_id).all()