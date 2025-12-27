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

configure()

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

            # Collect all text content
            full_text_content = []

            async for event in client.send_message(message):
                if isinstance(event, Message):
                    print(event.model_dump_json(exclude_none=True, indent=2))
                    # Extract text content from message parts
                    if event.parts:
                        for part in event.parts:
                            # Try to get the text content from the part's data
                            part_data = (
                                part.model_dump()
                                if hasattr(part, "model_dump")
                                else part.__dict__
                            )

                            print(f"\n[DEBUG] Part data: {part_data}\n")

                            # Look for text in various possible locations
                            if isinstance(part_data, dict):
                                # Check for direct text field
                                if "text" in part_data and part_data["text"]:
                                    full_text_content.append(part_data["text"])
                                    print(
                                        f"[DEBUG] Added text from direct field: {part_data['text'][:50]}..."
                                    )
                                # Check for nested text_part
                                elif (
                                    "text_part" in part_data
                                    and part_data["text_part"]
                                    and "text" in part_data["text_part"]
                                ):
                                    full_text_content.append(
                                        part_data["text_part"]["text"]
                                    )
                                    print(
                                        f"[DEBUG] Added text from text_part: {part_data['text_part']['text'][:50]}..."
                                    )
                                else:
                                    print(
                                        f"[DEBUG] No text found in part_data keys: {list(part_data.keys())}"
                                    )
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
