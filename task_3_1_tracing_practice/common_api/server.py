from typing import Optional


from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import uvicorn


def run_server(
    app: FastAPI,
    service_name: Optional[str] = None,
    port: int = 10000,
    log_level: str = "debug",
    # otel_endpoint: str = "http://localhost:4318/v1/traces",
):
    # Initialize OpenTelemetry, instrument FastAPI app, run FastAPI app.
    resource = Resource.create(
        {
            "service.name": service_name if service_name is not None else type(app).__name__,
            # add other attributes like service.version, deployment.environment etc.
            # "service.version": "0.1.0",
        }
    )
    provider = TracerProvider(resource=resource)

    # OTLP exporter: send to local Collector / Jaeger OTLP receiver
    # Default endpoint below assumes HTTP OTLP receiver on localhost:4318
    otlp_exporter = OTLPSpanExporter(
        # endpoint=otel_endpoint,  # <- change if needed
        # timeout=10,  # optional
        # headers=(("api-key", "xxx"),)  # optional
    )
    span_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)

    # Instrument the FastAPI app (auto-instruments incoming requests, routing, etc.)
    FastAPIInstrumentor.instrument_app(app)
    # Instrument requests library (outgoing HTTP calls)
    RequestsInstrumentor().instrument()
    # Instrument httpx library (async HTTP client)
    HTTPXClientInstrumentor().instrument()
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
