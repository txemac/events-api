from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

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
    def _create(
            cls,
            db_session: Session,
            data: BaseEventCreate
    ) -> BaseEventDB:
        """
        Create a new base event.

        :param Session db_session: database session
        :param BaseEventCreate data: data
        """
        base_event = cls(
            base_event_id=data.base_event_id,
            event=Event.create_or_update(db_session=db_session, event=data.event),
            sell_mode=data.sell_mode,
            title=data.title,
            organizer_company_id=data.organizer_company_id,
        )
        db_session.add(base_event)
        db_session.commit()
        db_session.refresh(base_event)

        return base_event

    @classmethod
    def _update(
            cls,
            db_session: Session,
            base_event_db: BaseEventDB,
            data: BaseEventCreate,
    ) -> BaseEventDB:
        """
        Create a new zone.

        :param Session db_session: database session
        :param BaseEventDB base_event_db: data at DB
        :param BaseEventCreate data: data
        """
        base_event_db.base_event_id = data.base_event_id
        base_event_db.event = Event.create_or_update(db_session=db_session, event=data.event)
        base_event_db.sell_mode = data.sell_mode
        base_event_db.title = data.title
        base_event_db.organizer_company_id = data.organizer_company_id
        base_event_db.dt_created = datetime.now()

        db_session.commit()
        db_session.refresh(base_event_db)

        return base_event_db

    @classmethod
    def _get_by_id(
            cls,
            db_session: Session,
            base_event_id: int
    ) -> BaseEventDB:
        """
        Get a base event by ID.

        :param Session db_session: database session
        :param int base_event_id: id
        :return BaseEventDB: zone
        """
        return db_session.query(cls).get(base_event_id)

    @classmethod
    def create_or_update(
            cls,
            db_session: Session,
            base_event: BaseEventCreate
    ) -> BaseEventDB:
        """
        Create a new zone. Update info it already exists.

        :param Session db_session: database session
        :param BaseEventCreate base_event: base event
        """
        base_event_db = cls._get_by_id(db_session=db_session, base_event_id=base_event.base_event_id)

        if base_event_db is None:
            base_event_db = cls._create(db_session=db_session, data=base_event)
        else:
            base_event_db = cls._update(db_session=db_session, base_event_db=base_event_db, data=base_event)

        return base_event_db

    @staticmethod
    def get_events(
            db_session: Session,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
            offline: Optional[bool] = False,
    ) -> List[BaseEventDB]:
        """
        Get event from database.

        :param Session db_session: database session
        :param date start_date: start date
        :param date end_date: end date
        :param bool offline: filter offline
        :return List: base events
        """
        result = db_session.query(BaseEvent)

        if start_date is not None:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            result = result.filter(BaseEvent.event.has(Event.event_date >= start_datetime))

        if end_date is not None:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            result = result.filter(BaseEvent.event.has(Event.event_date <= end_datetime))

        if offline is False:
            result = result.filter(BaseEvent.sell_mode == 'online')

        return result.all()
