from main.routes import routes
from config import Config

from flask import Flask

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

import logging
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import (
    set_logger_provider,
)
from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)

config = Config()
config.load_env_variables()

CONNECTION_STRING = config.CONNECTION_STRING
OTEL_SERVICE_NAME = config.OTEL_SERVICE_NAME


logger_provider = LoggerProvider()
set_logger_provider(logger_provider)
exporter = AzureMonitorLogExporter(
    connection_string=CONNECTION_STRING
)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

handler = LoggingHandler()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

logger.warning("Warning log message! This will generate a warning log message in Azure Monitor.")

try:
    val = 1 / 0
    print(val)
except ZeroDivisionError:
    logger.exception("Error: Division by zero")

try:
    val = 1 / 0
    print(val)
except ZeroDivisionError:
    logger.error("Error: Division by zero", stack_info=True, exc_info=True)

logger_provider.force_flush()

def create_app():
    app = Flask(__name__)

    # Load configuration of OpenTelemetry
    tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: OTEL_SERVICE_NAME})
    )

    trace.set_tracer_provider(tracer_provider)

    # Enable tracing for Flask library
    FlaskInstrumentor().instrument_app(app)

    # Enable tracing for requests library
    RequestsInstrumentor().instrument()

    trace_exporter = AzureMonitorTraceExporter(
        connection_string=CONNECTION_STRING
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    app.register_blueprint(routes.app)

    return app