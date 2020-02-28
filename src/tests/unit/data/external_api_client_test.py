from data.external_api_client import ExternalAPIClient
from tests.utils import assert_dicts


def test_get_base_events(mocker, xml, events):
    mocked_requests_get = mocker.patch('requests.get')
    mocked_requests_get.return_value.text = xml
    assert ExternalAPIClient.get_base_events() == events


def test__parse_text_to_base_events(xml, events):
    dicts = ExternalAPIClient._xml_to_dict(xml=xml)['eventList']['output']['base_event']
    dicts = [ExternalAPIClient._rename_keys(d) for d in dicts]
    result = ExternalAPIClient._parse_text_to_base_events(dicts=dicts)
    assert result == events


def test__text_to_dict(xml, dicts):
    result = ExternalAPIClient._xml_to_dict(xml=xml)['eventList']['output']['base_event']
    assert isinstance(result, list)
    assert result == dicts


def test__rename_keys():
    data = {
        '@base_event_id': '322',
        '@title': 'Theater',
        'event': {
            '@event_date': '2019-04-22T20:00:00',
            '@sold_out': 'false',
            'zone': [
                {
                    '@zone_id': '186',
                },
                {
                    '@zone_id': '186',
                }
            ]
        }
    }
    expected = {
        'base_event_id': '322',
        'title': 'Theater',
        'event': {
            'event_date': '2019-04-22T20:00:00',
            'sold_out': 'false',
            'zone': [
                {
                    'zone_id': '186',
                },
                {
                    'zone_id': '186',
                }
            ]
        }
    }
    result = ExternalAPIClient._rename_keys(data)
    assert_dicts(result=result, expected=expected)
