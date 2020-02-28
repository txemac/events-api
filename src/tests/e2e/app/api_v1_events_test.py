import pytest
from starlette.status import HTTP_200_OK


def test_get_events_none(client, mocked_requests_get, xml):
    mocked_requests_get.return_value.text = xml
    response = client.get(f"/api/v1/events?start_date=1982-04-25&end_date=1982-04-15")
    assert response.status_code == HTTP_200_OK
    assert response.json() == []


@pytest.mark.parametrize('start_date, end_date, offline, expected',
                         [('1982-04-25', '1983-04-25', 'false', 0),
                          ('2019-06-30', '2019-06-30', 'false', 1),
                          ('2019-04-21', '2019-04-23', 'false', 0),
                          ('2019-04-21', '2019-04-23', 'true', 1),
                          ('2019-07-29', '2019-08-01', 'false', 1),
                          ('2019-06-30', '2019-08-30', 'false', 2),
                          ('2019-03-30', '2019-09-30', 'false', 2),
                          ('2019-03-30', '2019-09-30', 'true', 3)])
def test_get_events_ok(client, mocked_requests_get, xml, start_date, end_date, offline, expected):
    mocked_requests_get.return_value.text = xml
    response = client.get(f"/api/v1/events?start_date={start_date}&end_date={end_date}&offline={offline}")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()) == expected
