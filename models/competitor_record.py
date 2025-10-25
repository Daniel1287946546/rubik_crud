from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from models.competitor import Competitor
from models.tournament import Tournament


class CompetitorRecordBase(SQLModel):
    event_type: str
    record_time: float
    record_date: date  # ✅ Permite escribir "2025-10-30" manualmente


class CompetitorRecordCreate(CompetitorRecordBase):
    competitor_id: int
    tournament_id: int


class CompetitorRecord(CompetitorRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    competitor_id: Optional[int] = Field(default=None, foreign_key="competitor.id")
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")

    competitor: Optional["Competitor"] = Relationship(back_populates="records")
    tournament: Optional["Tournament"] = Relationship(back_populates="records")


