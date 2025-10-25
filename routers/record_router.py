from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database.db import get_session
from models.competitor_record import CompetitorRecord, CompetitorRecordBase

router = APIRouter(
    prefix="/records",
    tags=["Records"]
)

# ✅ Crear un nuevo récord
@router.post("/", response_model=CompetitorRecord)
def create_record(record: CompetitorRecordBase, session: Session = Depends(get_session)):
    db_record = CompetitorRecord.from_orm(record)
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record


# ✅ Listar todos los récords
@router.get("/", response_model=list[CompetitorRecord])
def list_records(session: Session = Depends(get_session)):
    records = session.exec(select(CompetitorRecord)).all()
    return records


# ✅ Obtener récords por competidor
@router.get("/competitor/{competitor_id}", response_model=list[CompetitorRecord])
def get_records_by_competitor(competitor_id: int, session: Session = Depends(get_session)):
    records = session.exec(
        select(CompetitorRecord).where(CompetitorRecord.competitor_id == competitor_id)
    ).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records found for this competitor")
    return records


# ✅ Obtener récords por torneo
@router.get("/tournament/{tournament_id}", response_model=list[CompetitorRecord])
def get_records_by_tournament(tournament_id: int, session: Session = Depends(get_session)):
    records = session.exec(
        select(CompetitorRecord).where(CompetitorRecord.tournament_id == tournament_id)
    ).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records found for this tournament")
    return records
