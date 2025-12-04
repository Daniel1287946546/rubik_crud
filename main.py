from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database.db import create_tables
from routers import competitor_router, cube_router, tournament_router, record_router, upload_router

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

# Include Routers
app.include_router(competitor_router.router)
app.include_router(cube_router.router)
app.include_router(tournament_router.router)
app.include_router(record_router.router)
app.include_router(upload_router.router)


# ==================================================
# HOME
# ==================================================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    print("🏠 Accessing Home Page")
    return templates.TemplateResponse("index.html", {"request": request})
