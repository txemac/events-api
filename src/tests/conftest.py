import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database
from starlette.testclient import TestClient

from app.main import app
from data import external_api_client
from data.database import Base
from data.database import get_db
from data.schemas import BaseEvent
from data.schemas import Event
from data.schemas import Zone


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


url = f'{os.getenv("DATABASE_URL")}_test'
_db_conn = create_engine(url)


def get_test_db_conn():
    assert _db_conn is not None
    return _db_conn


def get_test_db():
    sess = Session(bind=_db_conn)

    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="session", autouse=True)
def database():
    if database_exists(url):
        drop_database(url)
    create_database(url)
    Base.metadata.create_all(_db_conn)
    app.dependency_overrides[get_db] = get_test_db
    yield
    drop_database(url)


@pytest.yield_fixture
def session():
    db_session = Session(bind=_db_conn)

    yield db_session
    for tbl in reversed(Base.metadata.sorted_tables):
        _db_conn.execute(tbl.delete())
    db_session.close()


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


@pytest.fixture
def xml():
    return str("""<?xml version="1.0" encoding="UTF-8"?>
<eventList version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:noNamespaceSchemaLocation="eventList.xsd">
    <output>
        <base_event base_event_id="291" sell_mode="online" title="Concert">
            <event event_date="2019-06-30T21:00:00" event_id="291" sell_from="2014-07-01T00:00:00"
            sell_to="2019-06-30T20:00:00" sold_out="false">
                <zone zone_id="40" capacity="243" max_price="20.00" name="Platea" numbered="true" />
                <zone zone_id="38" capacity="100" max_price="0.00" name="test" numbered="false" />
                <zone zone_id="30" capacity="90" max_price="0.00" name="A28" numbered="true" />
            </event>
        </base_event>
        <base_event base_event_id="322" sell_mode="offline" organizer_company_id="2" title="Theater">
            <event event_date="2019-04-22T20:00:00" event_id="1642" sell_from="2017-01-01T00:00:00"
            sell_to="2019-04-21T19:50:00" sold_out="false">
                <zone zone_id="311" capacity="2" max_price="55.00" name="A42" numbered="true" />
            </event>
        </base_event>
        <base_event base_event_id="1591" sell_mode="online"  organizer_company_id="1" title="Theater">
            <event event_date="2019-07-31T20:00:00" event_id="1642" sell_from="2017-06-26T00:00:00"
            sell_to="2019-07-31T19:50:00" sold_out="false">
                <zone zone_id="186" capacity="2" max_price="75.00" name="Amfiteatre" numbered="true" />
                <zone zone_id="186" capacity="16" max_price="75.00" name="Amfiteatre" numbered="false" />
            </event>
        </base_event>
    </output>
</eventList>""")


@pytest.fixture
def dict_1():
    return {
        '@base_event_id': '291',
        '@sell_mode': 'online',
        '@title': 'Concert',
        'event': {
            '@event_date': '2019-06-30T21:00:00',
            '@event_id': '291',
            '@sell_from': '2014-07-01T00:00:00',
            '@sell_to': '2019-06-30T20:00:00',
            '@sold_out': 'false',
            'zone': [
                {
                    '@zone_id': '40',
                    '@capacity': '243',
                    '@max_price': '20.00',
                    '@name': 'Platea',
                    '@numbered': 'true'
                },
                {
                    '@zone_id': '38',
                    '@capacity': '100',
                    '@max_price': '0.00',
                    '@name': 'test',
                    '@numbered': 'false'
                },
                {
                    '@zone_id': '30',
                    '@capacity': '90',
                    '@max_price': '0.00',
                    '@name': 'A28',
                    '@numbered': 'true'
                }
            ]
        }
    }


@pytest.fixture
def dict_2():
    return {
        '@base_event_id': '322',
        '@sell_mode': 'offline',
        '@organizer_company_id': '2',
        '@title': 'Theater',
        'event': {
            '@event_date': '2019-04-22T20:00:00',
            '@event_id': '1642',
            '@sell_from': '2017-01-01T00:00:00',
            '@sell_to': '2019-04-21T19:50:00',
            '@sold_out': 'false',
            'zone': {
                '@zone_id': '311',
                '@capacity': '2',
                '@max_price': '55.00',
                '@name': 'A42',
                '@numbered': 'true',
            },
        }
    }


@pytest.fixture
def dict_3():
    return {
        '@base_event_id': '1591',
        '@sell_mode': 'online',
        '@organizer_company_id': '1',
        '@title': 'Theater',
        'event': {
            '@event_date': '2019-07-31T20:00:00',
            '@event_id': '1642',
            '@sell_from': '2017-06-26T00:00:00',
            '@sell_to': '2019-07-31T19:50:00',
            '@sold_out': 'false',
            'zone': [
                {
                    '@zone_id': '186',
                    '@capacity': '2',
                    '@max_price': '75.00',
                    '@name': 'Amfiteatre',
                    '@numbered': 'true',
                },
                {
                    '@zone_id': '186',
                    '@capacity': '16',
                    '@max_price': '75.00',
                    '@name': 'Amfiteatre',
                    '@numbered': 'false',
                }
            ]
        }
    }


@pytest.fixture
def dicts(dict_1, dict_2, dict_3):
    return [dict_1, dict_2, dict_3]


@pytest.fixture
def event_1(dict_1):
    data = external_api_client._rename_keys(dict_1)
    return BaseEvent(**data)


@pytest.fixture
def event_2(dict_2):
    data = external_api_client._rename_keys(dict_2)
    return BaseEvent(**data)


@pytest.fixture
def event_3(dict_3):
    data = external_api_client._rename_keys(dict_3)
    return BaseEvent(**data)


@pytest.fixture
def base_events(event_1, event_2, event_3):
    return [event_1, event_2, event_3]


@pytest.fixture
def mocked_requests_get(mocker):
    return mocker.patch('requests.get')
