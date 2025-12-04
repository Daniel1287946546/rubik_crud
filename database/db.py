from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated, Generator
from fastapi import Depends

# Nombre y URL de la base de datos
db_name = "db.sqlite3"
db_url = f"sqlite:///{db_name}"

# Crear motor de SQLModel
engine = create_engine(db_url)

# Función para crear todas las tablas
def create_tables():
    SQLModel.metadata.create_all(engine)

# Generador de sesiones para dependencias
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Dependencia para FastAPI
SessionDep = Annotated[Session, Depends(get_session)]




