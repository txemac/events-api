from datetime import datetime
from typing import List

from pydantic import BaseModel


class ZoneCreate(BaseModel):
    zone_id: int
    name: str
    capacity: int
    max_price: float
    numbered: bool


class ZoneDB(ZoneCreate):
    dt_created = datetime


class EventCreate(BaseModel):
    event_id: int
    event_date: datetime
    sell_from: datetime
    sell_to: datetime
    sold_out: bool
    zone: List[ZoneCreate]


class BaseEventCreate(BaseModel):
    base_event_id: int
    sell_mode: str
    title: str
    organizer_company_id: int = None
    event: EventCreate
