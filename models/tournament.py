from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Mapped

if TYPE_CHECKING:
    from .cube import Cube
    from .competitor import Competitor
    from .competitor_record import CompetitorRecord

class Tournament(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # AUTOINCREMENT
    name: str
    date: str
    location: str
    is_active: bool = Field(default=True)

    cubes: Mapped[List["Cube"]] = Relationship(back_populates="tournament")
    competitors: Mapped[List["Competitor"]] = Relationship(back_populates="tournament")
    records: Mapped[List["CompetitorRecord"]] = Relationship(back_populates="tournament")

















