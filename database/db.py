from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated, Generator
from fastapi import Depends

db_name = "db.sqlite3"
db_url = f"sqlite:///{db_name}"

engine = create_engine(db_url, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]





