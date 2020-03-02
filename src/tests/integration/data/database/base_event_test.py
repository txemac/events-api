from datetime import datetime

from data.database import Zone
from data.database.base_event import BaseEvent
from data.database.event import Event
from data.schemas import BaseEventCreate


def test_create(session, data_base_event):
    count_base_event_1 = session.query(BaseEvent).count()
    count_event_1 = session.query(Event).count()
    count_zone_1 = session.query(Zone).count()
    data = BaseEventCreate(**data_base_event)
    base_event = BaseEvent.create(
        db_session=session,
        data=data,
    )
    count_base_event_2 = session.query(BaseEvent).count()
    count_event_2 = session.query(Event).count()
    count_zone_2 = session.query(Zone).count()
    assert count_base_event_1 + 1 == count_base_event_2
    assert count_event_1 + 1 == count_event_2
    assert count_zone_1 + 1 == count_zone_2

    assert base_event.base_event_id == data_base_event['base_event_id']
    assert base_event.sell_mode == data_base_event['sell_mode']
    assert base_event.title == data_base_event['title']
    assert base_event.organizer_company_id == data_base_event['organizer_company_id']
    assert base_event.event.event_id == data_base_event['event']['event_id']
    assert base_event.event.event_date == datetime.strptime(data_base_event['event']['event_date'], '%Y-%m-%dT%H:%M:%S')
    assert base_event.event.sell_from == datetime.strptime(data_base_event['event']['sell_from'], '%Y-%m-%dT%H:%M:%S')
    assert base_event.event.sell_to == datetime.strptime(data_base_event['event']['sell_to'], '%Y-%m-%dT%H:%M:%S')
    assert base_event.event.sold_out is data_base_event['event']['sold_out']
    assert base_event.event.zone[0].zone_id == data_base_event['event']['zone'][0]['zone_id']
    assert base_event.event.zone[0].name == data_base_event['event']['zone'][0]['name']
    assert base_event.event.zone[0].capacity == data_base_event['event']['zone'][0]['capacity']
    assert base_event.event.zone[0].max_price == data_base_event['event']['zone'][0]['max_price']
    assert base_event.event.zone[0].numbered is data_base_event['event']['zone'][0]['numbered']
