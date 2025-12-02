from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import create_tables
from routers.cube_router import router as cube_router
from routers.tournament_router import router as tournament_router
from routers.competitor_router import router as competitor_router
from routers.record_router import router as record_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Creando tablas si no existen...")
    create_tables()
    print("✅ Tablas listas.")
    yield
    print("👋 Finalizando aplicación...")


app = FastAPI(
    title="CRUD Cubo de Rubik 🧩",
    description=(
        "API para gestionar cubos, torneos, competidores y registros de tiempos "
        "de resolución. Desarrollado con FastAPI + SQLModel."
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(cube_router)
app.include_router(tournament_router)
app.include_router(competitor_router)
app.include_router(record_router)



@app.get("/")
def home():
    return {
        "message": "Bienvenido al CRUD del Cubo de Rubik 🧩",
        "docs": "Visita /docs para ver la documentación interactiva de la API",
        "status": "OK"
    }















