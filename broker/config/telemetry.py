from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
import os
from shared.config.preferences import OTEL_EXPORTER_OTLP_ENDPOINT

_logger = __import__('logging').getLogger(__name__)


def setup_broker_telemetry(app_name: str = "scoreboard-broker", app_version: str = "0.1.0"):
    """Setup OpenTelemetry tracing for the broker service."""
    
    # Create resource
    resource = Resource.create({
        SERVICE_NAME: app_name,
        SERVICE_VERSION: app_version,
    })
    
    # Setup tracing
    tracer_provider = TracerProvider(resource=resource)

    if OTEL_EXPORTER_OTLP_ENDPOINT:
        _logger.info("📡 Exporting traces to OTLP endpoint: %s", OTEL_EXPORTER_OTLP_ENDPOINT)
        otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    else:
        _logger.info("🖥️  Exporting traces to console (set OTEL_EXPORTER_OTLP_ENDPOINT for external export)")
        console_exporter = ConsoleSpanExporter()
        tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))
    
    trace.set_tracer_provider(tracer_provider)


def instrument_broker():
    """Instrument the broker service with OpenTelemetry tracing."""
    
    # Instrument Kafka
    AIOKafkaInstrumentor().instrument()
    
    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument()
    
    # Instrument AsyncPG
    AsyncPGInstrumentor().instrument()


def get_tracer(name: str):
    """Get a tracer instance."""
    return trace.get_tracer(name)
