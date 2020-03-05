from data.database import Zone
from data.schemas import ZoneCreate


def test__create(session, data_zone):
    count1 = session.query(Zone).count()
    data = ZoneCreate(**data_zone)
    zone = Zone._create(
        data=data,
    )
    count2 = session.query(Zone).count()
    assert count1 + 1 == count2

    assert zone.zone_id == data_zone['zone_id']
    assert zone.name == data_zone['name']
    assert zone.capacity == data_zone['capacity']
    assert zone.max_price == data_zone['max_price']
    assert zone.numbered is data_zone['numbered']


def test__update(session, new_zone):
    count1 = session.query(Zone).count()
    new_data = ZoneCreate(
        zone_id=new_zone.zone_id,
        name=new_zone.name + 'update',
        capacity=new_zone.capacity + 1,
        max_price=new_zone.max_price + 1,
        numbered=not new_zone.numbered,
    )
    zone = Zone._update(
        zone_db=new_zone,
        data=new_data,
    )
    count2 = session.query(Zone).count()
    assert count1 == count2

    assert zone.zone_id == new_data.zone_id
    assert zone.name == new_data.name
    assert zone.capacity == new_data.capacity
    assert zone.max_price == new_data.max_price
    assert zone.numbered is new_data.numbered


def test__get_by_id_ok(session, new_zone):
    assert Zone._get_by_id(zone_id=new_zone.zone_id) is not None


def test__get_by_id_not_exists(session):
    assert Zone._get_by_id(zone_id=9999) is None


def test_create_or_update_update(session, new_zone):
    count1 = session.query(Zone).count()
    new_data = ZoneCreate(
        zone_id=new_zone.zone_id,
        name=new_zone.name + 'update',
        capacity=new_zone.capacity + 1,
        max_price=new_zone.max_price + 1,
        numbered=not new_zone.numbered,
    )
    zone_db = Zone.create_or_update(
        zone=new_data,
    )
    count2 = session.query(Zone).count()
    assert count1 == count2
    assert new_zone == zone_db

    assert zone_db.zone_id == new_data.zone_id
    assert zone_db.name == new_data.name
    assert zone_db.capacity == new_data.capacity
    assert zone_db.max_price == new_data.max_price
    assert zone_db.numbered is new_data.numbered


def test_create_or_update_create(session, new_zone_create):
    count1 = session.query(Zone).count()
    Zone.create_or_update(
        zone=new_zone_create,
    )
    count2 = session.query(Zone).count()
    assert count1 + 1 == count2
