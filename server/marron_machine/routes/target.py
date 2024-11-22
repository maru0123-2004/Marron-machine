import asyncio
from datetime import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends
import tortoise
import tortoise.exceptions

from ..routes.auth import get_user
from ..exceptions import APIError, NotFound
from ..models.request.target import TargetCreate
from ..models.response.target import Target
from ..models.db import Target as TargetDB, User as UserDB
from ..models.db.target import TargetType

router=APIRouter(tags=["Target"])

async def _runner_once(target:TargetDB):
    if target.type == TargetType.dhcp_isc:
        pass
    await asyncio.sleep(10)

@router.get("/", response_model=List[Target])
async def gets(user:UserDB=Depends(get_user)):
    return await TargetDB.all()

@router.post("/", response_model=Target)
async def create(target:TargetCreate, user:UserDB=Depends(get_user)):
    try:
        return await TargetDB.create(**target.model_dump())
    except tortoise.exceptions.IntegrityError:
        raise APIError(detail="Cant create same type target")

@router.put("/{target_id}", response_model=Target)
async def update(target_id:UUID, url:str=None, interval:int=None, user:UserDB=Depends(get_user)):
    target=await TargetDB.get_or_none(id=target_id)
    if target is None:
        raise NotFound()
    if url is not None:
        target.url=url
    if interval is not None:
        target.interval=interval
    await target.save()
    return target

@router.delete("/{target_id}", response_model=Target)
async def delete(target_id:UUID, user:UserDB=Depends(get_user)):
    target=await TargetDB.get_or_none(id=target_id)
    if target is None:
        raise NotFound()
    await target.delete()
    return target

@router.post("/{target_id}/exec")
async def exec(background_tasks: BackgroundTasks, target_id:UUID, user:UserDB=Depends(get_user)):
    target=await TargetDB.get_or_none(id=target_id)
    if target is None:
        raise NotFound()
    background_tasks.add_task(_runner_once, target)