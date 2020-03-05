from datetime import datetime

from flask import Blueprint
from flask import request

from app import responder
from data.database import BaseEvent
from data.serializer.base_event import BaseEventSerializer

api_v1_events = Blueprint('api_v1_events', __name__, url_prefix='/api/v1/events')


@api_v1_events.route('', methods=['GET'])
def get_events():
    args = request.args
    start_date = args.get('start_date')
    if start_date is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = args.get('end_date')
    if end_date is not None:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    offline = True if args.get('offline') == 'true' else False

    result = BaseEvent.get_events(start_date=start_date, end_date=end_date, offline=offline)

    return responder.generate_get(
        data=[BaseEventSerializer.serialize(base_event=base_event) for base_event in result]
    )
