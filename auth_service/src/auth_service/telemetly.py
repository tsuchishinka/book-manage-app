from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from auth_service.src.auth_service.service.settings import Settings


def setup_telemetry(settings: Settings):
    provider = TracerProvider(
        resource=Resource.create({"service.name": settings.service_name})
    )

    exporter = OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint)

    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)
