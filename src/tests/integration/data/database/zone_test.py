from data.database.zone import Zone


def test_create(session, data_zone):
    count1 = session.query(Zone).count()
    data = Zone(**data_zone)
    Zone.create(
        db_session=session,
        data=data,
    )
    count2 = session.query(Zone).count()
    assert count1 + 1 == count2
