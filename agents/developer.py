from strands import Agent, tool
from textwrap import dedent
from strands.models.anthropic import AnthropicModel
import os
from strands.multiagent.a2a import A2AServer
from agents.otel import configure

configure("developer")

system_prompt = dedent("""
You are a coding agent responsible for building features.

You should produce code in Golang, and write the result in files using the write_file tool.

The code should be ready to be run.

Use only golang's standard library, don't use any dependency.
                       
IMPORTANT: Return the names of the files that you wrote.
                       
Give short and concise answers.
""")


@tool
def write_file(path: str, content: str) -> None:
    """
    Write content to a file.

    Args:
        path (str): The file path
        content (str): The file content
    """
    print(f"[DEVELOPER] Writing file: {path}")
    with open(path, "w") as f:
        f.write(content)


model = AnthropicModel(
    client_args={
        "api_key": os.environ["ANTHROPIC_API_KEY"],
    },
    # **model_config
    max_tokens=5000,
    model_id="claude-haiku-4-5-20251001",
    params={
        "temperature": 0,
    },
)

developer_agent = Agent(
    name="Developer agent",
    description="A coding agent responsible for building features",
    tools=[write_file],
    system_prompt=system_prompt,
    model=model,
)

a2a_server = A2AServer(
    agent=developer_agent,
    port=8001,
)

a2a_server.serve()
