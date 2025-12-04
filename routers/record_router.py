from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database.db import get_session
from models.competitor_record import CompetitorRecord
from models.competitor import Competitor
from models.cube import Cube
from models.tournament import Tournament
from datetime import date

router = APIRouter(prefix="/records", tags=["records"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def record_list(request: Request, db: Session = Depends(get_session)):
    records = db.query(CompetitorRecord).all()
    return templates.TemplateResponse("record_list.html", {
        "request": request,
        "records": records
    })

@router.get("/new", response_class=HTMLResponse)
def record_form(request: Request, db: Session = Depends(get_session)):
    competitors = db.query(Competitor).all()
    cubes = db.query(Cube).all()
    tournaments = db.query(Tournament).all()
    return templates.TemplateResponse("record_form.html", {
        "request": request,
        "competitors": competitors,
        "cubes": cubes,
        "tournaments": tournaments
    })

@router.post("/new")
def create_record(
    competitor_id: int = Form(...),
    cube_id: int = Form(...),
    record_time: float = Form(...),
    event_type: str = Form(...),
    tournament_id: str = Form(""),
    db: Session = Depends(get_session),
):
    r = CompetitorRecord(
        competitor_id=competitor_id,
        cube_id=cube_id,
        record_time=record_time,
        event_type=event_type,
        record_date=date.today(),
        tournament_id=int(tournament_id) if tournament_id else None
    )
    db.add(r)
    db.commit()
    return RedirectResponse("/records", status_code=302)

@router.get("/{record_id}/edit", response_class=HTMLResponse)
def edit_record(request: Request, record_id: int, db: Session = Depends(get_session)):
    record = db.get(CompetitorRecord, record_id)
    if not record:
        raise HTTPException(404, "Record no encontrado")

    competitors = db.query(Competitor).all()
    cubes = db.query(Cube).all()
    tournaments = db.query(Tournament).all()

    return templates.TemplateResponse("record_edit.html", {
        "request": request,
        "record": record,
        "competitors": competitors,
        "cubes": cubes,
        "tournaments": tournaments
    })

@router.post("/{record_id}/edit")
def update_record(
    record_id: int,
    competitor_id: int = Form(...),
    cube_id: int = Form(...),
    record_time: float = Form(...),
    event_type: str = Form(...),
    tournament_id: str = Form(""),
    db: Session = Depends(get_session),
):
    record = db.get(CompetitorRecord, record_id)
    if not record:
        raise HTTPException(404, "Record no encontrado")

    record.competitor_id = competitor_id
    record.cube_id = cube_id
    record.record_time = record_time
    record.event_type = event_type
    record.tournament_id = int(tournament_id) if tournament_id else None

    db.commit()
    return RedirectResponse("/records", status_code=302)

@router.post("/{record_id}/delete")
def delete_record(record_id: int, db: Session = Depends(get_session)):
    r = db.get(CompetitorRecord, record_id)
    if not r:
        raise HTTPException(404, "Record no encontrado")

    db.delete(r)
    db.commit()
    return RedirectResponse("/records", status_code=302)
