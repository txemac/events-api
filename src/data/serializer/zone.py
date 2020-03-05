from typing import Dict
from typing import Union

from data.schemas import ZoneDB


class ZoneSerializer:

    @staticmethod
    def serialize(
            zone: ZoneDB
    ) -> Dict[str, Union[str, int]]:
        return dict(
            zone_id=zone.zone_id,
            name=zone.name,
            capacity=zone.capacity,
            max_price=zone.max_price,
            numbered=zone.numbered,
        )
