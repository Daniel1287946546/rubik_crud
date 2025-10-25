from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .tournament import Tournament
    from .cube import Cube


class CompetitorBase(SQLModel):
    name: str
    country: str
    average_time: float  # Tiempo promedio de resolución


class Competitor(CompetitorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")
    cube_id: Optional[int] = Field(default=None, foreign_key="cube.id")

    # Relaciones
    tournament: Optional["Tournament"] = Relationship(back_populates="competitors")
    cube: Optional["Cube"] = Relationship(back_populates="competitors")


class CompetitorCreate(CompetitorBase):
    tournament_id: Optional[int] = None
    cube_id: Optional[int] = None


class CompetitorUpdate(CompetitorBase):
    tournament_id: Optional[int] = None
    cube_id: Optional[int] = None



