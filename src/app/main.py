from typing import Dict

from fastapi import FastAPI

from app.api_v1_events import api_v1_events


def create_app() -> FastAPI:
    api = FastAPI(
        title='Events API'
    )

    api.include_router(api_v1_events, prefix='/api/v1/events', tags=['events'])

    return api


app = create_app()


@app.get('/_health', status_code=200)
def get_health() -> Dict:
    return dict(status='OK')
