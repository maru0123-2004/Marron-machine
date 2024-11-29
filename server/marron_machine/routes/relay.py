from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from .auth import get_user
from ..models.db import User as UserDB, Relay as RelayDB
from ..models.response.relay import Relay
from ..models.response.user import User
from ..models.request.relay import RelayCreate, RelayUpdate
from ..exceptions import APIError, NotFound

router=APIRouter(tags=["Relay"])

@router.get("/", response_model=List[Relay])
async def gets(user:UserDB=Depends(get_user)):
    await user.fetch_related("relays")
    return user.relays

@router.post("/", response_model=Relay)
async def create(relay: RelayCreate,user:UserDB=Depends(get_user)):
    relay_db=await RelayDB.create(**relay.model_dump())
    await relay_db.owners.add(user)
    return relay_db

@router.put("/{relay_id}", response_model=Relay)
async def update(relay_id: UUID, relay:RelayUpdate, user:UserDB=Depends(get_user)):
    relay_db=await user.relays.filter(id=relay_id).first()
    if relay_db is None:
        raise NotFound()
    relay_db.update_from_dict(relay.model_dump(exclude_unset=True))
    await relay_db.save()
    return relay_db

@router.delete("/{relay_id}", response_model=Relay)
async def delete(relay_id: UUID, user:UserDB=Depends(get_user)):
    relay_db=await user.relays.filter(id=relay_id).first()
    if relay_db is None:
        raise NotFound()
    await relay_db.delete()
    return relay_db

@router.get("/{relay_id}/owner", response_model=List[User])
async def get_owner(relay_id: UUID, user:UserDB=Depends(get_user)):
    relay_db=await user.relays.filter(id=relay_id).first().prefetch_related("owners")
    if relay_db is None:
        raise NotFound()
    return relay_db.owners

@router.put("/{relay_id}/owner", response_model=List[User])
async def add_owner(relay_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    relay_db=await user.relays.filter(id=relay_id).first()
    if relay_db is None:
        raise NotFound()
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await relay_db.owners.add(owner)
    await relay_db.fetch_related("owners")
    return relay_db.owners

@router.delete("/{relay_id}/owner", response_model=List[User])
async def del_owner(relay_id: UUID, user_id:UUID, user:UserDB=Depends(get_user)):
    relay_db=await user.relays.filter(id=relay_id).first().prefetch_related("owners")
    if relay_db is None:
        raise NotFound()
    if len(relay_db.owners) <= 1:
        raise APIError(detail="Cant delete only you")
    owner=await UserDB.get_or_none(id=user_id)
    if owner is None:
        raise NotFound(detail="Owner Not found")
    await relay_db.owners.remove(owner)
    await relay_db.fetch_related("owners")
    return relay_db.owners