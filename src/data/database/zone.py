from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session

from data.database import Base
from data.schemas import ZoneCreate
from data.schemas import ZoneDB


class Zone(Base):
    __tablename__ = "zone"

    zone_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    max_price = Column(Float, nullable=False)
    numbered = Column(Boolean, nullable=False)
    dt_created = Column(DateTime, default=datetime.now(), nullable=False)

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
    def _create(
            cls,
            db_session: Session,
            data: ZoneCreate
    ) -> ZoneDB:
        """
        Create a new zone.

        :param Session db_session: database session
        :param Zone data: data
        :return ZoneDB: zone
        """
        zone = cls(
            zone_id=data.zone_id,
            name=data.name,
            capacity=data.capacity,
            max_price=data.max_price,
            numbered=data.numbered,
        )
        db_session.add(zone)
        db_session.commit()
        db_session.refresh(zone)

        return zone

    @classmethod
    def _update(
            cls,
            db_session: Session,
            zone_db: ZoneDB,
            data: ZoneCreate,
    ) -> ZoneDB:
        """
        Create a new zone.

        :param Session db_session: database session
        :param zone_db: data at DB
        :param Zone data: data
        :return ZoneDB: zone
        """
        zone_db.zone_id = data.zone_id
        zone_db.name = data.name
        zone_db.capacity = data.capacity
        zone_db.max_price = data.max_price
        zone_db.numbered = data.numbered
        zone_db.dt_created = datetime.now()

        db_session.commit()
        db_session.refresh(zone_db)

        return zone_db

    @classmethod
    def _get_by_id(
            cls,
            db_session: Session,
            zone_id: int
    ) -> ZoneDB:
        """
        Get a zone by ID.

        :param Session db_session: database session
        :param int zone_id: id
        :return ZoneDB: zone
        """
        return db_session.query(cls).get(zone_id)

    @classmethod
    def create_or_update(
            cls,
            db_session: Session,
            zone: ZoneCreate,
    ) -> ZoneDB:
        """
        Create a zone. Update if already exists.

        :param Session db_session: database session
        :param ZoneCreate zone: zone
        :return ZoneDB: zone
        """
        zone_db = cls._get_by_id(db_session=db_session, zone_id=zone.zone_id)
        if zone_db is None:
            zone_db = cls._create(db_session=db_session, data=zone)
        else:
            zone_db = cls._update(db_session=db_session, zone_db=zone_db, data=zone)
        return zone_db
