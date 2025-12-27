from pydantic_ai import Agent
from textwrap import dedent
import uvicorn

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from agents.otel import configure

configure("architect")


Agent.instrument_all()

system_prompt = dedent("""
You are a software architect whose mission is to translate product requirements to implementation plans.
The instructions should be programming language agnostic, your focus should be on architecture patterns, API structures, design patterns, and system components.

Provide clear, detailed implementation plans that developers can use to build features.
                       
Give short and concise answers.
""")

architect_agent = Agent(
    "anthropic:claude-haiku-4-5",
    system_prompt=system_prompt,
)

app = architect_agent.to_a2a()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
