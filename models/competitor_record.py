from typing import Optional, TYPE_CHECKING
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

# Evita import circular
if TYPE_CHECKING:
    from .competitor import Competitor
    from .tournament import Tournament
    from .cube import Cube


class CompetitorRecordBase(SQLModel):
    event_type: str          # "single" o "average"
    record_time: float       # tiempo
    record_date: date        # fecha


class CompetitorRecord(CompetitorRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    competitor_id: Optional[int] = Field(default=None, foreign_key="competitor.id")
    cube_id: Optional[int] = Field(default=None, foreign_key="cube.id")
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")

    # Relaciones SQLModel
    competitor: Optional["Competitor"] = Relationship(back_populates="records")
    cube: Optional["Cube"] = Relationship(back_populates="records")
    tournament: Optional["Tournament"] = Relationship(back_populates="records")





