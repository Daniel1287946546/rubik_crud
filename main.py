from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import create_tables
from routers import cube_router, tournament_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="CRUD Cubo de Rubik ",
    description="API para gestionar cubos y torneos de Rubik",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir routers
app.include_router(cube_router.router)
app.include_router(tournament_router.router)


@app.get("/")
def home():
    return {"message": "Bienvenido al CRUD del Cubo de Rubik 🧩"}










