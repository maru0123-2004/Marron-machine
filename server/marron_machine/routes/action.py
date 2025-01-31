from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from ..models.db.action import ActionModule
from .auth import get_user
from ..models.db import User as UserDB, Action as ActionDB, Target as TargetDB
from ..models.response.action import Action
from ..models.response.user import User
from ..models.response.target import Target
from ..models.response.history import History
from ..models.request.action import ActionCreate, ActionUpdate
from ..exceptions import APIError, NotFound
from ..action.ping import search_host_ping

router=APIRouter(tags=["Action"])

@router.get("/", response_model=List[Action])
async def gets(user:UserDB=Depends(get_user)):
    await user.fetch_related("actions")
    return user.actions

@router.post("/", response_model=Action)
async def create(action: ActionCreate,user:UserDB=Depends(get_user)):
    action_db=await ActionDB.create(**action.model_dump())
    await action_db.owners.add(user)
    return action_db

@router.put("/{action_id}", response_model=Action)
async def update(action_id: UUID, action:ActionUpdate, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first()
    if action_db is None:
        raise NotFound()
    action_db.update_from_dict(action.model_dump(exclude_unset=True))
    await action_db.save()
    return action_db

@router.delete("/{action_id}", response_model=Action)
async def delete(action_id: UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first()
    if action_db is None:
        raise NotFound()
    await action_db.delete()
    return action_db

@router.get("/{action_id}/owner", response_model=List[User])
async def get_owner(action_id: UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first().prefetch_related("owners")
    if action_db is None:
        raise NotFound()
    return action_db.owners

@router.put("/{action_id}/owner", response_model=List[User])
async def add_owner(action_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first()
    if action_db is None:
        raise NotFound()
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await action_db.owners.add(owner)
    await action_db.fetch_related("owners")
    return action_db.owners

@router.delete("/{action_id}/owner", response_model=List[User])
async def del_owner(action_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first().prefetch_related("owners")
    if action_db is None:
        raise NotFound()
    if len(action_db.owners) <= 1:
        raise APIError(detail="Cant delete only you")
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await action_db.owners.remove(owner)
    await action_db.fetch_related("owners")
    return action_db.owners

@router.get("/{action_id}/target", response_model=List[Target])
async def get_target(action_id: UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first().prefetch_related("targets")
    if action_db is None:
        raise NotFound()
    return action_db.targets

@router.put("/{action_id}/target", response_model=List[Target])
async def add_target(action_id: UUID, target_id:UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first()
    if action_db is None:
        raise NotFound()
    target=await TargetDB.get_or_none(id=target_id)
    if target is None:
        raise NotFound(detail="Target Not found")
    await action_db.targets.add(target)
    await action_db.fetch_related("targets")
    return action_db.targets

@router.delete("/{action_id}/target", response_model=List[Target])
async def del_target(action_id: UUID, target_id:UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first()
    if action_db is None:
        raise NotFound()
    target=await TargetDB.get_or_none(id=target_id)
    if target is None:
        raise NotFound(detail="Target Not found")
    await action_db.targets.remove(target)
    await action_db.fetch_related("targets")
    return action_db.targets

@router.get("/{action_id}/history", response_model=List[History])
async def get_historys(action_id:UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first().prefetch_related("historys")
    if action_db is None:
        raise NotFound()
    return action_db.historys

@router.get("/{action_id}/history/{history_id}", response_model=List[History])
async def del_history(action_id:UUID, history_id:UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first()
    if action_db is None:
        raise NotFound()
    history_db=await action_db.historys.filter(id=history_id).first()
    if history_db is None:
        raise NotFound(detail="History not found")
    await history_db.delete()
    await action_db.fetch_related("historys")
    return action_db.historys

@router.post("/{action_id}/run")
async def run_once(action_id: UUID, user:UserDB=Depends(get_user)):
    action_db=await user.actions.filter(id=action_id).first().prefetch_related("targets__relays")
    if action_db is None:
        raise NotFound()
    if action_db.action_module == ActionModule.collect_ip:
        await search_host_ping(action_db)