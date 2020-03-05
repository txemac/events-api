from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from data import database
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
    zone = relationship(Zone, secondary='event_zone')
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
            data: EventCreate
    ) -> EventDB:
        """
        Create a new event.

        :param EventCreate data: data
        """
        event = cls(
            event_id=data.event_id,
            event_date=data.event_date,
            sell_from=data.sell_from,
            sell_to=data.sell_to,
            sold_out=data.sold_out,
            zone=[Zone.create_or_update(zone=z) for z in data.zone],
        )
        database.save(event)

        return event

    @classmethod
    def _update(
            cls,
            event_db: EventDB,
            data: EventCreate,
    ) -> EventDB:
        """
        Update an event.

        :param EventDB event_db: event from DB
        :param EventCreate data: data
        """
        event_db.event_id = data.event_id
        event_db.event_date = data.event_date
        event_db.sell_from = data.sell_from
        event_db.sell_to = data.sell_to
        event_db.sold_out = data.sold_out
        event_db.zone = [Zone.create_or_update(zone=z) for z in data.zone]
        event_db.dt_created = datetime.now()

        database.db_session.commit()
        database.db_session.refresh(event_db)

        return event_db

    @classmethod
    def _get_by_id(
            cls,
            event_id: int
    ) -> EventDB:
        """
        Get an event by ID.

        :param int event_id: id
        :return EventDB: event
        """
        return database.db_session.query(cls).get(event_id)

    @classmethod
    def create_or_update(
            cls,
            event: EventCreate,
    ) -> EventDB:
        """
        Create an event. Update if already exists.

        :param EventCreate event: event
        :return EventDB: event
        """
        event_db = cls._get_by_id(event_id=event.event_id)
        if event_db is None:
            event_db = cls._create(data=event)
        else:
            event_db = cls._update(event_db=event_db, data=event)
        return event_db
