import pytest
from pydantic import ValidationError

from data.schemas import BaseEvent
from data.schemas import Event
from data.schemas import Zone


def test_zone_ok():
    assert Zone(
        zone_id=1,
        name='zone 1',
        capacity=17,
        max_price=123.45,
        numbered=True,
    ) is not None


@pytest.mark.parametrize('attr', ['zone_id', 'name', 'capacity', 'max_price', 'numbered'])
def test_zone_pop(data_zone, attr):
    data_zone.pop(attr)
    with pytest.raises(ValidationError):
        Zone(**data_zone)


@pytest.mark.parametrize('attr', ['zone_id', 'name', 'capacity', 'max_price', 'numbered'])
def test_zone_none(data_zone, attr):
    data_zone[attr] = None
    with pytest.raises(ValidationError):
        Zone(**data_zone)


@pytest.mark.parametrize('attr', ['zone_id', 'capacity', 'max_price'])
@pytest.mark.parametrize('value', ['hola', None])
def test_zone_not_number(data_zone, attr, value):
    data_zone[attr] = value
    with pytest.raises(ValidationError):
        Zone(**data_zone)


@pytest.mark.parametrize('value', ['hola', 17, None])
def test_zone_not_bool(data_zone, value):
    data_zone['numbered'] = value
    with pytest.raises(ValidationError):
        Zone(**data_zone)


def test_event_ok(new_zone):
    assert Event(
        event_id=1,
        event_date="1982-04-25T16:30:00",
        sell_from="1982-04-25T16:30:00",
        sell_to="1982-04-25T16:30:00",
        sold_out=False,
        zone=[new_zone],
    ) is not None


@pytest.mark.parametrize('attr', ['event_id', 'event_date', 'sell_from', 'sell_to', 'sold_out', 'zone'])
def test_event_pop(data_event, attr):
    data_event.pop(attr)
    with pytest.raises(ValidationError):
        Event(**data_event)


@pytest.mark.parametrize('attr', ['event_id', 'event_date', 'sell_from', 'sell_to', 'sold_out', 'zone'])
def test_event_none(data_event, attr):
    data_event[attr] = None
    with pytest.raises(ValidationError):
        Event(**data_event)


@pytest.mark.parametrize('value', ['hola', None])
def test_event_not_number(data_event, value):
    data_event['event_id'] = value
    with pytest.raises(ValidationError):
        Event(**data_event)


@pytest.mark.parametrize('value', ['hola', 17, None])
def test_event_not_bool(data_event, value):
    data_event['sold_out'] = value
    with pytest.raises(ValidationError):
        Zone(**data_event)


@pytest.mark.parametrize('value', ['hola', 17, None, '2020-01-01 12:34:56', '2020/01/01T12:34:56'])
@pytest.mark.parametrize('attr', ['event_date', 'sell_from', 'sell_to'])
def test_event_wrong_date(data_event, value, attr):
    data_event[attr] = value
    with pytest.raises(ValidationError):
        Zone(**data_event)


def test_base_event_ok(new_event):
    assert BaseEvent(
        base_event_id=1,
        sell_mode='offline',
        title='Test',
        organizer_company_id=12,
        event=new_event,
    ) is not None


@pytest.mark.parametrize('attr', ['base_event_id', 'sell_mode', 'title', 'event'])
def test_base_event_pop(data_base_event, attr):
    data_base_event.pop(attr)
    with pytest.raises(ValidationError):
        BaseEvent(**data_base_event)


@pytest.mark.parametrize('attr', ['base_event_id', 'sell_mode', 'title', 'event'])
def test_base_event_none(data_base_event, attr):
    data_base_event[attr] = None
    with pytest.raises(ValidationError):
        BaseEvent(**data_base_event)


@pytest.mark.parametrize('value', ['hola', None])
def test_base_event_not_number(data_base_event, value):
    data_base_event['base_event_id'] = value
    with pytest.raises(ValidationError):
        Event(**data_base_event)
