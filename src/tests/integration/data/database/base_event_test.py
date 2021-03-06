from datetime import datetime

import pytest

from data.database import BaseEvent
from data.database import Event
from data.database import Zone
from data.schemas import BaseEventCreate


def test_create(session, data_base_event):
    count_base_event_1 = session.query(BaseEvent).count()
    count_event_1 = session.query(Event).count()
    count_zone_1 = session.query(Zone).count()
    data = BaseEventCreate(**data_base_event)
    BaseEvent.create_or_update(
        db_session=session,
        base_event=data,
    )
    count_base_event_2 = session.query(BaseEvent).count()
    count_event_2 = session.query(Event).count()
    count_zone_2 = session.query(Zone).count()
    assert count_base_event_1 + 1 == count_base_event_2
    assert count_event_1 + 1 == count_event_2
    assert count_zone_1 + 1 == count_zone_2

    base_event_db = session.query(BaseEvent).get(data_base_event['base_event_id'])
    assert base_event_db.base_event_id == data_base_event['base_event_id']
    assert base_event_db.sell_mode == data_base_event['sell_mode']
    assert base_event_db.title == data_base_event['title']
    assert base_event_db.organizer_company_id == data_base_event['organizer_company_id']
    assert base_event_db.event.event_id == data_base_event['event']['event_id']
    assert base_event_db.event.event_date == datetime.strptime(data_base_event['event']['event_date'], '%Y-%m-%dT%H:%M:%S')
    assert base_event_db.event.sell_from == datetime.strptime(data_base_event['event']['sell_from'], '%Y-%m-%dT%H:%M:%S')
    assert base_event_db.event.sell_to == datetime.strptime(data_base_event['event']['sell_to'], '%Y-%m-%dT%H:%M:%S')
    assert base_event_db.event.sold_out is data_base_event['event']['sold_out']
    assert base_event_db.event.zone[0].zone_id == data_base_event['event']['zone'][0]['zone_id']
    assert base_event_db.event.zone[0].name == data_base_event['event']['zone'][0]['name']
    assert base_event_db.event.zone[0].capacity == data_base_event['event']['zone'][0]['capacity']
    assert base_event_db.event.zone[0].max_price == data_base_event['event']['zone'][0]['max_price']
    assert base_event_db.event.zone[0].numbered is data_base_event['event']['zone'][0]['numbered']


def test_get_events_empty(session):
    assert BaseEvent.get_events(db_session=session) == []


@pytest.mark.parametrize('offline, expected',
                         [(True, 3),
                          (False, 2)])
def test_get_events_offline(session, scenario, offline, expected):
    assert len(BaseEvent.get_events(db_session=session, offline=offline)) == expected


@pytest.mark.parametrize('start_date, end_date, expected',
                         [('1982-04-25', '1983-04-25', 0),
                          ('2019-06-30', '2019-06-30', 1),
                          ('2019-04-21', '2019-04-23', 0),
                          ('2019-07-29', '2019-08-01', 1),
                          ('2019-06-30', '2019-08-30', 2),
                          ('2019-03-30', '2019-09-30', 2)])
def test_get_events_date_range(session, scenario, start_date, end_date, expected):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    assert len(BaseEvent.get_events(db_session=session, start_date=start_date, end_date=end_date)) == expected
