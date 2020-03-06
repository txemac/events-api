from typing import Dict

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from pytz import utc

from app.api_v1_events import api_v1_events
from app.tasks import job_read_feed
from data.database import Base
from data.database import engine

Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    api = FastAPI(
        title='Events API'
    )

    api.include_router(api_v1_events, prefix='/api/v1/events', tags=['events'])

    # scheduler
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=utc)
    scheduler.add_job(job_read_feed, 'interval', minutes=5)
    scheduler.start()

    return api


app = create_app()


@app.get('/_health', status_code=200)
def get_health() -> Dict:
    return dict(status='OK')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
