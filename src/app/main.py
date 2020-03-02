from typing import Dict

from fastapi import FastAPI

from app.api_v1_events import api_v1_events
from data.database import Base
from data.database import engine

Base.metadata.create_all(bind=engine)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
