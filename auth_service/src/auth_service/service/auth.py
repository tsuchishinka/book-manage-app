import jwt
from auth_service.model.auth import Auth
from auth_service.model.role import Role
from auth_service.model.user import User
from fastapi import HTTPException, Request, Response

from auth_service.src.auth_service.service.settings import Settings

TOKEN_KEY = "book_app_auth_id"
REQUIRED_ROLE_KEY = "x-required-roles"


def _get_required_roles(request: Request):
    current_route = request.scope.get("route")

    if current_route and hasattr(current_route, "openapi_extra"):
        extra_data = current_route.openapi_extra
        return extra_data.get(REQUIRED_ROLE_KEY)

    return None


def verify_auth_param(mail_address: str, password: str):
    # TODO: メールアドレスとパスワード両方の存在チェック
    user = User
    return user


def _get_auth_client_param(token_payload: dict):
    mail_address = token_payload["mail_address"]
    name = token_payload["name"]
    role_id = token_payload["role_id"]
    grant_type = token_payload["grant_type"]
    scope = token_payload["scope"]
    return (mail_address, name, role_id, grant_type, scope)


def authorize(request):
    token_payload = _resolve_token(request)
    mail_address, name, role_id, grant_type, scope = _get_auth_client_param(
        token_payload
    )

    if role_id:
        _verify_role(request, role_id)
    elif grant_type and scope:
        _verify_grant(grant_type, scope)
    else:
        HTTPException(status_code=403)

    return Auth(
        mail_address=mail_address,
        name=name,
        role_id=role_id,
        grant_type=grant_type,
        scope=scope,
    )


def _verify_role(request: Request, role_id: Role):
    required_roles = _get_required_roles(request)

    if role_id not in required_roles:
        raise HTTPException(status_code=403)

    return True


def _verify_grant(grant_type: str, scope: str):
    if not grant_type == "client_credentials":
        raise HTTPException(status_code=403)

    if scope not in ["book", "admin", "loan"]:
        raise HTTPException(status_code=403)

    return True


def _create_token(auth: Auth, setting: Settings):
    payload = auth.model_dump()
    secret = setting.auth2_secret
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def attach_token(response: Response, auth: Auth, settings: Settings):
    token = _create_token(auth, settings)
    response.set_cookie(TOKEN_KEY, token)


def _get_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization")

    if authorize:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and token:
            return token

    return request.cookies.get(TOKEN_KEY)


def _resolve_token(request: Request, setting: Settings):
    token = _get_token(request)
    payload = jwt.decode(token, setting.auth2_secret)

    return payload
