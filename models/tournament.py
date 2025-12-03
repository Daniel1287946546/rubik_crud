from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

if TYPE_CHECKING:
    from .cube import Cube
    from .competitor import Competitor
    from .competitor_record import CompetitorRecord


class TournamentBase(SQLModel):
    name: str
    location: str
    date: date
    is_active: bool = True


class Tournament(TournamentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    cubes: List["Cube"] = Relationship(back_populates="tournament")
    competitors: List["Competitor"] = Relationship(back_populates="tournament")
    records: List["CompetitorRecord"] = Relationship(back_populates="tournament")


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(SQLModel):
    name: Optional[str] = None
    location: Optional[str] = None
    date: Optional[date] = None
    is_active: Optional[bool] = None



















