import contextlib
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .models.db.target import Target

from .exceptions import APIError, Forbidden, NotFound
from .config import Settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def custom_generate_unique_id(route: APIRouter):
    return f"{f'{route.tags[0]}-'if len(route.tags) else ''}{route.name}"

from tortoise.contrib.fastapi import RegisterTortoise
from .db import DB_CONFIG

scheduler=AsyncIOScheduler()

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    #from .routes.target import _runner_once
    async with RegisterTortoise(app, config=DB_CONFIG, use_tz=True, timezone=settings.TZ):
        # scheduler.start()
        # for target in await Target.all():
        #     scheduler.add_job(_runner_once, target.interval)
        #     target.last_exec=datetime.now(ZoneInfo(settings.TZ))
        yield

app = FastAPI(
    title="Marron-machine",
    description="Marron-machine",
    version="0.0.1",
    root_path="/api/v1",
    generate_unique_id_function=custom_generate_unique_id,
    responses={400: {"model": APIError}, 
               401: {"model": Forbidden},
               404: {"model": NotFound}},
    lifespan=lifespan
)

@app.exception_handler(APIError)
async def api_error_handler(request: Request, error: APIError):
    raise HTTPException(error.status_code, detail=error.detail)

settings=Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],
    allow_credentials=True,
    allow_methods=["*",],
    allow_headers=["*",],
)

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET)

from .routes import router
app.include_router(router)

if settings.SERVE_STATIC is not None:
    with open(f"{settings.SERVE_STATIC}/index.html", "r") as index_file:
        index=index_file.read()
    import os

    @app.get('/{full_path:path}')
    async def spa(full_path:str):
        if full_path=="": full_path="index.html"
        full_path = os.path.normpath(f"{settings.SERVE_STATIC}/{full_path}")
        if not full_path.startswith(settings.SERVE_STATIC):
            raise Forbidden(status_code=403, detail="Forbidden")
        if os.path.exists(full_path):
            return FileResponse(full_path)
        else:
            return HTMLResponse(index)