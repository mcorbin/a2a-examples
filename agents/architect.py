from pydantic_ai import Agent
from textwrap import dedent
import uvicorn

system_prompt = dedent("""
You are a software architect whose mission is to translate product requirements to implementation plans.
The instructions should be programming language agnostic, your focus should be on architecture patterns, API structures, design patterns, and system components.

Provide clear, detailed implementation plans that developers can use to build features.
""")

architect_agent = Agent(
    "anthropic:claude-haiku-4-5",
    system_prompt=system_prompt,
)

app = architect_agent.to_a2a()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
