from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from strands.telemetry import StrandsTelemetry
import os

from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

HTTPXClientInstrumentor().instrument()

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"


def configure(service_name: str) -> None:
    resource = Resource(attributes={SERVICE_NAME: service_name})

    exporter = OTLPSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(span_processor)

    set_tracer_provider(tracer_provider)
