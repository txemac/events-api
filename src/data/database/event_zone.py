from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import func

from data.database import Base


class EventZone(Base):
    __tablename__ = "event_zone"

    event_zone_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_id = Column(Integer, ForeignKey("event.event_id"))
    zone_id = Column(Integer, ForeignKey("zone.zone_id"))
    dt_created = Column(DateTime, default=func.now(), nullable=False)
