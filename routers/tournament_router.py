from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from database.db import engine
from models.tournament import Tournament, TournamentCreate, TournamentUpdate

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])


# 🟢 CREAR TORNEO
@router.post("/", response_model=Tournament)
def create_tournament(tournament_data: TournamentCreate):
    # Si la fecha llega como string, la convertimos a tipo date
    if isinstance(tournament_data.date, str):
        try:
            tournament_data.date = datetime.strptime(tournament_data.date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

    with Session(engine) as session:
        tournament = Tournament.from_orm(tournament_data)  # Convierte TournamentCreate → Tournament
        session.add(tournament)
        session.commit()
        session.refresh(tournament)
        return tournament


# 🔵 OBTENER TODOS LOS TORNEOS ACTIVOS
@router.get("/", response_model=List[Tournament])
def get_all_tournaments():
    with Session(engine) as session:
        tournaments = session.exec(
            select(Tournament).where(Tournament.is_active == True)
        ).all()
        return tournaments


# 🟣 OBTENER TORNEO POR ID
@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(tournament_id: int):
    with Session(engine) as session:
        tournament = session.get(Tournament, tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")
        return tournament


# 🟠 ACTUALIZAR TORNEO
@router.put("/{tournament_id}", response_model=Tournament)
def update_tournament(tournament_id: int, data: TournamentUpdate):
    with Session(engine) as session:
        tournament = session.get(Tournament, tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")

        if data.date:
            if isinstance(data.date, str):
                try:
                    data.date = datetime.strptime(data.date, "%Y-%m-%d").date()
                except ValueError:
                    raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

        # Actualiza solo los campos enviados
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tournament, key, value)

        session.add(tournament)
        session.commit()
        session.refresh(tournament)
        return tournament


# 🔴 ELIMINAR (MARCAR COMO INACTIVO)
@router.delete("/{tournament_id}")
def delete_tournament(tournament_id: int):
    with Session(engine) as session:
        tournament = session.get(Tournament, tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")

        tournament.is_active = False
        session.add(tournament)
        session.commit()
        session.refresh(tournament)
        return {"message": "Torneo marcado como inactivo"}


# ⚫ VER TORNEOS INACTIVOS
@router.get("/inactivos/", response_model=List[Tournament])
def get_inactive_tournaments():
    with Session(engine) as session:
        tournaments = session.exec(
            select(Tournament).where(Tournament.is_active == False)
        ).all()
        return tournaments



