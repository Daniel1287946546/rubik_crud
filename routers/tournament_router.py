from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database.db import get_session
from models.tournament import Tournament
from datetime import datetime

router = APIRouter(prefix="/tournaments", tags=["tournaments"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def tournament_list(request: Request, db: Session = Depends(get_session)):
    tournaments = db.query(Tournament).all()
    return templates.TemplateResponse("tournament_list.html", {
        "request": request,
        "tournaments": tournaments
    })

@router.get("/new", response_class=HTMLResponse)
def tournament_form(request: Request):
    return templates.TemplateResponse("tournament_form.html", {"request": request})

@router.post("/new")
def create_tournament(
    name: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_session),
):
    t = Tournament(
        name=name,
        location=location,
        date=datetime.strptime(date, "%Y-%m-%d").date()
    )
    db.add(t)
    db.commit()
    return RedirectResponse("/tournaments", status_code=302)

@router.get("/{tournament_id}/edit", response_class=HTMLResponse)
def edit_tournament(request: Request, tournament_id: int, db: Session = Depends(get_session)):
    tournament = db.get(Tournament, tournament_id)
    if not tournament:
        raise HTTPException(404, "Torneo no encontrado")

    return templates.TemplateResponse("tournament_edit.html", {
        "request": request,
        "tournament": tournament
    })

@router.post("/{tournament_id}/edit")
def update_tournament(
    tournament_id: int,
    name: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_session),
):
    tournament = db.get(Tournament, tournament_id)
    if not tournament:
        raise HTTPException(404, "Torneo no encontrado")

    tournament.name = name
    tournament.location = location
    tournament.date = datetime.strptime(date, "%Y-%m-%d").date()

    db.commit()
    return RedirectResponse("/tournaments", status_code=302)

@router.post("/{tournament_id}/delete")
def delete_tournament(tournament_id: int, db: Session = Depends(get_session)):
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(404, "Torneo no encontrado")

    db.delete(t)
    db.commit()
    return RedirectResponse("/tournaments", status_code=302)
