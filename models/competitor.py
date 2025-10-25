from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .tournament import Tournament
    from .cube import Cube
    from .competitor_record import CompetitorRecord



class CompetitorBase(SQLModel):
    name: str
    country: str
    average_time: float  


class Competitor(CompetitorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tournament_id: Optional[int] = Field(default=None, foreign_key="tournament.id")
    cube_id: Optional[int] = Field(default=None, foreign_key="cube.id")

  
    tournament: Optional["Tournament"] = Relationship(back_populates="competitors")
    cube: Optional["Cube"] = Relationship(back_populates="competitors")


    records: List["CompetitorRecord"] = Relationship(back_populates="competitor")



class CompetitorCreate(CompetitorBase):
    tournament_id: Optional[int] = None
    cube_id: Optional[int] = None


class CompetitorUpdate(CompetitorBase):
    tournament_id: Optional[int] = None
    cube_id: Optional[int] = None



