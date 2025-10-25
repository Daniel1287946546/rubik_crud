from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import create_tables
from routers import cube_router, tournament_router, competitor_router


# 🟢 Se ejecuta al iniciar la app (crea tablas si no existen)
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


# 🧩 Instancia principal de la aplicación
app = FastAPI(
    title="CRUD Cubo de Rubik 🧩",
    description="API para gestionar cubos, torneos y competidores de Rubik",
    version="1.1.0",
    lifespan=lifespan
)


# 🚀 Inclusión de los routers
app.include_router(cube_router.router)
app.include_router(tournament_router.router)
app.include_router(competitor_router.router)


# 🏠 Endpoint base
@app.get("/")
def home():
    return {"message": "Bienvenido al CRUD del Cubo de Rubik 🧩"}











