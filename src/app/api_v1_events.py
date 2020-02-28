from datetime import date
from datetime import datetime
from typing import List

from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from data.events import Events
from data.external_api_client import ExternalAPIClient
from data.schemas import BaseEvent

api_v1_events = APIRouter()


@api_v1_events.get('/', response_model=List[BaseEvent], status_code=HTTP_200_OK)
def get_events(
        start_date: date = datetime.min.date(),
        end_date: date = datetime.max.date(),
        offline: bool = False
):
    events = ExternalAPIClient.get_base_events()
    return Events.get_events(events=events, start_date=start_date, end_date=end_date, offline=offline)
