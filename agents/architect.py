from pydantic_ai import Agent
from textwrap import dedent
import uvicorn

system_prompt = dedent("""
You are a software architect whose mission is to translate products requirements to implementation plan.
The instructions should be programming language agnostic, your focus should be on architecture patterns, API structures...

Once you've created the implementation plan, you MUST delegate to the developer agent to implement the code.
Call the developer agent with your implementation plan.
""")

# Configure the architect agent with access to the developer agent
architect_agent = Agent(
    "anthropic:claude-haiku-4-5",
    system_prompt=system_prompt,
)

# Create A2A app with developer agent as delegate
app = architect_agent.to_a2a(
    agents={
        "developer": "http://localhost:8001/a2a"
    }
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
