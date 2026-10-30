from typing import Annotated

from auth_service.model.auth import Auth
from auth_service.service.auth import attach_token, authorize, verify_auth_param
from fastapi import APIRouter, Body, HTTPException, Response

from auth_service.src.auth_service.schema.auth import (
    AuthorizePostIn,
    AuthorizePostOut,
    TokenExchangePostIn,
    TokenExchangePostOut,
)

router = APIRouter()


@router.post("/auth/authorize", summary="認証", response_model=AuthorizePostOut)
async def post_authorize(
    params: Annotated[AuthorizePostIn, Body()], response: Response
):
    user = verify_auth_param(mail_address=params.mail_address, password=params.password)
    if user is None:
        return HTTPException(status_code=401)

    attach_token(response)
    return AuthorizePostOut(status="success")


@router.post(
    "/auth/token/exchange", summary="トークン交換", response_model=TokenExchangePostOut
)
async def exchange_token(
    params: Annotated[TokenExchangePostIn, Body()],
    auth: Annotated[Auth, authorize],
    response: Response,
):
    new_auth_param = Auth(grant_type=auth.grant_type, scope=params.new_scope)
    attach_token(response=response, auth=new_auth_param)
    return TokenExchangePostOut(status="success")
