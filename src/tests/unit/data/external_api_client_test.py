from data import external_api_client
from tests.utils import assert_dicts


def test_get_base_events(mocked_requests_get, xml, base_events):
    mocked_requests_get.return_value.text = xml
    assert external_api_client.get_base_events() == base_events


def test__parse_text_to_base_events(xml, base_events):
    dicts = external_api_client._xml_to_dict(xml=xml)['eventList']['output']['base_event']
    dicts = [external_api_client._rename_keys(d) for d in dicts]
    result = external_api_client._parse_text_to_base_events(dicts=dicts)
    assert result == base_events


def test__xml_to_dict(xml, dicts):
    result = external_api_client._xml_to_dict(xml=xml)['eventList']['output']['base_event']
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
    result = external_api_client._rename_keys(data)
    assert_dicts(result=result, expected=expected)
