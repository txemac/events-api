import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
Base = declarative_base()

Session = sessionmaker(bind=engine)
db_session = Session()

Base.metadata.create_all(engine)


def save(obj):
    db_session.add(obj)
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()
        raise


from .zone import Zone
from .event import Event
from .event_zone import EventZone
from .base_event import BaseEvent
