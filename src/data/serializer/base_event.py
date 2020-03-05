from typing import Dict
from typing import Union

from data.schemas import BaseEventDB
from data.serializer.event import EventSerializer


class BaseEventSerializer:

    @staticmethod
    def serialize(
            base_event: BaseEventDB
    ) -> Dict[str, Union[str, int]]:
        return dict(
            base_event_id=base_event.base_event_id,
            event=EventSerializer.serializer(event=base_event.event),
            sell_mode=base_event.sell_mode,
            title=base_event.title,
            organizer_company_id=base_event.organizer_company_id,
        )
