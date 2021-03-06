from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import Session
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from data.database import Base
from data.database import Zone
from data.schemas import EventCreate
from data.schemas import EventDB


class Event(Base):
    __tablename__ = "event"

    event_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_date = Column(DateTime, nullable=False)
    sell_from = Column(DateTime, nullable=False)
    sell_to = Column(DateTime, nullable=False)
    sold_out = Column(Boolean, nullable=False)
    zone = relationship(Zone, secondary='event_zone', backref=backref('event_zone', lazy='dynamic'))
    dt_created = Column(DateTime, default=datetime.now(), nullable=False)

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
    ) -> EventDB:
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
            zone=[Zone.create_or_update(db_session=db_session, zone=z) for z in data.zone],
        )
        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        return event

    @classmethod
    def _update(
            cls,
            db_session: Session,
            event_db: EventDB,
            data: EventCreate,
    ) -> EventDB:
        """
        Update an event.

        :param Session db_session: database session
        :param EventDB event_db: event from DB
        :param EventCreate data: data
        """
        event_db.event_id = data.event_id
        event_db.event_date = data.event_date
        event_db.sell_from = data.sell_from
        event_db.sell_to = data.sell_to
        event_db.sold_out = data.sold_out
        event_db.dt_created = datetime.now()

        event_db.zone.clear()
        event_db.zone = [Zone.create_or_update(db_session=db_session, zone=z) for z in data.zone]

        db_session.add(event_db)
        db_session.refresh(event_db)

        return event_db

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
    def create_or_update(
            cls,
            db_session: Session,
            event: EventCreate,
    ) -> EventDB:
        """
        Create an event. Update if already exists.

        :param Session db_session: database session
        :param EventCreate event: event
        :return EventDB: event
        """
        event_db = cls._get_by_id(db_session=db_session, event_id=event.event_id)
        if event_db is None:
            event_db = cls._create(db_session=db_session, data=event)
        else:
            event_db = cls._update(db_session=db_session, event_db=event_db, data=event)
        return event_db
