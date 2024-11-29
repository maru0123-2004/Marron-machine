from fastapi import APIRouter

router=APIRouter()

from .auth import router as auth_router
router.include_router(auth_router, prefix="/auth")

from .user import router as user_router
router.include_router(user_router, prefix="/user")

from .target import router as target_router
router.include_router(target_router, prefix="/target")

from .relay import router as relay_router
router.include_router(relay_router, prefix="/relay")