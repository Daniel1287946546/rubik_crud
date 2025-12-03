from fastapi import FastAPI, Request, Form, Depends, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from sqlmodel import Session
from datetime import datetime, date
import os
import shutil

# DB
from database.db import create_tables, get_session

# MODELOS
from models.cube import Cube
from models.competitor import Competitor
from models.tournament import Tournament
from models.competitor_record import CompetitorRecord


# ==================================================
# DB AUTO CREATION
# ==================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📦 Creando tablas...")
    create_tables()
    print("✅ Tablas listas")
    yield
    print("👋 Cerrando aplicación...")


app = FastAPI(
    title="Rubik CRUD 🧊",
    version="1.0",
    lifespan=lifespan
)


# ==================================================
# STATIC + TEMPLATES
# ==================================================
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ==================================================
# HOME
# ==================================================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ==================================================
# CUBES FRONTEND
# ==================================================
@app.get("/cubes", response_class=HTMLResponse)
def cube_list(request: Request, db: Session = Depends(get_session)):
    cubes = db.query(Cube).all()
    return templates.TemplateResponse("cube_list.html", {
        "request": request,
        "cubes": cubes
    })


@app.get("/cubes/new", response_class=HTMLResponse)
def cube_form(request: Request, db: Session = Depends(get_session)):
    tournaments = db.query(Tournament).all()
    return templates.TemplateResponse("cube_form.html", {
        "request": request,
        "tournaments": tournaments,
        "edit_mode": False
    })


@app.post("/cubes/new")
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


@app.get("/cubes/{cube_id}/edit", response_class=HTMLResponse)
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


@app.post("/cubes/{cube_id}/edit")
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


@app.post("/cubes/{cube_id}/delete")
def delete_cube(cube_id: int, db: Session = Depends(get_session)):
    cube = db.get(Cube, cube_id)
    if not cube:
        raise HTTPException(404, "Cubo no encontrado")

    db.delete(cube)
    db.commit()
    return RedirectResponse("/cubes", status_code=302)


# ==================================================
# COMPETITOR FRONTEND
# ==================================================
@app.get("/competitors", response_class=HTMLResponse)
def competitor_list(request: Request, db: Session = Depends(get_session)):
    competitors = db.query(Competitor).all()
    return templates.TemplateResponse("competitor_list.html", {
        "request": request,
        "competitors": competitors
    })


@app.get("/competitors/new", response_class=HTMLResponse)
def competitor_form(request: Request, db: Session = Depends(get_session)):
    cubes = db.query(Cube).all()
    tournaments = db.query(Tournament).all()
    return templates.TemplateResponse("competitor_form.html", {
        "request": request,
        "cubes": cubes,
        "tournaments": tournaments
    })


# ---------- CREAR COMPETIDOR CON IMAGEN ----------
@app.post("/competitors/new")
def create_competitor(
    name: str = Form(...),
    country: str = Form(...),
    average_time: float = Form(...),
    cube_id: str = Form(""),
    tournament_id: str = Form(""),
    image: UploadFile = File(None),
    db: Session = Depends(get_session),
):

    image_path = None

    if image:
        folder = "static/uploads/competitors/"
        os.makedirs(folder, exist_ok=True)
        filename = f"{name.lower().replace(' ','_')}_{image.filename}"
        image_path = folder + filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    comp = Competitor(
        name=name,
        country=country,
        average_time=average_time,
        cube_id=int(cube_id) if cube_id else None,
        tournament_id=int(tournament_id) if tournament_id else None,
        image_url=image_path
    )

    db.add(comp)
    db.commit()
    return RedirectResponse("/competitors", status_code=302)


@app.get("/competitors/{competitor_id}/edit", response_class=HTMLResponse)
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


@app.post("/competitors/{competitor_id}/edit")
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
        folder = "static/uploads/competitors/"
        os.makedirs(folder, exist_ok=True)
        filename = f"{name.lower().replace(' ','_')}_{image.filename}"
        image_path = folder + filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        competitor.image_url = image_path

    db.commit()
    return RedirectResponse("/competitors", status_code=302)


@app.post("/competitors/{competitor_id}/delete")
def delete_competitor(competitor_id: int, db: Session = Depends(get_session)):
    comp = db.get(Competitor, competitor_id)
    if not comp:
        raise HTTPException(404, "Competidor no encontrado")

    db.delete(comp)
    db.commit()
    return RedirectResponse("/competitors", status_code=302)


# ==================================================
# TOURNAMENT FRONTEND
# ==================================================
@app.get("/tournaments", response_class=HTMLResponse)
def tournament_list(request: Request, db: Session = Depends(get_session)):
    tournaments = db.query(Tournament).all()
    return templates.TemplateResponse("tournament_list.html", {
        "request": request,
        "tournaments": tournaments
    })


@app.get("/tournaments/new", response_class=HTMLResponse)
def tournament_form(request: Request):
    return templates.TemplateResponse("tournament_form.html", {"request": request})


@app.post("/tournaments/new")
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


@app.get("/tournaments/{tournament_id}/edit", response_class=HTMLResponse)
def edit_tournament(request: Request, tournament_id: int, db: Session = Depends(get_session)):
    tournament = db.get(Tournament, tournament_id)
    if not tournament:
        raise HTTPException(404, "Torneo no encontrado")

    return templates.TemplateResponse("tournament_edit.html", {
        "request": request,
        "tournament": tournament
    })


@app.post("/tournaments/{tournament_id}/edit")
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


@app.post("/tournaments/{tournament_id}/delete")
def delete_tournament(tournament_id: int, db: Session = Depends(get_session)):
    t = db.get(Tournament, tournament_id)
    if not t:
        raise HTTPException(404, "Torneo no encontrado")

    db.delete(t)
    db.commit()
    return RedirectResponse("/tournaments", status_code=302)


# ==================================================
# RECORDS FRONTEND
# ==================================================
@app.get("/records", response_class=HTMLResponse)
def record_list(request: Request, db: Session = Depends(get_session)):
    records = db.query(CompetitorRecord).all()
    return templates.TemplateResponse("record_list.html", {
        "request": request,
        "records": records
    })


@app.get("/records/new", response_class=HTMLResponse)
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


@app.post("/records/new")
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


@app.get("/records/{record_id}/edit", response_class=HTMLResponse)
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


@app.post("/records/{record_id}/edit")
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


@app.post("/records/{record_id}/delete")
def delete_record(record_id: int, db: Session = Depends(get_session)):
    r = db.get(CompetitorRecord, record_id)
    if not r:
        raise HTTPException(404, "Record no encontrado")

    db.delete(r)
    db.commit()
    return RedirectResponse("/records", status_code=302)












