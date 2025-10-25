from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database.db import get_session
from models.competitor_record import CompetitorRecord, CompetitorRecordCreate

router = APIRouter(prefix="/records", tags=["Competitor Records"])



@router.post("/", response_model=CompetitorRecord)
def create_record(record: CompetitorRecordCreate, session: Session = Depends(get_session)):
    new_record = CompetitorRecord.from_orm(record)
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return new_record



@router.get("/", response_model=List[CompetitorRecord])
def get_all_records(session: Session = Depends(get_session)):
    records = session.exec(select(CompetitorRecord)).all()
    return records



@router.get("/{record_id}", response_model=CompetitorRecord)
def get_record_by_id(record_id: int, session: Session = Depends(get_session)):
    record = session.get(CompetitorRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record no encontrado")
    return record


@router.put("/{record_id}", response_model=CompetitorRecord)
def update_record(record_id: int, updated_record: CompetitorRecordCreate, session: Session = Depends(get_session)):
    record = session.get(CompetitorRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record no encontrado")

    record.event_type = updated_record.event_type
    record.record_time = updated_record.record_time
    record.record_date = updated_record.record_date
    record.competitor_id = updated_record.competitor_id
    record.tournament_id = updated_record.tournament_id

    session.add(record)
    session.commit()
    session.refresh(record)
    return record



@router.delete("/{record_id}")
def delete_record(record_id: int, session: Session = Depends(get_session)):
    record = session.get(CompetitorRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record no encontrado")

    session.delete(record)
    session.commit()
    return {"ok": True, "message": "Record fue eliminado "}


