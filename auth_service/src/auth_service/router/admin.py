from typing import Annotated

from auth_service.cruds.user import insert_user
from auth_service.model.role import Role
from auth_service.model.user import User
from auth_service.service.auth import REQUIRED_ROLE_KEY, Auth, authorize
from auth_service.service.user import is_exist_mail_address
from fastapi import APIRouter, Body, Depends, HTTPException

from auth_service.src.auth_service.schema.admin import AdminPostIn, AdminPostOut

router = APIRouter()


@router.post(
    "/admin",
    summary="管理者登録",
    response_model=AdminPostOut,
    openapi_extra={REQUIRED_ROLE_KEY: [Role.ADMIN]},
)
async def create_admin(
    params: Annotated[AdminPostIn, Body()],
    auth: Annotated[Auth, Depends(authorize)],
):
    if is_exist_mail_address(params.mail_address):
        raise HTTPException(status_code=400, detail="duplicate mail address")

    user = User(
        name=params.name,
        mail_address=params.mail_address,
        password=params.password,
        role_id=Role.ADMIN,
    )
    user_id = insert_user(user)

    return AdminPostOut(user_id=user_id)
