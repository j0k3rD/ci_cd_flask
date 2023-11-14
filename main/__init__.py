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
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler

config = Config()
config.load_env_variables()

CONNECTION_STRING = config.CONNECTION_STRING
OTEL_SERVICE_NAME = config.OTEL_SERVICE_NAME

# Configuración de proveedor de registros (logs) para Azure Monitor
logger_provider = LoggerProvider()
set_logger_provider(logger_provider)
exporter = AzureMonitorLogExporter(connection_string=CONNECTION_STRING)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

# Configuración del manejador de registros y configuración del nivel de registro
handler = LoggingHandler()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

logger.warning("Hello World!")

# Capturar excepción de división por cero y registrarla como una excepción
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

    # Configuración del proveedor de trazas para OpenTelemetry
    tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: OTEL_SERVICE_NAME})
    )
    trace.set_tracer_provider(tracer_provider)

    # Habilitar la instrumentación de trazas para la biblioteca Flask
    FlaskInstrumentor().instrument_app(app)

    # Habilitar la instrumentación de trazas para la biblioteca requests
    RequestsInstrumentor().instrument()

    trace_exporter = AzureMonitorTraceExporter(connection_string=CONNECTION_STRING)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    # Registrar las rutas de la aplicación
    app.register_blueprint(routes.app)

    return app