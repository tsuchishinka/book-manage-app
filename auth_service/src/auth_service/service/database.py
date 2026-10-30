from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from auth_service.service.settings import Settings
from opentelemetry import trace
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

tracer = trace.get_tracer(__name__)


class DatabaseClient:
    def __init__(self, url: str):
        self.engine = create_async_engine(url)
        SQLAlchemyInstrumentor().instrument(engine=self.engine)

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncConnection]:
        async with (
            tracer.start_as_current_span("database.connection") as span,
            self.engine.connect() as conn,
        ):
            span.set_attribute("db.operation", "connection")
            yield conn

    @asynccontextmanager
    async def execute(self, sql: str) -> AsyncGenerator[AsyncConnection]:
        async with self.connect() as conn:
            conn.execute(str)

    @asynccontextmanager
    def transaction(self, conn: Connection):
        with tracer.start_as_current_span("database.transaction"), conn.begin():
            yield conn


def get_database(settings: Settings):
    return DatabaseClient(settings.database_url)
