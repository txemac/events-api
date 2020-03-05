from typing import Dict

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from pytz import utc

from app import responder
from app.api_v1_events import api_v1_events
from app.tasks import job_read_feed
from data.database import Base
from data.database import engine

Base.metadata.create_all(bind=engine)


def create_app() -> Flask:
    api = Flask(__name__)

    api.register_blueprint(api_v1_events)

    # scheduler
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=utc)
    scheduler.add_job(job_read_feed, 'interval', minutes=5)
    scheduler.start()

    return api


app = create_app()


@app.route(rule='/_health', methods=['GET'])
def get_health() -> Dict:
    return responder.generate_get()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
