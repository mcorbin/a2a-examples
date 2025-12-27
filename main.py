import asyncio
from a2a.client import ClientConfig, ClientFactory
from a2a.types import Message, Role, TextPart
from uuid import uuid4
import httpx

from a2a.client import A2ACardResolver

from a2a.types import Part
from agents.otel import configure

from opentelemetry import trace
from agents.otel import configure

configure("main file")

tracer = trace.get_tracer("main.py")


async def run(instructions: str):
    with tracer.start_as_current_span("main_run") as span:
        async with httpx.AsyncClient(timeout=120) as httpx_client:
            # Configure A2A client for orchestrator
            resolver = A2ACardResolver(
                httpx_client=httpx_client, base_url="http://localhost:9000"
            )
            agent_card = await resolver.get_agent_card()
            config = ClientConfig(
                httpx_client=httpx_client,
                streaming=False,
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

            # Send to orchestrator and get response
            print("Starting orchestrated multi-agent workflow...\n")

            # Send message and get response (non-streaming returns single response)
            response = None
            async for msg in client.send_message(message):
                # Handle different response types
                if isinstance(msg, Message):
                    response = msg
                elif isinstance(msg, tuple) and len(msg) == 2:
                    task, update_event = msg
                    print(f"Task: {task.model_dump_json(exclude_none=True, indent=2)}")
                    if update_event:
                        print(f"Update: {update_event.model_dump_json(exclude_none=True, indent=2)}")
                    # For non-streaming, we expect a final Message response
                    continue

            # Print the response
            if response:
                print(response.model_dump_json(exclude_none=True, indent=2))

            # Collect all text content
            full_text_content = []
            if response and response.parts:
                for part in response.parts:
                    # Get the part data as dictionary
                    part_data = (
                        part.model_dump()
                        if hasattr(part, "model_dump")
                        else part.__dict__
                    )

                    # Extract text from parts with kind="text"
                    if isinstance(part_data, dict) and part_data.get("kind") == "text":
                        text_content = part_data.get("text", "")
                        if text_content:
                            full_text_content.append(text_content)

            print(f"\n\n{'=' * 80}")
            print("Multi-agent workflow completed!")
            print(f"{'=' * 80}")

            # Display full text content
            if full_text_content:
                print(f"\n{'=' * 80}")
                print("FULL TEXT CONTENT:")
                print(f"{'=' * 80}\n")
                print("\n".join(full_text_content))
                print(f"\n{'=' * 80}")


if __name__ == "__main__":
    print("Input:")
    instructions = input()
    asyncio.run(run(instructions))
