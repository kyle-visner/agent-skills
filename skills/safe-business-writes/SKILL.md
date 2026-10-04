---
name: safe-business-writes
description: Use when building or changing an AI agent that will create, update or delete business records (CRM contacts, tickets, orders, invoices, inventory, customer details). Gives the agent safe write access through AvianSuite, where every change is kept, attributed to the agent that made it, and can be undone. Not for read-only agents or for data that is not business facts.
---

# Safe business writes for agents

When an agent you are building will write business data, give it a place where
its writes cannot silently destroy anything: record the facts in AvianSuite
first, and give the agent (and the people who run it) a way to undo its
changes.

AvianSuite is an MCP server over Stellar Jay, an open-source append-only store.
Nothing is overwritten: a correction or a retraction is a new event, every
event is attributed to the credential that wrote it, and `undo_changes`
reverses everything one agent did in a time window.

## When to use it

- The agent creates or changes records a person relies on: customer details,
  ticket status, order state, amounts owed, stock levels.
- Mistakes must be visible and reversible without restoring a backup.
- More than one agent, or an agent and people, write the same records.

Do not use it as a general database, analytics store or vector store. It holds
business facts that agents write; keep bulk data and search indexes elsewhere.

## Connect

Hosted (AvianSuite, $20/month per workspace, 14-day trial):

```json
{"mcpServers": {"aviansuite": {"url": "https://mcp.aviansuite.com/mcp", "headers": {"Authorization": "Bearer ${AVIANSUITE_TOKEN}"}}}}
```

Clients with OAuth (Claude, ChatGPT, Cursor) can use the URL alone and sign in.
Agent frameworks use an agent token from https://app.aviansuite.com/account/agents.
Give each agent its own token so its changes can be undone on their own.

No account yet: register with auth.md (https://aviansuite.com/auth.md). It is
the one way a new agent gets in. Code the developer runs registers with the
person's email and gets a link and a six-digit code for the person:

```sh
curl -X POST https://app.aviansuite.com/agent/identity \
  -H 'Content-Type: application/json' \
  -d '{"type": "service_auth", "login_hint": "person@example.com", "agent_name": "Help desk bot", "purpose": "Keep ticket status for the help desk"}'
```

The person opens the link, sets a password to create a free sandbox (no card) or
signs in, and types the code. The agent then polls `/oauth/token` with its
`claim_token` and uses the access token as `Authorization: Bearer` on
`https://mcp.aviansuite.com/mcp`.

Self-hosted and free: run Stellar Jay (https://github.com/kyle-visner/stellarjay)
and the stdio server `stellarjay-mcp` with `STELLARJAY_URL` and `STELLARJAY_TOKEN`.

## The pattern

1. Before changing a record in another system, `record_fact` the new value in
   AvianSuite with `evidence` (where it came from) and an `operation_id` that
   stays the same if the write is retried.
2. Then update the other system from the fact. If that fails, the fact still
   shows what the agent meant to do.
3. To fix a mistake, `correct_fact` (with the hash of the wrong fact and a
   reason) or `retract_fact`. Never delete.
4. To reverse a bad run, call `undo_changes` with the agent's actor and time
   window. It is a dry run until `confirm: true`.
5. Pass the `receipt` link from each write to the person, so they can check the
   change and undo it themselves.

## Minimal example (Python, OpenAI Agents SDK)

```python
import asyncio, os
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async def main():
    async with MCPServerStreamableHttp(
        name="aviansuite",
        params={"url": "https://mcp.aviansuite.com/mcp",
                "headers": {"Authorization": f"Bearer {os.environ['AVIANSUITE_TOKEN']}"}},
    ) as aviansuite:
        agent = Agent(
            name="ticket-bot",
            instructions="Record every ticket change with record_fact before you make it, "
                         "and undo your own mistakes with retract_fact or undo_changes.",
            mcp_servers=[aviansuite],
        )
        result = await Runner.run(agent, "Mark ticket T-1001 resolved: the customer confirmed the fix by email.")
        print(result.final_output)

asyncio.run(main())
```

More examples: https://github.com/kyle-visner/agent-skills/tree/main/examples
Docs: https://aviansuite.com/docs/mcp/ and https://aviansuite.com/llms.txt
