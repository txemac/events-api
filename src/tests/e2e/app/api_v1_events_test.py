# import pytest
# from starlette.status import HTTP_200_OK
#
#
# def test_get_events_none(client, mocked_requests_get, xml):
#     mocked_requests_get.return_value.text = xml
#     response = client.get(f"/api/v1/events?start_date=1982-04-25&end_date=1982-04-15")
#     assert response.status_code == HTTP_200_OK
#     assert response.json() == []
#
#
# @pytest.mark.parametrize('url, expected',
#                          [(f"/api/v1/events", 2),
#                           (f"/api/v1/events?offline=false", 2),
#                           (f"/api/v1/events?offline=true", 3),
#                           (f"/api/v1/events?start_date=2010-01-01", 2),
#                           (f"/api/v1/events?start_date=2010-01-01&offline=false", 2),
#                           (f"/api/v1/events?start_date=2019-07-01&offline=false", 1),
#                           (f"/api/v1/events?start_date=2010-01-01&offline=true", 3),
#                           (f"/api/v1/events?start_date=2019-07-01&offline=true", 1),
#                           (f"/api/v1/events?end_date=2010-01-01", 0),
#                           (f"/api/v1/events?end_date=2010-01-01&offline=false", 0),
#                           (f"/api/v1/events?end_date=2019-07-01&offline=false", 1),
#                           (f"/api/v1/events?end_date=2010-01-01&offline=true", 0),
#                           (f"/api/v1/events?end_date=2019-07-01&offline=true", 2),
#                           (f"/api/v1/events?start_date=1982-04-25&end_date=1983-04-25&offline=false", 0),
#                           (f"/api/v1/events?start_date=2019-06-30&end_date=2019-06-30&offline=false", 1),
#                           (f"/api/v1/events?start_date=2019-04-21&end_date=2019-04-23&offline=false", 0),
#                           (f"/api/v1/events?start_date=2019-04-21&end_date=2019-04-23&offline=true", 1),
#                           (f"/api/v1/events?start_date=2019-07-29&end_date=2019-08-01&offline=false", 1),
#                           (f"/api/v1/events?start_date=2019-06-30&end_date=2019-08-30&offline=false", 2),
#                           (f"/api/v1/events?start_date=2019-03-30&end_date=2019-09-30&offline=false", 2),
#                           (f"/api/v1/events?start_date=2019-03-30&end_date=2019-09-30&offline=true", 3)])
# def test_get_events_ok(client, mocked_requests_get, xml, url, expected):
#     mocked_requests_get.return_value.text = xml
#     response = client.get(url)
#     assert response.status_code == HTTP_200_OK
#     assert len(response.json()) == expected
