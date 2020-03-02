from datetime import datetime

import pytest

from data import events


def test_filter_offline(mocked_requests_get, base_events):
    assert events.filter_offline(events=base_events) == [base_events[0], base_events[2]]


@pytest.mark.parametrize('start_date, end_date, expected',
                         [('1982-04-25', '1983-04-25', 0),
                          ('2019-06-30', '2019-06-30', 1),
                          ('2019-04-21', '2019-04-23', 1),
                          ('2019-07-29', '2019-08-01', 1),
                          ('2019-06-30', '2019-08-30', 2),
                          ('2019-03-30', '2019-09-30', 3)])
def test_filter_date_range(mocked_requests_get, base_events, start_date, end_date, expected):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    assert len(events.filter_date_range(
        events=base_events,
        start_date=start_date,
        end_date=end_date,
    )) == expected
