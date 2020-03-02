from datetime import date
from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from data.database import get_db
from data.database.base_event import BaseEvent
from data.schemas import BaseEventDB

api_v1_events = APIRouter()


@api_v1_events.get('/', response_model=List[BaseEventDB], status_code=HTTP_200_OK)
def get_events(
        *,
        db_session: Session = Depends(get_db),
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        offline: Optional[bool] = False,
):
    return BaseEvent.get_events(db_session=db_session, start_date=start_date, end_date=end_date, offline=offline)
