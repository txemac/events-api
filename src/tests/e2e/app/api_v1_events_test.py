import pytest
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from data.database import BaseEvent


def test_get_events_none(client):
    response = client.get(f"/api/v1/events?start_date=1982-04-25&end_date=1982-04-15")
    assert response.status_code == HTTP_200_OK
    assert response.json() == []


@pytest.mark.parametrize('url, expected',
                         [(f"/api/v1/events", 2),
                          (f"/api/v1/events?offline=false", 2),
                          (f"/api/v1/events?offline=true", 3),
                          (f"/api/v1/events?start_date=2010-01-01", 2),
                          (f"/api/v1/events?start_date=2010-01-01&offline=false", 2),
                          (f"/api/v1/events?start_date=2019-07-01&offline=false", 1),
                          (f"/api/v1/events?start_date=2010-01-01&offline=true", 3),
                          (f"/api/v1/events?start_date=2019-07-01&offline=true", 2),
                          (f"/api/v1/events?end_date=2010-01-01", 0),
                          (f"/api/v1/events?end_date=2010-01-01&offline=false", 0),
                          (f"/api/v1/events?end_date=2019-07-01&offline=false", 1),
                          (f"/api/v1/events?end_date=2010-01-01&offline=true", 0),
                          (f"/api/v1/events?end_date=2019-07-01&offline=true", 1),
                          (f"/api/v1/events?start_date=1982-04-25&end_date=1983-04-25&offline=false", 0),
                          (f"/api/v1/events?start_date=2019-06-30&end_date=2019-06-30&offline=false", 1),
                          (f"/api/v1/events?start_date=2019-04-21&end_date=2019-04-23&offline=false", 0),
                          (f"/api/v1/events?start_date=2019-04-21&end_date=2019-04-23&offline=true", 0),
                          (f"/api/v1/events?start_date=2019-07-29&end_date=2019-08-01&offline=false", 1),
                          (f"/api/v1/events?start_date=2019-06-30&end_date=2019-08-30&offline=false", 2),
                          (f"/api/v1/events?start_date=2019-03-30&end_date=2019-09-30&offline=false", 2),
                          (f"/api/v1/events?start_date=2019-03-30&end_date=2019-09-30&offline=true", 3)])
def test_get_events_ok(client, scenario, xml, url, expected):
    response = client.get(url)
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == expected


def test_post_events(client, mocked_requests_get, xml, session):
    mocked_requests_get.return_value.text = xml

    count1 = session.query(BaseEvent).count()
    response = client.post(f"/api/v1/events/feed")
    assert response.status_code == HTTP_201_CREATED
    count2 = session.query(BaseEvent).count()
    assert count1 + 3 == count2
