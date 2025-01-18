from typing import List
from uuid import UUID
import aiohttp
import ansible_runner
from fastapi import APIRouter, Depends

from .auth import get_user
from ..models.db import User as UserDB, Target as TargetDB, Relay as RelayDB, TargetRelay as TargetRelayDB
from ..models.response.target import Target
from ..models.response.user import User
from ..models.response.relay import Relay
from ..models.request.target import TargetCreate, TargetUpdate
from ..exceptions import APIError, NotFound

router=APIRouter(tags=["Target"])

async def check_runner():
    ansible_runner.interface.run_async(streamer="transmit")

@router.get("/", response_model=List[Target])
async def gets(user:UserDB=Depends(get_user)):
    await user.fetch_related("targets")
    return user.targets

@router.post("/", response_model=Target)
async def create(target: TargetCreate,user:UserDB=Depends(get_user)):
    target_db=await TargetDB.create(**target.model_dump())
    await target_db.owners.add(user)
    return target_db

@router.put("/{target_id}", response_model=Target)
async def update(target_id: UUID, target:TargetUpdate, user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first()
    if target_db is None:
        raise NotFound()
    target_db.update_from_dict(target.model_dump(exclude_unset=True))
    await target_db.save()
    return target_db

@router.delete("/{target_id}", response_model=Target)
async def delete(target_id: UUID, user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first()
    if target_db is None:
        raise NotFound()
    await target_db.delete()
    return target_db

@router.get("/{target_id}/owner", response_model=List[User])
async def get_owner(target_id: UUID, user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first().prefetch_related("owners")
    if target_db is None:
        raise NotFound()
    return target_db.owners

@router.put("/{target_id}/owner", response_model=List[User])
async def add_owner(target_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first()
    if target_db is None:
        raise NotFound()
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await target_db.owners.add(owner)
    await target_db.fetch_related("owners")
    return target_db.owners

@router.delete("/{target_id}/owner", response_model=List[User])
async def del_owner(target_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first().prefetch_related("owners")
    if target_db is None:
        raise NotFound()
    if len(target_db.owners) <= 1:
        raise APIError(detail="Cant delete only you")
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await target_db.owners.remove(owner)
    await target_db.fetch_related("owners")
    return target_db.owners

@router.get("/{target_id}/relay", response_model=List[Relay])
async def get_relays(target_id: UUID, user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first().prefetch_related("relays")
    if target_db is None:
        raise NotFound()
    return target_db.relays

@router.post("/{target_id}/relay", response_model=List[Relay])
async def set_relays(target_id: UUID, relay_ids:List[UUID], user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first()
    if target_db is None:
        raise NotFound()
    relay_dbs=[await RelayDB.get_or_none(id=relay_id) for relay_id in relay_ids]
    if None in relay_dbs:
        raise NotFound(detail="Some relay is not found")
    await target_db.relays.clear()
    for i, relay_db in enumerate(relay_dbs):
        await TargetRelayDB.create(relay=relay_db, target=target_db, order=i)
    await target_db.fetch_related("relays")
    return target_db.relays

@router.post("/{target_id}/ping", response_model=bool)
async def ping(target_id: UUID, user:UserDB=Depends(get_user)):
    target_db=await user.targets.filter(id=target_id).first()
    if target_db is None:
        raise NotFound()
    async with aiohttp.ClientSession() as session:
        for addr in target_db.addr.hosts():
            res=await session.get(f"http://{addr}:{target_db.conn_info.get('port',80)}/ping")
    return res.ok
