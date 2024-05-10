from fastapi import FastAPI, APIRouter
from .config import Settings

def custom_generate_unique_id(route: APIRouter):
    return f"{f'{route.tags[0]}-'if len(route.tags) else ''}{route.name}"

app = FastAPI(
    title="Marron-machine",
    description="Marron-machine",
    version="0.0.1",
    root_path="/api/v1",
    generate_unique_id_function=custom_generate_unique_id,
)

settings=Settings()

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET)

from .routes import router
app.include_router(router)

from .db import register_db
register_db(app)