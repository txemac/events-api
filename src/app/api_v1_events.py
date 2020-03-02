from datetime import date
from datetime import datetime
from typing import List

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from data import events
from data import external_api_client
from data.schemas import BaseEventCreate

api_v1_events = APIRouter()


@api_v1_events.get('/', response_model=List[BaseEventCreate], status_code=HTTP_200_OK)
def get_events(
        start_date: date = datetime.min.date(),
        end_date: date = datetime.max.date(),
        offline: bool = False
):
    base_events = external_api_client.get_base_events()
    return events.get_events(events=base_events, start_date=start_date, end_date=end_date, offline=offline)
