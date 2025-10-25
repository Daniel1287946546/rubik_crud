from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.orm import Mapped

if TYPE_CHECKING:
    from .cube import Cube
    from .competitor import Competitor
    from .competitor_record import CompetitorRecord  # ✅ nuevo modelo intermedio


class Tournament(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: str
    location: str

    # ✅ Relación 1:N con cubos
    cubes: Mapped[List["Cube"]] = Relationship(back_populates="tournament")

    # ✅ Relación 1:N con competidores
    competitors: Mapped[List["Competitor"]] = Relationship(back_populates="tournament")

    # ✅ Relación N:N con CompetitorRecord (competencias registradas)
    records: Mapped[List["CompetitorRecord"]] = Relationship(back_populates="tournament")














