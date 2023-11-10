import flask, os, dotenv, logging
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter


app = flask.Flask(__name__)

dotenv.load_dotenv()

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: os.environ.get('OTEL_SERVICE_NAME')})
    )
)

logging.basicConfig(level=logging.DEBUG)
app_logger = logging.getLogger(__name__)

app_logger.debug(f"APPLICATIONINSIGHTS_CONNECTION_STRING: {os.environ.get('CONNECTION_STRING')}")
app_logger.debug(f"OTEL_SERVICE_NAME: {os.environ.get('OTEL_SERVICE_NAME')}")

# Enable tracing for Flask library
FlaskInstrumentor().instrument_app(app)

# Enable tracing for requests library
RequestsInstrumentor().instrument()

trace_exporter = AzureMonitorTraceExporter(
    connection_string=os.environ.get('CONNECTION_STRING')
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(trace_exporter)
)

@app.route('/')
def index():
    return flask.jsonify({'message': 'Hello World! DEPLOY AZURE!!!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')