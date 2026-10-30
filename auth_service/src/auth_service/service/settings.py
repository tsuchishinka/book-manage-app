from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth2_secret: str | None
    telemetry_service_name: str | None
    service_name: str | None
    otel_exporter_otlp_endpoint: str | None
    database_url: str | None


def get_setting():
    return Settings()
