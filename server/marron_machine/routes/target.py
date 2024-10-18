from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
import tortoise
import tortoise.exceptions

from ..routes.auth import get_user
from ..exceptions import APIError, NotFound
from ..models.request.target import TargetCreate
from ..models.response.target import Target
from ..models.db import Target as TargetDB, User as UserDB

router=APIRouter(tags=["Target"])

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
    