from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Mapped

if TYPE_CHECKING:
    from .tournament import Tournament
    from .competitor import Competitor
    from .competitor_record import CompetitorRecord


class CubeBase(SQLModel):
    brand: str
    mechanism: str
    pieces: int
    difficulty: str
    is_competition: bool
    world_record: float


class Cube(CubeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")

    # Relaciones
    tournament: Optional["Tournament"] = Relationship(back_populates="cubes")
    competitors: Mapped[List["Competitor"]] = Relationship(back_populates="cube")

    # 🔥 ESTA LÍNEA ES OBLIGATORIA
    records: Mapped[List["CompetitorRecord"]] = Relationship(back_populates="cube")


class CubeCreate(CubeBase):
    tournament_id: Optional[int] = None


class CubeUpdate(CubeBase):
    tournament_id: Optional[int] = None







