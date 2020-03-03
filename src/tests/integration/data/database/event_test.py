from datetime import datetime

from data.database import Event
from data.database import Zone
from data.schemas import EventCreate
from data.schemas import ZoneCreate


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


def test__update(session, new_event):
    count_event_1 = session.query(Event).count()
    count_zone_1 = session.query(Zone).count()
    update_zone_data = ZoneCreate(
        zone_id=new_event.zone[0].zone_id,
        name=new_event.zone[0].name + 'update',
        capacity=new_event.zone[0].capacity + 1,
        max_price=new_event.zone[0].max_price + 1,
        numbered=not new_event.zone[0].numbered,
    )
    Zone.create_or_update(db_session=session, zone=update_zone_data)
    new_data = EventCreate(
        event_id=new_event.event_id,
        event_date='2111-11-11T11:11:11',
        sell_from='2111-11-11T11:11:11',
        sell_to='2111-11-11T11:11:11',
        sold_out=not new_event.sold_out,
        zone=new_event.zone,
    )
    event = Event._update(
        db_session=session,
        event_db=new_event,
        data=new_data,
    )
    count_event_2 = session.query(Event).count()
    count_zone_2 = session.query(Zone).count()
    assert count_event_1 == count_event_2
    assert count_zone_1 == count_zone_2

    assert event.event_id == new_data.event_id
    assert event.event_date == new_data.event_date
    assert event.sell_from == new_data.sell_from
    assert event.sell_to == new_data.sell_to
    assert event.sold_out is new_data.sold_out
    assert event.zone[0].zone_id == update_zone_data.zone_id
    assert event.zone[0].name == update_zone_data.name
    assert event.zone[0].capacity == update_zone_data.capacity
    assert event.zone[0].max_price == update_zone_data.max_price
    assert event.zone[0].numbered is update_zone_data.numbered


def test__get_by_id_ok(session, new_event):
    assert Event._get_by_id(db_session=session, event_id=new_event.event_id) is not None


def test__get_by_id_not_exists(session):
    assert Event._get_by_id(db_session=session, event_id=9999) is None


def test_create_or_update_update(session, new_event):
    count1 = session.query(Event).count()
    update_zone_data = ZoneCreate(
        zone_id=new_event.zone[0].zone_id,
        name=new_event.zone[0].name + 'update',
        capacity=new_event.zone[0].capacity + 1,
        max_price=new_event.zone[0].max_price + 1,
        numbered=not new_event.zone[0].numbered,
    )
    Zone.create_or_update(db_session=session, zone=update_zone_data)
    new_data = EventCreate(
        event_id=new_event.event_id,
        event_date='2111-11-11T11:11:11',
        sell_from='2111-11-11T11:11:11',
        sell_to='2111-11-11T11:11:11',
        sold_out=not new_event.sold_out,
        zone=new_event.zone,
    )
    event_db = Event.create_or_update(
        db_session=session,
        event=new_data,
    )
    count2 = session.query(Event).count()
    assert count1 == count2
    assert new_event == event_db

    assert event_db.event_id == new_data.event_id
    assert event_db.event_date == new_data.event_date
    assert event_db.sell_from == new_data.sell_from
    assert event_db.sell_to == new_data.sell_to
    assert event_db.sold_out is new_data.sold_out
    assert event_db.zone[0].zone_id == update_zone_data.zone_id
    assert event_db.zone[0].name == update_zone_data.name
    assert event_db.zone[0].capacity == update_zone_data.capacity
    assert event_db.zone[0].max_price == update_zone_data.max_price
    assert event_db.zone[0].numbered is update_zone_data.numbered


def test_get_or_create_create(session, new_event_create):
    count1 = session.query(Event).count()
    Event.create_or_update(
        db_session=session,
        event=new_event_create,
    )
    count2 = session.query(Event).count()
    assert count1 + 1 == count2
