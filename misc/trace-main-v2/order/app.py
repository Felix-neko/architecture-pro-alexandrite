
from flask import Flask
import random
import time
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

trace.set_tracer_provider(
   TracerProvider(
       resource=Resource.create({SERVICE_NAME: "order"})
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


@app.route("/")
def order():
    with trace.get_tracer(__name__).start_as_current_span("order"):
        random_order_number = random.randint(1, 500)
        time.sleep(random_order_number*0.001) #задержка
        return str(random_order_number)