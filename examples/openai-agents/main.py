"""A ticket agent on the OpenAI Agents SDK that records its changes in
AvianSuite and undoes its own mistake.

    pip install openai-agents
    export OPENAI_API_KEY=... AVIANSUITE_TOKEN=...
    python main.py
"""
import asyncio
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

TASK = "Ticket T-1001: the customer confirmed the fix by email, so record its status as resolved. Then notice that T-1001 was the wrong ticket (the email was about T-1002): retract your T-1001 change with a reason, and record T-1002 as resolved instead. Finish by listing the receipt links for your changes."


async def main() -> None:
    async with MCPServerStreamableHttp(
        name="aviansuite",
        params={
            "url": os.environ.get("AVIANSUITE_MCP_URL", "https://mcp.aviansuite.com/mcp"),
            "headers": {"Authorization": f"Bearer {os.environ['AVIANSUITE_TOKEN']}"},
        },
    ) as aviansuite:
        agent = Agent(
            name="ticket-bot",
            instructions=(
                "You update help desk tickets. Record every change with record_fact "
                "(entity_id like ticket:T-1001, with evidence and a unique operation_id) "
                "before you make it. Fix your own mistakes with retract_fact or undo_changes; never delete."
            ),
            mcp_servers=[aviansuite],
        )
        result = await Runner.run(agent, TASK)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
