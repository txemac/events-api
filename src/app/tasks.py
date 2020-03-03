from data.api_client import feed_api_client
from data.database import BaseEvent


def job_read_feed(db_session):
    for base_event in feed_api_client.get_feed():
        BaseEvent.create_or_update(db_session=db_session, base_event=base_event)
