from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from database.db import engine
from models.tournament import Tournament

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])


@router.post("/", response_model=Tournament)
def create_tournament(tournament: Tournament):
    if isinstance(tournament.date, str):
        try:
            tournament.date = datetime.strptime(tournament.date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

    with Session(engine) as session:
        session.add(tournament)
        session.commit()
        session.refresh(tournament)
        return tournament


@router.get("/", response_model=List[Tournament])
def get_all_tournaments():
    with Session(engine) as session:
        tournaments = session.exec(select(Tournament)).all()
        return tournaments


@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(tournament_id: int):
    with Session(engine) as session:
        tournament = session.get(Tournament, tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")
        return tournament

@router.put("/{tournament_id}", response_model=Tournament)
def update_tournament(tournament_id: int, data: Tournament):
    with Session(engine) as session:
        tournament = session.get(Tournament, tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")

        if isinstance(data.date, str):
            try:
                data.date = datetime.strptime(data.date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

        tournament.name = data.name
        tournament.location = data.location
        tournament.date = data.date
        session.add(tournament)
        session.commit()
        session.refresh(tournament)
        return tournament


@router.delete("/{tournament_id}")
def delete_tournament(tournament_id: int):
    with Session(engine) as session:
        tournament = session.get(Tournament, tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")
        session.delete(tournament)
        session.commit()
        return {"message": "Torneo eliminado correctamente ✅"}


