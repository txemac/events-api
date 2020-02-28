from datetime import date
from datetime import datetime
from typing import List

from data.schemas import BaseEvent


class Events:

    @staticmethod
    def get_events(
            events: List[BaseEvent],
            start_date: date,
            end_date: date,
            offline: bool
    ) -> List[BaseEvent]:
        """
        Get event from

        :param List events: events
        :param date start_date: start date
        :param date end_date: end date
        :param bool offline: filter offline
        :return List: events
        """
        if offline is False:
            events = Events.filter_offline(events=events)

        result = Events.filter_date_range(events=events, start_date=start_date, end_date=end_date)

        return result

    @staticmethod
    def filter_offline(
            events: List[BaseEvent]
    ) -> List[BaseEvent]:
        """
        Filter the event NOT offline.

        :param List events: events
        :return List: events
        """
        return [event for event in events if event.sell_mode.lower() == 'online']

    @staticmethod
    def filter_date_range(
            events: List[BaseEvent],
            start_date: date,
            end_date: date,
    ) -> List[BaseEvent]:
        """
        Filter event by date range.

        :param List events: events
        :param date start_date: start date
        :param date end_date: end date
        :return List: events
        """
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        return [event for event in events if start_datetime <= event.event.event_date <= end_datetime]
