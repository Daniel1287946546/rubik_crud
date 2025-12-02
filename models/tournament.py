from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import date
from sqlalchemy.orm import Mapped

if TYPE_CHECKING:
    from .cube import Cube
    from .competitor import Competitor
    from .competitor_record import CompetitorRecord


# === MODELO PRINCIPAL ===
class Tournament(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: date
    location: str
    is_active: bool = Field(default=True)

    cubes: Mapped[List["Cube"]] = Relationship(back_populates="tournament")
    competitors: Mapped[List["Competitor"]] = Relationship(back_populates="tournament")
    records: Mapped[List["CompetitorRecord"]] = Relationship(back_populates="tournament")


# === MODELO PARA CREACIÓN (NO incluye id) ===
class TournamentCreate(SQLModel):
    name: str
    date: date
    location: str
    is_active: Optional[bool] = True


# === MODELO PARA ACTUALIZACIÓN PARCIAL ===
class TournamentUpdate(SQLModel):
    name: Optional[str] = None
    date: Optional[date] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None



















