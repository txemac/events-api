from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel


class ZoneCreate(BaseModel):
    zone_id: int
    name: str
    capacity: int
    max_price: float
    numbered: bool


class ZoneDB(ZoneCreate):
    dt_created = datetime

    class Config:
        orm_mode = True


class EventCreate(BaseModel):
    event_id: int
    event_date: datetime
    sell_from: datetime
    sell_to: datetime
    sold_out: bool
    zone: List[ZoneDB]


class EventDB(EventCreate):
    dt_created = datetime

    class Config:
        orm_mode = True


class BaseEventCreate(BaseModel):
    base_event_id: int
    sell_mode: str
    title: str
    organizer_company_id: Optional[int] = None
    event: EventDB


class BaseEventDB(BaseEventCreate):
    dt_created = datetime

    class Config:
        orm_mode = True
