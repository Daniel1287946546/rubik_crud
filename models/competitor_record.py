from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from models.competitor import Competitor
from models.tournament import Tournament


class CompetitorRecordBase(SQLModel):
    event_type: str  # Ej: "3x3", "2x2", "Pyraminx", etc.
    record_time: float  # Tiempo en segundos
    record_date: datetime = Field(default_factory=datetime.utcnow)


class CompetitorRecord(CompetitorRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    competitor_id: Optional[int] = Field(default=None, foreign_key="competitor.id")
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")

    # Relaciones inversas
    competitor: Optional["Competitor"] = Relationship(back_populates="records")
    tournament: Optional["Tournament"] = Relationship(back_populates="records")

