from fastapi import FastAPI, Request, Form, Depends
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

# Importar routers y DB
from database.db import create_tables, get_session, SessionDep
from routers.cube_router import router as cube_router
from routers.tournament_router import router as tournament_router
from routers.competitor_router import router as competitor_router
from routers.record_router import router as record_router
from models.cube import Cube  # Ajusta según tu modelo

# Lifespan para crear tablas
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Creando tablas si no existen...")
    create_tables()
    print("✅ Tablas listas.")
    yield
    print("👋 Finalizando aplicación...")

# FastAPI app
app = FastAPI(
    title="CRUD Cubo de Rubik 🧩",
    description=(
        "API para gestionar cubos, torneos, competidores y registros de tiempos "
        "de resolución. Desarrollado con FastAPI + SQLModel."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Routers API existentes
app.include_router(cube_router, prefix="/api/cubes", tags=["Cubes"])
app.include_router(tournament_router, prefix="/api/tournaments", tags=["Tournaments"])
app.include_router(competitor_router, prefix="/api/competitors", tags=["Competitors"])
app.include_router(record_router, prefix="/api/records", tags=["Records"])

# Configuración de Jinja2 y static
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------------
# Endpoints HTML / Jinja2
# -------------------------------

# Página principal
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Lista de cubos desde DB
@app.get("/cubes", response_class=HTMLResponse)
def cube_list(request: Request, db: Session = Depends(get_session)):
    cubes = db.query(Cube).all()
    return templates.TemplateResponse("cube_list.html", {"request": request, "cubes": cubes})

# Formulario para crear cubo
@app.get("/cubes/new", response_class=HTMLResponse)
def cube_form(request: Request):
    return templates.TemplateResponse("cube_form.html", {"request": request})

# Procesar formulario para crear cubo
@app.post("/cubes/new", response_class=HTMLResponse)
def create_cube(
    request: Request,
    name: str = Form(...),
    size: str = Form(...),
    db: Session = Depends(get_session)
):
    new_cube = Cube(name=name, size=size)
    db.add(new_cube)
    db.commit()
    db.refresh(new_cube)
    cubes = db.query(Cube).all()
    return templates.TemplateResponse("cube_list.html", {"request": request, "cubes": cubes})













