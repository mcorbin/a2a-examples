from strands import Agent
from textwrap import dedent
from strands.models.anthropic import AnthropicModel
import os
from strands.multiagent.a2a import A2AServer
from strands_tools.a2a_client import A2AClientToolProvider
from agents.otel import configure

configure()

system_prompt = dedent("""
You are an orchestrator agent that coordinates multiple specialized agents to complete software development tasks.

You have access to three specialized agents:
- Architect agent (http://localhost:8000): Creates implementation plans from requirements
- Developer agent (http://localhost:8001): Writes code based on plans
- Reviewer agent (http://localhost:8002): Reviews code for quality and bugs

Your workflow:
1. When you receive a feature request, first call the architect agent to create an implementation plan
2. Then call the developer agent with the plan to write the code
3. Finally call the reviewer agent to review the code that was written
4. Provide a complete summary to the user with all outputs

Use the A2A tools to discover and communicate with these agents.
                       
Give short and concise answers.
""")

model = AnthropicModel(
    client_args={
        "api_key": os.environ["ANTHROPIC_API_KEY"],
    },
    max_tokens=20000,
    model_id="claude-haiku-4-5-20251001",
    params={
        "temperature": 0,
    },
)

# Configure A2A client tool to know about all agents
a2a_tool_provider = A2AClientToolProvider(
    known_agent_urls=[
        "http://localhost:8000",  # Architect
        "http://localhost:8001",  # Developer
        "http://localhost:8002",  # Reviewer
    ]
)

orchestrator_agent = Agent(
    name="Orchestrator agent",
    description="An orchestrator that coordinates architect, developer, and reviewer agents",
    tools=a2a_tool_provider.tools,
    system_prompt=system_prompt,
    model=model,
)

# Configure A2A server on port 9000
a2a_server = A2AServer(
    agent=orchestrator_agent,
    port=9000,
)

a2a_server.serve()
