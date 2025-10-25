from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List
from database.db import engine
from models.competitor import Competitor, CompetitorCreate, CompetitorUpdate

router = APIRouter(prefix="/competitors", tags=["Competitors"])


# 🟢 CREATE
@router.post("/", response_model=Competitor)
def create_competitor(data: CompetitorCreate):
    with Session(engine) as session:
        competitor = Competitor.from_orm(data)
        session.add(competitor)
        session.commit()
        session.refresh(competitor)
        return competitor


# 🔵 READ ALL
@router.get("/", response_model=List[Competitor])
def get_all_competitors():
    with Session(engine) as session:
        competitors = session.exec(select(Competitor)).all()
        return competitors


# 🟣 READ ONE
@router.get("/{competitor_id}", response_model=Competitor)
def get_competitor(competitor_id: int):
    with Session(engine) as session:
        competitor = session.get(Competitor, competitor_id)
        if not competitor:
            raise HTTPException(status_code=404, detail="Competidor no encontrado")
        return competitor


# 🟠 UPDATE
@router.put("/{competitor_id}", response_model=Competitor)
def update_competitor(competitor_id: int, data: CompetitorUpdate):
    with Session(engine) as session:
        competitor = session.get(Competitor, competitor_id)
        if not competitor:
            raise HTTPException(status_code=404, detail="Competidor no encontrado")
        for key, value in data.dict(exclude_unset=True).items():
            setattr(competitor, key, value)
        session.add(competitor)
        session.commit()
        session.refresh(competitor)
        return competitor


# 🔴 DELETE
@router.delete("/{competitor_id}")
def delete_competitor(competitor_id: int):
    with Session(engine) as session:
        competitor = session.get(Competitor, competitor_id)
        if not competitor:
            raise HTTPException(status_code=404, detail="Competidor no encontrado")
        session.delete(competitor)
        session.commit()
        return {"message": "Competidor eliminado correctamente"}


