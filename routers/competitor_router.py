from fastapi import APIRouter, Request, Form, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database.db import get_session
from models.competitor import Competitor
from models.cube import Cube
from models.tournament import Tournament
from services.cloudinary_service import upload_image
import cloudinary_config # Import to ensure config is loaded

router = APIRouter(prefix="/competitors", tags=["competitors"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def competitor_list(request: Request, db: Session = Depends(get_session)):
    competitors = db.query(Competitor).all()
    return templates.TemplateResponse("competitor_list.html", {
        "request": request,
        "competitors": competitors
    })

@router.get("/new", response_class=HTMLResponse)
def competitor_form(request: Request, db: Session = Depends(get_session)):
    cubes = db.query(Cube).all()
    tournaments = db.query(Tournament).all()
    return templates.TemplateResponse("competitor_form.html", {
        "request": request,
        "cubes": cubes,
        "tournaments": tournaments
    })

@router.post("/new")
def create_competitor(
    name: str = Form(...),
    country: str = Form(...),
    average_time: float = Form(...),
    cube_id: str = Form(""),
    tournament_id: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(get_session),
):
    image_url = None

    if image:
        try:
            image_url = upload_image(image)
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            # Fallback o manejo de error (opcional)

    comp = Competitor(
        name=name,
        country=country,
        average_time=average_time,
        cube_id=int(cube_id) if cube_id else None,
        tournament_id=int(tournament_id) if tournament_id else None,
        image_url=image_url
    )

    db.add(comp)
    db.commit()
    return RedirectResponse("/competitors", status_code=302)

@router.get("/{competitor_id}/edit", response_class=HTMLResponse)
def competitor_edit(request: Request, competitor_id: int, db: Session = Depends(get_session)):
    competitor = db.get(Competitor, competitor_id)
    if not competitor:
        raise HTTPException(404, "Competidor no encontrado")

    cubes = db.query(Cube).all()
    tournaments = db.query(Tournament).all()

    return templates.TemplateResponse("competitor_edit.html", {
        "request": request,
        "competitor": competitor,
        "cubes": cubes,
        "tournaments": tournaments
    })

@router.post("/{competitor_id}/edit")
def update_competitor(
    competitor_id: int,
    name: str = Form(...),
    country: str = Form(...),
    average_time: float = Form(...),
    cube_id: str = Form(""),
    tournament_id: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(get_session),
):
    competitor = db.get(Competitor, competitor_id)
    if not competitor:
        raise HTTPException(404, "Competidor no encontrado")

    competitor.name = name
    competitor.country = country
    competitor.average_time = average_time
    competitor.cube_id = int(cube_id) if cube_id else None
    competitor.tournament_id = int(tournament_id) if tournament_id else None

    if image:
        try:
            competitor.image_url = upload_image(image)
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")

    db.commit()
    return RedirectResponse("/competitors", status_code=302)

@router.post("/{competitor_id}/delete")
def delete_competitor(competitor_id: int, db: Session = Depends(get_session)):
    comp = db.get(Competitor, competitor_id)
    if not comp:
        raise HTTPException(404, "Competidor no encontrado")

    db.delete(comp)
    db.commit()
    return RedirectResponse("/competitors", status_code=302)
