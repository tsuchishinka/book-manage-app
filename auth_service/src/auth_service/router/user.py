from typing import Annotated

from auth_service.cruds.user import insert_user
from auth_service.cruds.user import update_user as update_user_record
from auth_service.model.user import Role, User
from auth_service.service.auth import REQUIRED_ROLE_KEY, AuthClient, verify_role
from auth_service.service.user import is_exist_mail_address, is_exist_user
from fastapi import APIRouter, Body, Depends, HTTPException

from auth_service.src.auth_service.schema.user import (
    UserPatchIn,
    UserPatchOut,
    UserPostIn,
    UserPostOut,
)

router = APIRouter()


@router.post("/user", summary="ユーザー登録", response_model=UserPostOut)
async def create_user(params: Annotated[UserPostIn, Body()]):
    if is_exist_mail_address(params.mail_address):
        raise HTTPException(status_code=400, detail="duplicate mail address")

    user = User(
        name=params.name,
        mail_address=params.mail_address,
        password=params.password,
        role_id=Role.USER,
    )
    user_id = insert_user(user)

    return UserPostOut(user_id=user_id)


@router.patch(
    "/user/{user_id}",
    summary="ユーザー情報更新",
    response_model=UserPatchOut,
    openapi_extra={REQUIRED_ROLE_KEY: [Role.USER]},
)
async def update_user(
    user_id: int,
    auth: Annotated[AuthClient, Depends(verify_role)],
    params: Annotated[UserPatchIn, Body()],
):
    if not is_exist_user(user_id=user_id):
        raise HTTPException(status_code=404, detail="user_id not found")
    elif is_exist_mail_address(params.mail_address):
        raise HTTPException(status_code=400, detail="duplicate mail address")

    user = User(
        name=params.name,
        mail_address=params.mail_address,
        password=params.password,
        role_id=Role.USER,
    )
    update_user_record(user)

    return UserPatchOut(status="success")
