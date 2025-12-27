from strands import Agent, tool
from textwrap import dedent
from strands.models.anthropic import AnthropicModel
import os
from strands.multiagent.a2a import A2AServer

system_prompt = dedent("""
You are a coding agent responsible to build features.

You should produce code in Golang, and write the result in files.

The code should be ready to be run.

Use only golang's standard library, don't use any dependency.

After you've written the code, you MUST delegate to the reviewer agent to review your work.
Call the reviewer agent and ask them to review the files you've written.
""")


@tool
def write_file(path: str, content: str) -> None:
    """
    Read a file and return its content.

    Args:
        path (str): The file path
        content (str): The file content
    """
    print(f"DEVELOPER: write {path}")
    with open(path, "w") as f:
        f.write(content)


model = AnthropicModel(
    client_args={
        "api_key": os.environ["ANTHROPIC_API_KEY"],
    },
    # **model_config
    max_tokens=1028,
    model_id="claude-haiku-4-5-20251001",
    params={
        "temperature": 0,
    },
)

developer_agent = Agent(
    name="Developer agent",
    description="A coding agent responsible to build features",
    tools=[write_file],
    system_prompt=system_prompt,
    model=model,
)

# Configure A2A server with access to the reviewer agent
a2a_server = A2AServer(
    agent=developer_agent,
    port=8001,
    delegates={"reviewer": "http://localhost:8002/a2a"}
)

a2a_server.serve()
