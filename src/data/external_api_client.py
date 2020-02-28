import json
import os
from typing import Dict
from typing import List

import requests
import xmltodict

from data.schemas import BaseEvent

"""
External API client
"""


class ExternalAPIClient:

    @staticmethod
    def get_base_events() -> List[BaseEvent]:
        """
        Get info about events from external API.

        :return Dict: events
        """
        response = requests.get(url=os.getenv('EXTERNAL_API_URL'))
        dicts = ExternalAPIClient._xml_to_dict(xml=response.text)
        dicts = dicts['eventList']['output']['base_event']
        dicts = [ExternalAPIClient._rename_keys(d) for d in dicts]
        result = ExternalAPIClient._parse_text_to_base_events(dicts=dicts)
        return result

    @staticmethod
    def _parse_text_to_base_events(
            dicts: List[Dict]
    ) -> List[BaseEvent]:
        """
        Parse dictionary to base events model.

        :param List dicts: events
        :return List: events
        """
        return [BaseEvent(**item) for item in dicts]

    @staticmethod
    def _xml_to_dict(
            xml: str,
    ) -> Dict:
        """
        Parse xml text to a dictionary.

        :param str xml: xml
        :return Dict: dictionary
        """
        aux = dict(xmltodict.parse(xml))
        return json.loads(json.dumps(aux))

    @staticmethod
    def _rename_keys(
            d: Dict
    ) -> Dict:
        """
        Delete the chars @ at keys.
        Convert to List the parameter zone with only 1 element.

        :param Dict d: dict
        :return Dict: dict
        """
        new = {}
        for k, v in d.items():
            new_v = v
            if k == 'zone' and v and not isinstance(v, list):
                v = [v]
            if isinstance(v, dict):
                new_v = ExternalAPIClient._rename_keys(v)
            elif isinstance(v, list):
                new_v = list()
                for x in v:
                    new_v.append(ExternalAPIClient._rename_keys(x))
            new[k.replace('@', '')] = new_v
        return new
