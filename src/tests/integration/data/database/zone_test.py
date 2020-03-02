from data.database.zone import Zone
from data.schemas import ZoneCreate


def test__create(session, data_zone):
    count1 = session.query(Zone).count()
    data = ZoneCreate(**data_zone)
    Zone._create(
        db_session=session,
        data=data,
    )
    count2 = session.query(Zone).count()
    assert count1 + 1 == count2


def test__get_by_id_ok(session, new_zone):
    assert Zone._get_by_id(db_session=session, zone_id=new_zone.zone_id) is not None


def test__get_by_id_not_exists(session):
    assert Zone._get_by_id(db_session=session, zone_id=9999) is None


def test_get_or_create_get(session, new_zone):
    count1 = session.query(Zone).count()
    zone_db = Zone.get_or_create(
        db_session=session,
        zone=new_zone,
    )
    count2 = session.query(Zone).count()
    assert count1 == count2
    assert new_zone == zone_db


def test_get_or_create_create(session, new_zone_create):
    count1 = session.query(Zone).count()
    Zone.get_or_create(
        db_session=session,
        zone=new_zone_create,
    )
    count2 = session.query(Zone).count()
    assert count1 + 1 == count2
