"""A LangGraph ReAct agent that records ticket changes in AvianSuite and
undoes its own mistake.

    pip install langgraph langchain-mcp-adapters "langchain[anthropic]"
    export ANTHROPIC_API_KEY=... AVIANSUITE_TOKEN=...
    python main.py
"""
import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

TASK = "Ticket T-1001: the customer confirmed the fix by email, so record its status as resolved. Then notice that T-1001 was the wrong ticket (the email was about T-1002): retract your T-1001 change with a reason, and record T-1002 as resolved instead. Finish by listing the receipt links for your changes."


async def main() -> None:
    client = MultiServerMCPClient({
        "aviansuite": {
            "transport": "streamable_http",
            "url": os.environ.get("AVIANSUITE_MCP_URL", "https://mcp.aviansuite.com/mcp"),
            "headers": {"Authorization": f"Bearer {os.environ['AVIANSUITE_TOKEN']}"},
        }
    })
    tools = await client.get_tools()
    agent = create_react_agent(
        "anthropic:claude-opus-5",
        tools,
        prompt=(
            "You update help desk tickets. Record every change with record_fact before you make it, "
            "and fix your own mistakes with retract_fact or undo_changes; never delete."
        ),
    )
    result = await agent.ainvoke({"messages": [{"role": "user", "content": TASK}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
