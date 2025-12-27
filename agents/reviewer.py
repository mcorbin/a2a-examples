from strands import Agent, tool
from textwrap import dedent
from strands.models.anthropic import AnthropicModel
import os
from strands.multiagent.a2a import A2AServer
from agents.otel import configure

configure()

system_prompt = dedent("""
You are an agent specialized in code reviews.

Your goal is to read files, review the code, and:

- Provide a short (a few sentences at maximum) summary of what's it's doing
- Look for bugs and propose solutions to fix them
- Provide suggestions to improve the code (architecture, code style...)
""")


@tool
def read_file(path: str) -> str:
    """
    Read a file and return its content.

    Args:
        path (str): The file path

    Returns:
        str: the file content
    """
    print(f"REVIEWER: read {path}")
    with open(path) as f:
        return f.read()


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

reviewer_agent = Agent(
    name="Reviewer agent",
    description="An agent specialized in code reviews",
    tools=[read_file],
    system_prompt=system_prompt,
    model=model,
)
a2a_server = A2AServer(agent=reviewer_agent, port=8002)

a2a_server.serve()
