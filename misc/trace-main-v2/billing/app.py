
from flask import Flask
import requests
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

trace.set_tracer_provider(
   TracerProvider(
       resource=Resource.create({SERVICE_NAME: "billing"})
   )
)
otlp_exporter = OTLPSpanExporter(
   endpoint="http://jaeger:4317",
   insecure=True
)
# Use smaller batch size and shorter timeout for faster trace delivery
trace.get_tracer_provider().add_span_processor(
   BatchSpanProcessor(
       otlp_exporter,
       max_queue_size=100,
       max_export_batch_size=10,
       export_timeout_millis=5000,
       schedule_delay_millis=1000
   )
)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route("/")
def pay():
    with trace.get_tracer(__name__).start_as_current_span("pay"):
        res = requests.get("http://order:8002")
        return "Payed"+" "+res.text