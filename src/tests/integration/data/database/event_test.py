from datetime import datetime

from data.database import Zone
from data.database.event import Event
from data.schemas import EventCreate


def test__create(session, data_event):
    count_event_1 = session.query(Event).count()
    count_zone_1 = session.query(Zone).count()
    data = EventCreate(**data_event)
    event = Event._create(
        db_session=session,
        data=data,
    )
    count_event_2 = session.query(Event).count()
    count_zone_2 = session.query(Zone).count()
    assert count_event_1 + 1 == count_event_2
    assert count_zone_1 + 1 == count_zone_2

    assert event.event_id == data_event['event_id']
    assert event.event_date == datetime.strptime(data_event['event_date'], '%Y-%m-%dT%H:%M:%S')
    assert event.sell_from == datetime.strptime(data_event['sell_from'], '%Y-%m-%dT%H:%M:%S')
    assert event.sell_to == datetime.strptime(data_event['sell_to'], '%Y-%m-%dT%H:%M:%S')
    assert event.sold_out is data_event['sold_out']
    assert event.zone[0].zone_id == data_event['zone'][0]['zone_id']
    assert event.zone[0].name == data_event['zone'][0]['name']
    assert event.zone[0].capacity == data_event['zone'][0]['capacity']
    assert event.zone[0].max_price == data_event['zone'][0]['max_price']
    assert event.zone[0].numbered is data_event['zone'][0]['numbered']


def test__get_by_id_ok(session, new_event):
    assert Event._get_by_id(db_session=session, event_id=new_event.event_id) is not None


def test__get_by_id_not_exists(session):
    assert Event._get_by_id(db_session=session, event_id=9999) is None


def test_get_or_create_get(session, new_event):
    count1 = session.query(Event).count()
    event_db = Event.get_or_create(
        db_session=session,
        event=new_event,
    )
    count2 = session.query(Event).count()
    assert count1 == count2
    assert new_event == event_db


def test_get_or_create_create(session, new_event_create):
    count1 = session.query(Event).count()
    Event.get_or_create(
        db_session=session,
        event=new_event_create,
    )
    count2 = session.query(Event).count()
    assert count1 + 1 == count2
