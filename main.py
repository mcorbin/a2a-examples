import asyncio
from a2a.client import ClientConfig, ClientFactory
from a2a.types import Message, Role, TextPart
from uuid import uuid4
import httpx

from a2a.client import A2ACardResolver

from a2a.types import Part


async def run(instructions: str):
    async with httpx.AsyncClient(timeout=120) as httpx_client:
        # Configure A2A client for orchestrator
        resolver = A2ACardResolver(
            httpx_client=httpx_client, base_url="http://localhost:9000"
        )
        agent_card = await resolver.get_agent_card()
        config = ClientConfig(
            httpx_client=httpx_client,
            streaming=True,
        )
        factory = ClientFactory(config)
        client = factory.create(agent_card)

        print(f"\n{'=' * 80}")
        print(f"Instruction: {instructions}")
        print(f"{'=' * 80}\n")

        # Create message for the orchestrator
        message = Message(
            message_id=str(uuid4()),
            role=Role.user,
            parts=[Part(TextPart(kind="text", text=instructions))],
        )

        # Send to orchestrator and stream responses
        print("Starting orchestrated multi-agent workflow...\n")
        async for event in client.send_message(message):
            if isinstance(event, Message):
                print(event.model_dump_json(exclude_none=True, indent=2))
            elif isinstance(event, tuple) and len(event) == 2:
                task, update_event = event
                print(f"Task: {task.model_dump_json(exclude_none=True, indent=2)}")
                if update_event:
                    print(
                        f"Update: {update_event.model_dump_json(exclude_none=True, indent=2)}"
                    )
            else:
                # Fallback for other response types
                print(f"Response: {str(event)}")
        print(f"\n\n{'=' * 80}")
        print("Multi-agent workflow completed!")
        print(f"{'=' * 80}")


if __name__ == "__main__":
    print("Input:")
    instructions = input()
    asyncio.run(run(instructions))
