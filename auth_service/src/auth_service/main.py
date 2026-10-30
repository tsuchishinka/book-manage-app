from fastapi import FastAPI

from auth_service.src.auth_service.router.admin import router as AdminRouter
from auth_service.src.auth_service.router.auth import router as AuthRouter
from auth_service.src.auth_service.router.user import router as UserRouter
from auth_service.src.auth_service.telemetly import setup_telemetry

setup_telemetry()

app = FastAPI()
app.include_router(AdminRouter)
app.include_router(AuthRouter)
app.include_router(UserRouter)
