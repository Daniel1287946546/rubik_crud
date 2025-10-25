from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .tournament import Tournament


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

    tournament: Optional["Tournament"] = Relationship(back_populates="cubes")


class CubeCreate(CubeBase):
    tournament_id: Optional[int] = None


class CubeUpdate(CubeBase):
    tournament_id: Optional[int] = None





