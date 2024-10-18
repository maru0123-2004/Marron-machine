from fastapi import APIRouter, BackgroundTasks, Depends
import asyncio
from ..routes.auth import get_user
from ..models.db import User as UserDB

router=APIRouter(tags=["Runner"])

async def _runner():
    while 1:
        await _runner_once()

async def _runner_once():
    print("start", flush=True)
    await asyncio.sleep(10)
    print("end", flush=True)

@router.post("/now")
async def exec_now(background_tasks: BackgroundTasks, user:UserDB=Depends(get_user)):
    background_tasks.add_task(_runner_once)