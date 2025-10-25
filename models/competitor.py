from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .tournament import Tournament
    from .cube import Cube
    from .competitor_record import CompetitorRecord


# 🔹 Base del competidor
class CompetitorBase(SQLModel):
    name: str
    country: str
    average_time: float  # Tiempo promedio de resolución


# 🔹 Modelo principal Competitor
class Competitor(CompetitorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")
    cube_id: Optional[int] = Field(default=None, foreign_key="cube.id")

    # 🔹 Relaciones
    tournament: Optional["Tournament"] = Relationship(back_populates="competitors")
    cube: Optional["Cube"] = Relationship(back_populates="competitors")

    # ✅ Nueva relación N:N (competidor ↔ torneo mediante récords)
    records: List["CompetitorRecord"] = Relationship(back_populates="competitor")


# 🔹 Modelos para crear/actualizar (sin ID)
class CompetitorCreate(CompetitorBase):
    tournament_id: Optional[int] = None
    cube_id: Optional[int] = None


class CompetitorUpdate(CompetitorBase):
    tournament_id: Optional[int] = None
    cube_id: Optional[int] = None



