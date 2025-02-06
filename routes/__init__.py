from fastapi import APIRouter

from . import routes, user, admin, webhook


def meta() -> APIRouter:
    meta_router = APIRouter()
    meta_router.include_router(routes.router)
    meta_router.include_router(user.router, prefix="/user", tags=["user"])
    meta_router.include_router(admin.router, prefix="/admin", tags=["admin"])
    meta_router.include_router(webhook.router, tags=["webhook"])


    return meta_router