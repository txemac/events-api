import pytest
from starlette.testclient import TestClient

from app.main import app
from data.schemas import Event
from data.schemas import Zone


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def data_zone():
    return dict(
        zone_id=1,
        name='zone 1',
        capacity=17,
        max_price=123.45,
        numbered=True,
    )


@pytest.fixture
def new_zone(data_zone):
    return Zone(
        **data_zone
    )


@pytest.fixture
def data_event(data_zone):
    return dict(
        event_id=1,
        event_date="1982-04-25T16:30:00",
        sell_from="1982-04-25T16:30:00",
        sell_to="1982-04-25T16:30:00",
        sold_out=False,
        zone=[data_zone],
    )


@pytest.fixture
def new_event(data_event):
    return Event(
        **data_event
    )


@pytest.fixture
def data_base_event(data_event):
    return dict(
        base_event_id=1,
        sell_mode='online',
        title='Test',
        organizer_company_id=2,
        event=data_event,
    )
