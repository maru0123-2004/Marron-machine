from fastapi import APIRouter, BackgroundTasks
import asyncio

router=APIRouter(tags=["Runner"])

async def _runner():
    print("start", flush=True)
    await asyncio.sleep(10)
    print("end", flush=True)

@router.post("/now")
async def exec_now(background_tasks: BackgroundTasks):
    background_tasks.add_task(_runner)