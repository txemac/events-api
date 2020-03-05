from typing import Dict
from typing import Union

from data.schemas import EventDB
from data.serializer.zone import ZoneSerializer


class EventSerializer:

    @staticmethod
    def serializer(
            event: EventDB
    ) -> Dict[str, Union[str, int]]:
        return dict(
            event_id=event.event_id,
            event_date=event.event_date,
            sell_from=event.sell_from,
            sell_to=event.sell_to,
            sold_out=event.sold_out,
            zone=[ZoneSerializer.serialize(zone=zone) for zone in event.zone],
        )
