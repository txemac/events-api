from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

from data.database import Base
from data.database import Event
from data.schemas import BaseEventCreate
from data.schemas import BaseEventDB
from data.schemas import EventDB


class BaseEvent(Base):
    __tablename__ = "base_event"

    base_event_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_id = Column(Integer, ForeignKey("event.event_id"))
    event = relationship(Event)
    sell_mode = Column(String, nullable=False)
    title = Column(String, nullable=False)
    organizer_company_id = Column(Integer, nullable=True)
    dt_created = Column(DateTime, default=func.now(), nullable=False)

    def __init__(
            self,
            base_event_id: int,
            event: EventDB,
            sell_mode: str,
            title: str,
            organizer_company_id: int = None,
    ):
        self.base_event_id = base_event_id
        self.event = event
        self.sell_mode = sell_mode
        self.title = title
        self.organizer_company_id = organizer_company_id

    @classmethod
    def create(
            cls,
            db_session: Session,
            data: BaseEventCreate
    ) -> BaseEventDB:
        """
        Create a new zone.

        :param Session db_session: database session
        :param BaseEventCreate data: data
        """
        base_event = cls(
            base_event_id=data.base_event_id,
            event=Event.get_or_create(db_session=db_session, event=data.event),
            sell_mode=data.sell_mode,
            title=data.title,
            organizer_company_id=data.organizer_company_id,
        )
        db_session.add(base_event)
        db_session.commit()
        db_session.refresh(base_event)

        return base_event
