import googlecloudprofiler

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Link


# Profiler initialization. It starts a daemon thread which continuously
# collects and uploads profiles. Best done as early as possible.
def initialize_profiler():
    try:
        # service and service_version can be automatically inferred when running on App Engine.
        # project_id must be set if not running on GCP.
        googlecloudprofiler.start()
    except (ValueError, NotImplementedError) as exc:
        print(exc)  # Handle errors here


# Ref https://cloud.google.com/trace/docs/setup/python-ot
def initialize_tracer():
    tracer_provider = TracerProvider()
    cloud_trace_exporter = CloudTraceSpanExporter()
    tracer_provider.add_span_processor(
        # BatchSpanProcessor buffers spans and sends them in batches in a
        # background thread. The default parameters are sensible, but can be
        # tweaked to optimize your performance
        BatchSpanProcessor(cloud_trace_exporter)
    )
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(__name__)

    return tracer
