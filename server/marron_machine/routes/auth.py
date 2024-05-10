from fastapi.security import OAuth2AuthorizationCodeBearer
from ..config import Settings
from fastapi_sso.sso.google import GoogleSSO
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from ..db_models import Token as TokenDB
import secrets
from pydantic import BaseModel, EmailStr, ValidationError
from typing import List

class Token(BaseModel):
    id: str
    name: str
    email: EmailStr
    token:str

settings=Settings()

google_sso=GoogleSSO(
    client_id=settings.GOOGLE_ID,
    client_secret=settings.GOOGLE_SECRET
)

router=APIRouter(tags=["auth"])

@router.get("/login", response_class=RedirectResponse)
async def login():
    """Generate login url and redirect"""
    with google_sso:
        return await google_sso.get_login_redirect(redirect_uri=settings.CALLBACK_URL)

@router.get("/callback", response_class=RedirectResponse)
async def callback(request: Request):
    """Process login response from Google and return user info"""
    with google_sso:
        user = await google_sso.verify_and_process(request, redirect_uri=settings.CALLBACK_URL)
    token=await TokenDB.create(token=secrets.token_urlsafe(20), user_id=user.id)
    request.session.update(id=user.id, email=user.email, avater=user.picture, name=user.display_name, token=token.token)
    return RedirectResponse(url=settings.REDIRECT_URL)

@router.get("/token", response_model=Token)
async def token(request: Request):
    """Get infomation(and token) of user"""
    try:
        return Token.model_validate(request.session)
    except ValidationError:
        raise HTTPException(401, "Not authenticated")

oauth=OAuth2AuthorizationCodeBearer(authorizationUrl="/auth/login", tokenUrl="/auth/token", auto_error=False)

@router.post("/logout")
async def logout(request:Request, token: oauth=Depends()): # type: ignore
    if token:
        request.session.clear()
        return await TokenDB.filter(token=token).delete()
    raise HTTPException(401, "Not authenticated")

async def get_token(token: oauth=Depends()) -> List[str]: # type: ignore
    """Get token, userid from token(Dependencies)"""
    if token:
        token:TokenDB=await TokenDB.get(token=token)
        return token
    else:
        return None