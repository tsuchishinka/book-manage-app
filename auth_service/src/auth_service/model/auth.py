from pydantic import BaseModel


class Auth(BaseModel):
    mail_address: str | None
    name: str | None
    role_id: int | None
    grant_type: str | None
    scope: str
