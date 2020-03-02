from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

from data.database import Base
from data.database import Zone
from data.schemas import EventCreate
from data.schemas import EventDB


class Event(Base):
    __tablename__ = "event"

    event_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_date = Column(DateTime, default=func.now(), nullable=False)
    sell_from = Column(DateTime, default=func.now(), nullable=False)
    sell_to = Column(DateTime, default=func.now(), nullable=False)
    sold_out = Column(Boolean, nullable=False)
    zone = relationship(Zone, secondary='event_zone', lazy="joined")
    dt_created = Column(DateTime, default=func.now(), nullable=False)

    def __init__(
            self,
            event_id: int,
            event_date: datetime,
            sell_from: datetime,
            sell_to: datetime,
            sold_out: bool,
            zone: [Zone],
    ):
        self.event_id = event_id
        self.event_date = event_date
        self.sell_from = sell_from
        self.sell_to = sell_to
        self.sold_out = sold_out
        self.zone = zone

    @classmethod
    def _create(
            cls,
            db_session: Session,
            data: EventCreate
    ):
        """
        Create a new event.

        :param Session db_session: database session
        :param EventCreate data: data
        """
        event = cls(
            event_id=data.event_id,
            event_date=data.event_date,
            sell_from=data.sell_from,
            sell_to=data.sell_to,
            sold_out=data.sold_out,
            zone=[Zone.get_or_create(db_session=db_session, zone=z) for z in data.zone],
        )
        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        return cls._get_by_id(db_session=db_session, event_id=data.event_id)

    @classmethod
    def _get_by_id(
            cls,
            db_session: Session,
            event_id: int
    ) -> EventDB:
        """
        Get an event by ID.

        :param Session db_session: database session
        :param int event_id: id
        :return EventDB: event
        """
        return db_session.query(cls).get(event_id)

    @classmethod
    def get_or_create(
            cls,
            db_session: Session,
            event: EventCreate,
    ) -> EventDB:
        """
        Get an event. Create if it does not exists.

        :param Session db_session: database session
        :param EventCreate event: event
        :return EventDB: event
        """
        event_db = cls._get_by_id(db_session=db_session, event_id=event.event_id)
        if event_db is None:
            event_db = cls._create(db_session=db_session, data=event)
        return event_db
