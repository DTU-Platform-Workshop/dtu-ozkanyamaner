import os

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracer(service_name) -> trace.Tracer:
    resource = Resource.create(
        {
            # You can configure what name your app should have in the 
            # telemetry here
            "service.name": service_name, 
            "service.namespace": os.getenv("RUNTIME_NAME")
        }
    )

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=os.getenv(
                    "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
                ),
                insecure=True,
            )
        )
    )
    trace.set_tracer_provider(provider)

    return trace.get_tracer(service_name)


def instrument_app(app: FastAPI) -> None:
    FastAPIInstrumentor.instrument_app(app, excluded_urls="livez,readyz")
    RequestsInstrumentor().instrument()
