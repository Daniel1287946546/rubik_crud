from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database.db import get_session
from models.cube import Cube
from models.tournament import Tournament

router = APIRouter(prefix="/cubes", tags=["cubes"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def cube_list(request: Request, db: Session = Depends(get_session)):
    cubes = db.query(Cube).all()
    return templates.TemplateResponse("cube_list.html", {
        "request": request,
        "cubes": cubes
    })

@router.get("/new", response_class=HTMLResponse)
def cube_form(request: Request, db: Session = Depends(get_session)):
    tournaments = db.query(Tournament).all()
    return templates.TemplateResponse("cube_form.html", {
        "request": request,
        "tournaments": tournaments,
        "edit_mode": False
    })

@router.post("/new")
def create_cube(
    brand: str = Form(...),
    mechanism: str = Form(...),
    pieces: int = Form(...),
    difficulty: str = Form(...),
    is_competition: bool = Form(False),
    world_record: float = Form(...),
    tournament_id: str = Form(""),
    db: Session = Depends(get_session),
):
    cube = Cube(
        brand=brand,
        mechanism=mechanism,
        pieces=pieces,
        difficulty=difficulty,
        is_competition=is_competition,
        world_record=world_record,
        tournament_id=int(tournament_id) if tournament_id else None
    )
    db.add(cube)
    db.commit()
    return RedirectResponse("/cubes", status_code=302)

@router.get("/{cube_id}/edit", response_class=HTMLResponse)
def edit_cube(cube_id: int, request: Request, db: Session = Depends(get_session)):
    cube = db.get(Cube, cube_id)
    if not cube:
        raise HTTPException(404, "Cubo no encontrado")

    tournaments = db.query(Tournament).all()

    return templates.TemplateResponse("cube_form.html", {
        "request": request,
        "cube": cube,
        "tournaments": tournaments,
        "edit_mode": True
    })

@router.post("/{cube_id}/edit")
def update_cube(
    cube_id: int,
    brand: str = Form(...),
    mechanism: str = Form(...),
    pieces: int = Form(...),
    difficulty: str = Form(...),
    is_competition: bool = Form(False),
    world_record: float = Form(...),
    tournament_id: str = Form(""),
    db: Session = Depends(get_session),
):
    cube = db.get(Cube, cube_id)
    if not cube:
        raise HTTPException(404, "Cubo no encontrado")

    cube.brand = brand
    cube.mechanism = mechanism
    cube.pieces = pieces
    cube.difficulty = difficulty
    cube.is_competition = is_competition
    cube.world_record = world_record
    cube.tournament_id = int(tournament_id) if tournament_id else None

    db.commit()
    return RedirectResponse("/cubes", status_code=302)

@router.post("/{cube_id}/delete")
def delete_cube(cube_id: int, db: Session = Depends(get_session)):
    cube = db.get(Cube, cube_id)
    if not cube:
        raise HTTPException(404, "Cubo no encontrado")

    db.delete(cube)
    db.commit()
    return RedirectResponse("/cubes", status_code=302)
