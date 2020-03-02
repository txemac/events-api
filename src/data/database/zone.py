from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Session

from data.database import Base
from data.schemas import Zone


class Zone(Base):
    __tablename__ = "zone"

    zone_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    max_price = Column(Float, nullable=False)
    numbered = Column(Boolean, nullable=False)
    dt_created = Column(DateTime, default=func.now(), nullable=False)

    def __init__(
            self,
            zone_id: int,
            name: str,
            capacity: int,
            max_price: float,
            numbered: bool,
    ):
        self.zone_id = zone_id
        self.name = name
        self.capacity = capacity
        self.max_price = max_price
        self.numbered = numbered

    @classmethod
    def create(
            cls,
            db_session: Session,
            data: Zone
    ):
        """
        Create a new zone.

        :param Session db_session: database session
        :param UserPost data: data
        """
        zone = Zone(
            zone_id=data.zone_id,
            name=data.name,
            capacity=data.capacity,
            max_price=data.max_price,
            numbered=data.numbered,
        )
        db_session.add(zone)
        db_session.commit()
        db_session.refresh(zone)
